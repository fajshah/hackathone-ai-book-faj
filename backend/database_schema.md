# Database Schema: Users and User Profile

## Overview
This document defines the database schema for user authentication and profile data, separating authentication data from background/profile data for better organization and security.

## Current Schema (Existing Implementation)
The current implementation stores all user data in a single `users` table:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    failed_login_attempts INTEGER DEFAULT 0,
    account_locked_until TIMESTAMP,
    software_experience VARCHAR(50), -- "beginner", "intermediate", "advanced"
    hardware_knowledge VARCHAR(50), -- "none", "basic", "electronics", "robotics", "advanced"
    interests TEXT, -- JSON string: '["AI", "Robotics", "Web"]'
    email_verified BOOLEAN DEFAULT FALSE,
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Recommended Schema (Separated Authentication and Profile Data)

### 1. Users Table (Authentication Data)
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    failed_login_attempts INTEGER DEFAULT 0,
    account_locked_until TIMESTAMP,
    email_verified BOOLEAN DEFAULT FALSE,
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_active (is_active)
);
```

### 2. User Profiles Table (Background/Profile Data)
```sql
CREATE TABLE user_profiles (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    software_experience ENUM('beginner', 'intermediate', 'advanced') DEFAULT 'beginner',
    hardware_knowledge ENUM('none', 'basic', 'electronics', 'robotics', 'advanced') DEFAULT 'none',
    interests JSON, -- JSON array of strings: ["AI", "Robotics", "Web"]
    learning_goals TEXT,
    experience_level VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY uk_user_id (user_id),
    INDEX idx_software_experience (software_experience),
    INDEX idx_hardware_knowledge (hardware_knowledge)
);
```

## Schema Rationale

### Separation of Concerns
- **Authentication Data**: Core user identity and security information
- **Profile Data**: Background information for personalization and recommendations

### Benefits of Separation

1. **Security**:
   - Authentication data can have stricter access controls
   - Profile data can be accessed by recommendation engines without exposing sensitive auth data

2. **Performance**:
   - Authentication queries only load essential fields
   - Profile data can be loaded separately when needed for personalization

3. **Scalability**:
   - Profile data can be stored in separate tables or even separate databases
   - Authentication table remains lightweight for fast login operations

4. **Privacy**:
   - Profile data can be anonymized or deleted independently
   - Compliance with data protection regulations becomes easier

### Data Types and Constraints

#### Users Table
- `hashed_password`: Stores bcrypt/scrypt hashed passwords
- `is_active`: Prevents account access without deletion
- `failed_login_attempts`: Prevents brute force attacks
- `account_locked_until`: Temporary account lockout time

#### User Profiles Table
- `software_experience`: Enum for consistent values
- `hardware_knowledge`: Enum for consistent values
- `interests`: JSON for flexible storage of multiple interests
- `user_id`: Foreign key linking to users table

### Migration Strategy

To migrate from the current single-table approach:

1. **Create new user_profiles table**
2. **Migrate profile data** from users table to user_profiles table
3. **Remove profile columns** from users table
4. **Update application code** to use the new schema

### SQL Migration Example

```sql
-- Step 1: Create user_profiles table
CREATE TABLE user_profiles (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    software_experience ENUM('beginner', 'intermediate', 'advanced') DEFAULT 'beginner',
    hardware_knowledge ENUM('none', 'basic', 'electronics', 'robotics', 'advanced') DEFAULT 'none',
    interests JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY uk_user_id (user_id)
);

-- Step 2: Migrate existing profile data
INSERT INTO user_profiles (user_id, software_experience, hardware_knowledge, interests, created_at, updated_at)
SELECT id, software_experience, hardware_knowledge, interests, created_at, updated_at
FROM users
WHERE software_experience IS NOT NULL
   OR hardware_knowledge IS NOT NULL
   OR interests IS NOT NULL;

-- Step 3: Remove profile columns from users table
ALTER TABLE users
DROP COLUMN software_experience,
DROP COLUMN hardware_knowledge,
DROP COLUMN interests;
```

### API Considerations

The separation allows for:
- **Authentication API**: Only accesses users table
- **Profile API**: Accesses both tables for personalization
- **Analytics API**: Can access profile data separately for insights
- **Privacy API**: Can manage profile data independently for compliance

## Relationships

```
users (1) <---> (1) user_profiles
  |                |
  |                |
  +----------------+
```

The relationship is one-to-one, with user_profiles extending user information for personalization purposes.
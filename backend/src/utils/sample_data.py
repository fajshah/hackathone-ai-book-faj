"""
Sample data for the Physical AI & Humanoid Robotics textbook
This module provides sample textbook content for testing and demonstration
"""

# Sample textbook content organized by modules and chapters
TEXTBOOK_CONTENT = {
    "modules": [
        {
            "title": "Introduction to Physical AI",
            "description": "Foundations of Physical AI and its applications in robotics",
            "content": "Physical AI combines artificial intelligence with physical systems to create intelligent robots that can interact with the real world. This field encompasses robotics, computer vision, natural language processing, and control theory.",
            "module_type": "Physical AI",
            "week_number": 1
        },
        {
            "title": "ROS 2 Fundamentals",
            "description": "Robot Operating System 2 for robotics development",
            "content": "ROS 2 is the next generation of the Robot Operating System, designed for production environments. It provides libraries and tools to help software developers create robot applications.",
            "module_type": "ROS 2",
            "week_number": 2
        },
        {
            "title": "Gazebo & Unity Simulation",
            "description": "Simulation environments for robotics development",
            "content": "Gazebo and Unity provide powerful simulation environments for testing and developing robotics applications before deploying to real hardware.",
            "module_type": "Simulation",
            "week_number": 3
        },
        {
            "title": "NVIDIA Isaac Platform",
            "description": "NVIDIA's platform for AI-powered robotics",
            "content": "The NVIDIA Isaac platform provides tools and frameworks for developing AI-powered robots with advanced perception and navigation capabilities.",
            "module_type": "NVIDIA Isaac",
            "week_number": 4
        },
        {
            "title": "Vision-Language-Action Models",
            "description": "VLA models for embodied AI",
            "content": "Vision-Language-Action models enable robots to understand and interact with the world using vision, language, and action capabilities.",
            "module_type": "VLA",
            "week_number": 5
        }
    ],
    "chapters": [
        {
            "title": "What is Physical AI?",
            "description": "Understanding the core concepts of Physical AI",
            "content": "Physical AI is a field that combines artificial intelligence with physical systems to create robots that can perceive, reason, and act in the real world. Unlike traditional AI that operates on data, Physical AI operates on physical systems and their interactions with the environment.",
            "order_num": 1,
            "module_id": 1
        },
        {
            "title": "ROS 2 Architecture",
            "description": "Understanding the architecture of ROS 2",
            "content": "ROS 2 uses a client library implementation that provides the middleware for communication between nodes. The architecture is designed to be suitable for real-world applications with features like quality of service policies, security, and multi-robot systems.",
            "order_num": 1,
            "module_id": 2
        },
        {
            "title": "Simulation Environments",
            "description": "Using Gazebo and Unity for robotics simulation",
            "content": "Simulation is crucial for robotics development as it allows testing algorithms and behaviors in a safe, virtual environment before deployment to real robots. Gazebo provides realistic physics simulation, while Unity offers game-engine quality rendering.",
            "order_num": 1,
            "module_id": 3
        },
        {
            "title": "Isaac ROS",
            "description": "NVIDIA Isaac's ROS integration",
            "content": "Isaac ROS provides hardware-accelerated perception and navigation capabilities for robots. It includes GPU-accelerated computer vision, SLAM algorithms, and other perception tools optimized for NVIDIA hardware.",
            "order_num": 1,
            "module_id": 4
        },
        {
            "title": "Understanding VLA Models",
            "description": "Vision-Language-Action models in robotics",
            "content": "VLA models combine visual perception, language understanding, and action generation in a single neural network. These models enable robots to follow natural language commands and perform complex manipulation tasks in real-world environments.",
            "order_num": 1,
            "module_id": 5
        }
    ],
    "chunks": [
        {
            "content": "Physical AI combines artificial intelligence with physical systems to create intelligent robots that can interact with the real world. This field encompasses robotics, computer vision, natural language processing, and control theory. Unlike traditional AI that operates on data, Physical AI operates on physical systems and their interactions with the environment.",
            "chunk_type": "text",
            "source_document": "introduction_to_physical_ai.md",
            "source_page": 1,
            "module_id": 1,
            "chapter_id": 1
        },
        {
            "content": "ROS 2 (Robot Operating System 2) is the next generation of the Robot Operating System, designed for production environments. It provides libraries and tools to help software developers create robot applications with features like hardware abstraction, device drivers, libraries, visualizers, message-passing, package management, and more.",
            "chunk_type": "text",
            "source_document": "ros2_fundamentals.md",
            "source_page": 1,
            "module_id": 2,
            "chapter_id": 2
        },
        {
            "content": "Gazebo is a robot simulator that provides realistic physics simulation and rendering of environments. Unity is a game engine that can be used for robotics simulation with its robotics toolkit. Both platforms allow developers to test algorithms and behaviors in a safe, virtual environment before deploying to real robots.",
            "chunk_type": "text",
            "source_document": "simulation_environments.md",
            "source_page": 1,
            "module_id": 3,
            "chapter_id": 3
        },
        {
            "content": "The NVIDIA Isaac platform provides a complete solution for developing AI-powered robots. It includes Isaac ROS for hardware-accelerated perception, Isaac Sim for simulation, and Isaac Lab for reinforcement learning. The platform is optimized for NVIDIA GPUs and includes pre-trained models and reference applications.",
            "chunk_type": "text",
            "source_document": "nvidia_isaac_platform.md",
            "source_page": 1,
            "module_id": 4,
            "chapter_id": 4
        },
        {
            "content": "Vision-Language-Action (VLA) models are foundation models that combine visual perception, language understanding, and action generation. These models enable robots to follow natural language commands and perform complex manipulation tasks. Examples include RT-2, PaLM-E, and other embodied AI models that can operate in real-world environments.",
            "chunk_type": "text",
            "source_document": "vla_models.md",
            "source_page": 1,
            "module_id": 5,
            "chapter_id": 5
        },
        {
            "content": "ROS 2 architecture is built on DDS (Data Distribution Service) middleware, which provides quality of service policies, security, and multi-robot capabilities. The architecture supports multiple DDS implementations like Fast DDS, Cyclone DDS, and RTI Connext DDS, allowing for flexibility in deployment scenarios.",
            "chunk_type": "text",
            "source_document": "ros2_architecture.md",
            "source_page": 2,
            "module_id": 2,
            "chapter_id": 2
        }
    ],
    "assessments": [
        {
            "title": "Physical AI Quiz 1",
            "description": "Basic concepts of Physical AI",
            "content": "1. What is Physical AI?\n2. Name three components of Physical AI.\n3. How does Physical AI differ from traditional AI?",
            "assessment_type": "quiz",
            "difficulty_level": "beginner",
            "max_attempts": 3,
            "is_active": True,
            "module_id": 1,
            "chapter_id": 1
        },
        {
            "title": "ROS 2 Quiz 1",
            "description": "ROS 2 architecture and concepts",
            "content": "1. What is the main difference between ROS 1 and ROS 2?\n2. Explain the DDS middleware in ROS 2.\n3. How do you create a publisher and subscriber in ROS 2?",
            "assessment_type": "quiz",
            "difficulty_level": "intermediate",
            "max_attempts": 2,
            "is_active": True,
            "module_id": 2,
            "chapter_id": 2
        }
    ]
}

def get_sample_modules():
    """Get sample modules data"""
    return TEXTBOOK_CONTENT["modules"]

def get_sample_chapters():
    """Get sample chapters data"""
    return TEXTBOOK_CONTENT["chapters"]

def get_sample_chunks():
    """Get sample chunks data"""
    return TEXTBOOK_CONTENT["chunks"]

def get_sample_assessments():
    """Get sample assessments data"""
    return TEXTBOOK_CONTENT["assessments"]

def get_all_sample_data():
    """Get all sample data"""
    return TEXTBOOK_CONTENT
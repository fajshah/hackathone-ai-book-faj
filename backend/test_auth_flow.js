// Test script to verify the complete authentication flow
// This will register a user, login, and then test the ask endpoint

async function testAuthFlow() {
    console.log('🔐 Testing Authentication Flow...\n');

    try {
        // Step 1: Try to register a test user
        console.log('📝 Step 1: Registering test user...');
        const signupResponse = await fetch('http://localhost:8000/api/auth/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: 'testuser',
                email: 'test@example.com',
                full_name: 'Test User',
                password: 'testpassword123'
            })
        });

        console.log('   Signup Status:', signupResponse.status);

        if (signupResponse.status === 200) {
            console.log('   ✅ User registered successfully');
        } else if (signupResponse.status === 400) {
            console.log('   ℹ️  User already exists (this is OK)');
        } else {
            const errorData = await signupResponse.json();
            console.log('   Error:', errorData.detail);
        }

        // Step 2: Login to get access token
        console.log('\n🔑 Step 2: Logging in to get access token...');

        // For OAuth2PasswordRequestForm, we need to send form data, not JSON
        const formData = new URLSearchParams();
        formData.append('username', 'testuser');
        formData.append('password', 'testpassword123');

        const loginResponse = await fetch('http://localhost:8000/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData
        });

        console.log('   Login Status:', loginResponse.status);

        if (loginResponse.status === 200) {
            const tokenData = await loginResponse.json();
            const accessToken = tokenData.access_token;
            console.log('   ✅ Login successful');
            console.log('   🗝️  Access token received');

            // Step 3: Test the ask endpoint with the token
            console.log('\n💬 Step 3: Testing ask endpoint with authentication...');
            const askResponse = await fetch('http://localhost:8000/api/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                },
                body: JSON.stringify({
                    question: 'What is Physical AI?',
                    top_k: 3
                })
            });

            console.log('   Ask Status:', askResponse.status);

            if (askResponse.status === 200) {
                const askData = await askResponse.json();
                console.log('   ✅ Ask endpoint working with authentication');
                console.log('   📝 Response received:', typeof askData.answer === 'string' ? 'Answer received' : 'Unexpected response format');
            } else {
                const errorData = await askResponse.json();
                console.log('   Ask endpoint response:', errorData);
            }
        } else {
            console.log('   ❌ Login failed');
            const errorData = await loginResponse.json();
            console.log('   Error:', errorData.detail);
        }

        console.log('\n🎉 Authentication flow test completed!');

    } catch (error) {
        console.error('❌ Error during authentication test:', error.message);
    }
}

// Run the test
testAuthFlow();
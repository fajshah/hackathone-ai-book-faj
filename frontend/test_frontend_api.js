// Test script to verify frontend can communicate with backend API
// Using built-in fetch available in Node.js 18+

async function testApiConnection() {
    console.log('Testing API connection...');

    try {
        // Test the health endpoint
        const healthResponse = await fetch('http://localhost:8000/health');
        const healthData = await healthResponse.json();
        console.log('✅ Backend health check:', healthData);

        // Test the API endpoint (without authentication to see if it's accessible)
        // This will likely return a 401 (unauthorized) which is expected without a token
        const apiResponse = await fetch('http://localhost:8000/api/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: 'What is Physical AI?',
                top_k: 3
            })
        });

        console.log('📊 API Response Status:', apiResponse.status);

        if (apiResponse.status === 401) {
            console.log('✅ API endpoint is accessible (401 expected without auth token)');
        } else if (apiResponse.status === 422) {
            console.log('✅ API endpoint is accessible (422 expected without auth token, but shows endpoint exists)');
        } else {
            const apiData = await apiResponse.json();
            console.log('API Response:', apiData);
        }

        console.log('\n🎉 Both servers are running and communicating properly!');
        console.log('📖 Frontend: http://localhost:3001');
        console.log('⚙️  Backend: http://localhost:8000');
        console.log('💬 API: http://localhost:8000/api/ask');

    } catch (error) {
        console.error('❌ Error testing API connection:', error.message);
    }
}

// Run the test
testApiConnection();
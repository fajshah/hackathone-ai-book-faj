const testBetterAuth = async () => {
  try {
    console.log("Testing Better Auth service...");

    // Test health endpoint
    const healthResponse = await fetch('http://localhost:8002/health');
    console.log(`Health check status: ${healthResponse.status}`);
    console.log(`Health check response:`, await healthResponse.json());

    // Test if the auth endpoint is accessible
    const authResponse = await fetch('http://localhost:8002/api/auth/better');
    console.log(`Auth endpoint status: ${authResponse.status}`);

    console.log("Better Auth service is running successfully!");
  } catch (error) {
    console.error("Error testing Better Auth service:", error);
  }
};

testBetterAuth();
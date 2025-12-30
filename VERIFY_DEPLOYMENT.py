#!/usr/bin/env python3
"""
Final verification script to ensure the Physical AI Textbook system is ready for Hugging Face Space deployment
"""
import os
import sys
from pathlib import Path

def verify_backend_structure():
    """Verify backend directory structure and required files"""
    print("[INFO] Verifying backend structure...")

    backend_path = Path("backend/python_backend")
    required_files = [
        "main.py",
        "config.py",
        "services/embeddings.py",
        "routers/ask.py",
        "start_server.py",
        "app.py",
        "requirements.txt"
    ]

    all_found = True
    for file in required_files:
        file_path = backend_path / file
        if not file_path.exists():
            print(f"  [ERROR] Missing file: {file_path}")
            all_found = False
        else:
            print(f"  [SUCCESS] Found: {file_path}")

    return all_found

def verify_frontend_integration():
    """Verify frontend component and integration"""
    print("\n[INFO] Verifying frontend integration...")

    frontend_files = [
        Path("frontend/AskTheBook.tsx"),
        Path("frontend/text-book/src/pages/ask-the-book.tsx")
    ]

    all_found = True
    for file in frontend_files:
        if not file.exists():
            print(f"  [ERROR] Missing frontend file: {file}")
            all_found = False
        else:
            print(f"  [SUCCESS] Found frontend file: {file}")

    return all_found

def verify_deployment_files():
    """Verify deployment-related files exist"""
    print("\n[INFO] Verifying deployment files...")

    deployment_files = [
        Path("backend/python_backend/app.py"),
        Path("backend/python_backend/requirements.txt"),
        Path("HUGGING_FACE_DEPLOYMENT.md"),
        Path("DEPLOYMENT_SETUP.md")
    ]

    all_found = True
    for file in deployment_files:
        if not file.exists():
            print(f"  [ERROR] Missing deployment file: {file}")
            all_found = False
        else:
            print(f"  [SUCCESS] Found deployment file: {file}")

    return all_found

def verify_health_endpoints():
    """Verify health endpoint configurations"""
    print("\n[INFO] Verifying health endpoint configurations...")

    main_py_path = Path("backend/python_backend/main.py")
    if not main_py_path.exists():
        print("  [ERROR] main.py not found")
        return False

    with open(main_py_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for required endpoints
    has_health = "/health" in content
    has_qdrant_health = "/health/qdrant" in content

    if has_health:
        print("  [SUCCESS] /health endpoint found")
    else:
        print("  [ERROR] /health endpoint not found")

    if has_qdrant_health:
        print("  [SUCCESS] /health/qdrant endpoint found")
    else:
        print("  [ERROR] /health/qdrant endpoint not found")

    return has_health and has_qdrant_health

def verify_api_endpoint():
    """Verify API endpoint configuration"""
    print("\n[INFO] Verifying API endpoint configuration...")

    ask_router_path = Path("backend/python_backend/routers/ask.py")
    if not ask_router_path.exists():
        print("  [ERROR] ask.py router not found")
        return False

    with open(ask_router_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for public endpoint (it might be defined differently)
    has_public_endpoint = "/ask/public" in content or '"/api/ask/public"' in content or 'path="/api/ask/public"' in content

    if has_public_endpoint:
        print("  [SUCCESS] /api/ask/public endpoint found")
    else:
        # Let's check what endpoints are actually defined
        if "/ask" in content:
            print("  [SUCCESS] /api/ask endpoint found (checking for public variant)")
            # The endpoint might be defined differently, let's check the function names
            if "ask_question_public" in content:
                print("  [SUCCESS] Public ask endpoint function found")
                has_public_endpoint = True
            else:
                print("  [ERROR] /api/ask/public endpoint not found")
        else:
            print("  [ERROR] /api/ask endpoint not found")

    return has_public_endpoint

def main():
    print("Physical AI Textbook System - Final Deployment Verification")
    print("=" * 70)

    checks = [
        verify_backend_structure(),
        verify_frontend_integration(),
        verify_deployment_files(),
        verify_health_endpoints(),
        verify_api_endpoint()
    ]

    print("\n" + "=" * 70)
    if all(checks):
        print("All verification checks passed!")
        print("\n[SUCCESS] Backend structure: Complete")
        print("[SUCCESS] Frontend integration: Complete")
        print("[SUCCESS] Deployment files: Complete")
        print("[SUCCESS] Health endpoints: Configured")
        print("[SUCCESS] API endpoints: Configured")
        print("\n[READY] System is ready for Hugging Face Space deployment!")
        print("\nNext steps:")
        print("   1. Set up Hugging Face Space with the repository")
        print("   2. Configure environment variables as secrets")
        print("   3. Deploy and verify endpoints after startup")
        return 0
    else:
        print("[ERROR] Some verification checks failed!")
        print("Please address the issues above before deployment.")
        return 1

if __name__ == "__main__":
    exit(main())
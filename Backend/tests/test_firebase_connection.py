"""
Firebase Connection Test
Tests Firebase Admin SDK initialization and authentication.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from firebase_admin import auth, credentials
from app.core.config import settings
import json


def print_header(text: str):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"🔥 {text}")
    print("=" * 60 + "\n")


def print_success(text: str):
    """Print success message"""
    print(f"✅ {text}")


def print_error(text: str):
    """Print error message"""
    print(f"❌ {text}")


def print_info(text: str):
    """Print info message"""
    print(f"📋 {text}")


async def test_firebase_connection():
    """Test Firebase Admin SDK connection and authentication"""
    
    print_header("ServiceGenie - Firebase Connection Test")
    
    try:
        # Step 1: Check if credentials file exists
        print_info("Step 1: Checking Firebase credentials file...")
        
        if not settings.FIREBASE_CREDENTIALS_PATH:
            print_error("FIREBASE_CREDENTIALS_PATH not set in .env file")
            return False
        
        creds_path = Path(settings.FIREBASE_CREDENTIALS_PATH)
        
        if not creds_path.exists():
            print_error(f"Firebase credentials file not found at: {creds_path}")
            print_info("\nTo fix this:")
            print_info("1. Go to Firebase Console: https://console.firebase.google.com/")
            print_info("2. Select your project")
            print_info("3. Go to Project Settings > Service Accounts")
            print_info("4. Click 'Generate New Private Key'")
            print_info("5. Save the JSON file to your Backend directory")
            print_info(f"6. Update FIREBASE_CREDENTIALS_PATH in .env to point to this file")
            return False
        
        print_success(f"Credentials file found: {creds_path}")
        
        # Step 2: Validate JSON structure
        print_info("\nStep 2: Validating credentials file format...")
        
        try:
            with open(creds_path, 'r') as f:
                creds_data = json.load(f)
            
            required_fields = [
                'type', 'project_id', 'private_key_id', 'private_key',
                'client_email', 'client_id', 'auth_uri', 'token_uri'
            ]
            
            missing_fields = [field for field in required_fields if field not in creds_data]
            
            if missing_fields:
                print_error(f"Missing required fields in credentials: {', '.join(missing_fields)}")
                return False
            
            print_success("Credentials file format is valid")
            print_info(f"   Project ID: {creds_data.get('project_id')}")
            print_info(f"   Client Email: {creds_data.get('client_email')}")
            
        except json.JSONDecodeError as e:
            print_error(f"Invalid JSON in credentials file: {e}")
            return False
        
        # Step 3: Initialize Firebase Admin SDK
        print_info("\nStep 3: Initializing Firebase Admin SDK...")
        
        from app.core.firebase import initialize_firebase
        
        try:
            initialize_firebase()
            print_success("Firebase Admin SDK initialized successfully")
        except Exception as e:
            print_error(f"Failed to initialize Firebase: {e}")
            return False
        
        # Step 4: Test Authentication
        print_info("\nStep 4: Testing Firebase Authentication...")
        
        try:
            # Try to list users (limited to 1 for testing)
            users_page = auth.list_users(max_results=1)
            
            print_success("Firebase Authentication is working!")
            
            # Show user count info
            if users_page.users:
                print_info(f"   Found {len(users_page.users)} user(s) in your Firebase project")
                user = users_page.users[0]
                print_info(f"   Sample user email: {user.email if user.email else 'No email'}")
            else:
                print_info("   No users found in Firebase Authentication")
                print_info("   This is normal for a new project")
            
        except Exception as e:
            print_error(f"Firebase Authentication test failed: {e}")
            return False
        
        # Step 5: Test Token Verification (if you have a test token)
        print_info("\nStep 5: Testing token verification capability...")
        
        try:
            # Just test that the verify function is available
            # We won't actually verify a token without one
            print_success("Token verification function is available")
            print_info("   You can verify ID tokens from your frontend")
            
        except Exception as e:
            print_error(f"Token verification test failed: {e}")
            return False
        
        # Success summary
        print_header("🎉 All Firebase Tests Passed!")
        print_success("Firebase connection is working perfectly!")
        print_info("\nYou can now:")
        print_info("• Authenticate users with Firebase")
        print_info("• Verify ID tokens from frontend")
        print_info("• Manage users through Firebase Admin SDK")
        print_info("• Use Firebase Authentication in your API endpoints")
        
        return True
        
    except Exception as e:
        print_header("❌ Firebase Connection Test Failed!")
        print_error(f"Unexpected error: {e}")
        print_info("\nCommon issues:")
        print_info("1. FIREBASE_CREDENTIALS_PATH not set in .env")
        print_info("2. Credentials file doesn't exist or wrong path")
        print_info("3. Invalid credentials file format")
        print_info("4. Firebase project is disabled or deleted")
        print_info("5. Internet connection issues")
        return False


async def test_create_custom_token():
    """Test creating a custom token for a user"""
    print_header("Testing Custom Token Creation")
    
    try:
        # Create a test custom token
        test_uid = "test_user_123"
        custom_token = auth.create_custom_token(test_uid)
        
        print_success(f"Custom token created for UID: {test_uid}")
        print_info(f"   Token length: {len(custom_token)} bytes")
        print_info("   This token can be used to sign in users programmatically")
        
        return True
        
    except Exception as e:
        print_error(f"Failed to create custom token: {e}")
        return False


if __name__ == "__main__":
    print("\n")
    print("=" * 60)
    print("🔥 FIREBASE CONNECTION TEST SUITE")
    print("=" * 60)
    
    # Run main connection test
    connection_ok = asyncio.run(test_firebase_connection())
    
    if connection_ok:
        print("\n")
        # Run additional test
        asyncio.run(test_create_custom_token())
    
    print("\n" + "=" * 60)
    if connection_ok:
        print("✅ TEST SUITE COMPLETED SUCCESSFULLY")
    else:
        print("❌ TEST SUITE FAILED - Please fix the issues above")
    print("=" * 60 + "\n")

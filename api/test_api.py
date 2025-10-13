#!/usr/bin/env python3
"""
API Testing Script
Tests all endpoints with authentication flow
"""

import json
from typing import Optional

import requests

# API base URL
BASE_URL = "http://localhost:8000"

# Test user credentials
TEST_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123",
    "full_name": "Test User",
}

# ANSI colors
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def print_section(title: str):
    """Print a section header"""
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}{title}{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}\n")


def print_success(message: str):
    """Print success message"""
    print(f"{GREEN}✅ {message}{RESET}")


def print_error(message: str):
    """Print error message"""
    print(f"{RED}❌ {message}{RESET}")


def print_info(message: str):
    """Print info message"""
    print(f"{YELLOW}ℹ️  {message}{RESET}")


def test_health_check():
    """Test health check endpoint"""
    print_section("1. Testing Health Check")

    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print_success("Health check passed")
            print(json.dumps(response.json(), indent=2))
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error(
            "Cannot connect to API. Make sure it's running at http://localhost:8000"
        )
        return False


def test_register():
    """Test user registration"""
    print_section("2. Testing User Registration")

    response = requests.post(f"{BASE_URL}/auth/register", json=TEST_USER)

    if response.status_code == 200:
        print_success("User registered successfully")
        print(json.dumps(response.json(), indent=2))
        return True
    elif response.status_code == 400 and "already registered" in response.json().get(
        "detail", ""
    ):
        print_info("User already exists (this is OK)")
        return True
    else:
        print_error(f"Registration failed: {response.json()}")
        return False


def test_login() -> Optional[str]:
    """Test user login and return access token"""
    print_section("3. Testing User Login")

    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": TEST_USER["username"], "password": TEST_USER["password"]},
    )

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        print_success("Login successful")
        print(f"Access Token: {access_token[:50]}...")
        return access_token
    else:
        print_error(f"Login failed: {response.json()}")
        return None


def test_get_current_user(token: str):
    """Test getting current user info"""
    print_section("4. Testing Get Current User")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)

    if response.status_code == 200:
        print_success("Retrieved current user")
        print(json.dumps(response.json(), indent=2))
        return True
    else:
        print_error(f"Failed to get current user: {response.json()}")
        return False


def test_create_item(token: str) -> Optional[int]:
    """Test creating an item"""
    print_section("5. Testing Create Item")

    headers = {"Authorization": f"Bearer {token}"}
    item_data = {
        "title": "Test Item",
        "description": "This is a test item created by the API test script",
    }

    response = requests.post(f"{BASE_URL}/items", json=item_data, headers=headers)

    if response.status_code == 200:
        item = response.json()
        print_success("Item created successfully")
        print(json.dumps(item, indent=2))
        return item["id"]
    else:
        print_error(f"Failed to create item: {response.json()}")
        return None


def test_get_items(token: str):
    """Test getting all items"""
    print_section("6. Testing Get All Items")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/items", headers=headers)

    if response.status_code == 200:
        items = response.json()
        print_success(f"Retrieved {len(items)} items")
        print(json.dumps(items, indent=2))
        return True
    else:
        print_error(f"Failed to get items: {response.json()}")
        return False


def test_get_item(token: str, item_id: int):
    """Test getting a specific item"""
    print_section("7. Testing Get Specific Item")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/items/{item_id}", headers=headers)

    if response.status_code == 200:
        print_success(f"Retrieved item {item_id}")
        print(json.dumps(response.json(), indent=2))
        return True
    else:
        print_error(f"Failed to get item: {response.json()}")
        return False


def test_unauthorized_access():
    """Test accessing protected endpoint without token"""
    print_section("8. Testing Unauthorized Access")

    response = requests.get(f"{BASE_URL}/items")

    if response.status_code == 401:
        print_success("Unauthorized access correctly blocked")
        print(f"Response: {response.json()}")
        return True
    else:
        print_error("Unauthorized access should be blocked!")
        return False


def test_invalid_token():
    """Test accessing with invalid token"""
    print_section("9. Testing Invalid Token")

    headers = {"Authorization": "Bearer invalid_token_here"}
    response = requests.get(f"{BASE_URL}/items", headers=headers)

    if response.status_code == 401:
        print_success("Invalid token correctly rejected")
        print(f"Response: {response.json()}")
        return True
    else:
        print_error("Invalid token should be rejected!")
        return False


def test_delete_item(token: str, item_id: int):
    """Test deleting an item"""
    print_section("10. Testing Delete Item")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{BASE_URL}/items/{item_id}", headers=headers)

    if response.status_code == 200:
        print_success(f"Item {item_id} deleted successfully")
        print(json.dumps(response.json(), indent=2))
        return True
    else:
        print_error(f"Failed to delete item: {response.json()}")
        return False


def main():
    """Run all tests"""
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}🧪 REST API Testing Suite{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}")

    results = []

    # Test 1: Health check
    results.append(("Health Check", test_health_check()))
    if not results[-1][1]:
        print_error("\n⚠️  API is not running. Start it with: ./start-api.sh")
        return

    # Test 2: Register user
    results.append(("User Registration", test_register()))

    # Test 3: Login
    token = test_login()
    results.append(("User Login", token is not None))
    if not token:
        print_error("\n⚠️  Cannot continue without valid token")
        return

    # Test 4: Get current user
    results.append(("Get Current User", test_get_current_user(token)))

    # Test 5: Create item
    item_id = test_create_item(token)
    results.append(("Create Item", item_id is not None))

    # Test 6: Get all items
    results.append(("Get All Items", test_get_items(token)))

    # Test 7: Get specific item
    if item_id:
        results.append(("Get Specific Item", test_get_item(token, item_id)))

    # Test 8: Unauthorized access
    results.append(("Unauthorized Access Block", test_unauthorized_access()))

    # Test 9: Invalid token
    results.append(("Invalid Token Rejection", test_invalid_token()))

    # Test 10: Delete item
    if item_id:
        results.append(("Delete Item", test_delete_item(token, item_id)))

    # Print summary
    print_section("Test Summary")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = f"{GREEN}✅ PASS{RESET}" if result else f"{RED}❌ FAIL{RESET}"
        print(f"{status} - {test_name}")

    print(f"\n{BLUE}{'=' * 60}{RESET}")
    if passed == total:
        print(f"{GREEN}🎉 All {total} tests passed!{RESET}")
    else:
        print(f"{YELLOW}⚠️  {passed}/{total} tests passed{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}\n")


if __name__ == "__main__":
    main()

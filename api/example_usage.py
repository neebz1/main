#!/usr/bin/env python3
"""
Example: How to use the REST API from Python
Demonstrates the complete authentication flow
"""

from typing import Optional

import requests

# Base URL
BASE_URL = "http://localhost:8000"


class APIClient:
    """Simple API client with authentication"""

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.token: Optional[str] = None

    def register(self, username: str, email: str, password: str, full_name: str = None):
        """Register a new user"""
        response = requests.post(
            f"{self.base_url}/auth/register",
            json={
                "username": username,
                "email": email,
                "password": password,
                "full_name": full_name,
            },
        )
        response.raise_for_status()
        return response.json()

    def login(self, username: str, password: str):
        """Login and store access token"""
        response = requests.post(
            f"{self.base_url}/auth/login",
            data={"username": username, "password": password},
        )
        response.raise_for_status()
        data = response.json()
        self.token = data["access_token"]
        return data

    def get_current_user(self):
        """Get current user information"""
        if not self.token:
            raise ValueError("Not authenticated. Please login first.")

        response = requests.get(
            f"{self.base_url}/auth/me",
            headers={"Authorization": f"Bearer {self.token}"},
        )
        response.raise_for_status()
        return response.json()

    def create_item(self, title: str, description: str = None):
        """Create a new item"""
        if not self.token:
            raise ValueError("Not authenticated. Please login first.")

        response = requests.post(
            f"{self.base_url}/items",
            json={"title": title, "description": description},
            headers={"Authorization": f"Bearer {self.token}"},
        )
        response.raise_for_status()
        return response.json()

    def get_items(self):
        """Get all user's items"""
        if not self.token:
            raise ValueError("Not authenticated. Please login first.")

        response = requests.get(
            f"{self.base_url}/items", headers={"Authorization": f"Bearer {self.token}"}
        )
        response.raise_for_status()
        return response.json()

    def get_item(self, item_id: int):
        """Get a specific item"""
        if not self.token:
            raise ValueError("Not authenticated. Please login first.")

        response = requests.get(
            f"{self.base_url}/items/{item_id}",
            headers={"Authorization": f"Bearer {self.token}"},
        )
        response.raise_for_status()
        return response.json()

    def delete_item(self, item_id: int):
        """Delete an item"""
        if not self.token:
            raise ValueError("Not authenticated. Please login first.")

        response = requests.delete(
            f"{self.base_url}/items/{item_id}",
            headers={"Authorization": f"Bearer {self.token}"},
        )
        response.raise_for_status()
        return response.json()


def main():
    """Example usage of the API client"""

    print("🚀 API Client Example\n")

    # Create client
    client = APIClient()

    # Example user credentials
    username = "demo_user"
    email = "demo@example.com"
    password = "SecurePass123"

    try:
        # 1. Register a user (or skip if already exists)
        print("1️⃣  Registering user...")
        try:
            user = client.register(username, email, password, "Demo User")
            print(f"✅ Registered: {user['username']}")
        except requests.exceptions.HTTPError as e:
            if "already registered" in str(e.response.text):
                print("ℹ️  User already exists, continuing...")
            else:
                raise

        # 2. Login
        print("\n2️⃣  Logging in...")
        token_data = client.login(username, password)
        print(f"✅ Logged in! Token: {token_data['access_token'][:50]}...")

        # 3. Get current user
        print("\n3️⃣  Getting current user info...")
        current_user = client.get_current_user()
        print(f"✅ Current user: {current_user['username']} ({current_user['email']})")

        # 4. Create an item
        print("\n4️⃣  Creating an item...")
        new_item = client.create_item(
            title="My First Item",
            description="This item was created via the Python API client",
        )
        print(f"✅ Created item #{new_item['id']}: {new_item['title']}")

        # 5. Get all items
        print("\n5️⃣  Getting all items...")
        items = client.get_items()
        print(f"✅ Found {len(items)} item(s):")
        for item in items:
            print(f"   - #{item['id']}: {item['title']}")

        # 6. Get specific item
        print(f"\n6️⃣  Getting item #{new_item['id']}...")
        item = client.get_item(new_item["id"])
        print(f"✅ Retrieved: {item['title']}")
        print(f"   Description: {item['description']}")
        print(f"   Created: {item['created_at']}")

        # 7. Delete item (optional - uncomment to delete)
        # print(f"\n7️⃣  Deleting item #{new_item['id']}...")
        # result = client.delete_item(new_item['id'])
        # print(f"✅ {result['message']}")

        print("\n✅ All operations completed successfully!")

    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to API")
        print("Make sure the API is running: ./start-api.sh")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()

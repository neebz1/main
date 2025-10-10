#!/usr/bin/env python3
"""
Auto-deploy to Hugging Face using API
"""

from huggingface_hub import HfApi, create_repo, upload_file
import os
from pathlib import Path

# Load HF token from environment
from dotenv import load_dotenv
load_dotenv()
HF_TOKEN = os.getenv('HF_TOKEN')

# Initialize API
api = HfApi(token=HF_TOKEN)

# Get username
user_info = api.whoami(token=HF_TOKEN)
username = user_info['name']

print(f"🤖 Logged in as: {username}")
print("=" * 60)

# Create space
space_name = "noah-ai-builder"
repo_id = f"{username}/{space_name}"

print(f"📦 Creating Space: {repo_id}")

try:
    # Create the space
    create_repo(
        repo_id=repo_id,
        token=HF_TOKEN,
        repo_type="space",
        space_sdk="gradio",
        private=False
    )
    print(f"✅ Space created!")
except Exception as e:
    if "already exists" in str(e):
        print(f"✅ Space already exists!")
    else:
        print(f"⚠️  {e}")

# Upload files
print("\n📤 Uploading files...")

files_to_upload = [
    ("app.py", "app.py"),
    ("requirements.txt", "requirements.txt"),
    ("README-HUGGINGFACE.md", "README.md"),
]

for local_file, remote_file in files_to_upload:
    try:
        upload_file(
            path_or_fileobj=local_file,
            path_in_repo=remote_file,
            repo_id=repo_id,
            repo_type="space",
            token=HF_TOKEN
        )
        print(f"  ✅ Uploaded: {remote_file}")
    except Exception as e:
        print(f"  ⚠️  {remote_file}: {e}")

print("\n" + "=" * 60)
print("🎉 DEPLOYMENT COMPLETE!")
print("=" * 60)
print(f"\n🌐 Your Space URL:")
print(f"   https://huggingface.co/spaces/{repo_id}")
print(f"\n📱 Direct App URL:")
print(f"   https://{username}-{space_name}.hf.space")
print("\n⚠️  Remember to add TOGETHER_API_KEY to Space Secrets!")
print("   Go to: Settings → Variables and secrets")
print("\n🚀 Space is building (takes ~2 minutes)...")
print("\nOpen this URL on your phone to test! 📱")


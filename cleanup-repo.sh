#!/bin/bash

# GitHub Repository Cleanup Script
# This script removes redundant files from your repository
# Read GITHUB-CLEANUP-GUIDE.md for more details

echo "🧹 GitHub Repository Cleanup Script"
echo "===================================="
echo ""
echo "This script will:"
echo "  ✅ Create a backup of your repository"
echo "  ✅ Delete 40+ redundant files"
echo "  ✅ Keep only essential files"
echo ""
echo "⚠️  WARNING: This will delete files from your repository!"
echo "📦 A backup will be created on your Desktop first."
echo ""
read -p "Do you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Cleanup cancelled."
    exit 0
fi

echo ""
echo "📦 Step 1: Creating backup..."

# Create backup
backup_name="main-backup-$(date +%Y%m%d-%H%M%S).zip"
cd /Users/nr/main
zip -r ~/Desktop/$backup_name . -x "*.git*" "venv/*" "__pycache__/*" 2>&1 | grep -v "adding:"

if [ -f ~/Desktop/$backup_name ]; then
    echo "✅ Backup created: ~/Desktop/$backup_name"
else
    echo "❌ Backup failed! Aborting cleanup."
    exit 1
fi

echo ""
echo "🗑️  Step 2: Deleting redundant files..."

# Count files before
files_before=$(ls -1 | wc -l)

# Delete redundant documentation
rm -f CLEANUP-COMPLETE.md \
      AI-MIXING-ENGINEER-COMPLETE.md \
      AI-MIXING-ENGINEER-GUIDE.md \
      CHATGPT-TRAINING-SUMMARY.md \
      CLOUD-BUILDER-GUIDE.md \
      COMPLETE-AI-SUITE-SUMMARY.md \
      COMPLETE-SETUP-FINAL.md \
      DEPLOY-TO-HUGGINGFACE.md \
      FINAL-SETUP-SUMMARY.md \
      FINAL-TEST-STATUS.md \
      HOW-TO-USE-YOUR-AI-TOOLS.md \
      HUGGINGFACE-RESEARCH-SUMMARY.md \
      HUGGINGFACE-TRAINING-GUIDE.md \
      LIVE-AI-ASSISTANT-GUIDE.md \
      LOGIC-AI-PLUGIN-GUIDE.md \
      MASTER-GUIDE.md \
      MUSIC-AI-GUIDE.md \
      QUICK-START-CHATGPT-TRAINING.md \
      README-AI-SUITE.md \
      README-CHATGPT-TRAINING.md \
      README-HUGGINGFACE.md \
      README_HF.md \
      SESSION-SUMMARY.md \
      START-HERE-CHATGPT-TRAINING.md \
      YOUR-CLOUD-AI-IS-LIVE.md \
      AI_PROVIDERS.md \
      QUICK-REFERENCE.txt

# Delete extra scripts
rm -f ai_mixing_engineer.py \
      app.py \
      cloud_ai_builder.py \
      convert_chatgpt_export.py \
      demo_chatbot.py \
      live_ai_assistant.py \
      logic_ai_plugin.py \
      train_chatgpt_model.py \
      LogicAI_Scripter.js \
      example_chatgpt_data.json

# Delete extra requirements files
rm -f requirements.txt \
      requirements_chatgpt_training.txt \
      requirements_live_ai.txt \
      requirements_mixing.txt \
      requirements_plugin.txt

# Delete extra shell scripts
rm -f setup-chatgpt-training.sh \
      start-ai-mixing-engineer.sh \
      start-cloud-builder.sh \
      start-live-ai-assistant.sh \
      start-logic-ai-plugin.sh

# Count files after
files_after=$(ls -1 | wc -l)
files_deleted=$((files_before - files_after))

echo "✅ Deleted $files_deleted files"

echo ""
echo "📊 Cleanup Summary:"
echo "   Before: $files_before files"
echo "   After:  $files_after files"
echo "   Deleted: $files_deleted files"

echo ""
echo "📁 Essential files kept:"
echo "   ✅ README.md"
echo "   ✅ START-HERE.md"
echo "   ✅ GITHUB-CLEANUP-GUIDE.md"
echo "   ✅ LICENSE"
echo "   ✅ logic_copilot_lite.py"
echo "   ✅ start-music-ai.sh"
echo "   ✅ requirements_lite.txt"
echo "   ✅ sound_packs/"
echo "   ✅ .env (your API keys)"
echo "   ✅ .gitignore"

echo ""
echo "🎯 Next Steps:"
echo ""
echo "1. Review what was deleted:"
echo "   git status"
echo ""
echo "2. If everything looks good, commit:"
echo "   git add ."
echo "   git commit -m 'Clean up repository - removed redundant files'"
echo "   git push"
echo ""
echo "3. If you want to undo everything:"
echo "   git reset --hard"
echo ""
echo "✅ Cleanup complete! Your repository is now clean and organized."
echo ""
echo "📖 For more information, read: GITHUB-CLEANUP-GUIDE.md"

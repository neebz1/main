# 🤖 ChatGPT Model Training Guide

Train your own custom ChatGPT-style AI model using your conversation data.

---

## 🎯 What This Does

This toolkit allows you to:
- Export your ChatGPT conversation history
- Convert it to training format
- Train a custom AI model
- Deploy it for personal use
- Chat with your AI trained on your conversations

---

## 🚀 Quick Start

### 1. Setup (5 minutes)

```bash
# Run the setup script
./setup-chatgpt-training.sh

# This installs all dependencies and prepares your environment
```

### 2. Export Your ChatGPT Data

1. Go to ChatGPT settings
2. Click "Data Controls" → "Export Data"
3. Wait for email with download link
4. Download `conversations.json`
5. Place it in this directory

### 3. Convert Your Data

```bash
# Convert ChatGPT export to training format
python3 convert_chatgpt_export.py conversations.json

# Output: training_data.jsonl
```

### 4. Train Your Model

```bash
# Train on your conversations
python3 train_chatgpt_model.py

# This will:
# - Load your training data
# - Fine-tune a language model
# - Save the trained model
```

### 5. Chat With Your Model

```bash
# Launch the chatbot interface
python3 demo_chatbot.py

# Opens in browser at localhost:7862
```

---

## 📋 Detailed Workflow

### Step 1: Data Export

**From ChatGPT:**
1. Open ChatGPT (https://chat.openai.com)
2. Click your profile → Settings
3. Data Controls → Export Data
4. Confirm export
5. Wait for email (can take 24 hours)
6. Download ZIP file
7. Extract `conversations.json`

**What you get:**
- All your conversations
- Timestamps
- Full message history
- All models used

### Step 2: Data Conversion

```bash
python3 convert_chatgpt_export.py conversations.json
```

**What it does:**
- Parses ChatGPT's JSON format
- Extracts Q&A pairs
- Formats for model training
- Filters out system messages
- Creates `training_data.jsonl`

**Options:**
```bash
# Process specific conversation
python3 convert_chatgpt_export.py conversations.json --conversation-id "abc123"

# Limit number of examples
python3 convert_chatgpt_export.py conversations.json --max-examples 1000

# Filter by date range
python3 convert_chatgpt_export.py conversations.json --start-date "2024-01-01" --end-date "2024-12-31"
```

### Step 3: Model Training

```bash
python3 train_chatgpt_model.py
```

**What happens:**
1. Loads `training_data.jsonl`
2. Initializes base language model
3. Fine-tunes on your conversations
4. Validates on test set
5. Saves trained model to `./trained_model/`

**Training parameters:**
- **Epochs:** 3-5 (adjust in script)
- **Learning rate:** 2e-5
- **Batch size:** 4-8 (depends on GPU)
- **Max length:** 512 tokens

**Hardware requirements:**
- **CPU only:** Works but slow (hours)
- **GPU:** Much faster (minutes)
- **RAM:** 8GB minimum, 16GB recommended
- **Disk:** 5GB for model storage

### Step 4: Testing Your Model

```bash
python3 demo_chatbot.py
```

**Features:**
- Web-based chat interface
- Real-time responses
- Conversation history
- Model temperature control
- System prompt customization

**Access:** http://localhost:7862

---

## 🎓 Advanced Usage

### Custom Training Parameters

Edit `train_chatgpt_model.py`:

```python
# Training configuration
EPOCHS = 5  # More epochs = better learning (but slower)
BATCH_SIZE = 8  # Larger batch = more stable (needs more RAM)
LEARNING_RATE = 2e-5  # Lower = more careful learning
MAX_LENGTH = 512  # Longer = more context (needs more RAM)
```

### Data Filtering

```python
# In convert_chatgpt_export.py

# Only include conversations with specific keywords
filter_keywords = ["coding", "python", "AI"]

# Exclude certain topics
exclude_keywords = ["personal", "private"]

# Minimum conversation length
min_turns = 3  # Only conversations with 3+ messages
```

### Model Selection

Change base model in `train_chatgpt_model.py`:

```python
# Options:
MODEL_NAME = "microsoft/DialoGPT-medium"  # Default, balanced
MODEL_NAME = "microsoft/DialoGPT-small"   # Faster, less accurate
MODEL_NAME = "microsoft/DialoGPT-large"   # Slower, more accurate
MODEL_NAME = "facebook/blenderbot-400M-distill"  # Alternative
```

---

## 💡 Training Tips

### 1. Data Quality Matters
- More conversations = better model
- Diverse topics = more versatile AI
- Clear Q&A format = best results
- Remove personal info before training

### 2. Start Small
- Test with 100 conversations first
- Verify quality before full training
- Iterate on parameters
- Scale up gradually

### 3. Monitor Training
- Watch loss decrease (should go down)
- Test on validation set
- Stop if overfitting occurs
- Save checkpoints regularly

### 4. Optimize Performance
- Use GPU if available
- Adjust batch size for your RAM
- Use mixed precision training
- Cache processed data

### 5. Evaluate Results
- Test on varied prompts
- Compare to ChatGPT responses
- Check for biases
- Iterate and improve

---

## 📊 Example Results

### Before Training (Base Model)
```
You: How do I write a Python function?
AI: [Generic response]
```

### After Training (Your Model)
```
You: How do I write a Python function?
AI: [Response in your style, with your preferences, 
     using examples similar to your conversations]
```

---

## 🔧 Troubleshooting

### "Out of Memory" Error
- Reduce batch size: `BATCH_SIZE = 2`
- Reduce max length: `MAX_LENGTH = 256`
- Use smaller model: `DialoGPT-small`
- Close other applications

### "No Training Data" Error
- Verify `training_data.jsonl` exists
- Check file is not empty
- Re-run conversion script
- Check file permissions

### Poor Quality Responses
- Train longer: More epochs
- Use more data: Export more conversations
- Adjust temperature: Lower = more focused
- Try different base model

### Slow Training
- Use GPU if available
- Reduce dataset size
- Use smaller model
- Increase batch size (if RAM allows)

---

## 📁 Files Structure

```
/home/runner/work/main/main/
├── setup-chatgpt-training.sh          ← Setup script
├── convert_chatgpt_export.py          ← Data conversion
├── train_chatgpt_model.py             ← Training script
├── demo_chatbot.py                    ← Chat interface
├── requirements_chatgpt_training.txt  ← Dependencies
├── example_chatgpt_data.json          ← Example data
├── conversations.json                 ← Your ChatGPT export (you provide)
├── training_data.jsonl                ← Converted training data
└── trained_model/                     ← Your trained model (created)
```

---

## 💰 Costs

- **Data export:** Free
- **Training:** Free (uses local compute)
- **Deployment:** Free (runs locally)
- **APIs:** Optional (if you want to use OpenAI/OpenRouter instead)

**Total cost: $0** (just your computer's electricity!)

---

## 🎯 Use Cases

### 1. Personal AI Assistant
Train on your work conversations to get an AI that understands your domain expertise.

### 2. Writing Style Clone
Train on your writing to generate content in your voice.

### 3. Knowledge Base
Train on Q&A to create a searchable knowledge bot.

### 4. Learning Tool
Train to create a tutor that knows your learning style.

### 5. Creative Partner
Train on brainstorming sessions for idea generation.

---

## 🚀 Next Steps

After training your model:

1. **Deploy it:** Run `demo_chatbot.py` anytime
2. **Share it:** Package and share with team (ensure no personal data)
3. **Iterate:** Export more conversations and retrain
4. **Integrate:** Use in your apps via API
5. **Experiment:** Try different models and parameters

---

## 🔒 Privacy & Security

- **All training happens locally** (no data sent to cloud)
- **Your conversations stay on your machine**
- **Review data before training** (remove sensitive info)
- **Don't share trained model** if it contains personal data
- **Use .env for any API keys** (never commit)

---

## 📚 Additional Resources

- **Hugging Face Transformers:** https://huggingface.co/docs/transformers
- **DialoGPT Paper:** https://arxiv.org/abs/1911.00536
- **Fine-tuning Guide:** https://huggingface.co/docs/transformers/training

---

**Made with ❤️ for AI enthusiasts who want their own personal AI!**

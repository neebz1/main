# Quick Start: Train Your ChatGPT Model

This guide will get you training a custom AI model from ChatGPT transcripts in under 10 minutes!

## 📋 Prerequisites

- Python 3.8 or higher
- GPU recommended (but CPU works for small models)
- ChatGPT conversation exports

## 🚀 Setup

### 1. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv chatgpt_training_env
source chatgpt_training_env/bin/activate  # On Windows: chatgpt_training_env\Scripts\activate

# Install required packages
pip install -r requirements_chatgpt_training.txt
```

### 2. Prepare Your Data

#### Option A: Export from ChatGPT

1. Go to ChatGPT Settings → Data Controls
2. Click "Export data"
3. Download your conversations
4. Convert to the required format (see below)

#### Option B: Use Example Data

Use the provided `example_chatgpt_data.json` to test the system first.

### 3. Format Your Data

Your data should be in JSON format like this:

```json
[
  {
    "messages": [
      {"role": "user", "content": "Your question here"},
      {"role": "assistant", "content": "ChatGPT's response here"}
    ]
  }
]
```

**Save as:** `my_chatgpt_conversations.json`

## 🏃 Quick Training

### Basic Training (Recommended for First Try)

```bash
python train_chatgpt_model.py \
  --data example_chatgpt_data.json \
  --model microsoft/DialoGPT-medium \
  --epochs 3 \
  --output ./my-custom-chatbot
```

This will:
- Use the small DialoGPT model (fast training)
- Train for 3 epochs (~10-30 minutes on GPU)
- Save the model to `./my-custom-chatbot`

### Advanced Training (For Better Results)

```bash
python train_chatgpt_model.py \
  --data my_chatgpt_conversations.json \
  --model meta-llama/Llama-2-7b-chat-hf \
  --epochs 5 \
  --batch-size 4 \
  --max-length 1024 \
  --output ./my-llama-chatbot
```

**Note:** You'll need Hugging Face access for LLaMA models:
```bash
huggingface-cli login
```

## 🧪 Test Your Model

### Interactive Chat Script

Create `test_model.py`:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load your model
model_path = "./my-custom-chatbot"
model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

print("🤖 Your Custom ChatBot is Ready!")
print("Type 'quit' to exit\n")

conversation = []

while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        break
    
    # Add to conversation
    conversation.append({"role": "user", "content": user_input})
    
    # Format and generate
    prompt = tokenizer.apply_chat_template(conversation, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            temperature=0.7,
            do_sample=True
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Extract assistant response
    assistant_msg = response.split("assistant")[-1].strip()
    
    conversation.append({"role": "assistant", "content": assistant_msg})
    print(f"Bot: {assistant_msg}\n")
```

Run it:
```bash
python test_model.py
```

## 📊 Training Tips

### For Limited GPU Memory

```bash
# Use smaller batch size and enable gradient accumulation
python train_chatgpt_model.py \
  --data my_data.json \
  --model microsoft/DialoGPT-small \
  --batch-size 2 \
  --max-length 256 \
  --output ./my-model
```

### For CPU Training

```bash
# Use smallest model and reduced parameters
python train_chatgpt_model.py \
  --data my_data.json \
  --model gpt2 \
  --batch-size 1 \
  --epochs 2 \
  --no-fp16 \
  --output ./my-model
```

### For Best Quality

```bash
# Use LLaMA 2 with LoRA
python train_chatgpt_model.py \
  --data my_data.json \
  --model meta-llama/Llama-2-7b-chat-hf \
  --epochs 5 \
  --batch-size 4 \
  --learning-rate 2e-4 \
  --max-length 2048 \
  --output ./my-llama-model
```

## 🌐 Deploy Your Model

### Option 1: Gradio Web Interface

Create `app.py`:

```python
import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("./my-custom-chatbot")
tokenizer = AutoTokenizer.from_pretrained("./my-custom-chatbot")

def chat(message, history):
    messages = []
    for h in history:
        messages.append({"role": "user", "content": h[0]})
        messages.append({"role": "assistant", "content": h[1]})
    messages.append({"role": "user", "content": message})
    
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=256)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return response.split("assistant")[-1].strip()

demo = gr.ChatInterface(
    chat,
    title="My Custom ChatGPT Bot",
    description="Trained on my conversations"
)

demo.launch(share=True)
```

Run:
```bash
python app.py
```

### Option 2: Upload to Hugging Face

```bash
# Login
huggingface-cli login

# Train with auto-upload
python train_chatgpt_model.py \
  --data my_data.json \
  --model microsoft/DialoGPT-medium \
  --push-to-hub \
  --hub-name my-username/my-chatbot \
  --output ./my-model
```

## 📈 Monitor Training

Training creates a TensorBoard log:

```bash
# In another terminal
tensorboard --logdir ./my-custom-chatbot/runs
```

Open http://localhost:6006 to see:
- Loss curves
- Learning rate schedule
- Evaluation metrics

## 🎯 Data Recommendations

### Minimum Data Requirements

- **Quick Test**: 50-100 conversations
- **Decent Results**: 500-1,000 conversations
- **Production Quality**: 5,000+ conversations

### Data Quality Tips

1. **Diversity**: Include various topics
2. **Length**: Mix short and long conversations
3. **Quality**: Remove errors and irrelevant content
4. **Format**: Consistent structure
5. **Clean**: Remove personal information

## ❓ Troubleshooting

### "CUDA out of memory"

```bash
# Reduce batch size or max length
python train_chatgpt_model.py --batch-size 1 --max-length 256 ...
```

### "Model not found"

Some models require authentication:

```bash
huggingface-cli login
# Enter your access token
```

### Slow training

- Use GPU if available
- Reduce `--max-length`
- Use smaller model
- Enable LoRA (default)

### Poor results

- Train longer (more epochs)
- Use more data
- Try different base model
- Adjust learning rate

## 🔗 Next Steps

1. ✅ Train on example data
2. ✅ Format your ChatGPT conversations
3. ✅ Train with your data
4. ✅ Test the model
5. ✅ Deploy as web app
6. ✅ Share on Hugging Face

## 📚 Additional Resources

- **Full Guide**: See `HUGGINGFACE-TRAINING-GUIDE.md`
- **Hugging Face Docs**: https://huggingface.co/docs
- **Community**: https://discuss.huggingface.co/

## 💡 Example Commands

```bash
# Test run (fast)
python train_chatgpt_model.py --data example_chatgpt_data.json --model gpt2 --epochs 2

# Production run (quality)
python train_chatgpt_model.py --data my_data.json --model meta-llama/Llama-2-7b-chat-hf --epochs 5

# Push to Hub
python train_chatgpt_model.py --data my_data.json --push-to-hub --hub-name username/my-bot
```

---

**Ready to train your AI? Start with the test run above! 🚀**


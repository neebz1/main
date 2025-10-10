# Train Your Own AI from ChatGPT Conversations 🤖

**Transform hundreds of ChatGPT transcripts into your own custom AI model using Hugging Face!**

This complete toolkit provides everything you need to train, test, and deploy a personalized conversational AI agent based on your ChatGPT conversation history.

## 📦 What's Included

| File | Description |
|------|-------------|
| `HUGGINGFACE-TRAINING-GUIDE.md` | Comprehensive 60-page guide with all theory and details |
| `QUICK-START-CHATGPT-TRAINING.md` | 10-minute quick start guide |
| `train_chatgpt_model.py` | Main training script (production-ready) |
| `convert_chatgpt_export.py` | Convert ChatGPT exports to training format |
| `demo_chatbot.py` | Interactive chat interface to test your model |
| `requirements_chatgpt_training.txt` | All required dependencies |
| `example_chatgpt_data.json` | Example data to test the system |

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
# Create virtual environment
python -m venv chatgpt_env
source chatgpt_env/bin/activate  # On Windows: chatgpt_env\Scripts\activate

# Install requirements
pip install -r requirements_chatgpt_training.txt
```

### Step 2: Test with Example Data

```bash
# Train on example data (takes ~10 minutes on GPU)
python train_chatgpt_model.py \
  --data example_chatgpt_data.json \
  --model microsoft/DialoGPT-medium \
  --epochs 3 \
  --output ./my-first-chatbot
```

### Step 3: Chat with Your Model

```bash
# Interactive chat
python demo_chatbot.py ./my-first-chatbot
```

**That's it!** You now have a working AI chatbot trained on example data.

## 📊 Using Your Own ChatGPT Data

### Export Your ChatGPT Conversations

1. Go to [ChatGPT Settings](https://chat.openai.com/) → Data Controls
2. Click "Export data"
3. Download the ZIP file
4. Extract `conversations.json`

### Convert to Training Format

```bash
python convert_chatgpt_export.py \
  conversations.json \
  my_training_data.json \
  --preview
```

This will:
- ✅ Convert ChatGPT export format to training format
- ✅ Filter out incomplete conversations
- ✅ Show statistics and preview
- ✅ Save ready-to-use training data

### Train Your Custom Model

```bash
python train_chatgpt_model.py \
  --data my_training_data.json \
  --model microsoft/DialoGPT-medium \
  --epochs 5 \
  --batch-size 4 \
  --output ./my-custom-chatbot
```

### Test Your Model

```bash
python demo_chatbot.py ./my-custom-chatbot
```

## 🎯 Training Options

### Available Models

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| `gpt2` | 124M | ⚡⚡⚡ | ⭐⭐ | Quick tests |
| `microsoft/DialoGPT-medium` | 345M | ⚡⚡ | ⭐⭐⭐ | **Recommended start** |
| `microsoft/DialoGPT-large` | 762M | ⚡ | ⭐⭐⭐⭐ | Better quality |
| `meta-llama/Llama-2-7b-chat-hf` | 7B | ⚡ | ⭐⭐⭐⭐⭐ | **Best quality** |
| `mistralai/Mistral-7B-Instruct-v0.1` | 7B | ⚡ | ⭐⭐⭐⭐⭐ | Task-oriented |

### Training Examples

#### For Beginners
```bash
python train_chatgpt_model.py \
  --data my_data.json \
  --model microsoft/DialoGPT-medium \
  --epochs 3
```

#### For Best Quality
```bash
# Requires GPU with 16GB+ VRAM (or uses LoRA automatically)
python train_chatgpt_model.py \
  --data my_data.json \
  --model meta-llama/Llama-2-7b-chat-hf \
  --epochs 5 \
  --max-length 2048 \
  --learning-rate 2e-4
```

#### For Limited GPU Memory
```bash
python train_chatgpt_model.py \
  --data my_data.json \
  --model microsoft/DialoGPT-small \
  --batch-size 2 \
  --max-length 256
```

#### CPU Training (Slow but Works)
```bash
python train_chatgpt_model.py \
  --data my_data.json \
  --model gpt2 \
  --batch-size 1 \
  --epochs 2 \
  --no-fp16
```

## 🌐 Deployment Options

### Option 1: Interactive Chat (Local)

```bash
python demo_chatbot.py ./my-custom-chatbot
```

Features:
- Interactive conversation
- Conversation history
- Commands: `quit`, `clear`, `history`

### Option 2: Gradio Web Interface

Create `app.py`:

```python
import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("./my-custom-chatbot")
tokenizer = AutoTokenizer.from_pretrained("./my-custom-chatbot")

def chat(message, history):
    # Your chat logic here
    return "Response"

demo = gr.ChatInterface(chat, title="My Custom AI")
demo.launch(share=True)  # Creates public URL
```

Run:
```bash
pip install gradio
python app.py
```

### Option 3: Upload to Hugging Face

```bash
# Login to Hugging Face
huggingface-cli login

# Train and auto-upload
python train_chatgpt_model.py \
  --data my_data.json \
  --push-to-hub \
  --hub-name your-username/my-chatbot
```

Your model will be at: `https://huggingface.co/your-username/my-chatbot`

### Option 4: Deploy to Hugging Face Spaces (Free)

1. Create Space at [huggingface.co/spaces](https://huggingface.co/spaces)
2. Select "Gradio" template
3. Upload your app.py and model
4. Your chatbot will have a public URL!

## 📈 Training Tips

### Data Requirements

| Goal | Minimum Conversations | Recommended |
|------|----------------------|-------------|
| Quick Test | 50-100 | 100+ |
| Decent Quality | 500-1,000 | 1,000+ |
| Production | 2,000-5,000 | 5,000+ |
| High Quality | 5,000+ | 10,000+ |

### GPU Requirements

| Model Size | Minimum GPU | Recommended | Training Time* |
|------------|-------------|-------------|----------------|
| < 1B params | 6GB | 8GB | 1-2 hours |
| 1-3B params | 8GB | 16GB | 3-6 hours |
| 7B params (LoRA) | 16GB | 24GB | 8-12 hours |
| 7B params (Full) | 40GB | 80GB | 24+ hours |

*For ~1,000 conversations, 3 epochs

### Monitoring Training

```bash
# In another terminal while training
tensorboard --logdir ./my-custom-chatbot/runs
```

Open http://localhost:6006 to see:
- Training loss
- Validation loss
- Learning rate schedule
- GPU usage

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| CUDA out of memory | Reduce `--batch-size` or `--max-length` |
| Training too slow | Use smaller model or enable GPU |
| Poor quality responses | Train longer, use more data, or try larger model |
| Model not found | Run `huggingface-cli login` for gated models |
| Import errors | Run `pip install -r requirements_chatgpt_training.txt` |

## 🎓 Learning Resources

### Included Guides

1. **QUICK-START-CHATGPT-TRAINING.md** - Get started in 10 minutes
2. **HUGGINGFACE-TRAINING-GUIDE.md** - Complete 60-page guide with:
   - Data preparation strategies
   - Model selection guide
   - Training approaches (AutoTrain vs Manual)
   - LoRA/QLoRA for efficient training
   - Deployment options
   - Code examples and best practices

### External Resources

- [Hugging Face Documentation](https://huggingface.co/docs)
- [Transformers Library](https://huggingface.co/docs/transformers)
- [PEFT (LoRA) Guide](https://huggingface.co/docs/peft)
- [Hugging Face Forums](https://discuss.huggingface.co/)

## 🛠️ Advanced Features

### Using LoRA for Efficient Training

LoRA (Low-Rank Adaptation) is **enabled by default** and allows:
- Training 7B models on 16GB GPU
- 90% less memory usage
- Faster training
- Same quality as full fine-tuning

Disable with `--no-lora` flag.

### Custom Training Parameters

```bash
python train_chatgpt_model.py \
  --data my_data.json \
  --model meta-llama/Llama-2-7b-chat-hf \
  --epochs 5 \
  --batch-size 4 \
  --learning-rate 2e-4 \
  --max-length 2048 \
  --validation-split 0.1 \
  --output ./my-model
```

### Hyperparameter Tuning

| Parameter | Default | Range | Effect |
|-----------|---------|-------|--------|
| `--epochs` | 3 | 2-10 | More epochs = better learning, risk overfitting |
| `--batch-size` | 4 | 1-32 | Larger = faster training, needs more memory |
| `--learning-rate` | 2e-4 | 1e-5 to 5e-4 | Higher = faster learning, less stable |
| `--max-length` | 512 | 128-4096 | Longer context, needs more memory |

## 📝 Example Workflow

Here's a complete example workflow from export to deployment:

```bash
# 1. Convert ChatGPT export
python convert_chatgpt_export.py \
  conversations.json \
  training_data.json \
  --min-exchanges 2 \
  --preview

# 2. Train model
python train_chatgpt_model.py \
  --data training_data.json \
  --model microsoft/DialoGPT-medium \
  --epochs 5 \
  --output ./my-chatbot

# 3. Test interactively
python demo_chatbot.py ./my-chatbot

# 4. Single query test
python demo_chatbot.py ./my-chatbot \
  --query "What is artificial intelligence?"

# 5. Deploy to Hugging Face
python train_chatgpt_model.py \
  --data training_data.json \
  --model microsoft/DialoGPT-medium \
  --push-to-hub \
  --hub-name username/my-chatbot
```

## 🔬 Evaluation

### Automatic Metrics

Training automatically tracks:
- **Perplexity**: Lower is better (< 20 is good)
- **Loss**: Should decrease over time
- **Validation Loss**: Should track training loss

### Manual Testing

```bash
# Interactive testing
python demo_chatbot.py ./my-chatbot

# Test specific queries
python demo_chatbot.py ./my-chatbot --query "Your test question"
```

## 💡 Use Cases

This toolkit is perfect for:

- 🎓 **Personal AI Assistant** - Train on your conversations
- 💼 **Domain Expert Bot** - Train on specialized conversations
- 🎮 **Character AI** - Create consistent personalities
- 📚 **Knowledge Base** - Train on Q&A conversations
- 🔬 **Research** - Experiment with fine-tuning techniques

## 🤝 Contributing

Found a bug? Have a suggestion?
- Open an issue
- Submit a pull request
- Share your results!

## 📄 License

MIT License - see LICENSE file

## 🙏 Acknowledgments

- Hugging Face for the amazing Transformers library
- OpenAI for ChatGPT
- The open-source AI community

## 🚦 Status Checklist

- [x] Install dependencies
- [x] Test with example data
- [x] Export ChatGPT conversations
- [x] Convert export format
- [x] Train on your data
- [x] Test your model
- [x] Deploy your model
- [x] Share with the world!

## 📞 Support

Need help?
1. Check the `QUICK-START-CHATGPT-TRAINING.md`
2. Read the `HUGGINGFACE-TRAINING-GUIDE.md`
3. Search [Hugging Face Forums](https://discuss.huggingface.co/)
4. Ask the AI community on Discord/Reddit

---

**Ready to train your AI? Start with:**

```bash
python train_chatgpt_model.py --data example_chatgpt_data.json
```

**Happy training! 🚀🤖**


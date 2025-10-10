#!/usr/bin/env python3
"""
ChatGPT Transcript Model Trainer
Train a custom AI model from your ChatGPT conversation transcripts using Hugging Face
"""

import os
import json
import argparse
import torch
from pathlib import Path
from datasets import Dataset, load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)

# Optional: For efficient training with LoRA
try:
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    PEFT_AVAILABLE = True
except ImportError:
    PEFT_AVAILABLE = False
    print("⚠️  PEFT not installed. Install with: pip install peft bitsandbytes")


class ChatGPTModelTrainer:
    """Train a custom model from ChatGPT transcripts"""
    
    def __init__(self, config):
        self.config = config
        self.tokenizer = None
        self.model = None
        self.dataset = None
        
    def load_transcripts(self):
        """Load ChatGPT transcripts from file"""
        print(f"📂 Loading transcripts from {self.config['data_path']}...")
        
        file_path = Path(self.config['data_path'])
        
        if not file_path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")
        
        # Load based on file type
        if file_path.suffix == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        elif file_path.suffix == '.jsonl':
            data = []
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    data.append(json.loads(line))
        else:
            raise ValueError("Unsupported file format. Use .json or .jsonl")
        
        print(f"✅ Loaded {len(data)} conversations")
        return data
    
    def format_data(self, transcripts):
        """Format transcripts for training"""
        print("🔄 Formatting conversations...")
        
        formatted_data = []
        for conversation in transcripts:
            # Support different input formats
            if isinstance(conversation, dict):
                if 'messages' in conversation:
                    formatted_data.append(conversation)
                elif 'user' in conversation and 'assistant' in conversation:
                    # Convert simple format to messages format
                    formatted_data.append({
                        "messages": [
                            {"role": "user", "content": conversation['user']},
                            {"role": "assistant", "content": conversation['assistant']}
                        ]
                    })
            elif isinstance(conversation, list):
                formatted_data.append({"messages": conversation})
        
        print(f"✅ Formatted {len(formatted_data)} conversations")
        return formatted_data
    
    def prepare_dataset(self, formatted_data):
        """Create and tokenize dataset"""
        print("🔧 Preparing dataset...")
        
        # Create dataset
        dataset = Dataset.from_list(formatted_data)
        
        # Split into train/validation
        split_dataset = dataset.train_test_split(
            test_size=self.config.get('validation_split', 0.1),
            seed=42
        )
        
        print(f"📊 Train samples: {len(split_dataset['train'])}")
        print(f"📊 Validation samples: {len(split_dataset['test'])}")
        
        # Tokenize
        def tokenize_function(examples):
            texts = []
            for messages in examples["messages"]:
                try:
                    # Apply chat template
                    text = self.tokenizer.apply_chat_template(
                        messages,
                        tokenize=False,
                        add_generation_prompt=False
                    )
                    texts.append(text)
                except Exception as e:
                    print(f"⚠️  Error formatting message: {e}")
                    texts.append("")
            
            return self.tokenizer(
                texts,
                padding="max_length",
                truncation=True,
                max_length=self.config.get('max_length', 512),
            )
        
        print("🔄 Tokenizing dataset (this may take a while)...")
        tokenized_dataset = split_dataset.map(
            tokenize_function,
            batched=True,
            remove_columns=split_dataset["train"].column_names,
            desc="Tokenizing"
        )
        
        print("✅ Dataset ready for training")
        return tokenized_dataset
    
    def load_model(self):
        """Load base model and tokenizer"""
        print(f"🤖 Loading model: {self.config['model_name']}...")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.config['model_name'],
            trust_remote_code=True
        )
        
        # Set padding token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "right"
        
        # Load model
        self.model = AutoModelForCausalLM.from_pretrained(
            self.config['model_name'],
            torch_dtype=torch.float16 if self.config.get('fp16', True) else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
            trust_remote_code=True
        )
        
        # Apply LoRA if available and requested
        if PEFT_AVAILABLE and self.config.get('use_lora', True):
            print("🔧 Applying LoRA for efficient training...")
            lora_config = LoraConfig(
                r=self.config.get('lora_r', 16),
                lora_alpha=self.config.get('lora_alpha', 32),
                target_modules=["q_proj", "v_proj"],
                lora_dropout=0.05,
                bias="none",
                task_type="CAUSAL_LM"
            )
            self.model = prepare_model_for_kbit_training(self.model)
            self.model = get_peft_model(self.model, lora_config)
            self.model.print_trainable_parameters()
        
        print("✅ Model loaded successfully")
    
    def train(self):
        """Execute training"""
        print("🚀 Starting training pipeline...")
        
        # Load and prepare data
        transcripts = self.load_transcripts()
        formatted_data = self.format_data(transcripts)
        
        # Load model
        self.load_model()
        
        # Prepare dataset
        tokenized_dataset = self.prepare_dataset(formatted_data)
        
        # Training arguments
        output_dir = self.config.get('output_dir', './fine-tuned-chatgpt-model')
        
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=self.config.get('epochs', 3),
            per_device_train_batch_size=self.config.get('batch_size', 4),
            per_device_eval_batch_size=self.config.get('batch_size', 4),
            gradient_accumulation_steps=self.config.get('gradient_accumulation_steps', 4),
            learning_rate=self.config.get('learning_rate', 2e-4),
            weight_decay=0.01,
            logging_steps=10,
            evaluation_strategy="steps",
            eval_steps=100,
            save_steps=500,
            save_total_limit=3,
            fp16=self.config.get('fp16', True) and torch.cuda.is_available(),
            warmup_steps=100,
            lr_scheduler_type="cosine",
            report_to="tensorboard" if self.config.get('use_tensorboard', True) else "none",
            push_to_hub=self.config.get('push_to_hub', False),
        )
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )
        
        # Create trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=tokenized_dataset["train"],
            eval_dataset=tokenized_dataset["test"],
            data_collator=data_collator,
        )
        
        # Train
        print("🏋️  Training started...")
        print(f"📊 Training for {self.config.get('epochs', 3)} epochs")
        print(f"💾 Model will be saved to: {output_dir}")
        
        trainer.train()
        
        # Save model
        print("💾 Saving final model...")
        trainer.save_model(output_dir)
        self.tokenizer.save_pretrained(output_dir)
        
        print(f"✅ Training complete! Model saved to {output_dir}")
        
        # Optional: Push to Hub
        if self.config.get('push_to_hub', False):
            hub_name = self.config.get('hub_model_name', 'chatgpt-finetuned')
            print(f"📤 Pushing model to Hugging Face Hub: {hub_name}")
            self.model.push_to_hub(hub_name)
            self.tokenizer.push_to_hub(hub_name)
            print("✅ Model uploaded to Hugging Face Hub")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Train a model from ChatGPT transcripts")
    
    # Data arguments
    parser.add_argument('--data', type=str, required=True,
                       help='Path to ChatGPT transcripts (JSON or JSONL)')
    parser.add_argument('--output', type=str, default='./fine-tuned-chatgpt-model',
                       help='Output directory for trained model')
    
    # Model arguments
    parser.add_argument('--model', type=str, default='microsoft/DialoGPT-medium',
                       help='Base model to fine-tune')
    parser.add_argument('--max-length', type=int, default=512,
                       help='Maximum sequence length')
    
    # Training arguments
    parser.add_argument('--epochs', type=int, default=3,
                       help='Number of training epochs')
    parser.add_argument('--batch-size', type=int, default=4,
                       help='Training batch size')
    parser.add_argument('--learning-rate', type=float, default=2e-4,
                       help='Learning rate')
    parser.add_argument('--validation-split', type=float, default=0.1,
                       help='Validation set percentage')
    
    # Advanced options
    parser.add_argument('--no-lora', action='store_true',
                       help='Disable LoRA (not recommended for large models)')
    parser.add_argument('--no-fp16', action='store_true',
                       help='Disable mixed precision training')
    parser.add_argument('--push-to-hub', action='store_true',
                       help='Push model to Hugging Face Hub after training')
    parser.add_argument('--hub-name', type=str,
                       help='Model name for Hugging Face Hub')
    
    args = parser.parse_args()
    
    # Create config
    config = {
        'data_path': args.data,
        'output_dir': args.output,
        'model_name': args.model,
        'max_length': args.max_length,
        'epochs': args.epochs,
        'batch_size': args.batch_size,
        'learning_rate': args.learning_rate,
        'validation_split': args.validation_split,
        'use_lora': not args.no_lora,
        'fp16': not args.no_fp16,
        'push_to_hub': args.push_to_hub,
        'hub_model_name': args.hub_name,
    }
    
    # Print configuration
    print("=" * 60)
    print("🤖 ChatGPT Model Trainer")
    print("=" * 60)
    print(f"📂 Data: {config['data_path']}")
    print(f"🤖 Base Model: {config['model_name']}")
    print(f"💾 Output: {config['output_dir']}")
    print(f"📊 Epochs: {config['epochs']}")
    print(f"📦 Batch Size: {config['batch_size']}")
    print(f"📏 Learning Rate: {config['learning_rate']}")
    print(f"🔧 LoRA: {'Enabled' if config['use_lora'] else 'Disabled'}")
    print(f"⚡ FP16: {'Enabled' if config['fp16'] else 'Disabled'}")
    print("=" * 60)
    
    # Check CUDA availability
    if torch.cuda.is_available():
        print(f"🎮 GPU: {torch.cuda.get_device_name(0)}")
        print(f"💾 GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    else:
        print("⚠️  No GPU detected - training will be slow!")
    print("=" * 60)
    
    # Train
    trainer = ChatGPTModelTrainer(config)
    trainer.train()


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
Demo ChatBot - Test your trained model
Simple interactive chat interface for your fine-tuned ChatGPT model
"""

import argparse
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from pathlib import Path


class ChatBot:
    """Interactive chatbot for testing trained models"""
    
    def __init__(self, model_path, max_history=10):
        print(f"🤖 Loading model from: {model_path}")
        
        self.model_path = Path(model_path)
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        # Load model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None
        )
        
        self.conversation_history = []
        self.max_history = max_history
        
        print("✅ Model loaded successfully!")
        if torch.cuda.is_available():
            print(f"🎮 Using GPU: {torch.cuda.get_device_name(0)}")
        else:
            print("💻 Using CPU (responses may be slow)")
    
    def generate_response(self, user_message, temperature=0.7, max_tokens=256):
        """Generate a response to user message"""
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Keep only recent history
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-(self.max_history * 2):]
        
        # Format conversation with chat template
        try:
            prompt = self.tokenizer.apply_chat_template(
                self.conversation_history,
                tokenize=False,
                add_generation_prompt=True
            )
        except Exception:
            # Fallback if chat template not available
            prompt = "\n".join([
                f"{msg['role']}: {msg['content']}"
                for msg in self.conversation_history
            ]) + "\nassistant:"
        
        # Tokenize
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=2048
        )
        
        if torch.cuda.is_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode
        full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract just the assistant's response
        # Try to find the last assistant response
        if "assistant" in full_response.lower():
            parts = full_response.lower().split("assistant")
            if len(parts) > 1:
                assistant_response = parts[-1].strip()
            else:
                assistant_response = full_response
        else:
            # Fallback: take text after the prompt
            assistant_response = full_response[len(prompt):].strip()
        
        # Clean up the response
        assistant_response = assistant_response.strip()
        
        # Remove any "user:" prefix if it appears
        if assistant_response.lower().startswith("user:"):
            assistant_response = assistant_response.split(":", 1)[1].strip()
        
        # Add assistant response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_response
        })
        
        return assistant_response
    
    def chat_loop(self, temperature=0.7, max_tokens=256):
        """Interactive chat loop"""
        print("\n" + "=" * 60)
        print("🤖 ChatBot Ready!")
        print("=" * 60)
        print("Commands:")
        print("  - Type your message and press Enter to chat")
        print("  - Type 'quit' or 'exit' to end the conversation")
        print("  - Type 'clear' to clear conversation history")
        print("  - Type 'history' to see conversation history")
        print("=" * 60)
        print()
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Goodbye!")
                    break
                
                elif user_input.lower() == 'clear':
                    self.conversation_history = []
                    print("🗑️  Conversation history cleared\n")
                    continue
                
                elif user_input.lower() == 'history':
                    print("\n📜 Conversation History:")
                    for i, msg in enumerate(self.conversation_history, 1):
                        role = msg['role'].capitalize()
                        content = msg['content'][:100]
                        if len(msg['content']) > 100:
                            content += "..."
                        print(f"{i}. {role}: {content}")
                    print()
                    continue
                
                # Generate response
                print("🤔 Thinking...", end="\r")
                response = self.generate_response(
                    user_input,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                print(f"Bot: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Continuing...\n")
    
    def single_query(self, message, temperature=0.7, max_tokens=256):
        """Get single response without interactive loop"""
        response = self.generate_response(message, temperature, max_tokens)
        return response


def main():
    parser = argparse.ArgumentParser(
        description="Interactive chatbot demo for your trained model"
    )
    
    parser.add_argument('model', type=str,
                       help='Path to trained model directory')
    parser.add_argument('--temperature', type=float, default=0.7,
                       help='Sampling temperature (0.0-1.0, default: 0.7)')
    parser.add_argument('--max-tokens', type=int, default=256,
                       help='Maximum tokens to generate (default: 256)')
    parser.add_argument('--max-history', type=int, default=10,
                       help='Maximum conversation turns to remember (default: 10)')
    parser.add_argument('--query', type=str,
                       help='Single query mode (no interactive chat)')
    
    args = parser.parse_args()
    
    try:
        # Create chatbot
        bot = ChatBot(args.model, max_history=args.max_history)
        
        # Single query or interactive mode
        if args.query:
            print(f"\nYou: {args.query}")
            response = bot.single_query(
                args.query,
                temperature=args.temperature,
                max_tokens=args.max_tokens
            )
            print(f"Bot: {response}\n")
        else:
            bot.chat_loop(
                temperature=args.temperature,
                max_tokens=args.max_tokens
            )
    
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you've trained a model first:")
        print("  python train_chatgpt_model.py --data your_data.json")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()


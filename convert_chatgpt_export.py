#!/usr/bin/env python3
"""
Convert ChatGPT Export to Training Format
Converts ChatGPT conversation exports to the format needed for model training
"""

import json
import argparse
from pathlib import Path
from datetime import datetime


class ChatGPTConverter:
    """Convert ChatGPT exports to training format"""
    
    def __init__(self):
        self.conversations = []
        self.stats = {
            'total_conversations': 0,
            'total_messages': 0,
            'filtered_out': 0,
            'user_messages': 0,
            'assistant_messages': 0
        }
    
    def load_chatgpt_export(self, file_path):
        """Load ChatGPT export file"""
        print(f"📂 Loading ChatGPT export from: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data
    
    def convert_conversation(self, conversation, min_exchanges=1, max_length=None):
        """
        Convert a single conversation to training format
        
        ChatGPT exports typically have structure:
        {
            "title": "...",
            "create_time": ...,
            "mapping": {
                "id": {
                    "message": {
                        "author": {"role": "user" or "assistant"},
                        "content": {"parts": ["text"]}
                    }
                }
            }
        }
        """
        messages = []
        
        # Handle different export formats
        if 'mapping' in conversation:
            # Standard ChatGPT export format
            mapping = conversation.get('mapping', {})
            
            # Extract messages in order
            for node_id, node in mapping.items():
                if 'message' in node and node['message']:
                    message = node['message']
                    author = message.get('author', {})
                    role = author.get('role', '')
                    content = message.get('content', {})
                    
                    if role in ['user', 'assistant']:
                        # Get text content
                        parts = content.get('parts', [])
                        if parts and isinstance(parts, list):
                            text = ' '.join(str(part) for part in parts if part)
                            
                            if text.strip():
                                messages.append({
                                    "role": role,
                                    "content": text.strip()
                                })
                                
                                self.stats['total_messages'] += 1
                                if role == 'user':
                                    self.stats['user_messages'] += 1
                                else:
                                    self.stats['assistant_messages'] += 1
        
        elif 'messages' in conversation:
            # Already in messages format
            messages = conversation['messages']
            self.stats['total_messages'] += len(messages)
        
        # Filter by minimum exchanges
        if len(messages) < min_exchanges * 2:  # Each exchange = user + assistant
            self.stats['filtered_out'] += 1
            return None
        
        # Filter by maximum length
        if max_length:
            total_chars = sum(len(msg['content']) for msg in messages)
            if total_chars > max_length:
                self.stats['filtered_out'] += 1
                return None
        
        return {"messages": messages}
    
    def convert_export(self, export_data, min_exchanges=1, max_length=None):
        """Convert entire ChatGPT export"""
        print("🔄 Converting conversations...")
        
        # Handle different export structures
        conversations_data = []
        
        if isinstance(export_data, list):
            conversations_data = export_data
        elif isinstance(export_data, dict):
            # Some exports have conversations in different keys
            if 'conversations' in export_data:
                conversations_data = export_data['conversations']
            elif 'items' in export_data:
                conversations_data = export_data['items']
            else:
                # Assume single conversation
                conversations_data = [export_data]
        
        self.stats['total_conversations'] = len(conversations_data)
        
        # Convert each conversation
        for conv in conversations_data:
            converted = self.convert_conversation(conv, min_exchanges, max_length)
            if converted and converted['messages']:
                self.conversations.append(converted)
        
        print(f"✅ Converted {len(self.conversations)} conversations")
        return self.conversations
    
    def save_training_data(self, output_path, format='json'):
        """Save converted data for training"""
        print(f"💾 Saving to: {output_path}")
        
        output_path = Path(output_path)
        
        if format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.conversations, f, indent=2, ensure_ascii=False)
        
        elif format == 'jsonl':
            with open(output_path, 'w', encoding='utf-8') as f:
                for conv in self.conversations:
                    f.write(json.dumps(conv, ensure_ascii=False) + '\n')
        
        print(f"✅ Saved {len(self.conversations)} conversations")
    
    def print_stats(self):
        """Print conversion statistics"""
        print("\n" + "=" * 60)
        print("📊 Conversion Statistics")
        print("=" * 60)
        print(f"Total conversations in export: {self.stats['total_conversations']}")
        print(f"Conversations converted: {len(self.conversations)}")
        print(f"Conversations filtered out: {self.stats['filtered_out']}")
        print(f"Total messages: {self.stats['total_messages']}")
        print(f"  - User messages: {self.stats['user_messages']}")
        print(f"  - Assistant messages: {self.stats['assistant_messages']}")
        
        if self.conversations:
            avg_messages = self.stats['total_messages'] / len(self.conversations)
            print(f"Average messages per conversation: {avg_messages:.1f}")
        
        print("=" * 60)
    
    def preview_sample(self, num_samples=2):
        """Preview some converted conversations"""
        print(f"\n📋 Preview of {min(num_samples, len(self.conversations))} conversations:")
        print("=" * 60)
        
        for i, conv in enumerate(self.conversations[:num_samples], 1):
            print(f"\n--- Conversation {i} ---")
            for msg in conv['messages'][:4]:  # Show first 4 messages
                role = msg['role'].upper()
                content = msg['content'][:100]  # Truncate long messages
                if len(msg['content']) > 100:
                    content += "..."
                print(f"{role}: {content}")
            
            if len(conv['messages']) > 4:
                print(f"... and {len(conv['messages']) - 4} more messages")
        
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Convert ChatGPT export to training format"
    )
    
    parser.add_argument('input', type=str,
                       help='Input ChatGPT export file (JSON)')
    parser.add_argument('output', type=str,
                       help='Output file for training data')
    parser.add_argument('--format', choices=['json', 'jsonl'], default='json',
                       help='Output format (default: json)')
    parser.add_argument('--min-exchanges', type=int, default=1,
                       help='Minimum number of exchanges (user+assistant pairs) per conversation')
    parser.add_argument('--max-length', type=int,
                       help='Maximum total character length per conversation')
    parser.add_argument('--preview', action='store_true',
                       help='Show preview of converted conversations')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🔄 ChatGPT Export Converter")
    print("=" * 60)
    
    # Create converter
    converter = ChatGPTConverter()
    
    try:
        # Load export
        export_data = converter.load_chatgpt_export(args.input)
        
        # Convert
        converter.convert_export(
            export_data,
            min_exchanges=args.min_exchanges,
            max_length=args.max_length
        )
        
        # Save
        converter.save_training_data(args.output, format=args.format)
        
        # Show stats
        converter.print_stats()
        
        # Show preview if requested
        if args.preview:
            converter.preview_sample()
        
        print(f"\n✅ Conversion complete!")
        print(f"📁 Training data saved to: {args.output}")
        print(f"\n🚀 Next step: Train your model with:")
        print(f"   python train_chatgpt_model.py --data {args.output}")
        
    except FileNotFoundError:
        print(f"❌ Error: Input file not found: {args.input}")
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON in input file")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()


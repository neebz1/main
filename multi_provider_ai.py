#!/usr/bin/env python3
"""
Multi-Provider AI Integration with Monitoring
Provides automatic fallback between providers with health monitoring
"""

import os
from typing import Optional, Tuple, Any
from devops_monitor import DevOpsMonitor


class MultiProviderAI:
    """
    AI client with automatic provider fallback and monitoring integration
    """
    
    def __init__(self):
        """Initialize multi-provider AI with monitoring"""
        self.monitor = DevOpsMonitor()
        self.client = None
        self.provider = None
        self._initialize_provider()
    
    def _initialize_provider(self):
        """Initialize AI provider with fallback"""
        available_providers = self.monitor.get_provider_fallback_order()
        
        if not available_providers:
            print("⚠️  No API keys configured")
            return
        
        # Try providers in order of availability
        if "Together AI (Kimi K2)" in available_providers:
            if self._init_together():
                return
        
        if "Anthropic (Claude)" in available_providers:
            if self._init_anthropic():
                return
        
        if "OpenAI (GPT-4)" in available_providers:
            if self._init_openai():
                return
        
        if "Google Gemini" in available_providers:
            if self._init_google():
                return
        
        print("⚠️  Could not initialize any AI provider")
    
    def _init_together(self) -> bool:
        """Initialize Together AI"""
        try:
            from together import Together
            api_key = os.getenv('TOGETHER_API_KEY')
            if api_key:
                self.client = Together(api_key=api_key)
                self.provider = "together"
                print("✅ Using Together AI (Kimi K2)")
                return True
        except Exception as e:
            print(f"⚠️  Could not initialize Together AI: {e}")
        return False
    
    def _init_anthropic(self) -> bool:
        """Initialize Anthropic"""
        try:
            import anthropic
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if api_key:
                self.client = anthropic.Anthropic(api_key=api_key)
                self.provider = "anthropic"
                print("✅ Using Anthropic (Claude)")
                return True
        except Exception as e:
            print(f"⚠️  Could not initialize Anthropic: {e}")
        return False
    
    def _init_openai(self) -> bool:
        """Initialize OpenAI"""
        try:
            from openai import OpenAI
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                self.client = OpenAI(api_key=api_key)
                self.provider = "openai"
                print("✅ Using OpenAI (GPT-4)")
                return True
        except Exception as e:
            print(f"⚠️  Could not initialize OpenAI: {e}")
        return False
    
    def _init_google(self) -> bool:
        """Initialize Google Gemini"""
        try:
            import google.generativeai as genai
            api_key = os.getenv('GOOGLE_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
                self.client = genai.GenerativeModel('gemini-pro')
                self.provider = "google"
                print("✅ Using Google Gemini")
                return True
        except Exception as e:
            print(f"⚠️  Could not initialize Google: {e}")
        return False
    
    def chat(self, message: str, system_prompt: Optional[str] = None, 
             max_tokens: int = 1024) -> Tuple[Optional[str], Optional[str]]:
        """
        Send a chat message with automatic provider fallback
        
        Returns:
            Tuple of (response, error_message)
        """
        if not self.client:
            return None, "No AI provider available"
        
        try:
            if self.provider == "together":
                return self._chat_together(message, system_prompt, max_tokens)
            elif self.provider == "anthropic":
                return self._chat_anthropic(message, system_prompt, max_tokens)
            elif self.provider == "openai":
                return self._chat_openai(message, system_prompt, max_tokens)
            elif self.provider == "google":
                return self._chat_google(message, system_prompt, max_tokens)
        except Exception as e:
            return None, f"Error: {str(e)}"
        
        return None, "Unknown provider"
    
    def _chat_together(self, message: str, system_prompt: Optional[str], 
                      max_tokens: int) -> Tuple[Optional[str], Optional[str]]:
        """Chat with Together AI"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})
        
        response = self.client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.choices[0].message.content, None
    
    def _chat_anthropic(self, message: str, system_prompt: Optional[str], 
                       max_tokens: int) -> Tuple[Optional[str], Optional[str]]:
        """Chat with Anthropic"""
        kwargs = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": message}]
        }
        if system_prompt:
            kwargs["system"] = system_prompt
        
        response = self.client.messages.create(**kwargs)
        return response.content[0].text, None
    
    def _chat_openai(self, message: str, system_prompt: Optional[str], 
                    max_tokens: int) -> Tuple[Optional[str], Optional[str]]:
        """Chat with OpenAI"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content, None
    
    def _chat_google(self, message: str, system_prompt: Optional[str], 
                    max_tokens: int) -> Tuple[Optional[str], Optional[str]]:
        """Chat with Google Gemini"""
        full_prompt = message
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{message}"
        
        response = self.client.generate_content(full_prompt)
        return response.text, None
    
    def health_check(self) -> dict:
        """
        Perform health check and return status
        
        Returns:
            Dictionary with health status
        """
        report = self.monitor.perform_health_check()
        return {
            'provider': self.provider,
            'client_initialized': self.client is not None,
            'system_health': report.system_health,
            'issues': report.issues_found,
            'recommendations': report.recommendations
        }
    
    def get_status(self) -> dict:
        """Get current provider status"""
        return {
            'provider': self.provider,
            'initialized': self.client is not None,
            'available_providers': self.monitor.get_provider_fallback_order()
        }


def example_usage():
    """Example usage of MultiProviderAI"""
    print("🤖 Multi-Provider AI Integration Example")
    print("=" * 60)
    
    # Initialize AI
    ai = MultiProviderAI()
    
    # Check status
    status = ai.get_status()
    print(f"\n📊 Current Provider: {status['provider']}")
    print(f"Available Providers: {', '.join(status['available_providers']) or 'None'}")
    
    # Try a chat
    if ai.client:
        print("\n💬 Testing chat...")
        response, error = ai.chat(
            "Say hello in one sentence!",
            system_prompt="You are a helpful assistant."
        )
        
        if response:
            print(f"✅ Response: {response}")
        else:
            print(f"❌ Error: {error}")
    else:
        print("\n⚠️  No AI provider available. Please configure API keys.")
    
    # Health check
    print("\n🏥 Running health check...")
    health = ai.health_check()
    print(f"System Status: {health['system_health']['status']}")
    
    if health['issues']:
        print("\n⚠️  Issues:")
        for issue in health['issues']:
            print(f"  • {issue}")


if __name__ == "__main__":
    example_usage()

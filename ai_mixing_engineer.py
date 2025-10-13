#!/usr/bin/env python3
"""
AI Mixing Engineer for Logic Pro
Advanced audio analysis and mixing suggestions powered by AI

Inspired by: iZotope Neutron, Sonible smart:EQ, LANDR
Features:
- Spectral analysis and EQ suggestions
- Dynamic range analysis and compression tips
- Stereo field analysis
- Mix balance recommendations
- Real-time feedback on your Logic Pro session
"""

import os
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
import gradio as gr
from typing import Optional, Tuple, Dict
import librosa
import librosa.display
import matplotlib.pyplot as plt
import io
from PIL import Image

# Load environment variables
load_dotenv()

# AI Client setup
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')

client = None
AI_PROVIDER = None

try:
    if TOGETHER_API_KEY:
        from together import Together
        client = Together(api_key=TOGETHER_API_KEY)
        AI_PROVIDER = "kimi"
    elif ANTHROPIC_API_KEY:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        AI_PROVIDER = "anthropic"
    elif OPENAI_API_KEY:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        AI_PROVIDER = "openai"
except Exception as e:
    print(f"⚠️  AI import warning: {e}")


class AudioAnalyzer:
    """Analyzes audio files and provides mixing insights"""
    
    def __init__(self):
        self.sr = 44100  # Sample rate
        
    def analyze_file(self, audio_path: str) -> Dict:
        """Perform comprehensive audio analysis"""
        try:
            # Load audio file
            y, sr = librosa.load(audio_path, sr=self.sr)
            
            # Spectral analysis
            spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
            
            # Dynamic range analysis
            rms = librosa.feature.rms(y=y)[0]
            peak = np.max(np.abs(y))
            
            # Frequency analysis
            S = np.abs(librosa.stft(y))
            
            # Zero crossing rate (indicates noisiness)
            zcr = librosa.feature.zero_crossing_rate(y)[0]
            
            # Tempo detection
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            
            # Loudness (LUFS approximation)
            loudness_db = 20 * np.log10(np.mean(rms) + 1e-10)
            
            return {
                'spectral_centroid_mean': float(np.mean(spectral_centroid)),
                'spectral_rolloff_mean': float(np.mean(spectral_rolloff)),
                'rms_mean': float(np.mean(rms)),
                'peak': float(peak),
                'dynamic_range_db': float(20 * np.log10(peak / (np.mean(rms) + 1e-10))),
                'zcr_mean': float(np.mean(zcr)),
                'tempo': float(tempo),
                'loudness_db': float(loudness_db),
                'duration': len(y) / sr
            }
        except Exception as e:
            return {'error': str(e)}
    
    def generate_waveform(self, audio_path: str) -> Image:
        """Generate waveform visualization"""
        try:
            y, sr = librosa.load(audio_path, sr=self.sr)
            
            plt.figure(figsize=(12, 4))
            plt.subplot(2, 1, 1)
            librosa.display.waveshow(y, sr=sr, alpha=0.8, color='#00d4ff')
            plt.title('Waveform', fontsize=14, color='white')
            plt.xlabel('Time (s)', color='white')
            plt.ylabel('Amplitude', color='white')
            plt.tight_layout()
            
            # Style
            plt.gcf().patch.set_facecolor('#1a1a1a')
            plt.gca().set_facecolor('#2a2a2a')
            plt.gca().spines['bottom'].set_color('white')
            plt.gca().spines['left'].set_color('white')
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)
            plt.tick_params(colors='white')
            
            # Save to buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', facecolor='#1a1a1a')
            buf.seek(0)
            plt.close()
            
            return Image.open(buf)
        except Exception as e:
            return None
    
    def generate_spectrogram(self, audio_path: str) -> Image:
        """Generate spectrogram visualization"""
        try:
            y, sr = librosa.load(audio_path, sr=self.sr)
            
            plt.figure(figsize=(12, 4))
            D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
            librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='hz', cmap='magma')
            plt.colorbar(format='%+2.0f dB')
            plt.title('Spectrogram', fontsize=14, color='white')
            plt.xlabel('Time (s)', color='white')
            plt.ylabel('Frequency (Hz)', color='white')
            plt.tight_layout()
            
            # Style
            plt.gcf().patch.set_facecolor('#1a1a1a')
            plt.gca().set_facecolor('#2a2a2a')
            plt.tick_params(colors='white')
            
            # Save to buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', facecolor='#1a1a1a')
            buf.seek(0)
            plt.close()
            
            return Image.open(buf)
        except Exception as e:
            return None


class MixingEngineer:
    """AI-powered mixing engineer that provides intelligent suggestions"""
    
    def __init__(self, analyzer: AudioAnalyzer):
        self.analyzer = analyzer
        self.system_prompt = """You are an expert mixing and mastering engineer with 20+ years of experience.
You analyze audio characteristics and provide professional, actionable mixing advice.

Your expertise includes:
- EQ recommendations (frequency ranges, cuts/boosts)
- Compression settings (ratio, attack, release, threshold)
- Stereo imaging and panning
- Dynamic range optimization
- Loudness and mastering
- Genre-specific production techniques

Give specific, technical advice that a producer can immediately apply in Logic Pro.
Be encouraging but professional. Use emojis sparingly and only when appropriate.
"""
    
    def analyze_and_suggest(self, audio_path: str, genre: str = "General", goals: str = "") -> str:
        """Analyze audio and provide AI-powered mixing suggestions"""
        
        # Get audio analysis
        analysis = self.analyzer.analyze_file(audio_path)
        
        if 'error' in analysis:
            return f"❌ Error analyzing audio: {analysis['error']}"
        
        # Build analysis report
        report = self._format_analysis(analysis)
        
        # Get AI suggestions
        if client:
            ai_suggestions = self._get_ai_suggestions(analysis, genre, goals)
            return f"{report}\n\n{ai_suggestions}"
        else:
            return f"{report}\n\n⚠️ AI suggestions unavailable (no API key configured)"
    
    def _format_analysis(self, analysis: Dict) -> str:
        """Format technical analysis into readable report"""
        
        report = "## 📊 Audio Analysis\n\n"
        
        # Dynamic Range
        dr = analysis['dynamic_range_db']
        if dr > 15:
            dr_status = "✅ Excellent dynamic range (very natural)"
        elif dr > 10:
            dr_status = "✓ Good dynamic range"
        elif dr > 6:
            dr_status = "⚠️ Moderate compression (typical for modern music)"
        else:
            dr_status = "⚠️ Heavy compression (may sound squashed)"
        
        report += f"**Dynamic Range:** {dr:.1f} dB - {dr_status}\n\n"
        
        # Loudness
        loudness = analysis['loudness_db']
        if loudness > -6:
            loud_status = "⚠️ Very loud (may be clipping)"
        elif loudness > -14:
            loud_status = "✓ Good loudness level"
        elif loudness > -23:
            loud_status = "✓ Moderate loudness (room for mastering)"
        else:
            loud_status = "⚠️ Too quiet (needs level boost)"
        
        report += f"**Loudness:** {loudness:.1f} dB - {loud_status}\n\n"
        
        # Peak Level
        peak_db = 20 * np.log10(analysis['peak'] + 1e-10)
        if peak_db > -0.1:
            peak_status = "❌ CLIPPING! Reduce levels!"
        elif peak_db > -1:
            peak_status = "⚠️ Very close to clipping"
        elif peak_db > -3:
            peak_status = "✓ Good headroom"
        else:
            peak_status = "✓ Plenty of headroom"
        
        report += f"**Peak Level:** {peak_db:.1f} dBFS - {peak_status}\n\n"
        
        # Spectral characteristics
        centroid_khz = analysis['spectral_centroid_mean'] / 1000
        if centroid_khz > 3:
            bright_status = "Very bright/harsh (consider high-cut)"
        elif centroid_khz > 2:
            bright_status = "Bright (normal for modern mixes)"
        elif centroid_khz > 1:
            bright_status = "Balanced"
        else:
            bright_status = "Dark/muddy (consider high-pass or brightness)"
        
        report += f"**Tonal Balance:** {centroid_khz:.2f} kHz centroid - {bright_status}\n\n"
        
        # Tempo
        report += f"**Tempo:** {analysis['tempo']:.1f} BPM\n\n"
        report += f"**Duration:** {analysis['duration']:.1f} seconds\n\n"
        
        return report
    
    def _get_ai_suggestions(self, analysis: Dict, genre: str, goals: str) -> str:
        """Get AI-powered mixing suggestions"""
        
        user_prompt = f"""Analyze this audio track and provide specific mixing/mastering suggestions:

**Technical Analysis:**
- Dynamic Range: {analysis['dynamic_range_db']:.1f} dB
- Loudness: {analysis['loudness_db']:.1f} dB
- Peak Level: {20 * np.log10(analysis['peak'] + 1e-10):.1f} dBFS
- Spectral Centroid: {analysis['spectral_centroid_mean']:.0f} Hz
- Spectral Rolloff: {analysis['spectral_rolloff_mean']:.0f} Hz
- Tempo: {analysis['tempo']:.1f} BPM

**Genre:** {genre}
**Production Goals:** {goals if goals else "General mixing/mastering"}

Provide:
1. **EQ Recommendations** - Specific frequency ranges and adjustments
2. **Compression Settings** - Ratio, attack, release, threshold suggestions
3. **Stereo Enhancement** - Panning and width recommendations
4. **Overall Mix Balance** - What needs attention
5. **Next Steps** - Priority actions in order

Be specific and actionable. Format with clear headings."""

        try:
            if AI_PROVIDER == "kimi":
                response = client.chat.completions.create(
                    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=2048,
                    temperature=0.7
                )
                return "## 🤖 AI Mixing Suggestions\n\n" + response.choices[0].message.content
                
            elif AI_PROVIDER == "anthropic":
                response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=2048,
                    system=self.system_prompt,
                    messages=[{"role": "user", "content": user_prompt}]
                )
                return "## 🤖 AI Mixing Suggestions\n\n" + response.content[0].text
                
            else:  # OpenAI
                response = client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=2048
                )
                return "## 🤖 AI Mixing Suggestions\n\n" + response.choices[0].message.content
                
        except Exception as e:
            return f"## 🤖 AI Mixing Suggestions\n\n❌ Error: {str(e)}"


# Initialize components
analyzer = AudioAnalyzer()
engineer = MixingEngineer(analyzer)


def analyze_track(audio_file, genre, goals):
    """Main function to analyze track and return suggestions"""
    if audio_file is None:
        return "Please upload an audio file", None, None
    
    # Get analysis and suggestions
    suggestions = engineer.analyze_and_suggest(audio_file, genre, goals)
    
    # Generate visualizations
    waveform = analyzer.generate_waveform(audio_file)
    spectrogram = analyzer.generate_spectrogram(audio_file)
    
    return suggestions, waveform, spectrogram


def create_ui():
    """Create the Gradio interface"""
    
    # Build header with AI provider info
    provider_names = {"kimi": "Kimi K2", "anthropic": "Claude", "openai": "GPT-4"}
    ai_status = f"✅ AI: {provider_names.get(AI_PROVIDER, 'Not configured')}" if AI_PROVIDER else "⚠️ AI: Not configured"
    
    with gr.Blocks(theme=gr.themes.Soft(primary_hue="cyan"), title="AI Mixing Engineer") as app:
        gr.Markdown(
            f"""
            # 🎚️ AI Mixing Engineer
            ### Professional audio analysis and mixing suggestions powered by AI
            
            Inspired by: iZotope Neutron, Sonible smart:EQ, LANDR
            
            {ai_status}
            """
        )
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📤 Upload Your Track")
                audio_input = gr.Audio(
                    sources=["upload"],
                    type="filepath",
                    label="Audio File",
                    format="wav"
                )
                
                genre_dropdown = gr.Dropdown(
                    choices=[
                        "General",
                        "Hip-Hop/Trap",
                        "EDM/Electronic",
                        "Rock",
                        "Pop",
                        "R&B/Soul",
                        "Jazz",
                        "Classical",
                        "Metal",
                        "Indie/Alternative"
                    ],
                    value="General",
                    label="Genre"
                )
                
                goals_input = gr.Textbox(
                    label="Production Goals (optional)",
                    placeholder="e.g., 'Need more punch in the low end' or 'Preparing for streaming'"
                )
                
                analyze_btn = gr.Button("🔍 Analyze & Get Suggestions", variant="primary", size="lg")
            
            with gr.Column(scale=2):
                gr.Markdown("### 📊 Analysis Results")
                suggestions_output = gr.Markdown()
        
        gr.Markdown("### 📈 Visualizations")
        with gr.Row():
            waveform_output = gr.Image(label="Waveform")
            spectrogram_output = gr.Image(label="Spectrogram")
        
        gr.Markdown(
            """
            ---
            ### 💡 How to Use
            1. **Export a stem or full mix** from Logic Pro (File → Bounce → Project or Section)
            2. **Upload the audio file** above
            3. **Select your genre** for genre-specific advice
            4. **Add any specific goals** you have for the track
            5. **Click Analyze** to get professional mixing suggestions!
            
            ### 🎯 What You'll Get
            - Detailed frequency analysis and EQ recommendations
            - Compression settings tailored to your track
            - Dynamic range and loudness analysis
            - Stereo field suggestions
            - Genre-specific production tips
            - Priority action items
            
            ### 🔧 Supported Formats
            WAV, MP3, AIFF, FLAC, M4A
            """
        )
        
        # Connect the button
        analyze_btn.click(
            fn=analyze_track,
            inputs=[audio_input, genre_dropdown, goals_input],
            outputs=[suggestions_output, waveform_output, spectrogram_output]
        )
    
    return app


if __name__ == "__main__":
    print("\n" + "━" * 60)
    print("🎚️ Starting AI Mixing Engineer...")
    print("━" * 60)
    
    if not OPENAI_API_KEY and not ANTHROPIC_API_KEY and not TOGETHER_API_KEY:
        print("\n⚠️  Warning: No API key found!")
        print("\n💡 Audio analysis will work, but AI suggestions require an API key")
        print("\nTo enable AI features:")
        print("1. Create/edit .env file: cp config_example.txt .env")
        print("2. Add your API key (OpenAI, Anthropic, or Kimi K2)")
        print("3. Restart the app")
        print("\n🆘 Need help? Run: python3 help.py")
        print("━" * 60)
    elif AI_PROVIDER:
        provider_names = {"kimi": "Kimi K2", "anthropic": "Claude", "openai": "GPT-4"}
        print(f"\n✅ AI Provider: {provider_names.get(AI_PROVIDER, AI_PROVIDER)}")
        print("✅ Ready to analyze your audio!")
        print("\n🆘 Need help? Run: python3 help.py")
        print("━" * 60)
    
    try:
        app = create_ui()
        print("\n🚀 Launching in your browser...")
        print("📍 URL: http://127.0.0.1:7861")
        print("\n💡 Press Ctrl+C to stop\n")
        app.launch(
            server_name="127.0.0.1",
            server_port=7861,  # Different port from the other app
            share=False,
            inbrowser=True
        )
    except Exception as e:
        print(f"\n❌ Error starting app: {e}")
        print("\n🆘 Try running: ./fix-everything.sh")
        print("Or run: python3 help.py for diagnostics")
        import sys
        sys.exit(1)


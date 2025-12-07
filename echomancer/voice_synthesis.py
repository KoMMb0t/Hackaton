"""
EchoMancer - Voice Synthesis
Text-to-Speech für Battle-Commentary
"""

import os
import subprocess
from typing import Optional
from pathlib import Path


class VoiceSynthesizer:
    """
    Text-to-Speech System
    Nutzt ElevenLabs wenn API-Key vorhanden, sonst System-TTS
    """
    
    def __init__(self):
        self.has_elevenlabs = bool(os.getenv("ELEVENLABS_API_KEY"))
        self.output_dir = Path("echomancer/audio_output")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def synthesize(self, text: str, output_file: str, voice: str = 'dramatic') -> Optional[str]:
        """
        Synthetisiert Text zu Audio
        
        Args:
            text: Text zum Sprechen
            output_file: Ausgabe-Dateiname
            voice: Voice-Stil ('dramatic', 'epic', 'calm', 'hype')
        
        Returns:
            Pfad zur Audio-Datei oder None
        """
        
        output_path = self.output_dir / output_file
        
        if self.has_elevenlabs:
            return self._synthesize_elevenlabs(text, output_path, voice)
        else:
            return self._synthesize_system(text, output_path)
    
    def _synthesize_elevenlabs(self, text: str, output_path: Path, voice: str) -> Optional[str]:
        """Synthesize mit ElevenLabs API"""
        try:
            import requests
            
            api_key = os.getenv("ELEVENLABS_API_KEY")
            
            # Voice IDs (Beispiele - müssen angepasst werden)
            voice_ids = {
                'dramatic': 'EXAVITQu4vr4xnSDxMaL',  # Sarah
                'epic': '21m00Tcm4TlvDq8ikWAM',      # Rachel
                'calm': 'AZnzlk1XvdvUeBnXmlld',      # Domi
                'hype': 'ErXwobaYiN019PkySvjV'       # Antoni
            }
            
            voice_id = voice_ids.get(voice, voice_ids['dramatic'])
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"🎤 Voice synthesized: {output_path}")
                return str(output_path)
            else:
                print(f"⚠️  ElevenLabs API Error: {response.status_code}")
                return self._synthesize_system(text, output_path)
        
        except Exception as e:
            print(f"⚠️  ElevenLabs synthesis failed: {e}")
            return self._synthesize_system(text, output_path)
    
    def _synthesize_system(self, text: str, output_path: Path) -> Optional[str]:
        """Fallback: System TTS (macOS say, Linux espeak, etc.)"""
        try:
            # macOS
            if os.system("which say > /dev/null 2>&1") == 0:
                # Konvertiere zu AIFF, dann zu MP3 (wenn ffmpeg verfügbar)
                aiff_path = output_path.with_suffix('.aiff')
                subprocess.run(['say', '-o', str(aiff_path), text], check=True)
                
                # Versuche Konvertierung zu MP3
                if os.system("which ffmpeg > /dev/null 2>&1") == 0:
                    subprocess.run([
                        'ffmpeg', '-i', str(aiff_path),
                        '-acodec', 'libmp3lame', '-y',
                        str(output_path.with_suffix('.mp3'))
                    ], check=True, capture_output=True)
                    aiff_path.unlink()  # Lösche AIFF
                    print(f"🎤 Voice synthesized (macOS): {output_path.with_suffix('.mp3')}")
                    return str(output_path.with_suffix('.mp3'))
                else:
                    print(f"🎤 Voice synthesized (macOS): {aiff_path}")
                    return str(aiff_path)
            
            # Linux espeak
            elif os.system("which espeak > /dev/null 2>&1") == 0:
                wav_path = output_path.with_suffix('.wav')
                subprocess.run(['espeak', '-w', str(wav_path), text], check=True)
                print(f"🎤 Voice synthesized (Linux): {wav_path}")
                return str(wav_path)
            
            # Keine TTS verfügbar
            else:
                print("⚠️  No TTS system available (say, espeak, or ElevenLabs)")
                print("💡 Install ElevenLabs API key or system TTS")
                return None
        
        except Exception as e:
            print(f"⚠️  System TTS failed: {e}")
            return None
    
    def play_audio(self, audio_file: str):
        """Spielt Audio-Datei ab"""
        try:
            # macOS
            if os.system("which afplay > /dev/null 2>&1") == 0:
                subprocess.run(['afplay', audio_file])
            
            # Linux
            elif os.system("which aplay > /dev/null 2>&1") == 0:
                subprocess.run(['aplay', audio_file])
            
            # VLC (cross-platform)
            elif os.system("which vlc > /dev/null 2>&1") == 0:
                subprocess.run(['vlc', '--play-and-exit', audio_file])
            
            else:
                print(f"⚠️  No audio player available. File saved: {audio_file}")
        
        except Exception as e:
            print(f"⚠️  Audio playback failed: {e}")
    
    def synthesize_and_play(self, text: str, filename: str, voice: str = 'dramatic'):
        """Synthetisiert und spielt direkt ab"""
        audio_file = self.synthesize(text, filename, voice)
        
        if audio_file:
            self.play_audio(audio_file)
        else:
            print("⚠️  Could not synthesize audio")
    
    def get_available_voices(self) -> list:
        """Gibt verfügbare Voices zurück"""
        if self.has_elevenlabs:
            return ['dramatic', 'epic', 'calm', 'hype']
        else:
            return ['system_default']

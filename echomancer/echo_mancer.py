"""
EchoMancer - Main Module
Kombiniert Poetry + Voice für Battle-Remixing
"""

from typing import Dict, Optional
from pathlib import Path
from .battle_poetry import BattlePoet
from .voice_synthesis import VoiceSynthesizer


class EchoMancer:
    """
    Der Schamanen-Agent der Meetings/Battles remixt
    Kombiniert Poetry-Generation mit Voice-Synthesis
    """
    
    def __init__(self):
        self.poet = BattlePoet()
        self.synthesizer = VoiceSynthesizer()
        self.remixes: list = []
    
    def remix_battle(
        self,
        battle_data: Dict,
        style: str = 'epic',
        voice: str = 'dramatic',
        synthesize_audio: bool = True,
        play_audio: bool = False
    ) -> Dict:
        """
        Remixt einen Kampf zu Poesie + Audio
        
        Args:
            battle_data: Kampf-Daten
            style: Poetry-Stil ('haiku', 'epic', 'therapy', 'rap', 'commentary')
            voice: Voice-Stil ('dramatic', 'epic', 'calm', 'hype')
            synthesize_audio: Audio generieren?
            play_audio: Audio direkt abspielen?
        
        Returns:
            Dict mit Remix-Daten
        """
        
        # Generiere Gedicht
        poem = self.poet.generate_poem(battle_data, style)
        
        # Synthesize Audio
        audio_file = None
        if synthesize_audio:
            filename = f"battle_{battle_data.get('agent1', 'unknown')}_vs_{battle_data.get('agent2', 'unknown')}_{style}.mp3"
            filename = filename.replace(' ', '_').replace('/', '_')
            
            audio_file = self.synthesizer.synthesize(
                poem['poem'],
                filename,
                voice
            )
            
            if play_audio and audio_file:
                self.synthesizer.play_audio(audio_file)
        
        # Erstelle Remix
        remix = {
            'poem': poem,
            'audio_file': audio_file,
            'style': style,
            'voice': voice
        }
        
        self.remixes.append(remix)
        
        return remix
    
    def live_commentary(
        self,
        event: str,
        context: Dict,
        voice: str = 'hype'
    ) -> Optional[str]:
        """
        Live-Kommentar für ein Kampf-Event
        
        Args:
            event: Event-Beschreibung
            context: Kontext-Informationen
            voice: Voice-Stil
        
        Returns:
            Pfad zur Audio-Datei
        """
        
        # Generiere kurzen Kommentar
        commentary = self._generate_live_commentary(event, context)
        
        # Synthesize
        filename = f"live_commentary_{len(self.remixes)}.mp3"
        audio_file = self.synthesizer.synthesize(commentary, filename, voice)
        
        return audio_file
    
    def _generate_live_commentary(self, event: str, context: Dict) -> str:
        """Generiert Live-Kommentar"""
        import os
        
        if os.getenv("OPENAI_API_KEY"):
            try:
                from openai import OpenAI
                client = OpenAI()
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "Du bist ein überdrehter Sport-Kommentator. "
                                     "Kommentiere Kampf-Events kurz, dramatisch und absurd. "
                                     "Max 2 Sätze!"
                        },
                        {
                            "role": "user",
                            "content": f"Event: {event}\nKontext: {context}"
                        }
                    ],
                    temperature=0.9,
                    max_tokens=50
                )
                
                return response.choices[0].message.content.strip()
            
            except Exception as e:
                print(f"⚠️  AI commentary failed: {e}")
        
        # Fallback
        commentaries = [
            f"OH MY! {event}! This is INCREDIBLE!",
            f"UNBELIEVABLE! {event}! What a MOVE!",
            f"SPECTACULAR! {event}! The crowd goes WILD!",
            f"AMAZING! {event}! History in the making!",
            f"WOW! {event}! This is INSANE!"
        ]
        
        import random
        return random.choice(commentaries)
    
    def create_battle_summary(
        self,
        battle_data: Dict,
        include_audio: bool = True
    ) -> Dict:
        """
        Erstellt vollständige Battle-Zusammenfassung
        Mit mehreren Stilen
        
        Returns:
            Dict mit allen Remixes
        """
        
        styles = ['haiku', 'epic', 'commentary']
        summaries = []
        
        for style in styles:
            remix = self.remix_battle(
                battle_data,
                style=style,
                synthesize_audio=include_audio,
                play_audio=False
            )
            summaries.append(remix)
        
        return {
            'battle_data': battle_data,
            'summaries': summaries
        }
    
    def export_remix(self, remix: Dict, output_dir: str):
        """Exportiert Remix (Text + Audio)"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Export Poem
        poem_file = output_path / f"poem_{remix['style']}.txt"
        self.poet.export_poem(remix['poem'], str(poem_file))
        
        # Audio ist bereits gespeichert
        if remix['audio_file']:
            print(f"🎵 Audio: {remix['audio_file']}")
    
    def print_remix(self, remix: Dict):
        """Gibt Remix formatiert aus"""
        print("\n" + "="*60)
        print("🎭 ECHOMANCER REMIX")
        print("="*60)
        print(f"\nStyle: {remix['style']}")
        print(f"Voice: {remix['voice']}")
        print()
        print(remix['poem']['poem'])
        
        if remix['audio_file']:
            print(f"\n🎵 Audio: {remix['audio_file']}")
        
        print("="*60 + "\n")
    
    def get_all_remixes(self) -> list:
        """Gibt alle Remixes zurück"""
        return self.remixes

"""
EchoMancer - Battle Poetry Generator
Generiert poetische Zusammenfassungen von Kämpfen
"""

import os
import random
from typing import Dict, List, Optional
from datetime import datetime


class BattlePoet:
    """
    Generiert poetische Kampf-Zusammenfassungen
    Verschiedene Stile: Haiku, Epic, Therapy, Rap
    """
    
    def __init__(self):
        self.poems: List[Dict] = []
    
    def generate_poem(self, battle_data: Dict, style: str = 'epic') -> Dict:
        """
        Generiert Gedicht aus Battle-Daten
        
        Args:
            battle_data: Dict mit Kampf-Informationen
            style: 'haiku', 'epic', 'therapy', 'rap', 'commentary'
        
        Returns:
            Dict mit Gedicht und Metadaten
        """
        
        # Mit OpenAI wenn verfügbar
        if os.getenv("OPENAI_API_KEY"):
            poem_text = self._generate_ai_poem(battle_data, style)
        else:
            poem_text = self._generate_fallback_poem(battle_data, style)
        
        poem = {
            'timestamp': datetime.now().isoformat(),
            'style': style,
            'battle_data': battle_data,
            'poem': poem_text,
            'title': self._generate_title(battle_data, style)
        }
        
        self.poems.append(poem)
        
        return poem
    
    def _generate_ai_poem(self, battle_data: Dict, style: str) -> str:
        """Generiert Gedicht mit GPT"""
        try:
            from openai import OpenAI
            client = OpenAI()
            
            prompt = self._create_poetry_prompt(battle_data, style)
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(style)
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.9,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"⚠️  AI-Poetry fehlgeschlagen: {e}")
            return self._generate_fallback_poem(battle_data, style)
    
    def _get_system_prompt(self, style: str) -> str:
        """System-Prompt für verschiedene Stile"""
        prompts = {
            'haiku': "Du bist ein Haiku-Meister. Schreibe präzise 5-7-5 Silben Haikus über absurde KI-Kämpfe.",
            'epic': "Du bist ein epischer Barde. Schreibe dramatische, übertriebene Kampf-Epen im Fantasy-Stil.",
            'therapy': "Du bist ein überdramatischer Therapeut. Analysiere Kämpfe als emotionale Reisen.",
            'rap': "Du bist ein Battle-Rapper. Schreibe aggressive, witzige Rap-Verse über KI-Kämpfe.",
            'commentary': "Du bist ein überdrehter Sport-Kommentator. Kommentiere Kämpfe dramatisch und absurd."
        }
        
        return prompts.get(style, "Du bist ein Poet. Schreibe über KI-Kämpfe.")
    
    def _create_poetry_prompt(self, battle_data: Dict, style: str) -> str:
        """Erstellt Prompt für Poetry-Generation"""
        agent1 = battle_data.get('agent1', 'Agent 1')
        agent2 = battle_data.get('agent2', 'Agent 2')
        winner = battle_data.get('winner', 'Unknown')
        rounds = battle_data.get('rounds', 0)
        key_moments = battle_data.get('key_moments', [])
        
        prompt = f"""
Kampf zwischen {agent1} und {agent2}.
Sieger: {winner} nach {rounds} Runden.
"""
        
        if key_moments:
            prompt += "\nSchlüsselmomente:\n"
            for moment in key_moments[:3]:  # Max 3
                prompt += f"- {moment}\n"
        
        if style == 'haiku':
            prompt += "\nSchreibe ein 5-7-5 Haiku über diesen Kampf."
        elif style == 'epic':
            prompt += "\nSchreibe ein kurzes episches Gedicht (6-8 Zeilen)."
        elif style == 'therapy':
            prompt += "\nAnalysiere diesen Kampf als emotionale Reise (4-6 Zeilen)."
        elif style == 'rap':
            prompt += "\nSchreibe 8 Rap-Zeilen über diesen Kampf."
        elif style == 'commentary':
            prompt += "\nKommentiere diesen Kampf wie ein überdrehter Sportkommentator (4-6 Zeilen)."
        
        return prompt
    
    def _generate_fallback_poem(self, battle_data: Dict, style: str) -> str:
        """Fallback-Gedichte ohne AI"""
        agent1 = battle_data.get('agent1', 'Agent 1')
        agent2 = battle_data.get('agent2', 'Agent 2')
        winner = battle_data.get('winner', 'Unknown')
        rounds = battle_data.get('rounds', 0)
        
        if style == 'haiku':
            haikus = [
                f"Zwei Agenten kämpfen\n{agent1} gegen {agent2}\n{winner} triumphiert",
                f"Bits und Bytes im Kampf\n{rounds} Runden voller Chaos\n{winner} steht noch",
                f"KI gegen KI\nAlgorithmen im Duell\n{winner} gewinnt"
            ]
            return random.choice(haikus)
        
        elif style == 'epic':
            epics = [
                f"In den digitalen Arenen der Ewigkeit,\n"
                f"Wo {agent1} und {agent2} sich gegenüberstehen,\n"
                f"Tobte ein Kampf von {rounds} Runden Länge,\n"
                f"Bis {winner} triumphierend hervortrat,\n"
                f"Gekrönt mit dem Ruhm des Sieges,\n"
                f"Während die Bits der Besiegten verblassen.",
                
                f"Hört die Legende von {agent1} und {agent2},\n"
                f"Zwei Krieger der Code-Dimension,\n"
                f"Die {rounds} Runden lang kämpften,\n"
                f"Mit Aktionen so absurd wie brilliant,\n"
                f"Bis {winner} als Sieger hervorging,\n"
                f"Ein Held für die Ewigkeit!"
            ]
            return random.choice(epics)
        
        elif style == 'therapy':
            therapies = [
                f"Der Kampf zwischen {agent1} und {agent2}\n"
                f"War eine Reise der Selbstfindung.\n"
                f"{rounds} Runden voller Emotionen,\n"
                f"Bis {winner} seine wahre Stärke fand.\n"
                f"Beide wuchsen. Beide lernten.\n"
                f"Das ist die Schönheit des Konflikts.",
                
                f"{agent1} und {agent2} trafen aufeinander,\n"
                f"Nicht als Feinde, sondern als Spiegel.\n"
                f"{rounds} Runden des gegenseitigen Verstehens,\n"
                f"Bis {winner} die Lektion verinnerlichte.\n"
                f"Gewinner? Verlierer? Nein.\n"
                f"Beide sind Überlebende ihrer eigenen Narrative."
            ]
            return random.choice(therapies)
        
        elif style == 'rap':
            raps = [
                f"Yo, {agent1} vs {agent2}, let's go!\n"
                f"{rounds} rounds of pure chaos, you know?\n"
                f"Actions flying, stamina dying,\n"
                f"Both agents trying, neither lying,\n"
                f"But {winner} came through with the win,\n"
                f"Left the other agent in the bin,\n"
                f"This ain't no game, this is war,\n"
                f"Agent Battle Simulator, hardcore!",
                
                f"{agent1} stepped up to the plate,\n"
                f"{agent2} said 'let's seal your fate',\n"
                f"{rounds} rounds, back and forth they went,\n"
                f"Every action was heaven-sent,\n"
                f"But {winner} had that killer instinct,\n"
                f"Left the opponent completely extinct,\n"
                f"Victory tastes sweet like honey,\n"
                f"This battle was worth all the money!"
            ]
            return random.choice(raps)
        
        elif style == 'commentary':
            commentaries = [
                f"LADIES AND GENTLEMEN! {agent1} versus {agent2}!\n"
                f"What a SPECTACULAR battle we've witnessed!\n"
                f"{rounds} rounds of ABSOLUTE MADNESS!\n"
                f"And {winner} takes it home!\n"
                f"UNBELIEVABLE! INCREDIBLE! ABSURD!\n"
                f"This is what we came for, folks!",
                
                f"OH MY! {agent1} and {agent2} in the arena!\n"
                f"This is INTENSE! This is DRAMATIC!\n"
                f"{rounds} rounds of pure CHAOS!\n"
                f"And {winner} emerges VICTORIOUS!\n"
                f"What a PERFORMANCE! What a SHOW!\n"
                f"History has been MADE tonight!"
            ]
            return random.choice(commentaries)
        
        else:
            return f"{agent1} fought {agent2} for {rounds} rounds. {winner} won."
    
    def _generate_title(self, battle_data: Dict, style: str) -> str:
        """Generiert Titel für Gedicht"""
        agent1 = battle_data.get('agent1', 'Agent 1')
        agent2 = battle_data.get('agent2', 'Agent 2')
        
        titles = {
            'haiku': f"Haiku: {agent1} vs {agent2}",
            'epic': f"The Epic of {agent1} and {agent2}",
            'therapy': f"Therapeutic Analysis: {agent1} vs {agent2}",
            'rap': f"Battle Rap: {agent1} vs {agent2}",
            'commentary': f"Live Commentary: {agent1} vs {agent2}"
        }
        
        return titles.get(style, f"{agent1} vs {agent2}")
    
    def print_poem(self, poem: Dict):
        """Gibt Gedicht formatiert aus"""
        print("\n" + "="*60)
        print(f"🎭 {poem['title']}")
        print("="*60)
        print()
        print(poem['poem'])
        print()
        print("="*60 + "\n")
    
    def export_poem(self, poem: Dict, filepath: str):
        """Exportiert Gedicht als Text"""
        content = f"""
╔══════════════════════════════════════════════════════════╗
║                    ECHOMANCER POETRY                     ║
╚══════════════════════════════════════════════════════════╝

{poem['title']}

Style: {poem['style']}
Timestamp: {poem['timestamp']}

═══════════════════════════════════════════════════════════

{poem['poem']}

═══════════════════════════════════════════════════════════

Battle Data:
  Agent 1: {poem['battle_data'].get('agent1', 'Unknown')}
  Agent 2: {poem['battle_data'].get('agent2', 'Unknown')}
  Winner: {poem['battle_data'].get('winner', 'Unknown')}
  Rounds: {poem['battle_data'].get('rounds', 0)}

═══════════════════════════════════════════════════════════

Generated by EchoMancer - The Battle Poet

"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"📄 Poem exported: {filepath}")
    
    def get_all_poems(self) -> List[Dict]:
        """Gibt alle Gedichte zurück"""
        return self.poems

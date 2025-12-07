"""
AI-Generated Actions Module
Generiert dynamische Kampfaktionen mit GPT/LLM in Echtzeit
Feature #1: "KAMPF DER KONFERENZEN"
"""

import json
import os
from typing import Dict, List, Optional
from actions import Action


class AIActionGenerator:
    """Generiert neue Kampfaktionen mit AI/LLM"""
    
    def __init__(self, use_openai: bool = True):
        self.use_openai = use_openai
        self.generated_actions = []
        self.actions_db_path = "generated_actions.json"
        
        # OpenAI Client initialisieren (wenn verfügbar)
        if use_openai and os.getenv("OPENAI_API_KEY"):
            try:
                from openai import OpenAI
                self.client = OpenAI()
                self.model = "gpt-4.1-mini"  # Schneller und günstiger
                self.available = True
            except ImportError:
                print("⚠️  OpenAI nicht verfügbar. Installiere: pip install openai")
                self.available = False
        else:
            self.available = False
        
        # Lade bereits generierte Aktionen
        self.load_generated_actions()
    
    def load_generated_actions(self):
        """Lädt bereits generierte Aktionen aus Datei"""
        if os.path.exists(self.actions_db_path):
            try:
                with open(self.actions_db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.generated_actions = data.get('actions', [])
                print(f"✅ {len(self.generated_actions)} generierte Aktionen geladen")
            except Exception as e:
                print(f"⚠️  Fehler beim Laden: {e}")
    
    def save_generated_actions(self):
        """Speichert generierte Aktionen in Datei"""
        try:
            with open(self.actions_db_path, 'w', encoding='utf-8') as f:
                json.dump({'actions': self.generated_actions}, f, indent=2, ensure_ascii=False)
            print(f"💾 {len(self.generated_actions)} Aktionen gespeichert")
        except Exception as e:
            print(f"⚠️  Fehler beim Speichern: {e}")
    
    def generate_action(self, battle_context: Dict) -> Optional[Action]:
        """
        Generiert eine neue Kampfaktion basierend auf Kontext
        
        Args:
            battle_context: Dict mit Infos über den Kampf
                - round: Aktuelle Runde
                - agent1_hp: HP von Agent 1
                - agent2_hp: HP von Agent 2
                - recent_actions: Liste der letzten Aktionen
                - humor_level: 1-10 (wie absurd soll es sein?)
        
        Returns:
            Action-Objekt oder None bei Fehler
        """
        if not self.available:
            print("⚠️  AI-Generierung nicht verfügbar (OpenAI API fehlt)")
            return None
        
        try:
            # Erstelle Prompt
            prompt = self._create_prompt(battle_context)
            
            # API-Call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,  # Kreativ!
                max_tokens=300
            )
            
            # Parse Response
            action_data = self._parse_response(response.choices[0].message.content)
            
            if action_data:
                # Erstelle Action-Objekt
                action = Action(
                    name=action_data['name'],
                    damage=action_data['damage'],
                    stamina_cost=action_data['stamina_cost'],
                    cooldown=action_data.get('cooldown', 0),
                    effect_type=action_data.get('effect_type', 'damage'),
                    effect_value=action_data.get('effect_value', 0),
                    description=action_data.get('description', '')
                )
                
                # Speichere für Wiederverwendung
                self.generated_actions.append(action_data)
                self.save_generated_actions()
                
                print(f"✨ Neue Aktion generiert: {action.name}")
                return action
            
        except Exception as e:
            print(f"❌ Fehler bei AI-Generierung: {e}")
            return None
    
    def _get_system_prompt(self) -> str:
        """System-Prompt für GPT"""
        return """Du bist ein kreativer Game Designer für ein absurdes Kampfspiel.
Generiere neue, einzigartige Kampfaktionen die:
- Lustig und absurd sind (wie "Toilettenpapier-Tsunami")
- Spielmechanisch balanciert sind
- Einen kreativen Namen haben
- Einen humorvollen Effekt haben

Antworte NUR mit einem JSON-Objekt in diesem Format:
{
  "name": "Name der Aktion",
  "damage": 25,
  "stamina_cost": 15,
  "cooldown": 2,
  "effect_type": "damage|heal|buff|debuff|stun",
  "effect_value": 10,
  "description": "Lustige Beschreibung"
}

Wichtig: Damage sollte zwischen 15-50 sein, Stamina-Cost zwischen 10-30."""
    
    def _create_prompt(self, context: Dict) -> str:
        """Erstellt Prompt basierend auf Kontext"""
        humor = context.get('humor_level', 7)
        round_num = context.get('round', 1)
        recent = context.get('recent_actions', [])
        
        prompt = f"""Generiere eine neue absurde Kampfaktion für Runde {round_num}.

Kontext:
- Humor-Level: {humor}/10 (je höher, desto absurder)
- Kürzlich genutzte Aktionen: {', '.join(recent[-3:]) if recent else 'keine'}

Die Aktion sollte:
1. Einen kreativen, lustigen Namen haben
2. Thematisch zu einem absurden Büro-/Alltags-Szenario passen
3. Spielmechanisch balanciert sein
4. NICHT die gleichen Aktionen wie kürzlich wiederholen

Generiere jetzt eine neue Aktion als JSON:"""
        
        return prompt
    
    def _parse_response(self, response: str) -> Optional[Dict]:
        """Parsed GPT-Response zu Action-Dict"""
        try:
            # Finde JSON im Response
            start = response.find('{')
            end = response.rfind('}') + 1
            
            if start >= 0 and end > start:
                json_str = response[start:end]
                data = json.loads(json_str)
                
                # Validiere Daten
                if all(k in data for k in ['name', 'damage', 'stamina_cost']):
                    return data
            
            return None
        except Exception as e:
            print(f"⚠️  Parse-Fehler: {e}")
            return None
    
    def get_random_generated_action(self) -> Optional[Dict]:
        """Gibt eine zufällige bereits generierte Aktion zurück"""
        if self.generated_actions:
            import random
            return random.choice(self.generated_actions)
        return None
    
    def rate_action(self, action_name: str, rating: int):
        """
        Bewertet eine generierte Aktion (1-5 Sterne)
        Für zukünftiges Voting-System
        """
        for action in self.generated_actions:
            if action['name'] == action_name:
                if 'ratings' not in action:
                    action['ratings'] = []
                action['ratings'].append(rating)
                self.save_generated_actions()
                print(f"⭐ Aktion '{action_name}' bewertet: {rating}/5")
                return
    
    def get_best_actions(self, limit: int = 5) -> List[Dict]:
        """Gibt die am besten bewerteten Aktionen zurück"""
        rated_actions = [a for a in self.generated_actions if 'ratings' in a]
        
        # Sortiere nach Durchschnittsbewertung
        sorted_actions = sorted(
            rated_actions,
            key=lambda a: sum(a['ratings']) / len(a['ratings']),
            reverse=True
        )
        
        return sorted_actions[:limit]


# Fallback-Aktionen wenn AI nicht verfügbar
FALLBACK_ACTIONS = [
    {
        "name": "Kaffee-Tsunami",
        "damage": 30,
        "stamina_cost": 20,
        "cooldown": 3,
        "effect_type": "damage",
        "effect_value": 0,
        "description": "Eine Welle aus überkochtem Bürokaffee"
    },
    {
        "name": "Excel-Absturz",
        "damage": 35,
        "stamina_cost": 25,
        "cooldown": 4,
        "effect_type": "stun",
        "effect_value": 1,
        "description": "Lässt den Gegner vor Schreck erstarren"
    },
    {
        "name": "Drucker-Jam-Panik",
        "damage": 28,
        "stamina_cost": 18,
        "cooldown": 2,
        "effect_type": "debuff",
        "effect_value": 10,
        "description": "Verursacht Papierstau im Gehirn"
    }
]


def demo():
    """Demo der AI-Action-Generierung"""
    print("🧠 AI-Action-Generator Demo\n")
    
    generator = AIActionGenerator()
    
    if not generator.available:
        print("⚠️  OpenAI API nicht verfügbar. Nutze Fallback-Aktionen.")
        print("\nFallback-Aktionen:")
        for action in FALLBACK_ACTIONS:
            print(f"  - {action['name']}: {action['damage']} Schaden")
        return
    
    # Generiere eine Aktion
    context = {
        'round': 5,
        'agent1_hp': 80,
        'agent2_hp': 60,
        'recent_actions': ['Toilettenpapier-Tsunami', 'Smoothie-Attacke'],
        'humor_level': 8
    }
    
    print("Generiere neue Aktion...")
    action = generator.generate_action(context)
    
    if action:
        print(f"\n✨ Generiert: {action.name}")
        print(f"   Schaden: {action.damage}")
        print(f"   Stamina: {action.stamina_cost}")
        print(f"   Cooldown: {action.cooldown}")
        print(f"   Beschreibung: {action.description}")


if __name__ == "__main__":
    demo()

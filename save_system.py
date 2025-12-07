"""
Speichersystem für Agenten
Ermöglicht Speichern und Laden von Agenten-Fortschritt
"""

import json
import os
from typing import Tuple, Optional
from agents import Agent, AttackerAgent, DefenderAgent


class SaveSystem:
    """Klasse für Speichern und Laden von Agenten"""
    
    SAVE_DIR = "saves"
    SAVE_FILE = "agents_save.json"
    
    @staticmethod
    def ensure_save_dir():
        """Stellt sicher dass Save-Verzeichnis existiert"""
        if not os.path.exists(SaveSystem.SAVE_DIR):
            os.makedirs(SaveSystem.SAVE_DIR)
    
    @staticmethod
    def save_agents(attacker: Agent, defender: Agent) -> bool:
        """Speichert beide Agenten in Datei"""
        try:
            SaveSystem.ensure_save_dir()
            
            save_data = {
                'attacker': attacker.to_dict(),
                'defender': defender.to_dict()
            }
            
            save_path = os.path.join(SaveSystem.SAVE_DIR, SaveSystem.SAVE_FILE)
            
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Fehler beim Speichern: {e}")
            return False
    
    @staticmethod
    def load_agents() -> Optional[Tuple[Agent, Agent]]:
        """Lädt beide Agenten aus Datei"""
        try:
            save_path = os.path.join(SaveSystem.SAVE_DIR, SaveSystem.SAVE_FILE)
            
            if not os.path.exists(save_path):
                return None
            
            with open(save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            attacker = AttackerAgent.from_dict(save_data['attacker'])
            defender = DefenderAgent.from_dict(save_data['defender'])
            
            return attacker, defender
        except Exception as e:
            print(f"Fehler beim Laden: {e}")
            return None
    
    @staticmethod
    def save_exists() -> bool:
        """Prüft ob Speicherdatei existiert"""
        save_path = os.path.join(SaveSystem.SAVE_DIR, SaveSystem.SAVE_FILE)
        return os.path.exists(save_path)
    
    @staticmethod
    def delete_save() -> bool:
        """Löscht Speicherdatei"""
        try:
            save_path = os.path.join(SaveSystem.SAVE_DIR, SaveSystem.SAVE_FILE)
            if os.path.exists(save_path):
                os.remove(save_path)
            return True
        except Exception as e:
            print(f"Fehler beim Löschen: {e}")
            return False
    
    @staticmethod
    def export_agent(agent: Agent, filename: str) -> bool:
        """Exportiert einzelnen Agenten"""
        try:
            SaveSystem.ensure_save_dir()
            
            export_path = os.path.join(SaveSystem.SAVE_DIR, filename)
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(agent.to_dict(), f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Fehler beim Exportieren: {e}")
            return False
    
    @staticmethod
    def import_agent(filename: str, agent_type: str) -> Optional[Agent]:
        """Importiert einzelnen Agenten"""
        try:
            import_path = os.path.join(SaveSystem.SAVE_DIR, filename)
            
            if not os.path.exists(import_path):
                return None
            
            with open(import_path, 'r', encoding='utf-8') as f:
                agent_data = json.load(f)
            
            if agent_type.lower() == "attacker":
                return AttackerAgent.from_dict(agent_data)
            elif agent_type.lower() == "defender":
                return DefenderAgent.from_dict(agent_data)
            else:
                return None
        except Exception as e:
            print(f"Fehler beim Importieren: {e}")
            return None

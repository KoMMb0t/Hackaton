"""
Feature Configuration System
Zentrale Konfiguration für alle WOW-Features
"""

import json
import os
from typing import Dict, Any


class FeatureConfig:
    """Zentrale Feature-Konfiguration"""
    
    def __init__(self, config_file: str = "features.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Lädt Konfiguration aus Datei"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Fehler beim Laden der Config: {e}")
        
        # Default-Konfiguration
        return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Standard-Konfiguration"""
        return {
            "ai_actions": {
                "enabled": False,
                "use_openai": True,
                "model": "gpt-4.1-mini",
                "generation_frequency": "on_demand",  # on_demand, every_round, random
                "humor_level": 8,
                "save_generated": True
            },
            "twitch_integration": {
                "enabled": False,
                "channel": "",
                "allow_commands": True,
                "allow_voting": True,
                "command_cooldown": 5.0,
                "enabled_commands": [
                    "buff",
                    "debuff",
                    "heal",
                    "stun",
                    "toiletstorm",
                    "smoothie",
                    "meeting",
                    "skin",
                    "vote"
                ]
            },
            "agent_therapy": {
                "enabled": True,
                "auto_generate": True,
                "export_pdf": True,
                "export_text": True,
                "use_openai": True,
                "save_sessions": True
            },
            "general": {
                "openai_api_key": "",  # Wird aus ENV geladen
                "debug_mode": False,
                "log_level": "INFO"
            }
        }
    
    def save_config(self):
        """Speichert Konfiguration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            print(f"✅ Konfiguration gespeichert: {self.config_file}")
        except Exception as e:
            print(f"❌ Fehler beim Speichern: {e}")
    
    def get(self, feature: str, key: str = None, default: Any = None) -> Any:
        """Holt Konfigurations-Wert"""
        if feature not in self.config:
            return default
        
        if key is None:
            return self.config[feature]
        
        return self.config[feature].get(key, default)
    
    def set(self, feature: str, key: str, value: Any):
        """Setzt Konfigurations-Wert"""
        if feature not in self.config:
            self.config[feature] = {}
        
        self.config[feature][key] = value
        print(f"✅ {feature}.{key} = {value}")
    
    def is_enabled(self, feature: str) -> bool:
        """Prüft ob Feature aktiviert ist"""
        return self.config.get(feature, {}).get('enabled', False)
    
    def enable_feature(self, feature: str):
        """Aktiviert ein Feature"""
        self.set(feature, 'enabled', True)
    
    def disable_feature(self, feature: str):
        """Deaktiviert ein Feature"""
        self.set(feature, 'enabled', False)
    
    def print_status(self):
        """Zeigt Feature-Status"""
        print("\n" + "=" * 60)
        print("🎮 FEATURE STATUS")
        print("=" * 60)
        
        features = [
            ('ai_actions', '🧠 AI-Generierte Aktionen'),
            ('twitch_integration', '📺 Twitch-Integration'),
            ('agent_therapy', '🧘 Agenten-Therapie')
        ]
        
        for key, name in features:
            status = "✅ AKTIV" if self.is_enabled(key) else "❌ INAKTIV"
            print(f"{name}: {status}")
        
        print("=" * 60 + "\n")


def setup_wizard():
    """Interaktiver Setup-Wizard"""
    print("\n" + "=" * 60)
    print("🎮 AGENT BATTLE SIMULATOR - FEATURE SETUP")
    print("=" * 60 + "\n")
    
    config = FeatureConfig()
    
    # AI-Aktionen
    print("🧠 AI-GENERIERTE AKTIONEN")
    print("   Generiert dynamische Kampfaktionen mit GPT")
    response = input("   Aktivieren? (j/n): ").lower()
    if response == 'j':
        config.enable_feature('ai_actions')
        
        if not os.getenv("OPENAI_API_KEY"):
            print("   ⚠️  OPENAI_API_KEY nicht gesetzt!")
            print("   Setze: export OPENAI_API_KEY='your-key'")
    
    print()
    
    # Twitch
    print("📺 TWITCH-INTEGRATION")
    print("   Zuschauer können live mit dem Spiel interagieren")
    response = input("   Aktivieren? (j/n): ").lower()
    if response == 'j':
        channel = input("   Twitch-Channel: ")
        if channel:
            config.enable_feature('twitch_integration')
            config.set('twitch_integration', 'channel', channel)
    
    print()
    
    # Therapie
    print("🧘 AGENTEN-THERAPIE")
    print("   Post-Battle KI-Reflexionen mit PDF-Export")
    response = input("   Aktivieren? (j/n): ").lower()
    if response == 'j':
        config.enable_feature('agent_therapy')
    
    print()
    
    # Speichern
    config.save_config()
    
    print("\n✅ Setup abgeschlossen!")
    config.print_status()
    
    return config


def quick_enable_all():
    """Aktiviert alle Features schnell"""
    config = FeatureConfig()
    
    config.enable_feature('ai_actions')
    config.enable_feature('twitch_integration')
    config.enable_feature('agent_therapy')
    
    config.save_config()
    
    print("✅ Alle Features aktiviert!")
    config.print_status()
    
    return config


def demo():
    """Demo des Config-Systems"""
    print("⚙️  Feature Configuration Demo\n")
    
    config = FeatureConfig()
    
    print("Aktuelle Konfiguration:")
    config.print_status()
    
    print("\nBeispiel-Nutzung:")
    print(f"  AI-Aktionen aktiviert: {config.is_enabled('ai_actions')}")
    print(f"  Humor-Level: {config.get('ai_actions', 'humor_level')}")
    print(f"  Twitch-Channel: {config.get('twitch_integration', 'channel', 'nicht gesetzt')}")
    
    print("\n💡 Tipp: Nutze setup_wizard() für interaktive Konfiguration")
    print("💡 Oder quick_enable_all() um alles zu aktivieren")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "setup":
            setup_wizard()
        elif sys.argv[1] == "enable-all":
            quick_enable_all()
        else:
            print("Usage: python feature_config.py [setup|enable-all]")
    else:
        demo()

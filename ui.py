"""
User Interface für das Battle Simulator
Menüs, Visualisierung und Interaktion
"""

import os
import sys
from typing import Optional
from agents import Agent, AttackerAgent, DefenderAgent


class UI:
    """Klasse für User Interface"""
    
    @staticmethod
    def clear_screen():
        """Löscht den Bildschirm"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def show_title():
        """Zeigt den Titel-Screen"""
        UI.clear_screen()
        print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     ⚔️  AGENT BATTLE SIMULATOR  ⚔️                       ║
║                                                           ║
║        Angreifer vs. Verteidiger                         ║
║        Mit absurden Aktionen und XP-System               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
        """)
    
    @staticmethod
    def show_main_menu() -> str:
        """Zeigt das Hauptmenü und gibt Auswahl zurück"""
        print("\n" + "="*60)
        print("HAUPTMENÜ".center(60))
        print("="*60)
        print("\n1. 🎮 Neuer Kampf (Manuell)")
        print("2. 🤖 Neuer Kampf (Autopilot)")
        print("3. 🏆 Turnier starten (Best of 3)")
        print("4. 📊 Agenten-Statistiken anzeigen")
        print("5. 💾 Agenten speichern")
        print("6. 📂 Agenten laden")
        print("7. 🔄 Agenten zurücksetzen")
        print("8. ❌ Beenden")
        
        choice = input("\nWähle eine Option (1-8): ").strip()
        return choice
    
    @staticmethod
    def show_agent_stats(attacker: Agent, defender: Agent):
        """Zeigt detaillierte Agenten-Statistiken"""
        UI.clear_screen()
        print("\n" + "="*60)
        print("📊 AGENTEN-STATISTIKEN 📊".center(60))
        print("="*60)
        
        print(f"\n{attacker.name}")
        print("-" * 40)
        print(f"Level: {attacker.level}")
        print(f"XP: {attacker.xp}/{attacker.xp_to_next_level}")
        print(f"HP: {attacker.hp}/{attacker.max_hp}")
        print(f"Stamina: {attacker.stamina}/{attacker.max_stamina}")
        print(f"Attack Bonus: +{attacker.attack_bonus}")
        print(f"Defense Bonus: +{attacker.defense_bonus}")
        print(f"\nKampf-Statistiken:")
        print(f"  Siege: {attacker.battles_won}")
        print(f"  Niederlagen: {attacker.battles_lost}")
        print(f"  Gesamt Schaden: {attacker.total_damage_dealt}")
        print(f"  Aktionen genutzt: {attacker.actions_used}")
        
        print(f"\n{defender.name}")
        print("-" * 40)
        print(f"Level: {defender.level}")
        print(f"XP: {defender.xp}/{defender.xp_to_next_level}")
        print(f"HP: {defender.hp}/{defender.max_hp}")
        print(f"Stamina: {defender.stamina}/{defender.max_stamina}")
        print(f"Attack Bonus: +{defender.attack_bonus}")
        print(f"Defense Bonus: +{defender.defense_bonus}")
        print(f"\nKampf-Statistiken:")
        print(f"  Siege: {defender.battles_won}")
        print(f"  Niederlagen: {defender.battles_lost}")
        print(f"  Gesamt Schaden: {defender.total_damage_dealt}")
        print(f"  Aktionen genutzt: {defender.actions_used}")
        
        input("\nDrücke Enter um fortzufahren...")
    
    @staticmethod
    def show_actions_menu(agent: Agent) -> Optional[int]:
        """Zeigt verfügbare Aktionen und gibt Auswahl zurück"""
        available = agent.get_available_actions()
        
        if not available:
            print(f"\n{agent.name} hat keine verfügbaren Aktionen!")
            print("💤 Regeneriert automatisch Stamina...")
            return None
        
        print(f"\n{agent.name} - Wähle eine Aktion:")
        print("-" * 40)
        
        for i, action in enumerate(available, 1):
            cooldown_info = f" (Cooldown: {action.current_cooldown})" if action.current_cooldown > 0 else ""
            print(f"{i}. {action.name}")
            print(f"   Schaden: {action.damage} | Stamina: {action.stamina_cost} | Cooldown: {action.cooldown}{cooldown_info}")
        
        while True:
            try:
                choice = input(f"\nWähle Aktion (1-{len(available)}): ").strip()
                choice_num = int(choice)
                if 1 <= choice_num <= len(available):
                    return choice_num - 1
                else:
                    print(f"Bitte wähle eine Zahl zwischen 1 und {len(available)}")
            except ValueError:
                print("Ungültige Eingabe. Bitte gib eine Zahl ein.")
    
    @staticmethod
    def confirm_action(message: str) -> bool:
        """Fragt Benutzer nach Bestätigung"""
        while True:
            response = input(f"\n{message} (j/n): ").strip().lower()
            if response in ['j', 'ja', 'y', 'yes']:
                return True
            elif response in ['n', 'nein', 'no']:
                return False
            else:
                print("Bitte antworte mit 'j' oder 'n'")
    
    @staticmethod
    def show_loading(message: str, duration: float = 1.0):
        """Zeigt eine Lade-Animation"""
        import time
        print(f"\n{message}", end="", flush=True)
        for _ in range(3):
            time.sleep(duration / 3)
            print(".", end="", flush=True)
        print(" ✓")
    
    @staticmethod
    def show_error(message: str):
        """Zeigt eine Fehlermeldung"""
        print(f"\n❌ FEHLER: {message}")
        input("Drücke Enter um fortzufahren...")
    
    @staticmethod
    def show_success(message: str):
        """Zeigt eine Erfolgsmeldung"""
        print(f"\n✅ {message}")
        input("Drücke Enter um fortzufahren...")
    
    @staticmethod
    def show_welcome_message():
        """Zeigt Willkommensnachricht"""
        print("""
Willkommen beim Agent Battle Simulator!

In diesem Spiel kämpfen zwei KI-Agenten gegeneinander:
- 🔴 Der Angreifer: Aggressiv und schadensfokussiert
- 🔵 Der Verteidiger: Defensiv mit cleveren Kontern

Beide Agenten sammeln XP und leveln auf, wodurch sie stärker werden!

Features:
✨ Absurde Kampfaktionen wie "Toilettenpapier-Tsunami"
✨ Erfahrungspunkte-System mit Level-Ups
✨ Verschiedene KI-Strategien
✨ Autopilot-Modus zum Zuschauen
✨ Turnier-Modus für mehrere Kämpfe
✨ Speichern/Laden von Agenten

Viel Spaß beim Kämpfen! ⚔️
        """)
        input("\nDrücke Enter um zu starten...")
    
    @staticmethod
    def show_goodbye():
        """Zeigt Abschiedsnachricht"""
        UI.clear_screen()
        print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              Danke fürs Spielen! 🎮                      ║
║                                                           ║
║         Bis zum nächsten Kampf! ⚔️                       ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
        """)
    
    @staticmethod
    def get_tournament_settings() -> tuple:
        """Fragt Turnier-Einstellungen ab"""
        print("\n" + "="*60)
        print("TURNIER-EINSTELLUNGEN".center(60))
        print("="*60)
        
        while True:
            try:
                num_battles = input("\nAnzahl der Kämpfe (3, 5, 7): ").strip()
                num_battles = int(num_battles)
                if num_battles in [3, 5, 7]:
                    break
                else:
                    print("Bitte wähle 3, 5 oder 7 Kämpfe")
            except ValueError:
                print("Ungültige Eingabe. Bitte gib eine Zahl ein.")
        
        while True:
            try:
                delay = input("\nGeschwindigkeit (0.5 = schnell, 1.5 = normal, 3.0 = langsam): ").strip()
                delay = float(delay)
                if 0.1 <= delay <= 5.0:
                    break
                else:
                    print("Bitte wähle einen Wert zwischen 0.1 und 5.0")
            except ValueError:
                print("Ungültige Eingabe. Bitte gib eine Zahl ein.")
        
        return num_battles, delay

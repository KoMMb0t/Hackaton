#!/usr/bin/env python3
"""
Agent Battle Simulator - Hauptprogramm
Ein unterhaltsames Kampfspiel zwischen KI-Agenten mit XP-System

Für den Cline Hackathon (8.-14. Dezember)
"""

import sys
from agents import AttackerAgent, DefenderAgent
from game_engine import GameEngine, Tournament
from ui import UI
from save_system import SaveSystem


class BattleSimulator:
    """Hauptklasse für das Spiel"""
    
    def __init__(self):
        self.attacker = None
        self.defender = None
        self.running = True
    
    def initialize_agents(self):
        """Initialisiert oder lädt Agenten"""
        # Versuche gespeicherte Agenten zu laden
        if SaveSystem.save_exists():
            if UI.confirm_action("Gespeicherte Agenten gefunden. Laden?"):
                loaded = SaveSystem.load_agents()
                if loaded:
                    self.attacker, self.defender = loaded
                    UI.show_success("Agenten erfolgreich geladen!")
                    return
        
        # Erstelle neue Agenten
        self.attacker = AttackerAgent("🔴 Der Angreifer", level=1)
        self.defender = DefenderAgent("🔵 Der Verteidiger", level=1)
        print("\n✨ Neue Agenten erstellt!")
    
    def run(self):
        """Hauptschleife des Spiels"""
        UI.show_title()
        UI.show_welcome_message()
        
        self.initialize_agents()
        
        while self.running:
            UI.clear_screen()
            UI.show_title()
            
            choice = UI.show_main_menu()
            
            if choice == "1":
                self.manual_battle()
            elif choice == "2":
                self.auto_battle()
            elif choice == "3":
                self.tournament_mode()
            elif choice == "4":
                self.show_stats()
            elif choice == "5":
                self.save_agents()
            elif choice == "6":
                self.load_agents()
            elif choice == "7":
                self.reset_agents()
            elif choice == "8":
                self.quit_game()
            else:
                UI.show_error("Ungültige Auswahl. Bitte wähle 1-8.")
    
    def manual_battle(self):
        """Startet einen manuellen Kampf"""
        UI.clear_screen()
        engine = GameEngine(self.attacker, self.defender)
        engine.start_battle(auto_mode=False)
        input("\nDrücke Enter um fortzufahren...")
    
    def auto_battle(self):
        """Startet einen automatischen Kampf"""
        UI.clear_screen()
        
        # Frage nach Geschwindigkeit
        print("\n" + "="*60)
        print("AUTOPILOT-EINSTELLUNGEN".center(60))
        print("="*60)
        
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
        
        engine = GameEngine(self.attacker, self.defender)
        engine.start_battle(auto_mode=True, delay=delay)
        input("\nDrücke Enter um fortzufahren...")
    
    def tournament_mode(self):
        """Startet einen Turnier-Modus"""
        UI.clear_screen()
        
        num_battles, delay = UI.get_tournament_settings()
        
        tournament = Tournament(self.attacker, self.defender, num_battles)
        tournament.start_tournament(auto_mode=True, delay=delay)
        
        input("\nDrücke Enter um fortzufahren...")
    
    def show_stats(self):
        """Zeigt Agenten-Statistiken"""
        UI.show_agent_stats(self.attacker, self.defender)
    
    def save_agents(self):
        """Speichert Agenten"""
        UI.clear_screen()
        UI.show_loading("Speichere Agenten")
        
        if SaveSystem.save_agents(self.attacker, self.defender):
            UI.show_success("Agenten erfolgreich gespeichert!")
        else:
            UI.show_error("Fehler beim Speichern der Agenten")
    
    def load_agents(self):
        """Lädt Agenten"""
        UI.clear_screen()
        
        if not SaveSystem.save_exists():
            UI.show_error("Keine gespeicherten Agenten gefunden!")
            return
        
        if UI.confirm_action("Aktuelle Agenten werden überschrieben. Fortfahren?"):
            UI.show_loading("Lade Agenten")
            
            loaded = SaveSystem.load_agents()
            if loaded:
                self.attacker, self.defender = loaded
                UI.show_success("Agenten erfolgreich geladen!")
            else:
                UI.show_error("Fehler beim Laden der Agenten")
    
    def reset_agents(self):
        """Setzt Agenten zurück"""
        UI.clear_screen()
        
        if UI.confirm_action("Alle Agenten zurücksetzen? (Fortschritt geht verloren)"):
            self.attacker = AttackerAgent("🔴 Der Angreifer", level=1)
            self.defender = DefenderAgent("🔵 Der Verteidiger", level=1)
            
            # Lösche Speicherdatei
            SaveSystem.delete_save()
            
            UI.show_success("Agenten wurden zurückgesetzt!")
    
    def quit_game(self):
        """Beendet das Spiel"""
        UI.clear_screen()
        
        if UI.confirm_action("Möchtest du vor dem Beenden speichern?"):
            SaveSystem.save_agents(self.attacker, self.defender)
            print("\n✅ Gespeichert!")
        
        UI.show_goodbye()
        self.running = False


def main():
    """Hauptfunktion"""
    try:
        simulator = BattleSimulator()
        simulator.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Spiel wurde unterbrochen!")
        UI.show_goodbye()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Kritischer Fehler: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

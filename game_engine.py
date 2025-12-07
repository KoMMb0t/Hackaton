"""
Game Engine für das Battle Simulator
Verwaltet Kampflogik, Rundenablauf und Spielmechaniken
"""

import random
import time
from typing import Tuple, Optional
from agents import Agent, AttackerAgent, DefenderAgent
from actions import Action, get_random_comment


class GameEngine:
    """Hauptklasse für die Spielmechanik"""
    
    def __init__(self, attacker: Agent, defender: Agent):
        self.attacker = attacker
        self.defender = defender
        self.round_number = 0
        self.battle_log = []
        self.winner = None
        
    def start_battle(self, auto_mode: bool = False, delay: float = 1.5) -> Agent:
        """Startet einen Kampf zwischen den Agenten"""
        print("\n" + "="*60)
        print("⚔️  KAMPF BEGINNT! ⚔️".center(60))
        print("="*60)
        
        self._show_agents_status()
        
        if not auto_mode:
            input("\nDrücke Enter um zu starten...")
        else:
            time.sleep(delay)
        
        # Kampfschleife
        while self.attacker.is_alive() and self.defender.is_alive():
            self.round_number += 1
            self._execute_round(auto_mode, delay)
        
        # Kampf beendet
        self._end_battle()
        return self.winner
    
    def _execute_round(self, auto_mode: bool, delay: float) -> None:
        """Führt eine Kampfrunde aus"""
        print("\n" + "-"*60)
        print(f"⚡ RUNDE {self.round_number} ⚡".center(60))
        print("-"*60)
        
        # Regeneriere Stamina
        self.attacker.restore_stamina(10)
        self.defender.restore_stamina(10)
        
        # Reduziere Cooldowns
        self.attacker.reduce_cooldowns()
        self.defender.reduce_cooldowns()
        
        # Wende Buffs/Debuffs an
        self.attacker.apply_buffs_debuffs()
        self.defender.apply_buffs_debuffs()
        
        # Bestimme Reihenfolge (zufällig)
        if random.random() < 0.5:
            first, second = self.attacker, self.defender
        else:
            first, second = self.defender, self.attacker
        
        # Erste Aktion
        if not first.is_stunned:
            self._execute_action(first, second, auto_mode, delay)
        else:
            print(f"\n{first.name} ist STUNNED und kann nicht angreifen! 😵")
            first.is_stunned = False
        
        # Zweite Aktion (wenn beide noch leben)
        if self.attacker.is_alive() and self.defender.is_alive():
            if not second.is_stunned:
                self._execute_action(second, first, auto_mode, delay)
            else:
                print(f"\n{second.name} ist STUNNED und kann nicht angreifen! 😵")
                second.is_stunned = False
        
        # Status anzeigen
        self._show_agents_status()
        
        if not auto_mode and self.attacker.is_alive() and self.defender.is_alive():
            input("\nDrücke Enter für die nächste Runde...")
        elif auto_mode:
            time.sleep(delay)
    
    def _execute_action(self, actor: Agent, target: Agent, 
                       auto_mode: bool, delay: float) -> None:
        """Führt eine Aktion eines Agenten aus"""
        # Wähle Aktion
        action = actor.choose_action(target)
        
        if action is None:
            print(f"\n{actor.name} hat keine verfügbaren Aktionen!")
            print("💤 Regeneriert Stamina...")
            actor.restore_stamina(20)
            return
        
        # Verbrauche Stamina
        actor.use_stamina(action.stamina_cost)
        action.use()
        actor.actions_used += 1
        
        # Zeige Aktion
        print(f"\n{actor.name} nutzt: {action.name}")
        print(f"   {action.description}")
        
        # Berechne Schaden
        damage = action.get_actual_damage() + actor.attack_bonus
        
        # Wende Effekte an
        if action.effect_type == "heal":
            healed = actor.heal(action.effect_value)
            print(f"   💚 Heilt {healed} HP!")
        elif action.effect_type == "buff":
            actor.buffs.append({
                'name': action.name,
                'value': action.effect_value,
                'duration': 2
            })
            print(f"   ✨ Erhält Buff: +{action.effect_value} Defense!")
        elif action.effect_type == "debuff":
            target.debuffs.append({
                'name': action.name,
                'value': action.effect_value,
                'duration': 2
            })
            print(f"   💀 Gegner erhält Debuff: -{action.effect_value} Defense!")
        elif action.effect_type == "stun":
            target.is_stunned = True
            print(f"   😵 Gegner ist STUNNED für 1 Runde!")
        
        # Schaden zufügen
        if damage > 0:
            actual_damage = target.take_damage(damage)
            actor.total_damage_dealt += actual_damage
            print(f"   💥 Verursacht {actual_damage} Schaden!")
        
        # Witziger Kommentar
        print(f"\n   💬 {get_random_comment()}")
        
        if auto_mode:
            time.sleep(delay * 0.5)
    
    def _show_agents_status(self) -> None:
        """Zeigt Status beider Agenten"""
        print(self.attacker.get_status())
        print(self.defender.get_status())
    
    def _end_battle(self) -> None:
        """Beendet den Kampf und vergibt XP"""
        print("\n" + "="*60)
        print("🏁 KAMPF BEENDET! 🏁".center(60))
        print("="*60)
        
        if self.attacker.is_alive():
            self.winner = self.attacker
            loser = self.defender
            print(f"\n🎉 {self.attacker.name} GEWINNT! 🎉\n")
            self.attacker.battles_won += 1
            self.defender.battles_lost += 1
        else:
            self.winner = self.defender
            loser = self.attacker
            print(f"\n🎉 {self.defender.name} GEWINNT! 🎉\n")
            self.defender.battles_won += 1
            self.attacker.battles_lost += 1
        
        # XP vergeben
        winner_xp = 100 + (self.round_number * 10)
        loser_xp = 50 + (self.round_number * 5)
        
        print(f"{self.winner.name} erhält {winner_xp} XP!")
        leveled_up = self.winner.add_xp(winner_xp)
        
        print(f"{loser.name} erhält {loser_xp} XP (Trostpreis)!")
        loser.add_xp(loser_xp)
        
        # Statistiken
        print("\n" + "="*60)
        print("📊 KAMPF-STATISTIKEN 📊".center(60))
        print("="*60)
        print(f"\nRunden: {self.round_number}")
        print(f"\n{self.attacker.name}:")
        print(f"  Schaden verursacht: {self.attacker.total_damage_dealt}")
        print(f"  Schaden erhalten: {self.attacker.total_damage_taken}")
        print(f"  Aktionen genutzt: {self.attacker.actions_used}")
        print(f"  Siege: {self.attacker.battles_won} | Niederlagen: {self.attacker.battles_lost}")
        
        print(f"\n{self.defender.name}:")
        print(f"  Schaden verursacht: {self.defender.total_damage_dealt}")
        print(f"  Schaden erhalten: {self.defender.total_damage_taken}")
        print(f"  Aktionen genutzt: {self.defender.actions_used}")
        print(f"  Siege: {self.defender.battles_won} | Niederlagen: {self.defender.battles_lost}")
        
        # Heile beide Agenten für nächsten Kampf
        self.attacker.hp = self.attacker.max_hp
        self.attacker.stamina = self.attacker.max_stamina
        self.defender.hp = self.defender.max_hp
        self.defender.stamina = self.defender.max_stamina


class Tournament:
    """Turnier-Modus für mehrere Kämpfe"""
    
    def __init__(self, attacker: Agent, defender: Agent, num_battles: int = 3):
        self.attacker = attacker
        self.defender = defender
        self.num_battles = num_battles
        self.attacker_wins = 0
        self.defender_wins = 0
    
    def start_tournament(self, auto_mode: bool = True, delay: float = 1.0) -> None:
        """Startet ein Turnier mit mehreren Kämpfen"""
        print("\n" + "="*60)
        print(f"🏆 TURNIER STARTET - Best of {self.num_battles} 🏆".center(60))
        print("="*60)
        
        for battle_num in range(1, self.num_battles + 1):
            print(f"\n\n{'='*60}")
            print(f"⚔️  KAMPF {battle_num}/{self.num_battles} ⚔️".center(60))
            print("="*60)
            
            engine = GameEngine(self.attacker, self.defender)
            winner = engine.start_battle(auto_mode, delay)
            
            if winner == self.attacker:
                self.attacker_wins += 1
            else:
                self.defender_wins += 1
            
            print(f"\n📊 Aktueller Stand: {self.attacker.name} {self.attacker_wins} - {self.defender_wins} {self.defender.name}")
            
            if battle_num < self.num_battles:
                if auto_mode:
                    time.sleep(delay * 2)
                else:
                    input("\nDrücke Enter für den nächsten Kampf...")
        
        # Turnier-Sieger
        print("\n" + "="*60)
        print("🏆 TURNIER BEENDET! 🏆".center(60))
        print("="*60)
        
        if self.attacker_wins > self.defender_wins:
            print(f"\n🎉 {self.attacker.name} GEWINNT DAS TURNIER! 🎉")
            print(f"   Endstand: {self.attacker_wins} - {self.defender_wins}")
        elif self.defender_wins > self.attacker_wins:
            print(f"\n🎉 {self.defender.name} GEWINNT DAS TURNIER! 🎉")
            print(f"   Endstand: {self.attacker_wins} - {self.defender_wins}")
        else:
            print(f"\n🤝 UNENTSCHIEDEN! 🤝")
            print(f"   Endstand: {self.attacker_wins} - {self.defender_wins}")

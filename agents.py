"""
Agenten-Klassen für das Battle Simulator
Enthält Angreifer und Verteidiger mit XP-System
"""

import random
import json
from typing import List, Dict, Optional
from actions import Action, get_actions_for_agent


class Agent:
    """Basis-Klasse für alle Agenten"""
    
    def __init__(self, name: str, agent_type: str, level: int = 1):
        self.name = name
        self.agent_type = agent_type
        self.level = level
        self.xp = 0
        self.xp_to_next_level = 100
        
        # Basis-Stats (skalieren mit Level)
        self.max_hp = 100 + (level - 1) * 20
        self.hp = self.max_hp
        self.max_stamina = 100 + (level - 1) * 10
        self.stamina = self.max_stamina
        
        # Kampf-Stats
        self.attack_bonus = (level - 1) * 2
        self.defense_bonus = (level - 1) * 2
        
        # Status-Effekte
        self.buffs: List[Dict] = []
        self.debuffs: List[Dict] = []
        self.is_stunned = False
        
        # Aktionen
        self.actions = get_actions_for_agent(agent_type)
        
        # Statistiken
        self.total_damage_dealt = 0
        self.total_damage_taken = 0
        self.actions_used = 0
        self.battles_won = 0
        self.battles_lost = 0
        
    def take_damage(self, damage: int) -> int:
        """Nimmt Schaden und berücksichtigt Defense"""
        actual_damage = max(1, damage - self.defense_bonus)
        self.hp = max(0, self.hp - actual_damage)
        self.total_damage_taken += actual_damage
        return actual_damage
    
    def heal(self, amount: int) -> int:
        """Heilt HP"""
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp
    
    def restore_stamina(self, amount: int) -> int:
        """Stellt Stamina wieder her"""
        old_stamina = self.stamina
        self.stamina = min(self.max_stamina, self.stamina + amount)
        return self.stamina - old_stamina
    
    def use_stamina(self, amount: int) -> bool:
        """Verbraucht Stamina"""
        if self.stamina >= amount:
            self.stamina -= amount
            return True
        return False
    
    def add_xp(self, amount: int) -> bool:
        """Fügt XP hinzu und prüft Level-Up"""
        self.xp += amount
        if self.xp >= self.xp_to_next_level:
            self.level_up()
            return True
        return False
    
    def level_up(self) -> None:
        """Erhöht Level und Stats"""
        self.level += 1
        self.xp = 0
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
        
        # Erhöhe Stats
        old_max_hp = self.max_hp
        old_max_stamina = self.max_stamina
        
        self.max_hp += 20
        self.max_stamina += 10
        self.attack_bonus += 2
        self.defense_bonus += 2
        
        # Volle Heilung bei Level-Up
        self.hp = self.max_hp
        self.stamina = self.max_stamina
        
        print(f"\n🎉 {self.name} ist jetzt Level {self.level}!")
        print(f"   HP: {old_max_hp} → {self.max_hp}")
        print(f"   Stamina: {old_max_stamina} → {self.max_stamina}")
        print(f"   Attack: +{self.attack_bonus}")
        print(f"   Defense: +{self.defense_bonus}")
    
    def get_available_actions(self) -> List[Action]:
        """Gibt alle verfügbaren Aktionen zurück"""
        return [action for action in self.actions if action.is_available(self.stamina)]
    
    def apply_buffs_debuffs(self) -> None:
        """Wendet Buffs/Debuffs an und reduziert Dauer"""
        # Buffs
        for buff in self.buffs[:]:
            buff['duration'] -= 1
            if buff['duration'] <= 0:
                self.buffs.remove(buff)
        
        # Debuffs
        for debuff in self.debuffs[:]:
            debuff['duration'] -= 1
            if debuff['duration'] <= 0:
                self.debuffs.remove(debuff)
        
        # Stun
        if self.is_stunned:
            self.is_stunned = False
    
    def reduce_cooldowns(self) -> None:
        """Reduziert alle Cooldowns"""
        for action in self.actions:
            action.reduce_cooldown()
    
    def is_alive(self) -> bool:
        """Prüft ob Agent noch lebt"""
        return self.hp > 0
    
    def get_status(self) -> str:
        """Gibt Status-String zurück"""
        hp_bar = self._create_bar(self.hp, self.max_hp, 20, '█', '░')
        stamina_bar = self._create_bar(self.stamina, self.max_stamina, 20, '▓', '░')
        
        status = f"\n{self.name} (Level {self.level})\n"
        status += f"  HP:      [{hp_bar}] {self.hp}/{self.max_hp}\n"
        status += f"  Stamina: [{stamina_bar}] {self.stamina}/{self.max_stamina}\n"
        status += f"  XP:      {self.xp}/{self.xp_to_next_level}\n"
        
        if self.buffs:
            status += f"  Buffs: {', '.join([b['name'] for b in self.buffs])}\n"
        if self.debuffs:
            status += f"  Debuffs: {', '.join([d['name'] for d in self.debuffs])}\n"
        if self.is_stunned:
            status += f"  Status: 😵 STUNNED!\n"
        
        return status
    
    def _create_bar(self, current: int, maximum: int, length: int, 
                    filled_char: str, empty_char: str) -> str:
        """Erstellt eine visuelle Bar"""
        filled = int((current / maximum) * length)
        empty = length - filled
        return filled_char * filled + empty_char * empty
    
    def to_dict(self) -> Dict:
        """Konvertiert Agent zu Dictionary für Speicherung"""
        return {
            'name': self.name,
            'agent_type': self.agent_type,
            'level': self.level,
            'xp': self.xp,
            'hp': self.hp,
            'stamina': self.stamina,
            'total_damage_dealt': self.total_damage_dealt,
            'total_damage_taken': self.total_damage_taken,
            'actions_used': self.actions_used,
            'battles_won': self.battles_won,
            'battles_lost': self.battles_lost,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Agent':
        """Erstellt Agent aus Dictionary"""
        agent = cls(data['name'], data['agent_type'], data['level'])
        agent.xp = data['xp']
        agent.hp = data['hp']
        agent.stamina = data['stamina']
        agent.total_damage_dealt = data['total_damage_dealt']
        agent.total_damage_taken = data['total_damage_taken']
        agent.actions_used = data['actions_used']
        agent.battles_won = data['battles_won']
        agent.battles_lost = data['battles_lost']
        return agent


class AttackerAgent(Agent):
    """Angreifer-Agent mit aggressiver KI"""
    
    def __init__(self, name: str = "🔴 Der Angreifer", level: int = 1):
        super().__init__(name, "attacker", level)
        self.strategy = "aggressive"
    
    def choose_action(self, opponent: Agent) -> Optional[Action]:
        """Wählt eine Aktion basierend auf aggressiver Strategie"""
        available = self.get_available_actions()
        
        if not available:
            return None
        
        # Aggressive Strategie: Bevorzuge hohen Schaden
        if random.random() < 0.7:  # 70% Chance für höchsten Schaden
            return max(available, key=lambda a: a.damage)
        else:  # 30% Chance für zufällige Aktion
            return random.choice(available)


class DefenderAgent(Agent):
    """Verteidiger-Agent mit defensiver KI"""
    
    def __init__(self, name: str = "🔵 Der Verteidiger", level: int = 1):
        super().__init__(name, "defender", level)
        self.strategy = "defensive"
    
    def choose_action(self, opponent: Agent) -> Optional[Action]:
        """Wählt eine Aktion basierend auf defensiver Strategie"""
        available = self.get_available_actions()
        
        if not available:
            return None
        
        # Defensive Strategie: Heile wenn HP niedrig, sonst kontere
        if self.hp < self.max_hp * 0.3:  # Unter 30% HP
            heal_actions = [a for a in available if a.effect_type == "heal"]
            if heal_actions:
                return random.choice(heal_actions)
        
        # Bevorzuge Buffs wenn keine Heilung nötig
        if self.hp < self.max_hp * 0.6:  # Unter 60% HP
            buff_actions = [a for a in available if a.effect_type == "buff"]
            if buff_actions and random.random() < 0.5:
                return random.choice(buff_actions)
        
        # Sonst: Konter mit höchstem Schaden
        return max(available, key=lambda a: a.damage)

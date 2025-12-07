"""
Kampfaktionen für das Agent Battle Simulator
Jede Aktion hat Schaden, Kosten, Cooldown und Spezialeffekte
"""

import random
from typing import Dict, List, Tuple, Optional


class Action:
    """Basis-Klasse für alle Aktionen"""
    
    def __init__(self, name: str, description: str, damage: int, stamina_cost: int, 
                 cooldown: int, effect_type: Optional[str] = None, effect_value: int = 0):
        self.name = name
        self.description = description
        self.damage = damage
        self.stamina_cost = stamina_cost
        self.cooldown = cooldown
        self.current_cooldown = 0
        self.effect_type = effect_type  # 'buff', 'debuff', 'heal', 'stun', etc.
        self.effect_value = effect_value
        
    def is_available(self, stamina: int) -> bool:
        """Prüft ob Aktion verfügbar ist"""
        return self.current_cooldown == 0 and stamina >= self.stamina_cost
    
    def use(self) -> None:
        """Setzt Cooldown nach Nutzung"""
        self.current_cooldown = self.cooldown
        
    def reduce_cooldown(self) -> None:
        """Reduziert Cooldown um 1"""
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
    
    def get_actual_damage(self) -> int:
        """Berechnet tatsächlichen Schaden mit Zufallsfaktor"""
        variance = random.uniform(0.8, 1.2)
        return int(self.damage * variance)


# Angreifer-Aktionen (Offensiv)
ATTACKER_ACTIONS = [
    Action(
        name="🧻 Toilettenpapier-Tsunami",
        description="Eine Welle aus Toilettenpapier überflutet den Gegner!",
        damage=25,
        stamina_cost=15,
        cooldown=2,
        effect_type="debuff",
        effect_value=5
    ),
    Action(
        name="🔥 Feuerball der Bürofrustration",
        description="Alle aufgestaute Wut explodiert in einem Feuerball!",
        damage=40,
        stamina_cost=25,
        cooldown=3,
        effect_type=None,
        effect_value=0
    ),
    Action(
        name="🦠 Viren-E-Mail",
        description="Schickt eine verseuchte E-Mail mit 47 Anhängen!",
        damage=20,
        stamina_cost=10,
        cooldown=1,
        effect_type="debuff",
        effect_value=3
    ),
    Action(
        name="🪖 Meeting-Demoralisierung",
        description="Zwingt den Gegner zu einem 3-Stunden-Meeting ohne Agenda!",
        damage=15,
        stamina_cost=20,
        cooldown=4,
        effect_type="stun",
        effect_value=1
    ),
    Action(
        name="🧃 Smoothie-Attacke",
        description="Wirft einen Chia-Smoothie mit doppeltem Schaden!",
        damage=30,
        stamina_cost=18,
        cooldown=2,
        effect_type=None,
        effect_value=0
    ),
    Action(
        name="⚡ Blitz-Spam",
        description="Bombardiert mit 1000 Slack-Nachrichten pro Sekunde!",
        damage=22,
        stamina_cost=12,
        cooldown=1,
        effect_type="debuff",
        effect_value=4
    ),
    Action(
        name="🎯 Präzisions-Kritik",
        description="Eine messerscharfe Kritik am Code-Style!",
        damage=35,
        stamina_cost=20,
        cooldown=3,
        effect_type=None,
        effect_value=0
    ),
    Action(
        name="💣 Deadline-Bombe",
        description="Setzt eine unmögliche Deadline - HEUTE!",
        damage=45,
        stamina_cost=30,
        cooldown=5,
        effect_type="debuff",
        effect_value=8
    ),
]


# Verteidiger-Aktionen (Defensiv mit Kontern)
DEFENDER_ACTIONS = [
    Action(
        name="🧲 Magnetische Feldverwirrung",
        description="Verwirrt den Angreifer mit magnetischen Feldern!",
        damage=18,
        stamina_cost=12,
        cooldown=2,
        effect_type="debuff",
        effect_value=4
    ),
    Action(
        name="🦾 Selbstoptimierung",
        description="Philosophische Diskussion führt zu innerer Stärke!",
        damage=10,
        stamina_cost=15,
        cooldown=3,
        effect_type="heal",
        effect_value=20
    ),
    Action(
        name="🧠 Gedankenlesen",
        description="Liest die Gedanken des Gegners und kontert perfekt!",
        damage=28,
        stamina_cost=18,
        cooldown=3,
        effect_type="buff",
        effect_value=5
    ),
    Action(
        name="🛡️ Firewall der Gelassenheit",
        description="Blockt alle Angriffe mit stoischer Ruhe!",
        damage=5,
        stamina_cost=10,
        cooldown=1,
        effect_type="buff",
        effect_value=10
    ),
    Action(
        name="🔄 Reverse-Uno-Karte",
        description="Reflektiert 50% des letzten Schadens zurück!",
        damage=25,
        stamina_cost=20,
        cooldown=4,
        effect_type="reflect",
        effect_value=50
    ),
    Action(
        name="☕ Kaffee-Konter",
        description="Ein heißer Espresso bringt neue Energie!",
        damage=15,
        stamina_cost=8,
        cooldown=1,
        effect_type="heal",
        effect_value=15
    ),
    Action(
        name="🧘 Meditation der Unverwundbarkeit",
        description="Innere Ruhe macht immun gegen Stress!",
        damage=0,
        stamina_cost=25,
        cooldown=5,
        effect_type="buff",
        effect_value=15
    ),
    Action(
        name="⚔️ Zynischer Gegenangriff",
        description="Kontert mit sarkastischen Bemerkungen!",
        damage=32,
        stamina_cost=22,
        cooldown=3,
        effect_type="debuff",
        effect_value=6
    ),
]


# Witzige Kampfkommentare
COMBAT_COMMENTS = [
    "Und da trifft der Angriff mitten ins Ego!",
    "Autsch! Das hat wehgetan... emotional!",
    "Der Verteidiger ist jetzt in einer Existenzkrise!",
    "Das war so effektiv wie ein Meeting am Freitagnachmittag!",
    "Kritischer Treffer! Die Moral sinkt rapide!",
    "Der Angreifer sieht verwirrt aus... oder ist das normal?",
    "Oha! Das war knapp! Fast wie ein funktionierendes Deployment!",
    "Der Schaden ist real! Genau wie die Bugs in Production!",
    "Beide Kämpfer sind erschöpft... Zeit für eine Kaffeepause?",
    "Das Publikum (also niemand) ist begeistert!",
    "Ein taktisches Manöver! Oder doch nur Glück?",
    "Die Spannung steigt! Oder ist das nur der Koffein?",
    "Unglaublich! Fast so unglaublich wie funktionierende Tests!",
    "Der Kampf wird härter! Wie ein Sprint-Planning!",
    "Beide geben alles! Wie bei einem Merge-Conflict!",
]


def get_random_comment() -> str:
    """Gibt einen zufälligen Kampfkommentar zurück"""
    return random.choice(COMBAT_COMMENTS)


def get_actions_for_agent(agent_type: str) -> List[Action]:
    """Gibt die Aktionen für einen Agenten-Typ zurück"""
    if agent_type.lower() == "attacker":
        return ATTACKER_ACTIONS.copy()
    elif agent_type.lower() == "defender":
        return DEFENDER_ACTIONS.copy()
    else:
        raise ValueError(f"Unbekannter Agent-Typ: {agent_type}")

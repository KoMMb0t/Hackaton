"""
Skins Manager
Verwaltet verschiedene Skins/Avatare für Agenten
"""

from typing import Dict, List


class SkinManager:
    """Manager für Agent-Skins"""
    
    def __init__(self):
        # Skin-Datenbank (ASCII-Avatare und Namen)
        self.skins = {
            # Angreifer-Skins
            "default_attacker": {
                "name": "Klassischer Angreifer",
                "display": "🔴",
                "type": "attacker",
                "description": "Der klassische aggressive Agent"
            },
            "fire_warrior": {
                "name": "Feuer-Krieger",
                "display": "🔥",
                "type": "attacker",
                "description": "Brennt vor Kampfeslust"
            },
            "lightning_bolt": {
                "name": "Blitz-Schlag",
                "display": "⚡",
                "type": "attacker",
                "description": "Schnell wie der Blitz"
            },
            "bomb_expert": {
                "name": "Bomben-Experte",
                "display": "💣",
                "type": "attacker",
                "description": "Explosiv und gefährlich"
            },
            "rocket_launcher": {
                "name": "Raketen-Werfer",
                "display": "🚀",
                "type": "attacker",
                "description": "Zielt auf die Sterne"
            },
            "skull_crusher": {
                "name": "Schädel-Brecher",
                "display": "💀",
                "type": "attacker",
                "description": "Furchteinflößend"
            },
            "alien_invader": {
                "name": "Alien-Invasor",
                "display": "👽",
                "type": "attacker",
                "description": "Aus einer anderen Welt"
            },
            "robot_destroyer": {
                "name": "Roboter-Zerstörer",
                "display": "🤖",
                "type": "attacker",
                "description": "Mechanische Präzision"
            },
            
            # Verteidiger-Skins
            "default_defender": {
                "name": "Klassischer Verteidiger",
                "display": "🔵",
                "type": "defender",
                "description": "Der klassische defensive Agent"
            },
            "shield_master": {
                "name": "Schild-Meister",
                "display": "🛡️",
                "type": "defender",
                "description": "Unzerstörbare Verteidigung"
            },
            "ice_guardian": {
                "name": "Eis-Wächter",
                "display": "❄️",
                "type": "defender",
                "description": "Kalt und unerschütterlich"
            },
            "zen_master": {
                "name": "Zen-Meister",
                "display": "🧘",
                "type": "defender",
                "description": "Innere Ruhe und Balance"
            },
            "coffee_addict": {
                "name": "Kaffee-Süchtiger",
                "display": "☕",
                "type": "defender",
                "description": "Immer wach und bereit"
            },
            "brain_power": {
                "name": "Gehirn-Kraft",
                "display": "🧠",
                "type": "defender",
                "description": "Intelligenz über Stärke"
            },
            "crystal_sage": {
                "name": "Kristall-Weiser",
                "display": "💎",
                "type": "defender",
                "description": "Hart wie Diamant"
            },
            "ninja_shadow": {
                "name": "Ninja-Schatten",
                "display": "🥷",
                "type": "defender",
                "description": "Ausweichen ist die beste Verteidigung"
            },
            
            # Spezial-Skins (für beide)
            "unicorn_magic": {
                "name": "Einhorn-Magie",
                "display": "🦄",
                "type": "special",
                "description": "Magisch und fabelhaft"
            },
            "dragon_fury": {
                "name": "Drachen-Wut",
                "display": "🐉",
                "type": "special",
                "description": "Legendäre Kraft"
            },
            "ghost_phantom": {
                "name": "Geister-Phantom",
                "display": "👻",
                "type": "special",
                "description": "Ungreifbar und mysteriös"
            },
            "pizza_power": {
                "name": "Pizza-Power",
                "display": "🍕",
                "type": "special",
                "description": "Lecker und stark"
            },
            "toilet_paper": {
                "name": "Toilettenpapier-Held",
                "display": "🧻",
                "type": "special",
                "description": "Der legendäre Tsunami-Meister"
            },
            "smoothie_warrior": {
                "name": "Smoothie-Krieger",
                "display": "🧃",
                "type": "special",
                "description": "Gesund und gefährlich"
            },
        }
        
        # Skin-Listen nach Typ
        self.attacker_skins = [k for k, v in self.skins.items() if v["type"] == "attacker"]
        self.defender_skins = [k for k, v in self.skins.items() if v["type"] == "defender"]
        self.special_skins = [k for k, v in self.skins.items() if v["type"] == "special"]
        self.all_skins = list(self.skins.keys())
    
    def get_skin_display(self, skin_id: str) -> str:
        """Gibt das Display-Zeichen für einen Skin zurück"""
        if skin_id in self.skins:
            return self.skins[skin_id]["display"]
        return "❓"
    
    def get_skin_name(self, skin_id: str) -> str:
        """Gibt den Namen eines Skins zurück"""
        if skin_id in self.skins:
            return self.skins[skin_id]["name"]
        return "Unbekannt"
    
    def get_skin_description(self, skin_id: str) -> str:
        """Gibt die Beschreibung eines Skins zurück"""
        if skin_id in self.skins:
            return self.skins[skin_id]["description"]
        return ""
    
    def get_skin_type(self, skin_id: str) -> str:
        """Gibt den Typ eines Skins zurück"""
        if skin_id in self.skins:
            return self.skins[skin_id]["type"]
        return "unknown"
    
    def get_skins_by_type(self, skin_type: str) -> List[str]:
        """Gibt alle Skins eines bestimmten Typs zurück"""
        if skin_type == "attacker":
            return self.attacker_skins + self.special_skins
        elif skin_type == "defender":
            return self.defender_skins + self.special_skins
        elif skin_type == "special":
            return self.special_skins
        else:
            return self.all_skins
    
    def get_next_skin(self, current_skin: str, skin_type: str = None) -> str:
        """Gibt den nächsten Skin in der Liste zurück"""
        if skin_type:
            skins = self.get_skins_by_type(skin_type)
        else:
            skins = self.all_skins
        
        try:
            current_index = skins.index(current_skin)
            next_index = (current_index + 1) % len(skins)
            return skins[next_index]
        except ValueError:
            return skins[0] if skins else "default_attacker"
    
    def get_previous_skin(self, current_skin: str, skin_type: str = None) -> str:
        """Gibt den vorherigen Skin in der Liste zurück"""
        if skin_type:
            skins = self.get_skins_by_type(skin_type)
        else:
            skins = self.all_skins
        
        try:
            current_index = skins.index(current_skin)
            prev_index = (current_index - 1) % len(skins)
            return skins[prev_index]
        except ValueError:
            return skins[0] if skins else "default_attacker"
    
    def get_random_skin(self, skin_type: str = None) -> str:
        """Gibt einen zufälligen Skin zurück"""
        import random
        if skin_type:
            skins = self.get_skins_by_type(skin_type)
        else:
            skins = self.all_skins
        return random.choice(skins) if skins else "default_attacker"
    
    def get_all_skins_info(self) -> Dict:
        """Gibt alle Skin-Informationen zurück"""
        return self.skins
    
    def unlock_skin(self, skin_id: str):
        """Schaltet einen Skin frei (für zukünftige Unlock-Mechanik)"""
        # Placeholder für zukünftige Unlock-Mechanik
        # z.B. nach Erreichen bestimmter Levels oder Achievements
        pass
    
    def is_skin_unlocked(self, skin_id: str) -> bool:
        """Prüft ob ein Skin freigeschaltet ist"""
        # Aktuell sind alle Skins freigeschaltet
        # Kann später erweitert werden für Unlock-System
        return True


class SkinAnimator:
    """Animator für Skin-Animationen"""
    
    def __init__(self):
        self.animation_frames = {}
        self.current_frame = 0
        self.frame_counter = 0
        self.animation_speed = 10  # Frames pro Animation-Frame
    
    def add_animation(self, skin_id: str, frames: List[str]):
        """Fügt eine Animation für einen Skin hinzu"""
        self.animation_frames[skin_id] = frames
    
    def get_current_frame(self, skin_id: str) -> str:
        """Gibt den aktuellen Animations-Frame zurück"""
        if skin_id in self.animation_frames:
            frames = self.animation_frames[skin_id]
            return frames[self.current_frame % len(frames)]
        return "❓"
    
    def update(self):
        """Updated die Animation"""
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0
            self.current_frame += 1
    
    def reset(self):
        """Setzt die Animation zurück"""
        self.current_frame = 0
        self.frame_counter = 0


# Vordefinierte Animationen
ATTACK_ANIMATIONS = {
    "fire_warrior": ["🔥", "💥", "🔥"],
    "lightning_bolt": ["⚡", "✨", "⚡"],
    "bomb_expert": ["💣", "💥", "☁️"],
}

DEFEND_ANIMATIONS = {
    "shield_master": ["🛡️", "✨", "🛡️"],
    "ice_guardian": ["❄️", "💎", "❄️"],
    "zen_master": ["🧘", "🌟", "🧘"],
}

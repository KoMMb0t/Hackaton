"""
Multiplayer Manager
Verwaltet Spieler-Eingaben und lokalen Multiplayer
"""

from typing import Optional
from agents import Agent


class MultiplayerManager:
    """Manager für Multiplayer-Funktionalität"""
    
    def __init__(self):
        self.player1_agent: Optional[Agent] = None
        self.player2_agent: Optional[Agent] = None
        self.current_player = 1
        self.selected_action_index = None
        
        # Tastenbelegung
        self.player1_keys = {
            'action1': 'K_1',
            'action2': 'K_2',
            'action3': 'K_3',
            'action4': 'K_4',
            'action5': 'K_5',
            'action6': 'K_6',
            'action7': 'K_7',
            'action8': 'K_8',
        }
        
        self.player2_keys = {
            'action1': 'K_KP1',  # Numpad
            'action2': 'K_KP2',
            'action3': 'K_KP3',
            'action4': 'K_KP4',
            'action5': 'K_KP5',
            'action6': 'K_KP6',
            'action7': 'K_KP7',
            'action8': 'K_KP8',
        }
    
    def set_player_agent(self, agent: Agent, player_num: int):
        """Setzt den Agenten für einen Spieler"""
        if player_num == 1:
            self.player1_agent = agent
        elif player_num == 2:
            self.player2_agent = agent
    
    def get_current_agent(self) -> Optional[Agent]:
        """Gibt den aktuellen Spieler-Agenten zurück"""
        if self.current_player == 1:
            return self.player1_agent
        else:
            return self.player2_agent
    
    def switch_player(self):
        """Wechselt zum nächsten Spieler"""
        self.current_player = 2 if self.current_player == 1 else 1
        self.selected_action_index = None
    
    def select_action(self, action_index: int):
        """Wählt eine Aktion für den aktuellen Spieler"""
        agent = self.get_current_agent()
        if agent:
            available_actions = agent.get_available_actions()
            if 0 <= action_index < len(available_actions):
                self.selected_action_index = action_index
                return available_actions[action_index]
        return None
    
    def get_selected_action(self):
        """Gibt die ausgewählte Aktion zurück"""
        agent = self.get_current_agent()
        if agent and self.selected_action_index is not None:
            available_actions = agent.get_available_actions()
            if 0 <= self.selected_action_index < len(available_actions):
                return available_actions[self.selected_action_index]
        return None
    
    def is_player_turn(self, agent: Agent) -> bool:
        """Prüft ob der Agent vom aktuellen Spieler gesteuert wird"""
        if self.current_player == 1 and agent == self.player1_agent:
            return True
        elif self.current_player == 2 and agent == self.player2_agent:
            return True
        return False
    
    def reset(self):
        """Setzt den Manager zurück"""
        self.current_player = 1
        self.selected_action_index = None


class PlayerController:
    """Controller für menschliche Spieler"""
    
    def __init__(self, agent: Agent, player_num: int):
        self.agent = agent
        self.player_num = player_num
        self.is_human = True
    
    def choose_action(self, opponent: Agent):
        """Spieler wählt Aktion (wird von UI aufgerufen)"""
        # Diese Methode wird von der UI aufgerufen wenn der Spieler eine Taste drückt
        # Die eigentliche Auswahl passiert über die UI
        return None
    
    def get_available_actions(self):
        """Gibt verfügbare Aktionen zurück"""
        return self.agent.get_available_actions()


class AIController:
    """Controller für KI-Agenten"""
    
    def __init__(self, agent: Agent):
        self.agent = agent
        self.is_human = False
    
    def choose_action(self, opponent: Agent):
        """KI wählt Aktion automatisch"""
        return self.agent.choose_action(opponent)
    
    def get_available_actions(self):
        """Gibt verfügbare Aktionen zurück"""
        return self.agent.get_available_actions()


class GameMode:
    """Enum für Spielmodi"""
    AI_VS_AI = "AI_VS_AI"
    PLAYER_VS_AI = "PLAYER_VS_AI"
    PLAYER_VS_PLAYER = "PLAYER_VS_PLAYER"


class MultiplayerGame:
    """Verwaltet ein Multiplayer-Spiel"""
    
    def __init__(self, mode: str, agent1: Agent, agent2: Agent):
        self.mode = mode
        self.agent1 = agent1
        self.agent2 = agent2
        
        # Erstelle Controller
        if mode == GameMode.AI_VS_AI:
            self.controller1 = AIController(agent1)
            self.controller2 = AIController(agent2)
        elif mode == GameMode.PLAYER_VS_AI:
            self.controller1 = PlayerController(agent1, 1)
            self.controller2 = AIController(agent2)
        elif mode == GameMode.PLAYER_VS_PLAYER:
            self.controller1 = PlayerController(agent1, 1)
            self.controller2 = PlayerController(agent2, 2)
    
    def is_player_controlled(self, agent: Agent) -> bool:
        """Prüft ob Agent von Spieler gesteuert wird"""
        if agent == self.agent1:
            return self.controller1.is_human
        elif agent == self.agent2:
            return self.controller2.is_human
        return False
    
    def get_controller(self, agent: Agent):
        """Gibt Controller für Agenten zurück"""
        if agent == self.agent1:
            return self.controller1
        elif agent == self.agent2:
            return self.controller2
        return None
    
    def get_action_for_agent(self, agent: Agent, opponent: Agent):
        """Gibt Aktion für Agenten zurück"""
        controller = self.get_controller(agent)
        if controller:
            return controller.choose_action(opponent)
        return None

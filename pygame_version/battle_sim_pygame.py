#!/usr/bin/env python3
"""
Agent Battle Simulator - PyGame Version
Mit Grafik, Animationen, Multiplayer und Skins

Für den Cline Hackathon (8.-14. Dezember)
Steam-Ready Version
"""

import pygame
import sys
import os
from pathlib import Path
import time

# Füge Parent-Verzeichnis zum Path hinzu für Imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents import AttackerAgent, DefenderAgent
from game_engine import GameEngine
from src.pygame_ui import PyGameUI
from src.multiplayer import MultiplayerManager
from src.skins import SkinManager


class BattleSimulatorPyGame:
    """Hauptklasse für die PyGame-Version"""
    
    def __init__(self):
        pygame.init()
        
        # Fenster-Einstellungen
        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 720
        self.FPS = 60
        
        # Fenster erstellen
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Agent Battle Simulator - PyGame Edition")
        
        # Icon setzen (falls vorhanden)
        try:
            icon = pygame.image.load("assets/icon.png")
            pygame.display.set_icon(icon)
        except:
            pass
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Manager initialisieren
        self.ui = PyGameUI(self.screen, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.multiplayer = MultiplayerManager()
        self.skin_manager = SkinManager()
        
        # Spielzustand
        self.game_state = "MAIN_MENU"  # MAIN_MENU, GAME_MODE_SELECT, SKIN_SELECT, BATTLE, GAME_OVER
        self.selected_mode = None  # "AI_VS_AI", "PLAYER_VS_AI", "PLAYER_VS_PLAYER"
        
        # Agenten
        self.player1_agent = None
        self.player2_agent = None
        self.player1_skin = "default_attacker"
        self.player2_skin = "default_defender"
        
        # Skin selection state
        self.selected_player = 1  # 1 or 2 - which player's skin is being selected
        
        # Game Engine
        self.game_engine = None
        
        # Battle state
        self.battle_round = 0
        self.battle_log = []
        self.last_action_time = 0
        self.action_delay = 2.0  # Seconds between actions in AI vs AI mode
        self.battle_finished = False
        
    def run(self):
        """Hauptschleife"""
        while self.running:
            # Events verarbeiten
            self.handle_events()
            
            # Update
            self.update()
            
            # Render
            self.render()
            
            # FPS limitieren
            self.clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit()
    
    def handle_events(self):
        """Event-Handling"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # State-spezifisches Event-Handling
            if self.game_state == "MAIN_MENU":
                self.handle_main_menu_events(event)
            elif self.game_state == "GAME_MODE_SELECT":
                self.handle_mode_select_events(event)
            elif self.game_state == "SKIN_SELECT":
                self.handle_skin_select_events(event)
            elif self.game_state == "BATTLE":
                self.handle_battle_events(event)
            elif self.game_state == "GAME_OVER":
                self.handle_game_over_events(event)
    
    def handle_main_menu_events(self, event):
        """Main Menu Events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game_state = "GAME_MODE_SELECT"
            elif event.key == pygame.K_ESCAPE:
                self.running = False
    
    def handle_mode_select_events(self, event):
        """Mode Select Events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.selected_mode = "AI_VS_AI"
                self.game_state = "SKIN_SELECT"
            elif event.key == pygame.K_2:
                self.selected_mode = "PLAYER_VS_AI"
                self.game_state = "SKIN_SELECT"
            elif event.key == pygame.K_3:
                self.selected_mode = "PLAYER_VS_PLAYER"
                self.game_state = "SKIN_SELECT"
            elif event.key == pygame.K_ESCAPE:
                self.game_state = "MAIN_MENU"
    
    def handle_skin_select_events(self, event):
        """Skin Select Events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.start_battle()
            elif event.key == pygame.K_ESCAPE:
                self.game_state = "GAME_MODE_SELECT"
            # Switch between player 1 and player 2 with UP/DOWN
            elif event.key == pygame.K_UP:
                self.selected_player = 1
            elif event.key == pygame.K_DOWN:
                self.selected_player = 2
            # Skin-Auswahl mit LEFT/RIGHT
            elif event.key == pygame.K_LEFT:
                if self.selected_player == 1:
                    self.player1_skin = self.skin_manager.get_previous_skin(self.player1_skin)
                else:
                    self.player2_skin = self.skin_manager.get_previous_skin(self.player2_skin)
            elif event.key == pygame.K_RIGHT:
                if self.selected_player == 1:
                    self.player1_skin = self.skin_manager.get_next_skin(self.player1_skin)
                else:
                    self.player2_skin = self.skin_manager.get_next_skin(self.player2_skin)
    
    def handle_battle_events(self, event):
        """Battle Events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game_state = "MAIN_MENU"
                self.reset_battle()
            
            # Spieler-Aktionen (wenn Multiplayer)
            if self.selected_mode in ["PLAYER_VS_AI", "PLAYER_VS_PLAYER"]:
                if event.key == pygame.K_1:
                    self.multiplayer.select_action(0)
                elif event.key == pygame.K_2:
                    self.multiplayer.select_action(1)
                elif event.key == pygame.K_3:
                    self.multiplayer.select_action(2)
                elif event.key == pygame.K_4:
                    self.multiplayer.select_action(3)
    
    def handle_game_over_events(self, event):
        """Game Over Events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game_state = "MAIN_MENU"
                self.reset_battle()
            elif event.key == pygame.K_r:
                self.start_battle()  # Rematch
    
    def update(self):
        """Update-Logik"""
        if self.game_state == "BATTLE" and not self.battle_finished:
            # Battle-Update
            if self.game_engine and self.selected_mode == "AI_VS_AI":
                # Auto-play for AI vs AI mode
                current_time = time.time()
                if current_time - self.last_action_time >= self.action_delay:
                    self.execute_battle_round()
                    self.last_action_time = current_time
    
    def execute_battle_round(self):
        """Führt eine Kampfrunde aus"""
        if not self.player1_agent.is_alive() or not self.player2_agent.is_alive():
            self.battle_finished = True
            self.game_state = "GAME_OVER"
            return
        
        # Agent 1 wählt Aktion
        action1 = self.player1_agent.choose_action()
        
        # Agent 2 wählt Aktion
        action2 = self.player2_agent.choose_action()
        
        # Führe Aktionen aus
        if action1:
            result1 = self.game_engine.execute_action(self.player1_agent, self.player2_agent, action1)
            self.battle_log.append(f"{self.player1_agent.name}: {action1.name}")
        
        if action2 and self.player2_agent.is_alive():
            result2 = self.game_engine.execute_action(self.player2_agent, self.player1_agent, action2)
            self.battle_log.append(f"{self.player2_agent.name}: {action2.name}")
        
        # Regeneriere Stamina
        self.player1_agent.regenerate_stamina()
        self.player2_agent.regenerate_stamina()
        
        # Reduziere Cooldowns
        self.player1_agent.reduce_cooldowns()
        self.player2_agent.reduce_cooldowns()
        
        self.battle_round += 1
        
        # Keep only last 5 log entries
        if len(self.battle_log) > 10:
            self.battle_log = self.battle_log[-10:]
    
    def reset_battle(self):
        """Setzt den Battle-State zurück"""
        self.battle_round = 0
        self.battle_log = []
        self.last_action_time = 0
        self.battle_finished = False
        self.game_engine = None
    
    def render(self):
        """Rendering"""
        # Hintergrund
        self.screen.fill((20, 20, 30))
        
        # State-spezifisches Rendering
        if self.game_state == "MAIN_MENU":
            self.ui.render_main_menu()
        elif self.game_state == "GAME_MODE_SELECT":
            self.ui.render_mode_select()
        elif self.game_state == "SKIN_SELECT":
            self.ui.render_skin_select(self.player1_skin, self.player2_skin, 
                                      self.skin_manager, self.selected_player)
        elif self.game_state == "BATTLE":
            self.ui.render_battle(self.player1_agent, self.player2_agent,
                                 self.player1_skin, self.player2_skin,
                                 self.skin_manager, self.battle_log, self.battle_round)
        elif self.game_state == "GAME_OVER":
            winner = self.player1_agent if self.player1_agent.is_alive() else self.player2_agent
            self.ui.render_game_over(winner)
        
        # FPS anzeigen (Debug)
        fps_text = self.ui.small_font.render(f"FPS: {int(self.clock.get_fps())}", 
                                             True, (100, 100, 100))
        self.screen.blit(fps_text, (10, 10))
        
        pygame.display.flip()
    
    def start_battle(self):
        """Startet einen Kampf"""
        # Erstelle Agenten basierend auf Modus
        if self.selected_mode == "AI_VS_AI":
            self.player1_agent = AttackerAgent("🔴 Angreifer", level=1)
            self.player2_agent = DefenderAgent("🔵 Verteidiger", level=1)
        elif self.selected_mode == "PLAYER_VS_AI":
            self.player1_agent = AttackerAgent("🎮 Spieler", level=1)
            self.player2_agent = DefenderAgent("🤖 KI", level=1)
            self.multiplayer.set_player_agent(self.player1_agent, player_num=1)
        elif self.selected_mode == "PLAYER_VS_PLAYER":
            self.player1_agent = AttackerAgent("🎮 Spieler 1", level=1)
            self.player2_agent = DefenderAgent("🎮 Spieler 2", level=1)
            self.multiplayer.set_player_agent(self.player1_agent, player_num=1)
            self.multiplayer.set_player_agent(self.player2_agent, player_num=2)
        
        # Wende Skins an
        self.player1_agent.skin = self.player1_skin
        self.player2_agent.skin = self.player2_skin
        
        # Erstelle Game Engine
        self.game_engine = GameEngine(self.player1_agent, self.player2_agent)
        
        # Reset battle state
        self.reset_battle()
        self.last_action_time = time.time()
        
        self.game_state = "BATTLE"


def main():
    """Hauptfunktion"""
    try:
        game = BattleSimulatorPyGame()
        game.run()
    except KeyboardInterrupt:
        print("\n⚠️  Spiel wurde unterbrochen!")
        pygame.quit()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Kritischer Fehler: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()

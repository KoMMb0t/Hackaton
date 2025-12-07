"""
PyGame UI Module
Rendering für alle Screens und UI-Elemente
"""

import pygame
from typing import Optional


class PyGameUI:
    """UI-Manager für PyGame-Version"""
    
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        
        # Farben
        self.COLOR_BG = (20, 20, 30)
        self.COLOR_PRIMARY = (100, 200, 255)
        self.COLOR_SECONDARY = (255, 100, 150)
        self.COLOR_TEXT = (255, 255, 255)
        self.COLOR_TEXT_DIM = (150, 150, 150)
        self.COLOR_HP = (255, 50, 50)
        self.COLOR_STAMINA = (50, 200, 255)
        self.COLOR_XP = (255, 215, 0)
        
        # Fonts
        try:
            self.title_font = pygame.font.Font(None, 72)
            self.large_font = pygame.font.Font(None, 48)
            self.medium_font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)
        except:
            # Fallback wenn keine Fonts verfügbar
            self.title_font = pygame.font.SysFont("arial", 72)
            self.large_font = pygame.font.SysFont("arial", 48)
            self.medium_font = pygame.font.SysFont("arial", 36)
            self.small_font = pygame.font.SysFont("arial", 24)
    
    def render_main_menu(self):
        """Rendert das Hauptmenü"""
        # Titel
        title = self.title_font.render("AGENT BATTLE SIMULATOR", True, self.COLOR_PRIMARY)
        title_rect = title.get_rect(center=(self.width // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Untertitel
        subtitle = self.medium_font.render("PyGame Edition", True, self.COLOR_SECONDARY)
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 220))
        self.screen.blit(subtitle, subtitle_rect)
        
        # ASCII Art (vereinfacht)
        ascii_art = [
            "    ⚔️  VS  ⚔️",
            "  🔴      🔵",
        ]
        y = 300
        for line in ascii_art:
            text = self.large_font.render(line, True, self.COLOR_TEXT)
            text_rect = text.get_rect(center=(self.width // 2, y))
            self.screen.blit(text, text_rect)
            y += 60
        
        # Anweisungen
        instructions = [
            "Drücke SPACE um zu starten",
            "Drücke ESC zum Beenden"
        ]
        y = 500
        for instruction in instructions:
            text = self.small_font.render(instruction, True, self.COLOR_TEXT_DIM)
            text_rect = text.get_rect(center=(self.width // 2, y))
            self.screen.blit(text, text_rect)
            y += 40
        
        # Version Info
        version = self.small_font.render("v2.0 - Steam Edition", True, self.COLOR_TEXT_DIM)
        version_rect = version.get_rect(center=(self.width // 2, self.height - 30))
        self.screen.blit(version, version_rect)
    
    def render_mode_select(self):
        """Rendert die Modus-Auswahl"""
        # Titel
        title = self.large_font.render("WÄHLE SPIELMODUS", True, self.COLOR_PRIMARY)
        title_rect = title.get_rect(center=(self.width // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Modi
        modes = [
            ("1", "🤖 KI vs KI", "Zwei Agenten kämpfen automatisch"),
            ("2", "🎮 Spieler vs KI", "Du gegen die KI"),
            ("3", "👥 Spieler vs Spieler", "Lokaler Multiplayer"),
        ]
        
        y = 250
        for key, name, desc in modes:
            # Modus-Name
            mode_text = self.medium_font.render(f"[{key}] {name}", True, self.COLOR_TEXT)
            mode_rect = mode_text.get_rect(center=(self.width // 2, y))
            self.screen.blit(mode_text, mode_rect)
            
            # Beschreibung
            desc_text = self.small_font.render(desc, True, self.COLOR_TEXT_DIM)
            desc_rect = desc_text.get_rect(center=(self.width // 2, y + 30))
            self.screen.blit(desc_text, desc_rect)
            
            y += 100
        
        # Zurück
        back = self.small_font.render("ESC - Zurück", True, self.COLOR_TEXT_DIM)
        back_rect = back.get_rect(center=(self.width // 2, self.height - 50))
        self.screen.blit(back, back_rect)
    
    def render_skin_select(self, player1_skin, player2_skin, skin_manager):
        """Rendert die Skin-Auswahl"""
        # Titel
        title = self.large_font.render("WÄHLE SKINS", True, self.COLOR_PRIMARY)
        title_rect = title.get_rect(center=(self.width // 2, 80))
        self.screen.blit(title, title_rect)
        
        # Spieler 1 Skin
        p1_title = self.medium_font.render("Spieler 1", True, self.COLOR_PRIMARY)
        p1_title_rect = p1_title.get_rect(center=(self.width // 4, 200))
        self.screen.blit(p1_title, p1_title_rect)
        
        # Skin-Preview (ASCII)
        p1_skin_display = skin_manager.get_skin_display(player1_skin)
        p1_skin_text = self.title_font.render(p1_skin_display, True, self.COLOR_TEXT)
        p1_skin_rect = p1_skin_text.get_rect(center=(self.width // 4, 300))
        self.screen.blit(p1_skin_text, p1_skin_rect)
        
        # Skin-Name
        p1_name = self.small_font.render(skin_manager.get_skin_name(player1_skin), 
                                         True, self.COLOR_TEXT_DIM)
        p1_name_rect = p1_name.get_rect(center=(self.width // 4, 380))
        self.screen.blit(p1_name, p1_name_rect)
        
        # Spieler 2 Skin
        p2_title = self.medium_font.render("Spieler 2", True, self.COLOR_SECONDARY)
        p2_title_rect = p2_title.get_rect(center=(3 * self.width // 4, 200))
        self.screen.blit(p2_title, p2_title_rect)
        
        p2_skin_display = skin_manager.get_skin_display(player2_skin)
        p2_skin_text = self.title_font.render(p2_skin_display, True, self.COLOR_TEXT)
        p2_skin_rect = p2_skin_text.get_rect(center=(3 * self.width // 4, 300))
        self.screen.blit(p2_skin_text, p2_skin_rect)
        
        p2_name = self.small_font.render(skin_manager.get_skin_name(player2_skin), 
                                         True, self.COLOR_TEXT_DIM)
        p2_name_rect = p2_name.get_rect(center=(3 * self.width // 4, 380))
        self.screen.blit(p2_name, p2_name_rect)
        
        # Anweisungen
        instructions = [
            "← → Skin wechseln",
            "ENTER - Start",
            "ESC - Zurück"
        ]
        y = 500
        for instruction in instructions:
            text = self.small_font.render(instruction, True, self.COLOR_TEXT_DIM)
            text_rect = text.get_rect(center=(self.width // 2, y))
            self.screen.blit(text, text_rect)
            y += 35
    
    def render_battle(self, agent1, agent2, skin1, skin2, skin_manager):
        """Rendert den Kampf"""
        # Agenten-Avatare
        avatar1 = self.title_font.render(skin_manager.get_skin_display(skin1), 
                                         True, self.COLOR_PRIMARY)
        avatar1_rect = avatar1.get_rect(center=(self.width // 4, 200))
        self.screen.blit(avatar1, avatar1_rect)
        
        avatar2 = self.title_font.render(skin_manager.get_skin_display(skin2), 
                                         True, self.COLOR_SECONDARY)
        avatar2_rect = avatar2.get_rect(center=(3 * self.width // 4, 200))
        self.screen.blit(avatar2, avatar2_rect)
        
        # VS
        vs_text = self.large_font.render("VS", True, self.COLOR_TEXT)
        vs_rect = vs_text.get_rect(center=(self.width // 2, 200))
        self.screen.blit(vs_text, vs_rect)
        
        # Agent-Namen
        name1 = self.medium_font.render(agent1.name, True, self.COLOR_TEXT)
        name1_rect = name1.get_rect(center=(self.width // 4, 300))
        self.screen.blit(name1, name1_rect)
        
        name2 = self.medium_font.render(agent2.name, True, self.COLOR_TEXT)
        name2_rect = name2.get_rect(center=(3 * self.width // 4, 300))
        self.screen.blit(name2, name2_rect)
        
        # Stats - Agent 1
        self.render_agent_stats(agent1, self.width // 4, 350)
        
        # Stats - Agent 2
        self.render_agent_stats(agent2, 3 * self.width // 4, 350)
        
        # Kampf-Log (unten)
        log_text = self.small_font.render("Kampf läuft...", True, self.COLOR_TEXT_DIM)
        log_rect = log_text.get_rect(center=(self.width // 2, self.height - 50))
        self.screen.blit(log_text, log_rect)
    
    def render_agent_stats(self, agent, x, y):
        """Rendert Agent-Stats"""
        # HP Bar
        self.render_bar(x, y, agent.hp, agent.max_hp, self.COLOR_HP, "HP")
        
        # Stamina Bar
        self.render_bar(x, y + 40, agent.stamina, agent.max_stamina, 
                       self.COLOR_STAMINA, "Stamina")
        
        # Level & XP
        level_text = self.small_font.render(f"Level {agent.level}", True, self.COLOR_TEXT)
        level_rect = level_text.get_rect(center=(x, y + 80))
        self.screen.blit(level_text, level_rect)
        
        xp_text = self.small_font.render(f"XP: {agent.xp}/{agent.xp_to_next_level}", 
                                         True, self.COLOR_XP)
        xp_rect = xp_text.get_rect(center=(x, y + 105))
        self.screen.blit(xp_text, xp_rect)
    
    def render_bar(self, x, y, current, maximum, color, label):
        """Rendert eine Status-Bar"""
        bar_width = 200
        bar_height = 20
        
        # Hintergrund
        bg_rect = pygame.Rect(x - bar_width // 2, y, bar_width, bar_height)
        pygame.draw.rect(self.screen, (50, 50, 50), bg_rect)
        
        # Füllstand
        fill_width = int((current / maximum) * bar_width)
        fill_rect = pygame.Rect(x - bar_width // 2, y, fill_width, bar_height)
        pygame.draw.rect(self.screen, color, fill_rect)
        
        # Rahmen
        pygame.draw.rect(self.screen, self.COLOR_TEXT, bg_rect, 2)
        
        # Text
        text = self.small_font.render(f"{label}: {current}/{maximum}", 
                                      True, self.COLOR_TEXT)
        text_rect = text.get_rect(center=(x, y + bar_height // 2))
        self.screen.blit(text, text_rect)
    
    def render_game_over(self, winner):
        """Rendert Game Over Screen"""
        # Titel
        title = self.title_font.render("GAME OVER", True, self.COLOR_PRIMARY)
        title_rect = title.get_rect(center=(self.width // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Gewinner
        winner_text = self.large_font.render(f"{winner.name} GEWINNT!", 
                                             True, self.COLOR_SECONDARY)
        winner_rect = winner_text.get_rect(center=(self.width // 2, 300))
        self.screen.blit(winner_text, winner_rect)
        
        # Statistiken
        stats = [
            f"Level: {winner.level}",
            f"Schaden verursacht: {winner.total_damage_dealt}",
            f"Aktionen genutzt: {winner.actions_used}",
        ]
        y = 400
        for stat in stats:
            text = self.medium_font.render(stat, True, self.COLOR_TEXT)
            text_rect = text.get_rect(center=(self.width // 2, y))
            self.screen.blit(text, text_rect)
            y += 50
        
        # Optionen
        options = [
            "SPACE - Hauptmenü",
            "R - Rematch"
        ]
        y = 600
        for option in options:
            text = self.small_font.render(option, True, self.COLOR_TEXT_DIM)
            text_rect = text.get_rect(center=(self.width // 2, y))
            self.screen.blit(text, text_rect)
            y += 35

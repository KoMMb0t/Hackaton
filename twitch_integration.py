"""
Twitch Chat Integration Module
Ermöglicht Live-Interaktion mit Zuschauern während des Kampfes
Feature #2: "STREAM SABOTAGE"
"""

import socket
import threading
import time
import re
from typing import Dict, List, Callable, Optional
from collections import defaultdict


class TwitchChatBot:
    """Twitch-Chat-Bot für Live-Interaktion"""
    
    def __init__(self, channel: str, oauth_token: Optional[str] = None):
        """
        Args:
            channel: Twitch-Channel-Name (ohne #)
            oauth_token: OAuth-Token (optional, für anonymes Lesen nicht nötig)
        """
        self.channel = channel.lower()
        self.oauth_token = oauth_token or "oauth:justinfan12345"  # Anonymous
        self.nickname = "justinfan12345"  # Anonymous bot
        
        # IRC-Connection
        self.server = "irc.chat.twitch.tv"
        self.port = 6667
        self.socket = None
        self.connected = False
        
        # Command-Handler
        self.command_handlers: Dict[str, Callable] = {}
        self.cooldowns: Dict[str, float] = {}
        self.global_cooldown = 5.0  # Sekunden zwischen Commands
        self.last_command_time = 0
        
        # Voting-System
        self.active_vote = None
        self.vote_options = {}
        self.vote_end_time = 0
        
        # Thread
        self.running = False
        self.thread = None
    
    def connect(self) -> bool:
        """Verbindet mit Twitch-Chat"""
        try:
            self.socket = socket.socket()
            self.socket.connect((self.server, self.port))
            
            # Authentifizierung
            self.socket.send(f"PASS {self.oauth_token}\n".encode('utf-8'))
            self.socket.send(f"NICK {self.nickname}\n".encode('utf-8'))
            self.socket.send(f"JOIN #{self.channel}\n".encode('utf-8'))
            
            self.connected = True
            print(f"✅ Mit Twitch-Chat verbunden: #{self.channel}")
            return True
            
        except Exception as e:
            print(f"❌ Twitch-Verbindung fehlgeschlagen: {e}")
            return False
    
    def disconnect(self):
        """Trennt Verbindung"""
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        self.connected = False
        print("🔌 Twitch-Verbindung getrennt")
    
    def register_command(self, command: str, handler: Callable, cooldown: float = 5.0):
        """
        Registriert einen Chat-Command
        
        Args:
            command: Command-Name (ohne !)
            handler: Funktion die aufgerufen wird
            cooldown: Cooldown in Sekunden
        """
        self.command_handlers[command.lower()] = handler
        self.cooldowns[command.lower()] = cooldown
        print(f"📝 Command registriert: !{command} (Cooldown: {cooldown}s)")
    
    def start_listening(self):
        """Startet Chat-Listener in separatem Thread"""
        if not self.connected:
            print("⚠️  Nicht verbunden! Rufe erst connect() auf.")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()
        print("👂 Twitch-Chat-Listener gestartet")
    
    def _listen_loop(self):
        """Haupt-Loop für Chat-Listening"""
        buffer = ""
        
        while self.running:
            try:
                # Empfange Daten
                response = self.socket.recv(2048).decode('utf-8', errors='ignore')
                buffer += response
                
                # Verarbeite Zeilen
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    self._handle_message(line.strip())
                
                time.sleep(0.1)
                
            except Exception as e:
                if self.running:
                    print(f"⚠️  Chat-Fehler: {e}")
                break
    
    def _handle_message(self, message: str):
        """Verarbeitet eine Chat-Nachricht"""
        # PING-PONG (wichtig für Verbindung)
        if message.startswith('PING'):
            self.socket.send("PONG :tmi.twitch.tv\n".encode('utf-8'))
            return
        
        # Parse Chat-Message
        match = re.match(r':(\w+)!.*PRIVMSG #\w+ :(.+)', message)
        if not match:
            return
        
        username = match.group(1)
        text = match.group(2).strip()
        
        # Prüfe auf Command
        if text.startswith('!'):
            self._handle_command(username, text)
    
    def _handle_command(self, username: str, text: str):
        """Verarbeitet einen Command"""
        parts = text[1:].split()  # Entferne ! und splitte
        if not parts:
            return
        
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        # Prüfe ob Command existiert
        if command not in self.command_handlers:
            return
        
        # Prüfe Cooldown
        current_time = time.time()
        if current_time - self.last_command_time < self.global_cooldown:
            return  # Global Cooldown aktiv
        
        # Command ausführen
        try:
            handler = self.command_handlers[command]
            handler(username, args)
            self.last_command_time = current_time
            print(f"⚡ Command ausgeführt: !{command} von {username}")
        except Exception as e:
            print(f"❌ Command-Fehler: {e}")
    
    def start_vote(self, question: str, options: List[str], duration: int = 30):
        """
        Startet eine Abstimmung im Chat
        
        Args:
            question: Frage
            options: Liste von Optionen
            duration: Dauer in Sekunden
        """
        self.active_vote = question
        self.vote_options = {str(i+1): {'option': opt, 'votes': 0} 
                            for i, opt in enumerate(options)}
        self.vote_end_time = time.time() + duration
        
        print(f"🗳️  Abstimmung gestartet: {question}")
        print(f"   Optionen: {', '.join(options)}")
        print(f"   Dauer: {duration}s")
    
    def vote(self, username: str, choice: str):
        """Registriert eine Stimme"""
        if not self.active_vote:
            return
        
        if time.time() > self.vote_end_time:
            self.end_vote()
            return
        
        if choice in self.vote_options:
            self.vote_options[choice]['votes'] += 1
            print(f"✅ {username} voted: {self.vote_options[choice]['option']}")
    
    def end_vote(self) -> Optional[str]:
        """Beendet Abstimmung und gibt Gewinner zurück"""
        if not self.active_vote:
            return None
        
        # Finde Option mit meisten Stimmen
        winner = max(self.vote_options.items(), 
                    key=lambda x: x[1]['votes'])
        
        result = winner[1]['option']
        votes = winner[1]['votes']
        
        print(f"🏆 Abstimmung beendet: '{result}' gewinnt mit {votes} Stimmen!")
        
        self.active_vote = None
        self.vote_options = {}
        
        return result


class TwitchGameIntegration:
    """Integration von Twitch-Chat mit dem Spiel"""
    
    def __init__(self, channel: str):
        self.bot = TwitchChatBot(channel)
        self.game_callbacks = {}
        self.enabled = False
    
    def setup(self):
        """Richtet alle Game-Commands ein"""
        # Kampf-Commands
        self.bot.register_command('buff', self._handle_buff, cooldown=10.0)
        self.bot.register_command('debuff', self._handle_debuff, cooldown=10.0)
        self.bot.register_command('heal', self._handle_heal, cooldown=15.0)
        self.bot.register_command('stun', self._handle_stun, cooldown=20.0)
        
        # Spezial-Aktionen
        self.bot.register_command('toiletstorm', self._handle_toilet_storm, cooldown=30.0)
        self.bot.register_command('smoothie', self._handle_smoothie, cooldown=25.0)
        self.bot.register_command('meeting', self._handle_meeting, cooldown=30.0)
        
        # Skin-Wechsel
        self.bot.register_command('skin', self._handle_skin_change, cooldown=60.0)
        
        # Voting
        self.bot.register_command('vote', self._handle_vote, cooldown=2.0)
        
        print("✅ Twitch-Integration eingerichtet")
    
    def connect_and_start(self) -> bool:
        """Verbindet und startet Bot"""
        if self.bot.connect():
            self.bot.start_listening()
            self.enabled = True
            return True
        return False
    
    def register_callback(self, event: str, callback: Callable):
        """Registriert Callback für Game-Events"""
        self.game_callbacks[event] = callback
    
    def trigger_event(self, event: str, **kwargs):
        """Triggert ein Game-Event"""
        if event in self.game_callbacks:
            self.game_callbacks[event](**kwargs)
    
    # Command-Handler
    
    def _handle_buff(self, username: str, args: List[str]):
        """!buff [P1|P2] - Gibt Spieler einen Buff"""
        target = args[0] if args else "P1"
        self.trigger_event('buff', target=target, username=username)
    
    def _handle_debuff(self, username: str, args: List[str]):
        """!debuff [P1|P2] - Gibt Spieler einen Debuff"""
        target = args[0] if args else "P2"
        self.trigger_event('debuff', target=target, username=username)
    
    def _handle_heal(self, username: str, args: List[str]):
        """!heal [P1|P2] - Heilt Spieler"""
        target = args[0] if args else "P1"
        self.trigger_event('heal', target=target, amount=20, username=username)
    
    def _handle_stun(self, username: str, args: List[str]):
        """!stun [P1|P2] - Stunned Spieler"""
        target = args[0] if args else "P2"
        self.trigger_event('stun', target=target, duration=1, username=username)
    
    def _handle_toilet_storm(self, username: str, args: List[str]):
        """!toiletstorm - Löst Toilettenpapier-Tsunami aus"""
        self.trigger_event('special_action', action='toilet_storm', username=username)
    
    def _handle_smoothie(self, username: str, args: List[str]):
        """!smoothie - Löst Smoothie-Attacke aus"""
        self.trigger_event('special_action', action='smoothie', username=username)
    
    def _handle_meeting(self, username: str, args: List[str]):
        """!meeting - Löst Meeting-Demoralisierung aus"""
        self.trigger_event('special_action', action='meeting', username=username)
    
    def _handle_skin_change(self, username: str, args: List[str]):
        """!skin [name] - Wechselt Skin"""
        skin = args[0] if args else "random"
        self.trigger_event('skin_change', skin=skin, username=username)
    
    def _handle_vote(self, username: str, args: List[str]):
        """!vote [1-4] - Stimmt ab"""
        if args and self.bot.active_vote:
            self.bot.vote(username, args[0])
    
    def start_action_vote(self, options: List[str], duration: int = 20):
        """Startet Abstimmung über nächste Aktion"""
        self.bot.start_vote("Welche Aktion soll ausgeführt werden?", 
                           options, duration)
    
    def get_vote_result(self) -> Optional[str]:
        """Gibt Voting-Ergebnis zurück"""
        return self.bot.end_vote()
    
    def shutdown(self):
        """Beendet Bot"""
        self.bot.disconnect()
        self.enabled = False


def demo():
    """Demo der Twitch-Integration"""
    print("📺 Twitch-Integration Demo\n")
    print("⚠️  Hinweis: Für echte Nutzung Twitch-Channel angeben!\n")
    
    # Beispiel-Setup
    integration = TwitchGameIntegration("your_channel_name")
    
    # Callbacks registrieren
    def on_buff(target, username):
        print(f"🎁 {username} gibt {target} einen Buff!")
    
    def on_special_action(action, username):
        print(f"⚡ {username} löst {action} aus!")
    
    integration.register_callback('buff', on_buff)
    integration.register_callback('special_action', on_special_action)
    
    # Setup
    integration.setup()
    
    print("✅ Integration bereit!")
    print("\nVerfügbare Commands:")
    print("  !buff [P1|P2] - Gibt Buff")
    print("  !heal [P1|P2] - Heilt Spieler")
    print("  !toiletstorm - Tsunami!")
    print("  !smoothie - Smoothie-Attacke")
    print("  !vote [1-4] - Abstimmen")
    print("\nUm zu starten: integration.connect_and_start()")


if __name__ == "__main__":
    demo()

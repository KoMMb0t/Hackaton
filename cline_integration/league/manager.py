"""
Autonomous Battle League Manager
Verwaltet selbstlaufende Turniere mit Ranglisten
"""

import json
import random
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents import AttackerAgent, DefenderAgent
from game_engine import GameEngine


class LeagueManager:
    """Verwaltet die Battle League"""
    
    def __init__(self, data_dir: str = "cline_integration/data/league"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.seasons_file = self.data_dir / "seasons.json"
        self.agents_file = self.data_dir / "agents.json"
        self.battles_file = self.data_dir / "battles.json"
        
        self.seasons = self._load_json(self.seasons_file, [])
        self.agents = self._load_json(self.agents_file, {})
        self.battles = self._load_json(self.battles_file, [])
    
    def _load_json(self, filepath: Path, default):
        """Lädt JSON-Datei"""
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default
    
    def _save_json(self, filepath: Path, data):
        """Speichert JSON-Datei"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def create_season(self, season_num: int, num_agents: int) -> Dict:
        """Erstellt eine neue Season"""
        season = {
            'season': season_num,
            'start_date': datetime.now().isoformat(),
            'status': 'active',
            'agents': [],
            'standings': {}
        }
        
        # Generiere Agenten
        for i in range(num_agents):
            agent_name = self._generate_agent_name()
            agent_type = random.choice(['attacker', 'defender'])
            
            agent_data = {
                'name': agent_name,
                'type': agent_type,
                'level': 1,
                'season': season_num,
                'created_at': datetime.now().isoformat()
            }
            
            season['agents'].append(agent_name)
            season['standings'][agent_name] = {
                'wins': 0,
                'losses': 0,
                'points': 0
            }
            
            self.agents[agent_name] = agent_data
        
        self.seasons.append(season)
        self._save_all()
        
        return season
    
    def _generate_agent_name(self) -> str:
        """Generiert zufälligen Agenten-Namen"""
        prefixes = ['Mighty', 'Swift', 'Dark', 'Bright', 'Iron', 'Golden', 'Shadow', 'Thunder']
        suffixes = ['Warrior', 'Knight', 'Mage', 'Assassin', 'Guardian', 'Champion', 'Hunter', 'Master']
        
        while True:
            name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
            if name not in self.agents:
                return name
    
    def get_current_season(self) -> Optional[Dict]:
        """Gibt aktuelle Season zurück"""
        for season in reversed(self.seasons):
            if season['status'] == 'active':
                return season
        return None
    
    def get_season(self, season_num: int) -> Optional[Dict]:
        """Gibt spezifische Season zurück"""
        for season in self.seasons:
            if season['season'] == season_num:
                return season
        return None
    
    def record_battle(self, agent1_name: str, agent2_name: str, winner_name: str, rounds: int):
        """Zeichnet Kampf auf"""
        season = self.get_current_season()
        if not season:
            return
        
        battle = {
            'season': season['season'],
            'agent1': agent1_name,
            'agent2': agent2_name,
            'winner': winner_name,
            'rounds': rounds,
            'timestamp': datetime.now().isoformat()
        }
        
        self.battles.append(battle)
        
        # Update Standings
        loser_name = agent2_name if winner_name == agent1_name else agent1_name
        
        season['standings'][winner_name]['wins'] += 1
        season['standings'][winner_name]['points'] += 3
        
        season['standings'][loser_name]['losses'] += 1
        
        self._save_all()
    
    def get_standings(self, season_num: Optional[int] = None) -> List[Dict]:
        """Gibt Rangliste zurück"""
        if season_num:
            season = self.get_season(season_num)
        else:
            season = self.get_current_season()
        
        if not season:
            return []
        
        standings = []
        for agent_name, stats in season['standings'].items():
            standings.append({
                'name': agent_name,
                'wins': stats['wins'],
                'losses': stats['losses'],
                'points': stats['points'],
                'games': stats['wins'] + stats['losses']
            })
        
        # Sortiere nach Punkten
        standings.sort(key=lambda x: x['points'], reverse=True)
        
        return standings
    
    def get_champion(self, season_num: int) -> Optional[Dict]:
        """Gibt Champion einer Season zurück"""
        standings = self.get_standings(season_num)
        return standings[0] if standings else None
    
    def get_agent_stats(self, agent_name: str) -> Dict:
        """Gibt Statistiken eines Agenten zurück"""
        agent_battles = [b for b in self.battles if agent_name in [b['agent1'], b['agent2']]]
        
        wins = sum(1 for b in agent_battles if b['winner'] == agent_name)
        losses = len(agent_battles) - wins
        
        return {
            'name': agent_name,
            'total_battles': len(agent_battles),
            'wins': wins,
            'losses': losses,
            'win_rate': wins / len(agent_battles) if agent_battles else 0,
            'agent_data': self.agents.get(agent_name, {})
        }
    
    def _save_all(self):
        """Speichert alle Daten"""
        self._save_json(self.seasons_file, self.seasons)
        self._save_json(self.agents_file, self.agents)
        self._save_json(self.battles_file, self.battles)


# CLI-Funktionen

def init_season(season_num: int, num_agents: int):
    """Initialisiert neue Season"""
    print("=" * 60)
    print("🏆 LEAGUE INITIALIZATION")
    print("=" * 60)
    print()
    
    manager = LeagueManager()
    season = manager.create_season(season_num, num_agents)
    
    print(f"✅ Season {season_num} erstellt!")
    print(f"   Agenten: {num_agents}")
    print(f"   Start: {season['start_date']}")
    print()
    
    print("📋 Teilnehmer:")
    for i, agent_name in enumerate(season['agents'], 1):
        agent_data = manager.agents[agent_name]
        print(f"   {i}. {agent_name} ({agent_data['type']})")
    print()
    
    print("✅ Liga bereit!")


def show_standings(season_num: Optional[int] = None):
    """Zeigt Rangliste"""
    manager = LeagueManager()
    
    if season_num:
        season = manager.get_season(season_num)
        title = f"Season {season_num}"
    else:
        season = manager.get_current_season()
        title = "Aktuelle Season"
    
    if not season:
        print("❌ Keine Season gefunden!")
        return
    
    print("=" * 60)
    print(f"📊 RANGLISTE - {title}")
    print("=" * 60)
    print()
    
    standings = manager.get_standings(season_num)
    
    print(f"{'Platz':<6} {'Agent':<25} {'Spiele':<8} {'Siege':<8} {'Niederlagen':<12} {'Punkte':<8}")
    print("-" * 60)
    
    for i, entry in enumerate(standings, 1):
        print(f"{i:<6} {entry['name']:<25} {entry['games']:<8} {entry['wins']:<8} {entry['losses']:<12} {entry['points']:<8}")
    
    print()


def show_champion(season_num: int):
    """Zeigt Champion"""
    manager = LeagueManager()
    champion = manager.get_champion(season_num)
    
    if not champion:
        print(f"❌ Keine Daten für Season {season_num}!")
        return
    
    print("=" * 60)
    print(f"🏆 CHAMPION - Season {season_num}")
    print("=" * 60)
    print()
    print(f"   {champion['name']}")
    print(f"   Siege: {champion['wins']}")
    print(f"   Punkte: {champion['points']}")
    print()


def show_agent_stats(agent_name: str):
    """Zeigt Agent-Statistiken"""
    manager = LeagueManager()
    stats = manager.get_agent_stats(agent_name)
    
    if stats['total_battles'] == 0:
        print(f"❌ Keine Daten für {agent_name}!")
        return
    
    print("=" * 60)
    print(f"📊 STATISTIKEN - {agent_name}")
    print("=" * 60)
    print()
    print(f"   Gesamt-Kämpfe: {stats['total_battles']}")
    print(f"   Siege: {stats['wins']}")
    print(f"   Niederlagen: {stats['losses']}")
    print(f"   Win-Rate: {stats['win_rate']*100:.1f}%")
    print()
    
    if stats['agent_data']:
        print(f"   Typ: {stats['agent_data'].get('type', 'Unknown')}")
        print(f"   Season: {stats['agent_data'].get('season', 'Unknown')}")
    print()

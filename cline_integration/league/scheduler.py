"""
League Scheduler
Plant und führt automatische tägliche Kämpfe aus
"""

import random
import sys
from pathlib import Path
from datetime import datetime
import time
import schedule

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents import AttackerAgent, DefenderAgent
from game_engine import GameEngine
from .manager import LeagueManager


def run_daily_battles(num_battles: int = 3):
    """
    Führt tägliche Liga-Kämpfe aus
    
    Args:
        num_battles: Anzahl der Kämpfe
    """
    print("=" * 60)
    print(f"⚔️  DAILY BATTLES - {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 60)
    print()
    
    manager = LeagueManager()
    season = manager.get_current_season()
    
    if not season:
        print("❌ Keine aktive Season! Nutze: league init")
        return
    
    print(f"🏆 Season {season['season']}")
    print(f"📅 {num_battles} Kämpfe geplant")
    print()
    
    # Wähle zufällige Agenten-Paare
    agent_names = season['agents']
    
    for i in range(num_battles):
        # Zufällige Auswahl
        agent1_name, agent2_name = random.sample(agent_names, 2)
        
        print(f"[Kampf {i+1}/{num_battles}] {agent1_name} vs {agent2_name}")
        
        # Erstelle Agenten
        agent1_data = manager.agents[agent1_name]
        agent2_data = manager.agents[agent2_name]
        
        agent1 = create_agent_from_data(agent1_data)
        agent2 = create_agent_from_data(agent2_data)
        
        # Kampf
        engine = GameEngine(agent1, agent2)
        winner = engine.start_battle(auto_mode=True)
        rounds = engine.round_number
        
        print(f"   → Sieger: {winner.name} (nach {rounds} Runden)")
        
        # Aufzeichnen
        manager.record_battle(agent1_name, agent2_name, winner.name, rounds)
        
        print()
        time.sleep(1)  # Kurze Pause
    
    # Zeige aktuelle Rangliste
    print("=" * 60)
    print("📊 AKTUELLE RANGLISTE")
    print("=" * 60)
    print()
    
    standings = manager.get_standings()
    for i, entry in enumerate(standings[:5], 1):  # Top 5
        print(f"   {i}. {entry['name']}: {entry['points']} Punkte ({entry['wins']}W/{entry['losses']}L)")
    
    print()
    print("✅ Daily Battles abgeschlossen!")


def create_agent_from_data(data: dict):
    """Erstellt Agent aus Daten"""
    if data['type'] == 'attacker':
        agent = AttackerAgent(name=data['name'])
    else:
        agent = DefenderAgent(name=data['name'])
    
    # Level-Up
    for _ in range(data.get('level', 1) - 1):
        agent.level_up()
    
    return agent


def schedule_daily(time_str: str, num_battles: int = 3):
    """
    Plant tägliche automatische Kämpfe
    
    Args:
        time_str: Uhrzeit im Format "HH:MM"
        num_battles: Anzahl Kämpfe pro Tag
    """
    print("=" * 60)
    print("⏰ LEAGUE SCHEDULER")
    print("=" * 60)
    print()
    print(f"📅 Tägliche Kämpfe geplant:")
    print(f"   Uhrzeit: {time_str}")
    print(f"   Kämpfe: {num_battles}")
    print()
    
    # Schedule Job
    schedule.every().day.at(time_str).do(run_daily_battles, num_battles=num_battles)
    
    print("✅ Scheduler aktiv!")
    print("⚠️  Drücke Ctrl+C zum Beenden")
    print()
    
    # Run Loop
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n\n⚠️  Scheduler gestoppt!")


def run_battle_now(agent1_name: str, agent2_name: str):
    """Führt sofort einen Kampf zwischen zwei Agenten aus"""
    manager = LeagueManager()
    
    if agent1_name not in manager.agents or agent2_name not in manager.agents:
        print("❌ Agent nicht gefunden!")
        return
    
    print(f"⚔️  {agent1_name} vs {agent2_name}")
    print()
    
    # Erstelle Agenten
    agent1 = create_agent_from_data(manager.agents[agent1_name])
    agent2 = create_agent_from_data(manager.agents[agent2_name])
    
    # Kampf
    engine = GameEngine(agent1, agent2)
    winner = engine.start_battle(auto_mode=True)
    rounds = engine.round_number
    
    print(f"✅ Sieger: {winner.name} (nach {rounds} Runden)")
    
    # Aufzeichnen
    manager.record_battle(agent1_name, agent2_name, winner.name, rounds)


# Zusätzliche Utility-Funktionen

def simulate_season(num_rounds: int = 10):
    """Simuliert eine komplette Season"""
    manager = LeagueManager()
    season = manager.get_current_season()
    
    if not season:
        print("❌ Keine aktive Season!")
        return
    
    print("=" * 60)
    print(f"🏆 SEASON {season['season']} SIMULATION")
    print("=" * 60)
    print()
    
    agent_names = season['agents']
    total_battles = 0
    
    # Jeder gegen jeden
    for i in range(len(agent_names)):
        for j in range(i + 1, len(agent_names)):
            for round_num in range(num_rounds):
                agent1_name = agent_names[i]
                agent2_name = agent_names[j]
                
                agent1 = create_agent_from_data(manager.agents[agent1_name])
                agent2 = create_agent_from_data(manager.agents[agent2_name])
                
                engine = GameEngine(agent1, agent2)
                winner = engine.start_battle(auto_mode=True)
                rounds = engine.round_number
                
                manager.record_battle(agent1_name, agent2_name, winner.name, rounds)
                total_battles += 1
                
                if total_battles % 10 == 0:
                    print(f"   {total_battles} Kämpfe simuliert...")
    
    print()
    print(f"✅ {total_battles} Kämpfe abgeschlossen!")
    print()
    
    # Finale Rangliste
    print("🏆 FINALE RANGLISTE:")
    print()
    standings = manager.get_standings()
    for i, entry in enumerate(standings, 1):
        print(f"   {i}. {entry['name']}: {entry['points']} Punkte ({entry['wins']}W/{entry['losses']}L)")
    
    print()
    print(f"🎉 Champion: {standings[0]['name']}!")

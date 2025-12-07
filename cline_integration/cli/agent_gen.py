"""
Agent Generator Module
Generiert neue Agenten mit verschiedenen Konfigurationen
"""

import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents import AttackerAgent, DefenderAgent
from save_system import SaveSystem


def create_agent(agent_type: str, level: int, skin: str, name: str):
    """
    Erstellt einen neuen Agenten
    
    Args:
        agent_type: 'attacker' oder 'defender'
        level: Start-Level
        skin: Skin-ID (optional)
        name: Agent-Name (optional)
    """
    print("=" * 60)
    print("🤖 AGENT-GENERATOR")
    print("=" * 60)
    print()
    
    # Erstelle Agent
    if agent_type == 'attacker':
        agent = AttackerAgent(name=name or "Neuer Angreifer")
        emoji = "🔴"
    else:
        agent = DefenderAgent(name=name or "Neuer Verteidiger")
        emoji = "🔵"
    
    # Level-Up
    for _ in range(level - 1):
        agent.level_up()
    
    # Skin setzen (wenn vorhanden)
    if skin:
        agent.skin = skin
    
    # Zeige Agent-Info
    print(f"{emoji} Agent erstellt:")
    print(f"   Name: {agent.name}")
    print(f"   Typ: {agent_type.capitalize()}")
    print(f"   Level: {agent.level}")
    print(f"   HP: {agent.max_hp}")
    print(f"   Stamina: {agent.max_stamina}")
    print(f"   Attack Bonus: +{agent.attack_bonus}")
    print(f"   Defense Bonus: +{agent.defense_bonus}")
    if skin:
        print(f"   Skin: {skin}")
    print()
    
    # Speichern?
    save_prompt = input("💾 Agent speichern? (j/n): ")
    if save_prompt.lower() == 'j':
        save_agent(agent)
    
    # Export als JSON
    export_agent_json(agent, agent_type)
    
    print("\n✅ Agent-Generierung abgeschlossen!")


def save_agent(agent):
    """Speichert Agent mit SaveSystem"""
    saver = SaveSystem()
    filename = f"{agent.name.replace(' ', '_').lower()}.json"
    saver.save_agent(agent, filename)
    print(f"✅ Agent gespeichert: {filename}")


def export_agent_json(agent, agent_type: str):
    """Exportiert Agent-Daten als JSON"""
    output_dir = Path("cline_integration/data/agents")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{agent.name.replace(' ', '_').lower()}_{timestamp}.json"
    filepath = output_dir / filename
    
    data = {
        'name': agent.name,
        'type': agent_type,
        'level': agent.level,
        'hp': agent.hp,
        'max_hp': agent.max_hp,
        'stamina': agent.stamina,
        'max_stamina': agent.max_stamina,
        'xp': agent.xp,
        'attack_bonus': agent.attack_bonus,
        'defense_bonus': agent.defense_bonus,
        'skin': getattr(agent, 'skin', None),
        'created_at': datetime.now().isoformat()
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Agent-Daten exportiert: {filepath}")

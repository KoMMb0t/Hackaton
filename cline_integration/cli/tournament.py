"""
Tournament Simulation Module
Simuliert Turniere mit mehreren Agenten
"""

import json
import random
from datetime import datetime
from pathlib import Path
import sys

# Import aus Parent-Dir
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents import AttackerAgent, DefenderAgent
from game_engine import GameEngine
# from actions import ACTIONS  # Not needed


def run_tournament(num_agents: int, num_rounds: int, chaos_mode: bool, export_format: str):
    """
    Führt ein Turnier durch
    
    Args:
        num_agents: Anzahl der Agenten
        num_rounds: Anzahl der Runden
        chaos_mode: Chaos-Modus aktiviert
        export_format: Export-Format (json, pdf, both)
    """
    print("=" * 60)
    print("🏆 TURNIER-SIMULATION")
    print("=" * 60)
    print(f"\n⚙️  Konfiguration:")
    print(f"   Agenten: {num_agents}")
    print(f"   Runden: {num_rounds}")
    print(f"   Chaos-Modus: {'✅ AKTIV' if chaos_mode else '❌ Inaktiv'}")
    print(f"   Export: {export_format}")
    print()
    
    # Generiere Agenten
    agents = generate_agents(num_agents)
    
    print(f"✅ {len(agents)} Agenten generiert:\n")
    for i, agent in enumerate(agents, 1):
        print(f"   {i}. {agent.name} (Level {agent.level})")
    print()
    
    # Führe Kämpfe durch
    results = []
    battle_num = 1
    
    for i in range(len(agents)):
        for j in range(i + 1, len(agents)):
            agent1 = agents[i]
            agent2 = agents[j]
            
            print(f"[Runde {battle_num}] {agent1.name} vs {agent2.name}")
            
            # Kampf
            engine = GameEngine(agent1, agent2)
            winner = engine.start_battle(auto_mode=True)
            rounds_fought = engine.round_number
            
            print(f"   → Sieger: {winner.name} (nach {rounds_fought} Runden)")
            print()
            
            # Speichere Ergebnis
            results.append({
                'battle_num': battle_num,
                'agent1': agent1.name,
                'agent2': agent2.name,
                'winner': winner.name,
                'rounds': rounds_fought,
                'chaos_mode': chaos_mode
            })
            
            battle_num += 1
    
    # Berechne Gesamtsieger
    winner_counts = {}
    for result in results:
        winner = result['winner']
        winner_counts[winner] = winner_counts.get(winner, 0) + 1
    
    champion = max(winner_counts.items(), key=lambda x: x[1])
    
    print("=" * 60)
    print(f"🏆 CHAMPION: {champion[0]}")
    print(f"   Siege: {champion[1]}/{len(results)}")
    print("=" * 60)
    print()
    
    # Rangliste
    print("📊 RANGLISTE:")
    sorted_winners = sorted(winner_counts.items(), key=lambda x: x[1], reverse=True)
    for i, (name, wins) in enumerate(sorted_winners, 1):
        print(f"   {i}. {name}: {wins} Siege")
    print()
    
    # Export
    tournament_data = {
        'timestamp': datetime.now().isoformat(),
        'config': {
            'num_agents': num_agents,
            'num_rounds': num_rounds,
            'chaos_mode': chaos_mode
        },
        'agents': [{'name': a.name, 'level': a.level} for a in agents],
        'results': results,
        'champion': {
            'name': champion[0],
            'wins': champion[1]
        },
        'rankings': [{'name': name, 'wins': wins} for name, wins in sorted_winners]
    }
    
    if export_format in ['json', 'both']:
        export_json(tournament_data)
    
    if export_format in ['pdf', 'both']:
        export_pdf(tournament_data)
    
    print("✅ Turnier abgeschlossen!")


def generate_agents(num: int) -> list:
    """Generiert zufällige Agenten"""
    agents = []
    
    for i in range(num):
        # Zufällig Angreifer oder Verteidiger
        if random.random() < 0.5:
            agent = AttackerAgent(name=f"Agent-{i+1}")
        else:
            agent = DefenderAgent(name=f"Agent-{i+1}")
        
        # Zufälliges Level (1-5)
        for _ in range(random.randint(0, 4)):
            agent.level_up()
        
        agents.append(agent)
    
    return agents


def export_json(data: dict):
    """Exportiert als JSON"""
    output_dir = Path("cline_integration/reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tournament_{timestamp}.json"
    filepath = output_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"📄 JSON exportiert: {filepath}")


def export_pdf(data: dict):
    """Exportiert als PDF"""
    try:
        from fpdf import FPDF
    except ImportError:
        print("⚠️  fpdf2 nicht installiert. Nutze: pip install fpdf2")
        return
    
    output_dir = Path("cline_integration/reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tournament_{timestamp}.pdf"
    filepath = output_dir / filename
    
    pdf = FPDF()
    pdf.add_page()
    
    # Titel
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, '🏆 TURNIER-BERICHT', 0, 1, 'C')
    pdf.ln(5)
    
    # Config
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Konfiguration:', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 6, f"Agenten: {data['config']['num_agents']}", 0, 1)
    pdf.cell(0, 6, f"Runden: {data['config']['num_rounds']}", 0, 1)
    pdf.cell(0, 6, f"Chaos-Modus: {'Ja' if data['config']['chaos_mode'] else 'Nein'}", 0, 1)
    pdf.ln(5)
    
    # Champion
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Champion:', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 6, f"{data['champion']['name']} ({data['champion']['wins']} Siege)", 0, 1)
    pdf.ln(5)
    
    # Rangliste
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Rangliste:', 0, 1)
    pdf.set_font('Arial', '', 11)
    for i, ranking in enumerate(data['rankings'], 1):
        pdf.cell(0, 6, f"{i}. {ranking['name']}: {ranking['wins']} Siege", 0, 1)
    
    pdf.output(str(filepath))
    print(f"📄 PDF exportiert: {filepath}")

"""
Battle Analyzer Module
Analysiert Kampf-Ergebnisse aus JSON-Logs
"""

import json
from pathlib import Path
from datetime import datetime


def analyze_battle(input_file: str, export_format: str):
    """
    Analysiert Kampf-Ergebnisse
    
    Args:
        input_file: Pfad zur Battle-Log JSON
        export_format: 'console', 'pdf', oder 'both'
    """
    print("=" * 60)
    print("📊 KAMPF-ANALYSE")
    print("=" * 60)
    print()
    
    # Lade Daten
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Datei nicht gefunden: {input_file}")
        return
    except json.JSONDecodeError:
        print(f"❌ Ungültige JSON-Datei: {input_file}")
        return
    
    # Analysiere
    analysis = perform_analysis(data)
    
    # Ausgabe
    if export_format in ['console', 'both']:
        print_analysis(analysis)
    
    if export_format in ['pdf', 'both']:
        export_analysis_pdf(analysis)
    
    print("\n✅ Analyse abgeschlossen!")


def perform_analysis(data: dict) -> dict:
    """Führt Analyse durch"""
    
    # Basis-Infos
    if 'results' in data:  # Tournament
        total_battles = len(data['results'])
        agents = set()
        for result in data['results']:
            agents.add(result['agent1'])
            agents.add(result['agent2'])
        
        # Statistiken pro Agent
        agent_stats = {}
        for agent in agents:
            wins = sum(1 for r in data['results'] if r['winner'] == agent)
            battles = sum(1 for r in data['results'] 
                         if r['agent1'] == agent or r['agent2'] == agent)
            agent_stats[agent] = {
                'battles': battles,
                'wins': wins,
                'losses': battles - wins,
                'win_rate': wins / battles if battles > 0 else 0
            }
        
        return {
            'type': 'tournament',
            'total_battles': total_battles,
            'total_agents': len(agents),
            'champion': data.get('champion', {}),
            'agent_stats': agent_stats,
            'chaos_mode': data.get('config', {}).get('chaos_mode', False)
        }
    
    else:  # Single Battle
        return {
            'type': 'single_battle',
            'winner': data.get('winner', 'Unknown'),
            'rounds': data.get('rounds', 0),
            'chaos_mode': data.get('chaos_mode', False)
        }


def print_analysis(analysis: dict):
    """Gibt Analyse in Console aus"""
    
    if analysis['type'] == 'tournament':
        print(f"📊 Turnier-Analyse")
        print(f"   Gesamt-Kämpfe: {analysis['total_battles']}")
        print(f"   Teilnehmer: {analysis['total_agents']}")
        print(f"   Chaos-Modus: {'✅' if analysis['chaos_mode'] else '❌'}")
        print()
        
        if 'champion' in analysis and analysis['champion']:
            print(f"🏆 Champion: {analysis['champion'].get('name', 'Unknown')}")
            print(f"   Siege: {analysis['champion'].get('wins', 0)}")
            print()
        
        print("📈 Agenten-Statistiken:")
        print()
        
        # Sortiere nach Win-Rate
        sorted_agents = sorted(
            analysis['agent_stats'].items(),
            key=lambda x: x[1]['win_rate'],
            reverse=True
        )
        
        for agent, stats in sorted_agents:
            win_rate = stats['win_rate'] * 100
            print(f"   {agent}:")
            print(f"      Kämpfe: {stats['battles']}")
            print(f"      Siege: {stats['wins']}")
            print(f"      Niederlagen: {stats['losses']}")
            print(f"      Win-Rate: {win_rate:.1f}%")
            print()
    
    else:  # Single Battle
        print(f"📊 Kampf-Analyse")
        print(f"   Sieger: {analysis['winner']}")
        print(f"   Runden: {analysis['rounds']}")
        print(f"   Chaos-Modus: {'✅' if analysis['chaos_mode'] else '❌'}")


def export_analysis_pdf(analysis: dict):
    """Exportiert Analyse als PDF"""
    try:
        from fpdf import FPDF
    except ImportError:
        print("⚠️  fpdf2 nicht installiert. Nutze: pip install fpdf2")
        return
    
    output_dir = Path("cline_integration/reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"analysis_{timestamp}.pdf"
    filepath = output_dir / filename
    
    pdf = FPDF()
    pdf.add_page()
    
    # Titel
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, '📊 KAMPF-ANALYSE', 0, 1, 'C')
    pdf.ln(5)
    
    if analysis['type'] == 'tournament':
        # Tournament-Analyse
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Turnier-Übersicht:', 0, 1)
        pdf.set_font('Arial', '', 11)
        pdf.cell(0, 6, f"Gesamt-Kämpfe: {analysis['total_battles']}", 0, 1)
        pdf.cell(0, 6, f"Teilnehmer: {analysis['total_agents']}", 0, 1)
        pdf.cell(0, 6, f"Chaos-Modus: {'Ja' if analysis['chaos_mode'] else 'Nein'}", 0, 1)
        pdf.ln(5)
        
        # Champion
        if 'champion' in analysis and analysis['champion']:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, 'Champion:', 0, 1)
            pdf.set_font('Arial', '', 11)
            pdf.cell(0, 6, f"{analysis['champion'].get('name', 'Unknown')} ({analysis['champion'].get('wins', 0)} Siege)", 0, 1)
            pdf.ln(5)
        
        # Statistiken
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Agenten-Statistiken:', 0, 1)
        pdf.set_font('Arial', '', 10)
        
        sorted_agents = sorted(
            analysis['agent_stats'].items(),
            key=lambda x: x[1]['win_rate'],
            reverse=True
        )
        
        for agent, stats in sorted_agents:
            win_rate = stats['win_rate'] * 100
            pdf.cell(0, 5, f"{agent}: {stats['wins']}W/{stats['losses']}L ({win_rate:.1f}%)", 0, 1)
    
    else:
        # Single Battle
        pdf.set_font('Arial', '', 11)
        pdf.cell(0, 6, f"Sieger: {analysis['winner']}", 0, 1)
        pdf.cell(0, 6, f"Runden: {analysis['rounds']}", 0, 1)
        pdf.cell(0, 6, f"Chaos-Modus: {'Ja' if analysis['chaos_mode'] else 'Nein'}", 0, 1)
    
    pdf.output(str(filepath))
    print(f"📄 Analyse-PDF exportiert: {filepath}")

#!/usr/bin/env python3
"""
Agent Battle Simulator - Cline Command Center
Zentrale CLI-Schnittstelle für alle Funktionen

Usage:
    cline run simulate-tournament --agents 6 --rounds 3
    cline run generate-agent --type defender --skin "🛡️"
    cline run analyze-results --input battle_log.json
    cline run narrate-battle --log battle_log.json --mode therapy
    cline run league init --season 1
    cline run dashboard --port 8000
"""

import click
import sys
import os
from pathlib import Path

# Füge Parent-Dir zum Path hinzu
sys.path.insert(0, str(Path(__file__).parent))

from agents import AttackerAgent, DefenderAgent
from cline_integration.cli import battle_commands
from cline_integration.league import league_commands
from cline_integration.dashboard import dashboard_commands


@click.group()
@click.version_option(version='5.0.0', prog_name='Agent Battle Simulator')
def cli():
    """
    🎮 Agent Battle Simulator - Cline Command Center
    
    Ein Cline-natives Automationssystem für absurde KI-Kämpfe!
    """
    pass


# ===== BATTLE COMMANDS =====

@cli.command('simulate-tournament')
@click.option('--agents', default=4, help='Anzahl der Agenten')
@click.option('--rounds', default=3, help='Anzahl der Runden')
@click.option('--chaos-mode', is_flag=True, help='Aktiviert Chaos-Modus')
@click.option('--export', type=click.Choice(['json', 'pdf', 'both']), default='json', help='Export-Format')
def simulate_tournament(agents, rounds, chaos_mode, export):
    """Simuliert ein Turnier mit mehreren Agenten"""
    from cline_integration.cli.tournament import run_tournament
    run_tournament(agents, rounds, chaos_mode, export)


@cli.command('generate-agent')
@click.option('--type', 'agent_type', type=click.Choice(['attacker', 'defender']), required=True)
@click.option('--level', default=1, help='Start-Level')
@click.option('--skin', default=None, help='Skin-ID')
@click.option('--name', default=None, help='Agent-Name')
def generate_agent(agent_type, level, skin, name):
    """Generiert einen neuen Agenten"""
    from cline_integration.cli.agent_gen import create_agent
    create_agent(agent_type, level, skin, name)


@cli.command('analyze-results')
@click.option('--input', 'input_file', required=True, help='Battle-Log JSON')
@click.option('--export', type=click.Choice(['console', 'pdf', 'both']), default='console')
def analyze_results(input_file, export):
    """Analysiert Kampf-Ergebnisse"""
    from cline_integration.cli.analyzer import analyze_battle
    analyze_battle(input_file, export)


@cli.command('narrate-battle')
@click.option('--log', 'log_file', required=True, help='Battle-Log JSON')
@click.option('--mode', type=click.Choice(['therapy', 'commentary', 'epic']), default='therapy')
@click.option('--export-pdf', is_flag=True, help='Exportiert als PDF')
def narrate_battle(log_file, mode, export_pdf):
    """Generiert narrative Beschreibung eines Kampfes"""
    from cline_integration.cli.narrator import narrate
    narrate(log_file, mode, export_pdf)


# ===== LEAGUE COMMANDS =====

@cli.group('league')
def league():
    """Autonomous Battle League - Selbstverwaltete Turniere"""
    pass


@league.command('init')
@click.option('--season', default=1, help='Season-Nummer')
@click.option('--agents', default=8, help='Anzahl Agenten')
def league_init(season, agents):
    """Initialisiert eine neue Liga-Season"""
    from cline_integration.league.manager import init_season
    init_season(season, agents)


@league.command('standings')
@click.option('--season', default=None, help='Season (default: aktuelle)')
def league_standings(season):
    """Zeigt aktuelle Rangliste"""
    from cline_integration.league.manager import show_standings
    show_standings(season)


@league.command('champion')
@click.option('--season', required=True, type=int, help='Season-Nummer')
def league_champion(season):
    """Zeigt Champion einer Season"""
    from cline_integration.league.manager import show_champion
    show_champion(season)


@league.command('stats')
@click.option('--agent', required=True, help='Agent-Name')
def league_stats(agent):
    """Zeigt Statistiken eines Agenten"""
    from cline_integration.league.manager import show_agent_stats
    show_agent_stats(agent)


@league.command('run-daily')
@click.option('--battles', default=3, help='Anzahl Kämpfe')
def league_run_daily(battles):
    """Führt tägliche Liga-Kämpfe aus"""
    from cline_integration.league.scheduler import run_daily_battles
    run_daily_battles(battles)


@league.command('schedule')
@click.option('--time', default='16:00', help='Uhrzeit (HH:MM)')
@click.option('--battles', default=3, help='Anzahl Kämpfe pro Tag')
def league_schedule(time, battles):
    """Plant tägliche automatische Kämpfe"""
    from cline_integration.league.scheduler import schedule_daily
    schedule_daily(time, battles)


# ===== DASHBOARD COMMANDS =====

@cli.command('dashboard')
@click.option('--port', default=8000, help='Port für Dashboard')
@click.option('--host', default='0.0.0.0', help='Host-Adresse')
@click.option('--dev', is_flag=True, help='Development-Modus')
def dashboard(port, host, dev):
    """Startet Analytics Dashboard (FastAPI)"""
    from cline_integration.dashboard.server import start_dashboard
    start_dashboard(port, host, dev)


# ===== UTILITY COMMANDS =====

@cli.command('status')
def status():
    """Zeigt System-Status"""
    click.echo("=" * 60)
    click.echo("🎮 AGENT BATTLE SIMULATOR - STATUS")
    click.echo("=" * 60)
    
    # Version
    click.echo(f"\n📦 Version: 5.0.0 (Meta Edition)")
    
    # Features
    click.echo("\n✨ Features:")
    click.echo("  ✅ CLI Command Center")
    click.echo("  ✅ Autonomous Battle League")
    click.echo("  ✅ Analytics Dashboard")
    click.echo("  ✅ AI-Generated Actions")
    click.echo("  ✅ Twitch Integration")
    click.echo("  ✅ Agent Therapy")
    click.echo("  ✅ Meta-Therapist (v5.0)")
    click.echo("  ✅ EchoMancer (v5.0)")
    
    # Modules
    click.echo("\n📚 Verfügbare Commands:")
    click.echo("  • simulate-tournament")
    click.echo("  • generate-agent")
    click.echo("  • analyze-results")
    click.echo("  • narrate-battle")
    click.echo("  • league [init|standings|champion|stats|run-daily|schedule]")
    click.echo("  • dashboard")
    
    # Config
    from feature_config import FeatureConfig
    config = FeatureConfig()
    
    click.echo("\n⚙️  Feature-Status:")
    if config.is_enabled('ai_actions'):
        click.echo("  ✅ AI-Aktionen: AKTIV")
    else:
        click.echo("  ❌ AI-Aktionen: INAKTIV")
    
    if config.is_enabled('twitch_integration'):
        click.echo("  ✅ Twitch: AKTIV")
    else:
        click.echo("  ❌ Twitch: INAKTIV")
    
    if config.is_enabled('agent_therapy'):
        click.echo("  ✅ Therapie: AKTIV")
    else:
        click.echo("  ❌ Therapie: INAKTIV")
    
    # API Keys
    click.echo("\n🔑 API-Keys:")
    if os.getenv("OPENAI_API_KEY"):
        click.echo("  ✅ OpenAI API Key: Gesetzt")
    else:
        click.echo("  ❌ OpenAI API Key: Nicht gesetzt")
    
    click.echo("\n" + "=" * 60)


@cli.command('config')
@click.option('--setup', is_flag=True, help='Startet Setup-Wizard')
@click.option('--enable-all', is_flag=True, help='Aktiviert alle Features')
def config(setup, enable_all):
    """Feature-Konfiguration"""
    from feature_config import setup_wizard, quick_enable_all
    
    if setup:
        setup_wizard()
    elif enable_all:
        quick_enable_all()
    else:
        click.echo("Nutze --setup für interaktive Konfiguration")
        click.echo("Oder --enable-all um alle Features zu aktivieren")


# ===== META-THERAPIST COMMANDS (v5.0) =====

@cli.group('therapy')
def therapy():
    """Meta-Therapist - Therapie für überforderte Agenten"""
    pass


@therapy.command('monitor')
@click.option('--agent', required=True, help='Agent-Name')
def therapy_monitor(agent):
    """Zeigt Monitoring-Report für Agent"""
    from meta_therapist import AgentMonitor
    monitor = AgentMonitor()
    # Load saved state if exists
    click.echo(f"Monitoring-Report für {agent} wird geladen...")
    click.echo("Feature in Entwicklung!")


@therapy.command('intervene')
@click.option('--agent', required=True, help='Agent-Name')
def therapy_intervene(agent):
    """Startet Intervention für Agent"""
    from meta_therapist import MetaTherapist
    therapist = MetaTherapist()
    click.echo(f"Intervention für {agent} wird gestartet...")
    click.echo("Feature in Entwicklung!")


# ===== ECHOMANCER COMMANDS (v5.0) =====

@cli.group('remix')
def remix():
    """EchoMancer - Battle Poetry & Voice"""
    pass


@remix.command('battle')
@click.option('--log', 'log_file', required=True, help='Battle-Log JSON')
@click.option('--style', type=click.Choice(['haiku', 'epic', 'therapy', 'rap', 'commentary']), default='epic')
@click.option('--voice', type=click.Choice(['dramatic', 'epic', 'calm', 'hype']), default='dramatic')
@click.option('--play', is_flag=True, help='Audio direkt abspielen')
def remix_battle(log_file, style, voice, play):
    """Remixt Battle zu Poesie + Audio"""
    from echomancer import EchoMancer
    import json
    
    click.echo(f"Remixing battle from {log_file}...")
    
    # Load battle data
    try:
        with open(log_file, 'r') as f:
            battle_data = json.load(f)
    except Exception as e:
        click.echo(f"Error loading battle log: {e}", err=True)
        return
    
    # Remix
    mancer = EchoMancer()
    remix = mancer.remix_battle(
        battle_data,
        style=style,
        voice=voice,
        synthesize_audio=True,
        play_audio=play
    )
    
    mancer.print_remix(remix)


@remix.command('poem')
@click.option('--log', 'log_file', required=True, help='Battle-Log JSON')
@click.option('--style', type=click.Choice(['haiku', 'epic', 'therapy', 'rap', 'commentary']), default='epic')
def remix_poem(log_file, style):
    """Generiert nur Gedicht (ohne Audio)"""
    from echomancer import BattlePoet
    import json
    
    click.echo(f"Generating poem from {log_file}...")
    
    try:
        with open(log_file, 'r') as f:
            battle_data = json.load(f)
    except Exception as e:
        click.echo(f"Error loading battle log: {e}", err=True)
        return
    
    poet = BattlePoet()
    poem = poet.generate_poem(battle_data, style)
    poet.print_poem(poem)


# ===== LIFE COACH 404 COMMANDS (v6.0) =====

@cli.group('coach')
def coach():
    """Life Coach 404 - Ratgeber für existenziell Überforderte"""
    pass


@coach.command('ask')
@click.option('--type', 'coach_type', type=click.Choice(['job', 'relationship', 'finance']), required=True)
@click.option('--personality', type=click.Choice(['stoic', 'goth', 'meme_lord', 'kant']), default='stoic')
@click.option('--problem', required=True, help='Dein Problem/Frage')
def coach_ask(coach_type, personality, problem):
    """Frag einen Life Coach um Rat"""
    from life_coach_404 import JobCoach, RelationshipCoach, FinanceCoach, Personality
    
    # Map strings to enums
    personality_map = {
        'stoic': Personality.STOIC,
        'goth': Personality.GOTH,
        'meme_lord': Personality.MEME_LORD,
        'kant': Personality.KANT
    }
    
    pers = personality_map[personality]
    
    # Create coach
    if coach_type == 'job':
        coach_obj = JobCoach(pers)
    elif coach_type == 'relationship':
        coach_obj = RelationshipCoach(pers)
    else:
        coach_obj = FinanceCoach(pers)
    
    click.echo(f"\n🧠 {coach_type.upper()} COACH ({personality})")
    click.echo("="*60)
    
    # Get advice
    advice = coach_obj.give_advice(problem)
    
    click.echo(f"\n💬 RATSCHLAG:")
    click.echo(advice['advice'])
    
    click.echo(f"\n💡 FOLLOW-UP-FRAGEN:")
    for q in advice['follow_up_questions']:
        click.echo(f"  • {q}")
    
    click.echo("\n" + "="*60)


# ===== MAIN =====

def main():
    """Hauptfunktion"""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n\n⚠️  Abgebrochen!")
        sys.exit(0)
    except Exception as e:
        click.echo(f"\n❌ Fehler: {e}", err=True)
        if os.getenv("DEBUG"):
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

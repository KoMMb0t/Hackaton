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
@click.version_option(version='4.0.0', prog_name='Agent Battle Simulator')
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
    click.echo(f"\n📦 Version: 4.0.0 (Cline Edition)")
    
    # Features
    click.echo("\n✨ Features:")
    click.echo("  ✅ CLI Command Center")
    click.echo("  ✅ Autonomous Battle League")
    click.echo("  ✅ Analytics Dashboard")
    click.echo("  ✅ AI-Generated Actions")
    click.echo("  ✅ Twitch Integration")
    click.echo("  ✅ Agent Therapy")
    
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

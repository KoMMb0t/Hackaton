"""
CLI Commands Module
Alle CLI-Befehle für Agent Battle Simulator
"""

from . import tournament
from . import agent_gen
from . import analyzer
from . import narrator

__all__ = ['tournament', 'agent_gen', 'analyzer', 'narrator']

# Command Registry
battle_commands = {
    'simulate-tournament': tournament.run_tournament,
    'generate-agent': agent_gen.create_agent,
    'analyze-results': analyzer.analyze_battle,
    'narrate-battle': narrator.narrate
}

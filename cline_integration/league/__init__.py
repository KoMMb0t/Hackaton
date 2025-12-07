"""
Autonomous Battle League Module
Selbstverwaltete Turniere mit Ranglisten
"""

from . import manager
from . import scheduler

__all__ = ['manager', 'scheduler']

# Command Registry
league_commands = {
    'init': manager.init_season,
    'standings': manager.show_standings,
    'champion': manager.show_champion,
    'stats': manager.show_agent_stats,
    'run-daily': scheduler.run_daily_battles,
    'schedule': scheduler.schedule_daily
}

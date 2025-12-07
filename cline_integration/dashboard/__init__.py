"""
Analytics Dashboard Module
Web-Dashboard für Battle Analytics mit FastAPI
"""

from . import server

__all__ = ['server']

# Command Registry
dashboard_commands = {
    'start': server.start_dashboard
}

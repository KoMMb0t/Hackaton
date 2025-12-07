"""
Analytics Dashboard Server
FastAPI-basiertes Web-Dashboard für Battle Analytics
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# FastAPI
try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect
    from fastapi.responses import HTMLResponse, JSONResponse
    from fastapi.staticfiles import StaticFiles
    import uvicorn
except ImportError:
    print("⚠️  FastAPI nicht installiert. Nutze: pip install fastapi uvicorn websockets")
    sys.exit(1)

# Import League Manager
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from cline_integration.league.manager import LeagueManager
from cline_integration.league.scheduler import create_agent_from_data
from agents import AttackerAgent, DefenderAgent
from game_engine import GameEngine


# FastAPI App
app = FastAPI(title="Agent Battle Analytics Dashboard")

# WebSocket Connections
active_connections: List[WebSocket] = []


# ===== API ENDPOINTS =====

@app.get("/", response_class=HTMLResponse)
async def root():
    """Haupt-Dashboard-Seite"""
    html_path = Path(__file__).parent / "static" / "index.html"
    if html_path.exists():
        with open(html_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "<h1>Dashboard wird geladen...</h1>"


@app.get("/api/status")
async def get_status():
    """System-Status"""
    manager = LeagueManager()
    season = manager.get_current_season()
    
    return {
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "current_season": season['season'] if season else None,
        "active_agents": len(season['agents']) if season else 0
    }


@app.get("/api/agents/rankings")
async def get_rankings(season: Optional[int] = None):
    """Agenten-Rangliste"""
    manager = LeagueManager()
    standings = manager.get_standings(season)
    
    return {
        "season": season or (manager.get_current_season() or {}).get('season'),
        "rankings": standings
    }


@app.get("/api/agents/{agent_name}")
async def get_agent_details(agent_name: str):
    """Agent-Details"""
    manager = LeagueManager()
    stats = manager.get_agent_stats(agent_name)
    
    if stats['total_battles'] == 0:
        return JSONResponse(
            status_code=404,
            content={"error": "Agent not found"}
        )
    
    return stats


@app.get("/api/statistics/overview")
async def get_statistics():
    """Gesamt-Statistiken"""
    manager = LeagueManager()
    season = manager.get_current_season()
    
    if not season:
        return {"error": "No active season"}
    
    standings = manager.get_standings()
    
    # Berechne Statistiken
    total_battles = sum(s['games'] for s in standings)
    total_wins = sum(s['wins'] for s in standings)
    
    # Top Performer
    top_agent = standings[0] if standings else None
    
    return {
        "season": season['season'],
        "total_agents": len(season['agents']),
        "total_battles": total_battles,
        "total_wins": total_wins,
        "top_agent": top_agent['name'] if top_agent else None,
        "top_agent_wins": top_agent['wins'] if top_agent else 0
    }


@app.post("/api/battle/start")
async def start_battle(agent1_name: str, agent2_name: str):
    """Startet einen neuen Kampf"""
    manager = LeagueManager()
    
    # Prüfe ob Agenten existieren
    if agent1_name not in manager.agents or agent2_name not in manager.agents:
        return JSONResponse(
            status_code=404,
            content={"error": "Agent not found"}
        )
    
    # Erstelle Agenten
    agent1 = create_agent_from_data(manager.agents[agent1_name])
    agent2 = create_agent_from_data(manager.agents[agent2_name])
    
    # Starte Kampf
    engine = GameEngine(agent1, agent2)
    winner = engine.start_battle(auto_mode=True)
    rounds = engine.round_number
    
    # Aufzeichnen
    manager.record_battle(agent1_name, agent2_name, winner.name, rounds)
    
    # Broadcast über WebSocket
    await broadcast_battle_result({
        'agent1': agent1_name,
        'agent2': agent2_name,
        'winner': winner.name,
        'rounds': rounds,
        'timestamp': datetime.now().isoformat()
    })
    
    return {
        "success": True,
        "winner": winner.name,
        "rounds": rounds
    }


@app.get("/api/battles/recent")
async def get_recent_battles(limit: int = 10):
    """Letzte Kämpfe"""
    manager = LeagueManager()
    battles = manager.battles[-limit:]  # Letzte N
    battles.reverse()  # Neueste zuerst
    return {"battles": battles}


# ===== WEBSOCKET =====

@app.websocket("/api/battle/live")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket für Live-Updates"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Warte auf Messages (keep-alive)
            data = await websocket.receive_text()
            
            # Echo zurück
            await websocket.send_json({
                "type": "pong",
                "timestamp": datetime.now().isoformat()
            })
    
    except WebSocketDisconnect:
        active_connections.remove(websocket)


async def broadcast_battle_result(data: Dict):
    """Broadcastet Kampf-Ergebnis an alle Clients"""
    message = {
        "type": "battle_result",
        "data": data
    }
    
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except:
            pass


# ===== STARTUP =====

def start_dashboard(port: int = 8000, host: str = "0.0.0.0", dev: bool = False):
    """Startet Dashboard-Server"""
    print("=" * 60)
    print("📊 ANALYTICS DASHBOARD")
    print("=" * 60)
    print()
    print(f"🌐 Server: http://{host}:{port}")
    print(f"📡 WebSocket: ws://{host}:{port}/api/battle/live")
    print()
    print("📋 API Endpoints:")
    print(f"   GET  /api/status")
    print(f"   GET  /api/agents/rankings")
    print(f"   GET  /api/agents/{{name}}")
    print(f"   GET  /api/statistics/overview")
    print(f"   POST /api/battle/start")
    print(f"   GET  /api/battles/recent")
    print()
    print("✅ Dashboard gestartet!")
    print("⚠️  Drücke Ctrl+C zum Beenden")
    print()
    
    # Starte Server
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info" if dev else "warning"
    )


if __name__ == "__main__":
    start_dashboard(dev=True)

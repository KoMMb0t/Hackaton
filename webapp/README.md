# 🌐 Agent Battle Simulator - Web Edition

Browser-based version of the Agent Battle Simulator with modern UI and real-time gameplay.

## ✨ Features

- **21 Unique Battle Bots** - Each with unique stats, abilities, and special powers
- **8 Combat Actions** - Strategic action selection with stamina management
- **Real-time Battle UI** - Live HP/Stamina updates, buff/debuff tracking
- **Intelligent AI** - Score-based action selection for challenging gameplay
- **Complete Game Loop** - From bot selection to victory screen
- **Stamina Regeneration** - +20 stamina per round (starting round 2)
- **Buff/Debuff System** - Duration-based effects that expire automatically
- **Combat Log** - Detailed action history with damage and comments
- **Victory Screen** - Celebration screen with battle statistics

## 🚀 Quick Start

### Installation

```bash
cd webapp
pip install -r requirements.txt
```

### Run Server

```bash
python app.py
```

Then open http://localhost:3000 in your browser!

## 🎮 How to Play

1. **Select Bots** - Choose one bot for each agent
2. **Start Battle** - Click "Kampf Starten" to begin
3. **Choose Actions** - Select from 8 different combat actions
4. **Watch the Battle** - See HP, Stamina, and effects update in real-time
5. **Victory!** - First agent to reach 0 HP loses

## 🏗️ Architecture

### Backend (Flask)
- `app.py` - Main Flask application with API endpoints
- `game/` - Game logic (agents, actions, battle, bots)
- `battle_storage.py` - Battle state management

### Frontend
- `templates/index.html` - Main game UI
- `static/js/game.js` - Game controller and UI updates
- `static/css/style.css` - Styling and animations

## 🐛 Bug Fixes (Latest)

- ✅ Fixed action names showing "undefined"
- ✅ Fixed combat log not displaying
- ✅ Fixed UI not updating after actions
- ✅ Fixed stamina regeneration
- ✅ Fixed buff/debuff duration system
- ✅ Complete battle flow tested until victory

## 📝 API Endpoints

- `GET /api/bots` - Get all available bots
- `GET /api/actions` - Get all combat actions
- `POST /api/battle/start` - Start a new battle
- `POST /api/battle/turn` - Execute a battle turn

## 🎨 Tech Stack

- **Backend:** Python 3.11, Flask, Flask-CORS
- **Frontend:** Vanilla JavaScript, HTML5, CSS3
- **Storage:** In-memory (Redis-compatible interface)

## 📄 License

Same as parent project (see root LICENSE file)

## 🙏 Credits

Built during the Manus Hackathon 2024
Based on the original CLI version in the parent directory

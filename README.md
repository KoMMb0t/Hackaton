# 🎮 Agent Battle Simulator

**Ein Cline-natives Automationssystem für absurde KI-Kämpfe**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-5.0-orange.svg)](https://github.com/KoMMb0t/Hackaton/releases)

**Repository:** https://github.com/KoMMb0t/Hackaton

---

## 🚀 Quick Start

### CLI Version
```bash
# Clone & Run
git clone https://github.com/KoMMb0t/Hackaton.git
cd Hackaton
python3 agentbattle.py --help

# Turnier simulieren
python3 agentbattle.py simulate-tournament --agents 4 --rounds 3

# Life Coach fragen
python3 agentbattle.py coach ask --type job --personality goth --problem "Soll ich kündigen?"

# Dashboard starten
python3 agentbattle.py dashboard --port 8000
```

### Web Version 🌐 NEW!
```bash
cd webapp
pip install -r requirements.txt
python app.py
# Open http://localhost:3000 in browser
```

---

## 🎯 Was ist das?

**Agent Battle Simulator** ist ein vollständiges Multi-Version-Projekt das von einem einfachen CLI-Kampfspiel zu einem komplexen System mit AI-Integration, Voice-Synthesis, Therapie für überforderte Agenten und existenzieller Krisen-Beratung evolviert ist.

### 🏆 Hackathon-Kategorien

- ✅ **Best Agentic App** - Multi-Agent-System
- ✅ **Best Voice Agent** - EchoMancer
- ✅ **Most Delightfully Weird** - Therapie für KI
- ✅ **Best Solo Dev** - 48h autonom

---

## ✨ Features

### Version 1.0 - CLI Battle System
- ⚔️ Rundenbasierte Kämpfe
- 🎲 16 absurde Aktionen
- 📈 XP-System & Level-Ups
- 💾 Speichern/Laden

### Version 2.0 - PyGame Edition
- 🎮 Grafisches Interface
- 🎨 20+ Skins
- 👥 Lokaler Multiplayer
- 🖼️ ASCII-Art Avatare

### Version 3.0 - WOW Features
- 🧠 AI-Generated Actions (GPT-4)
- 📺 Twitch-Integration
- 🧘 Agent Therapy + PDF-Export

### Version 4.0 - Cline Edition
- 🎮 CLI Command Center
- 🤖 Autonomous Battle League
- 📊 Analytics Dashboard (FastAPI)

### Version 5.0 - Meta Edition ⭐
- 🧠 **Meta-Therapist** - Echtzeit-Monitoring & Interventionen
- 🎤 **EchoMancer** - Battle Poetry + Voice-Synthesis
- 🧽 **Life Coach 404** - Multi-Agent-Ratgeber (Job, Beziehung, Finanzen)

### Version 6.0 - Web Edition 🌐 NEU!
- 🌐 **Browser-Based UI** - Modern web interface with real-time updates
- 🎮 **21 Battle Bots** - Unique agents with special abilities
- ⚔️ **8 Combat Actions** - Strategic gameplay with stamina management
- 🤖 **Intelligent AI** - Score-based action selection
- 📊 **Live Battle Stats** - Real-time HP, Stamina, Buffs, Debuffs
- 🏆 **Complete Game Loop** - From bot selection to victory screen

---

## 🎭 Highlights

### Meta-Therapist 🧠
Überwacht Agenten in Echtzeit und greift ein bei:
- Action-Loops
- Stamina-Depletion
- Burnout-Symptomen

```bash
python3 agentbattle.py therapy monitor --agent "Agent Name"
```

### EchoMancer 🎤
Generiert poetische Zusammenfassungen:
- Haiku, Epic, Therapy, Rap, Commentary
- Voice-Synthesis (ElevenLabs + TTS)

```bash
python3 agentbattle.py remix poem --log battle.json --style haiku
```

### Life Coach 404 🧽
3 Coaches × 4 Persönlichkeiten = 12 Beratungs-Stile
- 💼 Job (Stoic, Goth, Meme-Lord, Kant)
- ❤️ Relationship
- 💰 Finance

```bash
python3 agentbattle.py coach ask --type job --personality goth --problem "Soll ich kündigen?"
```

---

## 📊 Projekt-Statistiken

| Metrik | Wert |
|--------|------|
| Versionen | 5 |
| Python-Module | 31 |
| Zeilen Code | ~6000 |
| Features | 50+ |
| Entwicklungszeit | ~12h |

---

## 🏗️ Architektur

```
Agent Battle Simulator
├── Core (v1-2) - CLI + PyGame
├── AI Features (v3) - GPT, Twitch, Therapy
├── Cline (v4) - CLI, League, Dashboard
└── Meta-Layer (v5) - Therapist, EchoMancer, Life Coach
```

---

## 🛠️ Tech Stack

- **Core:** Python 3.11
- **CLI:** Click
- **Web:** FastAPI
- **Game:** PyGame
- **AI:** OpenAI GPT-4
- **Voice:** ElevenLabs, System-TTS
- **Twitch:** IRC-Bot

---

## 📚 Dokumentation

- **[HACKATHON_HANDOVER.md](HACKATHON_HANDOVER.md)** - Komplette Übersicht ⭐
- [CLINE_EDITION.md](CLINE_EDITION.md) - Cline-Features
- [WOW_FEATURES.md](WOW_FEATURES.md) - AI-Features
- [DOCUMENTATION.md](DOCUMENTATION.md) - Technische Doku

---

## 🎯 Roadmap

### v6.0 - The Complete Experience
- 🕵️ MemeCIA - Battle-Pattern-Analyzer
- 🎙️ ShowerThoughtsFM - Battle-Radio
- 🪖 Bureaucrabot - Training-Mode
- ⚔️ Gladiator Mode - Voice-Commentary + Wetten

### v7.0 - Cline Daemon
- 🤖 Self-modifying Agents
- 🧬 Evolution-System
- 📊 Auto-Balancing
- 🎴 Agent Cards

---

## 📝 Lizenz

Apache License 2.0 - Copyright 2024 KoMMb0t

---

## 🙏 Credits

Made with 💻 & ☕ for the **Cline Hackathon 2024**

*"Wenn deine Agenten Therapie brauchen, haben wir ein Problem. Oder ein Feature."*

---

## 🔗 Links

- **Repository:** https://github.com/KoMMb0t/Hackaton
- **Email:** kommuniverse@gmail.com

---

**⭐ Star this repo if you like absurd AI battles!**

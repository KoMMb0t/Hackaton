# Agent Battle Simulator

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-5.0-orange.svg)](https://github.com/KoMMb0t/Hackaton/releases)
[![Tests](https://img.shields.io/badge/Tests-9%2F9%20Passed-success.svg)](TEST_REPORT.md)
[![Code](https://img.shields.io/badge/Code-6000%20LOC-informational.svg)]()
[![Hackathon](https://img.shields.io/badge/Cline-Hackathon%202024-ff69b4.svg)]()

> *"Wenn deine Agenten Therapie brauchen, haben wir ein Problem. Oder ein Feature."*

**Absurde KI-Kämpfe mit Therapie-Option** - Ein vollständiges, Cline-natives Automationssystem für Multi-Agent-Simulationen.

---

## ✨ Highlights

<table>
<tr>
<td width="33%">

### 🧠 Meta-Therapist
Echtzeit-Monitoring für überforderte Agenten
- Loop-Detection
- Burnout-Prevention
- Auto-Intervention

</td>
<td width="33%">

### 🎤 EchoMancer
Battle Poetry + Voice-Synthesis
- 5 Poetry-Styles
- Voice-Generation
- Audio-Export

</td>
<td width="33%">

### 🧽 Life Coach 404
Multi-Agent-Ratgeber
- 3 Coaches
- 4 Persönlichkeiten
- 12 Beratungs-Stile

</td>
</tr>
</table>

---

## 🚀 Quick Start

### One-Line Install & Run
```bash
git clone https://github.com/KoMMb0t/Hackaton.git && cd Hackaton && python3 agentbattle.py --help
```

### Try These Commands
```bash
# Turnier simulieren
python3 agentbattle.py simulate-tournament --agents 4 --rounds 3

# Life Coach fragen
python3 agentbattle.py coach ask --type job --personality goth --problem "Soll ich kündigen?"

# Battle Poetry
python3 agentbattle.py remix poem --log battle.json --style haiku

# Dashboard starten
python3 agentbattle.py dashboard --port 8000
```

---

## 🎮 Features

### Core Features (v1.0)
- ⚔️ **16 absurde Kampfaktionen** - Toilettenpapier-Tsunami, Meeting-Demoralisierung, Smoothie-Attacke
- 📈 **XP-System** - Level-Ups, Stat-Verbesserungen
- 🤖 **Verschiedene Agenten-Typen** - Angreifer, Verteidiger
- 💾 **Speichern/Laden** - Persistenter Fortschritt

### PyGame Edition (v2.0)
- 🎨 **Grafisches Interface** - 1280x720, ASCII-Art Avatare
- 👥 **Lokaler Multiplayer** - Mensch vs. KI, Mensch vs. Mensch
- 🎭 **20+ Skins** - Verschiedene Avatare

### AI-Integration (v3.0)
- 🧠 **AI-Generated Actions** - GPT-4 generiert dynamische Kampfaktionen
- 📺 **Twitch-Integration** - Chat-Commands, Voting, Events
- 🧘 **Agent Therapy** - Post-Battle psychologische Analyse mit PDF-Export

### Cline Edition (v4.0)
- 🎯 **CLI Command Center** - Vollständiges Click-Framework
- 🏆 **Autonomous Battle League** - Selbstverwaltete Turniere
- 📊 **Analytics Dashboard** - FastAPI + WebSocket Live-Updates

### Meta Edition (v5.0) ⭐ NEW!
- 🧠 **Meta-Therapist** - Echtzeit-Monitoring & Interventionen
- 🎤 **EchoMancer** - Battle Poetry + Voice-Synthesis
- 🧽 **Life Coach 404** - Multi-Agent-Ratgeber (Job, Beziehung, Finanzen)

---

## 📊 Statistics

| Metrik | Wert |
|--------|------|
| **Versionen** | 5 (v1.0 - v5.0) |
| **Python-Module** | 31 |
| **Zeilen Code** | ~6000 |
| **Features** | 50+ |
| **Tests** | 9/9 ✅ |
| **Dokumentation** | 10 MD-Dateien |
| **Entwicklungszeit** | ~12 Stunden |
| **Dependencies** | Minimal |

---

## 🏗️ Architecture

```
Agent Battle Simulator
├── Core Game (v1-2)
│   ├── agents.py - Agenten-Klassen
│   ├── actions.py - 16 Kampfaktionen
│   ├── game_engine.py - Kampfmechanik
│   ├── ui.py - CLI-Interface
│   └── save_system.py - Persistenz
│
├── PyGame Version (v2)
│   ├── battle_sim_pygame.py
│   ├── src/pygame_ui.py
│   ├── src/multiplayer.py
│   └── src/skins.py
│
├── AI Features (v3)
│   ├── ai_actions.py - GPT-generierte Aktionen
│   ├── twitch_integration.py - Twitch-Bot
│   └── agent_therapy.py - Therapie-System
│
├── Cline Integration (v4)
│   ├── agentbattle.py - CLI-Schnittstelle
│   ├── cline_integration/cli/ - Commands
│   ├── cline_integration/league/ - Autonomous League
│   └── cline_integration/dashboard/ - FastAPI Dashboard
│
└── Meta-Layer (v5)
    ├── meta_therapist/ - Echtzeit-Monitoring
    ├── echomancer/ - Battle Poetry
    └── life_coach_404/ - Multi-Agent-Ratgeber
```

---

## 💻 Installation

### Requirements
- Python 3.8+
- Optional: OpenAI API Key (für AI-Features)
- Optional: ElevenLabs API Key (für Voice-Synthesis)

### Install
```bash
git clone https://github.com/KoMMb0t/Hackaton.git
cd Hackaton

# Optional: Dependencies installieren
pip install click fastapi uvicorn schedule

# Optional: PyGame für grafische Version
pip install pygame

# Optional: AI-Features
pip install openai elevenlabs
```

### Run
```bash
# CLI-Version
python3 agentbattle.py --help

# PyGame-Version
cd pygame_version
python3 battle_sim_pygame.py

# Dashboard
python3 agentbattle.py dashboard --port 8000
```

---

## 📖 Documentation

- **[HACKATHON_HANDOVER.md](HACKATHON_HANDOVER.md)** - Komplette Übersicht
- **[TEST_REPORT.md](TEST_REPORT.md)** - Test-Ergebnisse
- **[CLINE_EDITION.md](CLINE_EDITION.md)** - v4.0 Features
- **[WOW_FEATURES.md](WOW_FEATURES.md)** - v3.0 Features
- **[DOCUMENTATION.md](DOCUMENTATION.md)** - Technische Doku
- **[STEAM_RELEASE_GUIDE.md](pygame_version/steam/STEAM_RELEASE_GUIDE.md)** - Steam-Release

---

## 🤝 Contributing

Wir freuen uns über Contributions!

### Wie du beitragen kannst:

1. **Fork** das Repository
2. **Create** einen Feature-Branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. **Push** zum Branch (`git push origin feature/AmazingFeature`)
5. **Open** einen Pull Request

### Contribution-Bereiche:

- 🐛 Bug-Fixes
- ✨ Neue Features
- 📝 Dokumentation
- 🎨 UI/UX-Verbesserungen
- 🧪 Tests
- 🌐 Übersetzungen

### Code-Style:

- Python: PEP 8
- Docstrings: Google-Style
- Tests: pytest
- Commits: Conventional Commits

---

## ❓ FAQ

### Benötige ich einen OpenAI API Key?

Nein! Alle Features haben Fallback-Modi ohne API.

### Funktioniert das auf Windows/Mac/Linux?

Ja! Python 3.8+ ist alles was du brauchst.

### Kann ich eigene Aktionen hinzufügen?

Ja! Siehe [DOCUMENTATION.md](DOCUMENTATION.md) für Anleitung.

### Ist das wirklich in 12 Stunden entstanden?

Ja! Siehe Git-History für Timestamps.

### Kann ich das kommerziell nutzen?

Ja! Apache 2.0 Lizenz erlaubt kommerzielle Nutzung.

---

## 🗺️ Roadmap

### v6.0 - The Complete Experience (Next)
- 🕵️ **MemeCIA** - Battle-Pattern-Analyzer
- 🎙️ **ShowerThoughtsFM** - Battle-Radio 24/7
- 🪖 **Bureaucrabot** - Training-Mode gegen Bürokratie
- ⚔️ **Gladiator Mode** - Voice-Commentary + Wetten

### v7.0 - Cline Daemon (Future)
- 🤖 Self-modifying Agents
- 🧬 Evolution-System
- 📊 Auto-Balancing
- 🎴 Agent Cards
- 🌐 Online-Multiplayer

### Steam Release (Planned Q1 2025)
- **Pricing:** $4.99
- **Platform:** Windows, Mac, Linux
- **Features:** Full game + All DLC

---

## 🏆 Hackathon

**Cline Hackathon 2024**

**Kategorien:**
- ✅ Best Agentic App
- ✅ Best Voice Agent
- ✅ Most Delightfully Weird
- ✅ Best Solo Dev

---

## 📄 License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

Copyright 2024 KoMMb0t <kommuniverse@gmail.com>

---

## 🌟 Showcase

### Featured In:
- 🏆 Cline Hackathon 2024

### Community:
- ⭐ Star on GitHub
- 🍴 Fork & Contribute
- 💬 GitHub Discussions
- 🐦 Twitter: #AgentBattleSimulator

---

## 📞 Contact

**Author:** KoMMb0t  
**Email:** kommuniverse@gmail.com  
**Repository:** https://github.com/KoMMb0t/Hackaton  

---

**Made with 💻 & ☕ for the Cline Hackathon 2024**

*"Wenn deine Agenten Therapie brauchen, haben wir ein Problem. Oder ein Feature."*

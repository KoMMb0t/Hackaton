# 🎮 Agent Battle Simulator

Ein unterhaltsames Python-basiertes Kampfspiel zwischen KI-Agenten mit absurden Aktionen, einem Erfahrungspunkte-System und verschiedenen Spielmodi.

**Jetzt mit PyGame-Version UND 3 WOW-Features! 🚀**

---

## 🌟 Versionen

### ⭐ v4.0 - Cline Edition (NEU!)
**Ein vollständiges, Cline-natives Automationssystem!**

✅ **CLI Command Center** - Click-basiertes Framework  
✅ **Autonomous Battle League** - Selbstverwaltete Turniere  
✅ **Analytics Dashboard** - FastAPI Web-Interface  

📖 **[Vollständige Dokumentation → CLINE_EDITION.md](CLINE_EDITION.md)**

```bash
# Schnellstart
python3 agentbattle.py --help
python3 agentbattle.py league init --season 1
python3 agentbattle.py dashboard --port 8000
```

### 📟 v1.0 - CLI-Version (Original)
Die klassische Terminal-Version mit ASCII-Art und Textinterface.

### 🎮 v2.0 - PyGame-Version
Grafische Version mit lokalem Multiplayer, 20+ Skins und Steam-Vorbereitung.

### 🚀 v3.0 - WOW-Features (NEU!)
Drei originelle Erweiterungen die die Hackathon-Jury umhauen:
- 🧠 **AI-Generierte Kampfaktionen** - Dynamische Aktionen mit GPT
- 📺 **Twitch-Chat-Integration** - Live-Interaktion mit Zuschauern
- 🧘 **Agenten-Therapie** - KI-Reflexionen mit PDF-Export

---

## 🎯 Features

### Kern-Features (v1.0 - alle Versionen)

- **🤖 Zwei KI-Agenten** mit unterschiedlichen Strategien
  - 🔴 Der Angreifer: Aggressiv und schadensfokussiert
  - 🔵 Der Verteidiger: Defensiv mit cleveren Kontern

- **⚔️ 16 absurde Kampfaktionen**
  - 🧻 Toilettenpapier-Tsunami
  - 🔥 Feuerball der Bürofrustration
  - 🪖 Meeting-Demoralisierung
  - 🧃 Smoothie-Attacke mit doppeltem Chia-Schaden
  - 🧲 Magnetische Feldverwirrung
  - 🧠 Gedankenlesen
  - ☕ Kaffee-Konter
  - Und viele mehr!

- **📈 Erfahrungspunkte-System**
  - Agenten sammeln XP und leveln auf
  - Stats skalieren mit Level
  - Persistenter Fortschritt

- **🎮 Mehrere Spielmodi**
  - Manueller Kampf (Schritt-für-Schritt)
  - Autopilot (Vollautomatisch)
  - Turnier-Modus (Best of 3/5/7)

- **💾 Speichersystem**
  - Speichern/Laden von Agenten
  - JSON-basierte Persistenz

### PyGame-Features (v2.0)

- **👥 Lokaler Multiplayer**
  - Spieler vs KI
  - Spieler vs Spieler
  - KI vs KI (zum Zuschauen)

- **🎭 Skins-System**
  - Über 20 verschiedene Avatare
  - Angreifer-, Verteidiger- und Spezial-Skins
  - Von 🔥 Feuer-Krieger bis 🍕 Pizza-Power

- **🏆 Steam-Integration (vorbereitet)**
  - 20 Achievements
  - Leaderboards
  - Cloud Saves

### WOW-Features (v3.0) 🚀

#### 🧠 AI-Generierte Kampfaktionen
- Dynamische Aktionen in Echtzeit mit GPT-4
- Kontext-basiert (Kampfverlauf, Stats)
- Automatisches Balancing
- Lokale Speicherung & Wiederverwendung
- Voting-System für Bewertung

#### 📺 Twitch-Chat-Integration
- Live-Interaktion mit Zuschauern
- 9 verschiedene Chat-Commands
- Cooldown-System
- Voting für kritische Entscheidungen
- Perfekt für Streamer!

#### 🧘 Agenten-Therapie
- Post-Battle KI-Reflexionen
- Übertrieben dramatisch & philosophisch
- PDF-Export (professionell formatiert)
- Text-Export
- Session-Speicherung

**Siehe [WOW_FEATURES.md](WOW_FEATURES.md) für Details!**

---

## 📋 Installation

### Voraussetzungen

- Python 3.8 oder höher

### CLI-Version (v1.0)

```bash
# Repository klonen
git clone https://github.com/KoMMb0t/Hackaton.git
cd Hackaton

# Keine Dependencies nötig!
python3 battle_sim.py
```

### PyGame-Version (v2.0)

```bash
cd Hackaton/pygame_version

# Dependencies installieren
pip install -r requirements.txt

# Spiel starten
python3 battle_sim_pygame.py
```

### WOW-Features (v3.0)

```bash
cd Hackaton

# Dependencies installieren
pip install -r requirements_v3.txt

# OpenAI API Key setzen (für AI-Features)
export OPENAI_API_KEY='your-key-here'

# Features konfigurieren
python3 feature_config.py setup

# Oder alle Features aktivieren
python3 feature_config.py enable-all
```

---

## 🎮 Nutzung

### CLI-Version

```bash
python3 battle_sim.py
```

Folge den Menü-Anweisungen:
1. Neuer Kampf (Manuell/Autopilot)
2. Turnier starten
3. Statistiken anzeigen
4. Speichern/Laden

### PyGame-Version

```bash
cd pygame_version
python3 battle_sim_pygame.py
```

Steuerung:
- **SPACE** - Menü-Navigation
- **1-3** - Modus-Auswahl
- **← →** - Skin-Auswahl
- **1-8** - Aktionen (im Kampf)

### WOW-Features

```python
# AI-Aktionen
from ai_actions import AIActionGenerator
generator = AIActionGenerator()
action = generator.generate_action(context)

# Twitch-Integration
from twitch_integration import TwitchGameIntegration
integration = TwitchGameIntegration("your_channel")
integration.connect_and_start()

# Agenten-Therapie
from agent_therapy import AgentTherapist
therapist = AgentTherapist()
session = therapist.generate_therapy_session(battle_data)
therapist.export_to_pdf(session)
```

Siehe [WOW_FEATURES.md](WOW_FEATURES.md) für vollständige Dokumentation!

---

## 🏗️ Projektstruktur

```
Hackaton/
├── 📟 CLI-Version (v1.0)
│   ├── battle_sim.py          # CLI Hauptprogramm
│   ├── agents.py              # Agenten-Klassen & KI
│   ├── actions.py             # Kampfaktionen
│   ├── game_engine.py         # Spielmechanik
│   ├── ui.py                  # CLI Interface
│   ├── save_system.py         # Persistenz
│   └── requirements.txt       # Keine Dependencies!
│
├── 🎮 PyGame-Version (v2.0)
│   └── pygame_version/
│       ├── battle_sim_pygame.py
│       ├── src/
│       │   ├── pygame_ui.py
│       │   ├── multiplayer.py
│       │   └── skins.py
│       ├── assets/
│       ├── steam/
│       └── requirements.txt
│
├── 🚀 WOW-Features (v3.0)
│   ├── ai_actions.py          # AI-Generierte Aktionen
│   ├── twitch_integration.py  # Twitch-Chat-Bot
│   ├── agent_therapy.py       # Therapie-System
│   ├── feature_config.py      # Konfiguration
│   ├── WOW_FEATURES.md        # Feature-Doku
│   └── requirements_v3.txt    # Dependencies
│
├── 📚 Dokumentation
│   ├── README.md              # Diese Datei
│   ├── DOCUMENTATION.md       # Technische Doku
│   ├── HACKATHON_SUBMISSION.md
│   ├── HANDOVER_TO_MONDAY.md
│   ├── HANDOVER_TO_MANUS_V2.md
│   └── WOW_FEATURES.md        # WOW-Features-Doku
│
└── LICENSE                    # Apache 2.0
```

---

## 🎲 Spielmechanik

### Stats
Jeder Agent hat:
- **HP (Health Points)**: Lebenspunkte
- **Stamina**: Energie für Aktionen
- **Level**: Steigt mit XP
- **XP**: Erfahrungspunkte
- **Attack/Defense Bonus**: Skaliert mit Level

### Aktionen
Jede Aktion hat:
- **Schaden**: Basis-Schadenswert
- **Stamina-Kosten**: Benötigte Energie
- **Cooldown**: Wartezeit nach Nutzung
- **Spezialeffekte**: Buffs, Debuffs, Heilung, Stun

### Level-System
- Gewinner: 100 XP + (Runden × 10)
- Verlierer: 50 XP + (Runden × 5)
- Level-Up: +20 HP, +10 Stamina, +2 Attack/Defense

---

## 🏆 Für den Cline Hackathon

Dieses Projekt wurde für den **Cline Hackathon** (8.-14. Dezember 2024) entwickelt.

### Highlights:
- ✅ Vollständig funktionsfähig (3 Versionen!)
- ✅ Exzellent dokumentiert (6 MD-Dateien)
- ✅ Modulares Design (20+ Module)
- ✅ Keine externen Dependencies (CLI-Version)
- ✅ Erweiterbar (v3.0 beweist es!)
- ✅ Unterhaltsam & einzigartig!

### Alleinstellungsmerkmale (v3.0):
1. **AI-generierte Kampfaktionen** - Niemand sonst hat das!
2. **Twitch-Chat-Kontrolle** - Live-Entertainment-Tool!
3. **Post-Battle-Therapie** - Meta-Level Humor!

---

## 🚀 Steam-Release

Die PyGame-Version ist vorbereitet für einen **Steam-Release als Joke-Game**!

Features:
- 20 Steam Achievements
- Leaderboards
- Cloud Saves
- Trading Cards (geplant)

Siehe `pygame_version/steam/STEAM_RELEASE_GUIDE.md` für Details.

---

## 📊 Projekt-Statistiken

| Metrik | v1.0 | v2.0 | v3.0 | Gesamt |
|--------|------|------|------|--------|
| **Python-Dateien** | 6 | 4 | 4 | **14** |
| **Zeilen Code** | ~1650 | ~600 | ~800 | **~3050** |
| **Klassen** | 8 | 6 | 6 | **20** |
| **Features** | 6 | 9 | 12 | **27** |
| **Skins** | - | 20+ | - | **20+** |
| **Achievements** | - | 20 | - | **20** |
| **Dependencies** | 0 | 1 | 2 | **3** |
| **Dokumentation** | 3 MD | 2 MD | 2 MD | **7 MD** |

**Gesamt-Komplexität**: Hoch  
**Code-Qualität**: Professionell  
**Dokumentation**: Exzellent  
**Spielbarkeit**: Vollständig funktional  
**WOW-Faktor**: 🔥🔥🔥🔥🔥

---

## 🔧 Entwicklung

### Neue Aktionen hinzufügen

Siehe `DOCUMENTATION.md` für Details.

### Neue Skins hinzufügen (PyGame)

```python
# In pygame_version/src/skins.py
"my_skin": {
    "name": "Mein Skin",
    "display": "🎨",
    "type": "special",
    "description": "Cool!"
}
```

### Executable erstellen

```bash
cd pygame_version
pip install pyinstaller
pyinstaller --onefile --windowed battle_sim_pygame.py
```

---

## 🐛 Bekannte Probleme

### CLI-Version (v1.0)
- Keine (soweit bekannt!)

### PyGame-Version (v2.0)
- Keine Sound-Effekte (noch nicht implementiert)
- Nur lokaler Multiplayer (kein Online)

### WOW-Features (v3.0)
- Benötigt OpenAI API Key für AI-Features
- Twitch-Integration benötigt aktiven Stream
- PDF-Export benötigt fpdf2

---

## 🚀 Roadmap

### Version 3.1 (geplant)
- [ ] TTS für Therapie-Reflexionen
- [ ] Mehr Twitch-Commands
- [ ] AI-generierte Skins
- [ ] Statistik-Dashboard

### Version 4.0 (Zukunft)
- [ ] Online-Multiplayer
- [ ] Ranked-Modus
- [ ] Discord-Integration
- [ ] Mobile Version

---

## 📝 Lizenz

Apache License 2.0 - Siehe LICENSE Datei

Copyright 2024 KoMMb0t <kommuniverse@gmail.com>

---

## 🎉 Credits

Entwickelt für den **Cline Hackathon** (8.-14. Dezember 2024)

**v1.0 & v2.0**: Cline AI  
**v3.0 WOW-Features**: Designed by Monday AI (MondayManusKIon)

Inspiriert von klassischen RPG-Kampfsystemen und modernem Game Design.

---

## 🤝 Contributing

Contributions sind willkommen! Öffne ein Issue oder Pull Request.

---

## 📞 Support

- **GitHub**: https://github.com/KoMMb0t/Hackaton
- **Email**: kommuniverse@gmail.com

---

## 🌟 Danksagungen

- Dem Cline Hackathon für die Motivation
- Der Python-Community
- OpenAI für GPT-4
- Twitch für die API
- Allen die "Toilettenpapier-Tsunami" für eine legitime Waffe halten
- Monday AI für die verrückten Feature-Ideen

---

**Viel Spaß beim Kämpfen! ⚔️🎮🚀**

*"Wo Toilettenpapier-Tsunamis auf AI-generierte Aktionen, Twitch-Chaos und existenzielle Therapie treffen!"*

# 🎮 Agent Battle Simulator

Ein unterhaltsames Python-basiertes Kampfspiel zwischen KI-Agenten mit absurden Aktionen, einem Erfahrungspunkte-System und verschiedenen Spielmodi.

**Jetzt auch mit PyGame-Version! 🚀**

## 🚀 Zwei Versionen verfügbar

### 📟 CLI-Version (Original)
Die klassische Terminal-Version mit ASCII-Art und Textinterface.

### 🎮 PyGame-Version (NEU!)
Grafische Version mit:
- 🎨 Visuelles Interface
- 👥 Lokaler Multiplayer (2 Spieler)
- 🎭 20+ verschiedene Skins
- 🏆 Steam-Ready
- ⚡ Animationen

---

## 🎯 Features

### Kern-Features (beide Versionen)

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

### Exklusiv in der PyGame-Version

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

---

## 📋 Installation

### Voraussetzungen

- Python 3.8 oder höher

### CLI-Version

```bash
# Repository klonen
git clone https://github.com/KoMMb0t/Hackaton.git
cd Hackaton

# Keine Dependencies nötig!
python3 battle_sim.py
```

### PyGame-Version

```bash
cd Hackaton/pygame_version

# Dependencies installieren
pip install -r requirements.txt

# Spiel starten
python3 battle_sim_pygame.py
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

---

## 🏗️ Projektstruktur

```
Hackaton/
├── battle_sim.py          # CLI Hauptprogramm
├── agents.py              # Agenten-Klassen & KI
├── actions.py             # Kampfaktionen
├── game_engine.py         # Spielmechanik
├── ui.py                  # CLI Interface
├── save_system.py         # Persistenz
├── requirements.txt       # Keine Dependencies!
├── README.md              # Diese Datei
├── DOCUMENTATION.md       # Technische Doku
├── HACKATHON_SUBMISSION.md
├── HANDOVER_TO_MONDAY.md
├── LICENSE                # Apache 2.0
│
└── pygame_version/        # PyGame-Version
    ├── battle_sim_pygame.py
    ├── src/
    │   ├── pygame_ui.py
    │   ├── multiplayer.py
    │   └── skins.py
    ├── assets/
    │   ├── sprites/
    │   ├── sounds/
    │   └── fonts/
    ├── steam/
    │   ├── steam_config.json
    │   ├── achievements.json
    │   └── STEAM_RELEASE_GUIDE.md
    ├── requirements.txt
    └── README_PYGAME.md
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
- ✅ Vollständig funktionsfähig
- ✅ Gut dokumentiert
- ✅ Modulares Design
- ✅ Keine externen Dependencies (CLI-Version)
- ✅ Erweiterbar
- ✅ Unterhaltsam!

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

- **~2500 Zeilen Code** (beide Versionen)
- **14 Python-Module**
- **10+ Klassen**
- **16 Kampfaktionen**
- **20+ Skins** (PyGame)
- **20 Achievements** (Steam)
- **0 Dependencies** (CLI-Version)

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

### CLI-Version
- Keine (soweit bekannt!)

### PyGame-Version
- Keine Sound-Effekte (noch nicht implementiert)
- Nur lokaler Multiplayer (kein Online)

---

## 🚀 Roadmap

### Version 2.1 (geplant)
- [ ] Sound-Effekte für PyGame
- [ ] Bessere Animationen
- [ ] Mehr Skins
- [ ] Achievements-Tracking

### Version 3.0 (Zukunft)
- [ ] Online-Multiplayer
- [ ] Ranked-Modus
- [ ] Custom Skins
- [ ] Map-Editor
- [ ] Mobile Version?

---

## 📝 Lizenz

Apache License 2.0 - Siehe LICENSE Datei

Copyright 2024 KoMMb0t <kommuniverse@gmail.com>

---

## 🎉 Credits

Entwickelt für den **Cline Hackathon** (8.-14. Dezember 2024)

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
- Allen die "Toilettenpapier-Tsunami" für eine legitime Waffe halten

---

**Viel Spaß beim Kämpfen! ⚔️🎮**

*"Wo Toilettenpapier-Tsunamis auf philosophische Selbstoptimierung treffen!"*

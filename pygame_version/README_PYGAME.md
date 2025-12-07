# 🎮 Agent Battle Simulator - PyGame Edition

Die grafische Version des Agent Battle Simulator mit PyGame, Multiplayer und Skins!

## 🚀 Features

### Neu in der PyGame-Version:

- **🎨 Grafisches Interface** - Kein CLI mehr, echte Grafik!
- **👥 Lokaler Multiplayer** - Spiele gegen deinen Freund oder dein Ego
- **🎭 20+ Skins** - Verschiedene Avatare für deine Agenten
- **🎮 Drei Spielmodi**:
  - 🤖 KI vs KI (Autopilot)
  - 🎮 Spieler vs KI
  - 👥 Spieler vs Spieler (Lokaler Multiplayer)
- **🏆 Steam-Ready** - Vorbereitet für Steam-Release
- **⚡ Animationen** - Flüssige Kampf-Animationen
- **📊 Visuelle Stats** - HP/Stamina-Bars in Echtzeit

### Alle Original-Features:

- ⚔️ 16 absurde Kampfaktionen
- 📈 XP-System mit Level-Ups
- 💾 Speichern/Laden
- 🏆 Turnier-Modus
- 🎲 Verschiedene KI-Strategien

---

## 📋 Installation

### Voraussetzungen

- Python 3.8 oder höher
- PyGame 2.5.0 oder höher

### Setup

```bash
# Repository klonen
git clone https://github.com/KoMMb0t/Hackaton.git
cd Hackaton/pygame_version

# Dependencies installieren
pip install -r requirements.txt

# Spiel starten
python battle_sim_pygame.py
```

---

## 🎮 Steuerung

### Hauptmenü
- **SPACE** - Spiel starten
- **ESC** - Beenden

### Modus-Auswahl
- **1** - KI vs KI
- **2** - Spieler vs KI
- **3** - Spieler vs Spieler
- **ESC** - Zurück

### Skin-Auswahl
- **← →** - Skin wechseln
- **ENTER** - Bestätigen
- **ESC** - Zurück

### Im Kampf (Spieler-Modus)
- **1-8** - Aktion auswählen (Spieler 1)
- **Numpad 1-8** - Aktion auswählen (Spieler 2)
- **ESC** - Zum Hauptmenü

---

## 🎭 Verfügbare Skins

### Angreifer-Skins
- 🔴 Klassischer Angreifer
- 🔥 Feuer-Krieger
- ⚡ Blitz-Schlag
- 💣 Bomben-Experte
- 🚀 Raketen-Werfer
- 💀 Schädel-Brecher
- 👽 Alien-Invasor
- 🤖 Roboter-Zerstörer

### Verteidiger-Skins
- 🔵 Klassischer Verteidiger
- 🛡️ Schild-Meister
- ❄️ Eis-Wächter
- 🧘 Zen-Meister
- ☕ Kaffee-Süchtiger
- 🧠 Gehirn-Kraft
- 💎 Kristall-Weiser
- 🥷 Ninja-Schatten

### Spezial-Skins (für beide)
- 🦄 Einhorn-Magie
- 🐉 Drachen-Wut
- 👻 Geister-Phantom
- 🍕 Pizza-Power
- 🧻 Toilettenpapier-Held
- 🧃 Smoothie-Krieger

---

## 🏗️ Projektstruktur

```
pygame_version/
├── battle_sim_pygame.py    # Hauptprogramm
├── src/
│   ├── pygame_ui.py         # UI-Rendering
│   ├── multiplayer.py       # Multiplayer-Manager
│   └── skins.py             # Skins-System
├── assets/
│   ├── sprites/             # Sprite-Grafiken
│   ├── sounds/              # Sound-Effekte
│   └── fonts/               # Schriftarten
├── steam/
│   ├── steam_config.json    # Steam-Konfiguration
│   ├── achievements.json    # Achievement-Definitionen
│   └── STEAM_RELEASE_GUIDE.md
├── requirements.txt
└── README_PYGAME.md
```

---

## 🎯 Spielmodi im Detail

### 🤖 KI vs KI
Lehne dich zurück und schaue zu wie zwei KI-Agenten gegeneinander kämpfen. Perfekt zum Entspannen oder als Screensaver!

### 🎮 Spieler vs KI
Fordere die KI heraus! Wähle deine Aktionen strategisch und besiege den Computer-Gegner.

### 👥 Spieler vs Spieler
Lokaler Multiplayer für 2 Spieler am gleichen Computer. Perfekt für Couch-Gaming mit Freunden!

**Steuerung:**
- Spieler 1: Tasten 1-8
- Spieler 2: Numpad 1-8

---

## 🏆 Steam-Release

Dieses Spiel ist vorbereitet für einen Steam-Release als **Joke-Game**!

### Geplante Steam-Features:
- ✅ Steam Achievements (20 Achievements)
- ✅ Steam Leaderboards
- ✅ Steam Cloud Saves
- ✅ Steam Overlay
- ✅ Trading Cards (geplant)

Siehe `steam/STEAM_RELEASE_GUIDE.md` für Details.

---

## 🔧 Entwicklung

### Executable erstellen

```bash
# PyInstaller installieren
pip install pyinstaller

# Windows Executable
pyinstaller --onefile --windowed \
  --name "AgentBattleSimulator" \
  --icon="assets/icon.ico" \
  --add-data "assets:assets" \
  battle_sim_pygame.py

# Ausführen
./dist/AgentBattleSimulator.exe
```

### Neue Skins hinzufügen

Öffne `src/skins.py` und füge einen neuen Eintrag hinzu:

```python
"my_new_skin": {
    "name": "Mein Neuer Skin",
    "display": "🎨",
    "type": "special",
    "description": "Eine coole Beschreibung"
}
```

### Neue Achievements hinzufügen

Öffne `steam/achievements.json` und füge ein neues Achievement hinzu.

---

## 🐛 Bekannte Probleme

- Keine Sound-Effekte (noch nicht implementiert)
- Animationen sind basic (ASCII-basiert)
- Nur lokaler Multiplayer (kein Online)

---

## 🚀 Roadmap

### Version 2.1 (geplant)
- [ ] Sound-Effekte
- [ ] Bessere Animationen
- [ ] Mehr Skins
- [ ] Achievements-Tracking
- [ ] Statistik-Export

### Version 3.0 (Zukunft)
- [ ] Online-Multiplayer
- [ ] Ranked-Modus
- [ ] Turniere
- [ ] Custom Skins
- [ ] Map-Editor

---

## 📝 Lizenz

Apache License 2.0 - Siehe ../LICENSE

Copyright 2024 KoMMb0t <kommuniverse@gmail.com>

---

## 🎉 Credits

Entwickelt für den **Cline Hackathon** (8.-14. Dezember 2024)

Basierend auf dem originalen CLI-Version des Agent Battle Simulator.

---

## 🤝 Contributing

Contributions sind willkommen! Öffne ein Issue oder Pull Request auf GitHub.

---

## 📞 Support

- GitHub: https://github.com/KoMMb0t/Hackaton
- Email: kommuniverse@gmail.com

---

**Viel Spaß beim Kämpfen! ⚔️🎮**

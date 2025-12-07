# 🎮 Steam Release Guide - Agent Battle Simulator

## Übersicht

Dieses Dokument beschreibt die Schritte für einen Steam-Release des Agent Battle Simulator.

---

## 📋 Voraussetzungen

### 1. Steam Partner Account
- [ ] Registrierung bei [Steamworks](https://partner.steamgames.com/)
- [ ] $100 Steam Direct Fee bezahlen
- [ ] Steuerinformationen hinterlegen
- [ ] Bankverbindung für Auszahlungen einrichten

### 2. Spiel-Build vorbereiten
- [ ] PyGame-Version finalisieren
- [ ] Als Executable kompilieren (PyInstaller)
- [ ] Auf verschiedenen Systemen testen
- [ ] Performance optimieren

### 3. Assets erstellen
- [ ] App-Icon (verschiedene Größen)
- [ ] Store-Banner (verschiedene Formate)
- [ ] Screenshots (mindestens 5)
- [ ] Trailer-Video (optional aber empfohlen)
- [ ] Achievement-Icons

---

## 🔧 Technische Vorbereitung

### Executable erstellen

```bash
# PyInstaller installieren
pip install pyinstaller

# Executable erstellen
pyinstaller --onefile --windowed \
  --name "AgentBattleSimulator" \
  --icon="assets/icon.ico" \
  --add-data "assets:assets" \
  battle_sim_pygame.py

# Testen
./dist/AgentBattleSimulator
```

### Steam SDK Integration

```python
# Steamworks SDK einbinden
# https://partner.steamgames.com/doc/sdk

from steamworks import STEAMWORKS

# Initialisierung
if STEAMWORKS.Init():
    print("Steam initialized successfully")
    
# Achievement freischalten
def unlock_achievement(achievement_id):
    STEAMWORKS.UserStats().SetAchievement(achievement_id)
    STEAMWORKS.UserStats().StoreStats()

# Cloud Save
def save_to_cloud(filename, data):
    STEAMWORKS.RemoteStorage().FileWrite(filename, data)

def load_from_cloud(filename):
    return STEAMWORKS.RemoteStorage().FileRead(filename)
```

---

## 📝 Store Page Setup

### Erforderliche Informationen

**Basis-Informationen**
- App-Name: Agent Battle Simulator
- Kurzbeschreibung (300 Zeichen)
- Lange Beschreibung (unbegrenzt)
- Genre: Action, Indie, Strategy, Casual
- Tags: Turn-Based, Local Multiplayer, Funny, AI

**Medien**
- Header Capsule: 460x215px
- Small Capsule: 231x87px
- Main Capsule: 616x353px
- Header: 1920x622px
- Screenshots: mindestens 1920x1080px (5-10 Stück)
- Trailer: 1920x1080, max 2 Minuten

**System-Anforderungen**
```
Minimum:
- OS: Windows 7/8/10/11
- Processor: 1 GHz
- Memory: 512 MB RAM
- Graphics: Any
- Storage: 100 MB

Empfohlen:
- OS: Windows 10/11
- Processor: 2 GHz
- Memory: 1 GB RAM
- Graphics: Any
- Storage: 200 MB
```

---

## 🏆 Steam Features Integration

### Achievements

```python
# achievements.py
class SteamAchievements:
    def __init__(self):
        self.achievements = {
            'FIRST_BLOOD': False,
            'TOILET_MASTER': False,
            'LEVEL_10': False,
            # ... siehe achievements.json
        }
    
    def check_achievement(self, achievement_id, condition):
        if condition and not self.achievements[achievement_id]:
            self.unlock(achievement_id)
    
    def unlock(self, achievement_id):
        self.achievements[achievement_id] = True
        # Steam API Call
        unlock_achievement(achievement_id)
```

### Leaderboards

```python
# leaderboards.py
class SteamLeaderboards:
    LEADERBOARDS = {
        'HIGHEST_LEVEL': 'highest_level_reached',
        'TOTAL_WINS': 'total_battles_won',
        'WIN_STREAK': 'longest_win_streak',
        'TOTAL_DAMAGE': 'total_damage_dealt',
    }
    
    def upload_score(self, leaderboard, score):
        # Steam API Call
        STEAMWORKS.UserStats().UploadLeaderboardScore(
            leaderboard, 
            score
        )
```

### Cloud Saves

```python
# cloud_saves.py
def save_game_to_cloud(agent_data):
    data = json.dumps(agent_data)
    save_to_cloud('agent_save.json', data)

def load_game_from_cloud():
    data = load_from_cloud('agent_save.json')
    return json.loads(data) if data else None
```

---

## 📦 Build & Upload

### 1. Build erstellen

```bash
# Windows Build
python setup.py build

# Testen
./build/AgentBattleSimulator.exe

# Zip erstellen
zip -r AgentBattleSimulator_Windows.zip build/
```

### 2. Steamworks Upload

```bash
# SteamCMD installieren
# https://partner.steamgames.com/doc/sdk/uploading

# Build hochladen
steamcmd +login <username> +run_app_build <app_build_script.vdf> +quit
```

### 3. Build-Script (app_build_script.vdf)

```vdf
"AppBuild"
{
    "AppID" "YOUR_APP_ID"
    "Desc" "Agent Battle Simulator v2.0"
    "BuildOutput" "output"
    "ContentRoot" "build"
    "SetLive" "default"
    
    "Depots"
    {
        "YOUR_DEPOT_ID"
        {
            "FileMapping"
            {
                "LocalPath" "*"
                "DepotPath" "."
                "recursive" "1"
            }
        }
    }
}
```

---

## 🎨 Marketing Assets

### Store Banner Text

```
🎮 AGENT BATTLE SIMULATOR 🎮

Absurde Kämpfe. Epische Aktionen. Lokaler Multiplayer.

⚔️ Kämpfe mit Toilettenpapier-Tsunamis
🎯 Über 20 einzigartige Skins
🏆 XP-System & Level-Ups
👥 Lokaler Multiplayer (2 Spieler)

KOSTENLOS SPIELEN!
```

### Feature-Liste für Store

- ✅ Rundenbasierte Kämpfe
- ✅ 16 absurde Kampfaktionen
- ✅ Lokaler Multiplayer (2 Spieler)
- ✅ KI vs KI Modus zum Zuschauen
- ✅ Über 20 freischaltbare Skins
- ✅ XP-System mit Level-Ups
- ✅ Turnier-Modus
- ✅ Steam Achievements
- ✅ Steam Leaderboards
- ✅ Cloud Saves
- ✅ Vollständig auf Deutsch & Englisch

---

## 📊 Release-Strategie

### Pre-Launch (4 Wochen vor Release)

- [ ] Store Page veröffentlichen
- [ ] Wishlist-Kampagne starten
- [ ] Social Media Teaser
- [ ] Press Kit erstellen
- [ ] Influencer kontaktieren

### Launch Week

- [ ] Release-Trailer veröffentlichen
- [ ] Reddit-Posts (r/IndieGaming, r/Python, r/gaming)
- [ ] Twitter/X-Thread
- [ ] Discord-Community starten
- [ ] Twitch-Streamer kontaktieren

### Post-Launch

- [ ] Community-Feedback sammeln
- [ ] Bugs fixen
- [ ] Updates planen
- [ ] DLC/Erweiterungen überlegen

---

## 💰 Pricing-Strategie

**Empfehlung: Free to Play**

Vorteile:
- Keine Einstiegsbarriere
- Größere Spielerbasis
- Virales Potenzial
- Community-Wachstum

Alternative: $2.99 - $4.99
- Mit Launch-Rabatt 20%
- Bundle-Deals möglich

---

## 🐛 Testing Checklist

- [ ] Windows 10/11 getestet
- [ ] Verschiedene Auflösungen getestet
- [ ] Multiplayer funktioniert
- [ ] Alle Skins funktionieren
- [ ] Achievements funktionieren
- [ ] Cloud Saves funktionieren
- [ ] Performance ist gut (60 FPS+)
- [ ] Keine Crashes
- [ ] Speichern/Laden funktioniert
- [ ] Audio funktioniert (wenn vorhanden)

---

## 📞 Support & Community

### Support-Kanäle einrichten

- [ ] Discord-Server
- [ ] Steam-Forum
- [ ] GitHub Issues
- [ ] E-Mail-Support

### FAQ erstellen

**Q: Ist das Spiel kostenlos?**
A: Ja, komplett kostenlos!

**Q: Gibt es Multiplayer?**
A: Ja, lokaler Multiplayer für 2 Spieler.

**Q: Welche Sprachen werden unterstützt?**
A: Deutsch und Englisch.

**Q: Gibt es DLCs?**
A: Aktuell nicht geplant, alle Features sind kostenlos.

---

## 🎯 Success Metrics

### KPIs tracken

- Wishlist-Conversions
- Downloads/Installs
- Daily Active Users (DAU)
- Average Session Length
- Achievement-Completion-Rate
- Multiplayer-Nutzung
- Review-Score
- Community-Engagement

---

## 🚀 Launch Checklist

**1 Woche vor Launch:**
- [ ] Final Build hochgeladen
- [ ] Store Page finalisiert
- [ ] Trailer veröffentlicht
- [ ] Press Kit versendet
- [ ] Social Media vorbereitet

**Launch Day:**
- [ ] Release-Button drücken
- [ ] Social Media Posts
- [ ] Community-Monitoring
- [ ] Bug-Tracking aktiv

**1 Woche nach Launch:**
- [ ] Feedback analysieren
- [ ] Hotfixes deployen
- [ ] Reviews beantworten
- [ ] Update-Roadmap teilen

---

## 📚 Ressourcen

- [Steamworks Documentation](https://partner.steamgames.com/doc/home)
- [Steam SDK](https://partner.steamgames.com/doc/sdk)
- [PyInstaller Docs](https://pyinstaller.org/)
- [Steam Marketing Guide](https://partner.steamgames.com/doc/marketing)

---

## ✅ Final Notes

**Wichtig:**
- Qualität vor Geschwindigkeit
- Community-Feedback ernst nehmen
- Regelmäßige Updates planen
- Transparent kommunizieren

**Joke-Game Status:**
Auch wenn es als "Joke-Game" startet, kann es durch gute Execution und Community-Support zu einem echten Hit werden! 🚀

---

**Viel Erfolg beim Steam-Release! 🎮🏆**

# 📚 Agent Battle Simulator - Dokumentation

## Übersicht

Der **Agent Battle Simulator** ist ein unterhaltsames, rundenbasiertes Kampfspiel zwischen zwei KI-Agenten. Das Spiel kombiniert absurde Kampfaktionen mit einem ausgefeilten Erfahrungspunkte-System und verschiedenen KI-Strategien.

## 🎯 Spielkonzept

### Die Agenten

**🔴 Der Angreifer**
- Aggressive KI-Strategie
- Fokussiert auf hohen Schaden
- Bevorzugt offensive Aktionen
- Impulsiv und schadensfokussiert

**🔵 Der Verteidiger**
- Defensive KI-Strategie
- Fokussiert auf Heilung und Buffs
- Nutzt clevere Konter
- Zynisch und taktisch

### Spielmechaniken

#### Stats
Jeder Agent hat folgende Attribute:
- **HP (Health Points)**: Lebenspunkte, bei 0 ist der Agent besiegt
- **Stamina**: Energie für Aktionen, regeneriert sich jede Runde
- **Level**: Steigt mit XP, erhöht alle Stats
- **XP (Experience Points)**: Erfahrungspunkte zum Leveln
- **Attack Bonus**: Zusätzlicher Schaden bei Angriffen
- **Defense Bonus**: Reduziert erlittenen Schaden

#### Aktionen

Jede Aktion hat:
- **Schaden**: Basis-Schadenswert
- **Stamina-Kosten**: Benötigte Energie
- **Cooldown**: Wartezeit nach Nutzung
- **Spezialeffekte**: Buffs, Debuffs, Heilung, Stun, etc.

##### Angreifer-Aktionen
1. **🧻 Toilettenpapier-Tsunami** - Debuff-Attacke
2. **🔥 Feuerball der Bürofrustration** - Hoher Schaden
3. **🦠 Viren-E-Mail** - Schneller Debuff
4. **🪖 Meeting-Demoralisierung** - Stun-Effekt
5. **🧃 Smoothie-Attacke** - Mittlerer Schaden
6. **⚡ Blitz-Spam** - Schneller Debuff
7. **🎯 Präzisions-Kritik** - Hoher Schaden
8. **💣 Deadline-Bombe** - Maximaler Schaden mit Debuff

##### Verteidiger-Aktionen
1. **🧲 Magnetische Feldverwirrung** - Debuff-Attacke
2. **🦾 Selbstoptimierung** - Heilung
3. **🧠 Gedankenlesen** - Schaden + Buff
4. **🛡️ Firewall der Gelassenheit** - Buff
5. **🔄 Reverse-Uno-Karte** - Schaden-Reflektion
6. **☕ Kaffee-Konter** - Schnelle Heilung
7. **🧘 Meditation der Unverwundbarkeit** - Starker Buff
8. **⚔️ Zynischer Gegenangriff** - Schaden + Debuff

#### Effekte

**Buffs** (Positive Effekte)
- Erhöhen Defense temporär
- Halten 2 Runden
- Stapelbar

**Debuffs** (Negative Effekte)
- Reduzieren Defense temporär
- Halten 2 Runden
- Stapelbar

**Stun**
- Agent kann 1 Runde nicht angreifen
- Wird automatisch nach 1 Runde aufgehoben

**Heilung**
- Stellt HP wieder her
- Kann nicht über Maximum heilen

#### Level-System

**XP-Vergabe**
- Gewinner: 100 XP + (Runden × 10)
- Verlierer: 50 XP + (Runden × 5)

**Level-Up Effekte**
- +20 Max HP
- +10 Max Stamina
- +2 Attack Bonus
- +2 Defense Bonus
- Volle Heilung von HP und Stamina
- XP-Anforderung steigt um 50%

**XP-Formel**
```
XP für nächstes Level = Aktuelles Requirement × 1.5
Start: 100 XP
Level 2: 150 XP
Level 3: 225 XP
Level 4: 337 XP
etc.
```

## 🎮 Spielmodi

### 1. Manueller Kampf
- Schritt-für-Schritt Durchführung
- Benutzer drückt Enter für nächste Runde
- Ideal zum Lernen und Verstehen

### 2. Autopilot-Kampf
- Vollautomatischer Ablauf
- Einstellbare Geschwindigkeit (0.5 - 5.0 Sekunden)
- Perfekt zum Zuschauen

### 3. Turnier-Modus
- Best of 3, 5 oder 7 Kämpfe
- Automatischer Ablauf
- Zeigt Gesamtsieger am Ende

## 💾 Speichersystem

### Speichern
- Speichert beide Agenten mit allen Stats
- Speicherort: `saves/agents_save.json`
- Automatische Verzeichniserstellung

### Laden
- Lädt gespeicherte Agenten
- Überschreibt aktuelle Agenten
- Warnung vor Überschreiben

### Zurücksetzen
- Erstellt neue Level-1 Agenten
- Löscht Speicherdatei
- Bestätigung erforderlich

## 🏗️ Architektur

### Modulstruktur

```
Hackaton/
├── battle_sim.py       # Hauptprogramm & Menü-Loop
├── agents.py           # Agent-Klassen & KI-Logik
├── actions.py          # Kampfaktionen & Effekte
├── game_engine.py      # Kampfmechanik & Rundenablauf
├── ui.py               # User Interface & Menüs
├── save_system.py      # Speichern/Laden
├── requirements.txt    # Dependencies (keine!)
├── README.md           # Projekt-Übersicht
├── DOCUMENTATION.md    # Diese Datei
└── LICENSE             # MIT Lizenz
```

### Klassendiagramm

```
Agent (Basis-Klasse)
├── AttackerAgent (Aggressive KI)
└── DefenderAgent (Defensive KI)

Action (Aktions-Klasse)
├── Schaden-Berechnung
├── Cooldown-Management
└── Effekt-Anwendung

GameEngine
├── Kampf-Loop
├── Runden-Verwaltung
└── XP-Vergabe

Tournament
├── Mehrere Kämpfe
└── Sieger-Ermittlung

UI (Static Methods)
├── Menüs
├── Status-Anzeige
└── Benutzer-Eingabe

SaveSystem (Static Methods)
├── JSON-Serialisierung
└── Datei-Verwaltung
```

## 🔧 Erweiterungsmöglichkeiten

### Neue Aktionen hinzufügen

1. Öffne `actions.py`
2. Füge neue Action zu `ATTACKER_ACTIONS` oder `DEFENDER_ACTIONS` hinzu:

```python
Action(
    name="🌟 Deine Neue Aktion",
    description="Beschreibung der Aktion",
    damage=30,
    stamina_cost=20,
    cooldown=3,
    effect_type="buff",  # oder "debuff", "heal", "stun"
    effect_value=10
)
```

### Neue KI-Strategien

1. Öffne `agents.py`
2. Erstelle neue Agent-Klasse:

```python
class CustomAgent(Agent):
    def __init__(self, name: str, level: int = 1):
        super().__init__(name, "attacker", level)
        self.strategy = "custom"
    
    def choose_action(self, opponent: Agent) -> Optional[Action]:
        # Deine eigene Logik hier
        available = self.get_available_actions()
        # ... Strategie implementieren
        return chosen_action
```

### Neue Effekte

1. Erweitere `Action`-Klasse in `actions.py`
2. Implementiere Effekt-Logik in `game_engine.py` in `_execute_action()`

### Multiplayer

Mögliche Erweiterung für menschliche Spieler:
1. Erweitere `Agent.choose_action()` um manuelle Auswahl
2. Nutze `UI.show_actions_menu()` für Benutzer-Input
3. Implementiere Spieler-Klasse die von `Agent` erbt

## 🎨 Anpassung

### Kampfkommentare

Bearbeite `COMBAT_COMMENTS` in `actions.py` für eigene witzige Kommentare.

### Visuals

Alle visuellen Elemente sind in `ui.py`:
- `show_title()`: Titel-Screen
- `show_welcome_message()`: Willkommensnachricht
- `show_goodbye()`: Abschiedsnachricht
- `get_status()`: Status-Bars in `agents.py`

### Balance

Passe Werte in `agents.py` an:
- `max_hp`: Basis-Lebenspunkte
- `max_stamina`: Basis-Energie
- `xp_to_next_level`: XP-Anforderung
- Level-Up Boni in `level_up()`

## 🐛 Debugging

### Logging aktivieren

Füge in `battle_sim.py` hinzu:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Testmodus

Erstelle `test_battle.py`:
```python
from agents import AttackerAgent, DefenderAgent
from game_engine import GameEngine

attacker = AttackerAgent(level=5)
defender = DefenderAgent(level=5)

engine = GameEngine(attacker, defender)
winner = engine.start_battle(auto_mode=True, delay=0.1)
print(f"Winner: {winner.name}")
```

## 📊 Statistiken

Das Spiel trackt folgende Statistiken pro Agent:
- Gesamt verursachter Schaden
- Gesamt erlittener Schaden
- Anzahl genutzter Aktionen
- Anzahl Siege
- Anzahl Niederlagen

Diese werden in `agents.py` verwaltet und in `ui.py` angezeigt.

## 🚀 Performance

- Keine externen Dependencies = Schneller Start
- Reine Python Standard Library
- Minimaler Speicherverbrauch
- Läuft auf jedem System mit Python 3.8+

## 🤝 Beitragen

Dieses Projekt ist für den Cline Hackathon erstellt. Erweiterungen willkommen!

### Ideen für Erweiterungen
- [ ] Mehr Agenten-Typen (Heiler, Tank, etc.)
- [ ] Items und Equipment-System
- [ ] Skill-Trees für Agenten
- [ ] Multiplayer-Modus
- [ ] Grafisches Interface (PyGame/Tkinter)
- [ ] Achievements-System
- [ ] Replay-Funktion
- [ ] Statistik-Export (CSV/JSON)
- [ ] Kampf-Logs speichern
- [ ] Online-Leaderboard

## 📝 Lizenz

MIT License - Siehe LICENSE Datei

## 🎉 Credits

Entwickelt für den **Cline Hackathon** (8.-14. Dezember 2024)

Inspiriert von klassischen RPG-Kampfsystemen und modernem Game Design.

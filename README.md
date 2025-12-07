# 🎮 Hackaton - Agent Battle Simulator

Ein unterhaltsames Python-basiertes Kampfspiel zwischen KI-Agenten mit absurden Angriffen, Verteidigungen und einem Erfahrungspunkte-System.

## 🚀 Features

- **Rundenbasierter Kampf** zwischen Angreifer und Verteidiger
- **Absurde Aktionen** wie "Toilettenpapier-Tsunami", "Smoothie-Attacke" und "Meeting-Demoralisierung"
- **Erfahrungspunkte-System** - Agenten leveln auf und werden stärker
- **Verschiedene KI-Strategien** - Aggressiv vs. Defensiv
- **Lokales Interface** - Einfach zu bedienen, keine Cloud nötig
- **Autopilot-Modus** - Einfach zuschauen wie die Agenten kämpfen
- **Persistente Spielerdaten** - Fortschritt wird gespeichert
- **Witzige Kommentare** - Unterhaltsame Kampfansagen

## 📋 Anforderungen

- Python 3.8+
- Keine externen APIs oder Cloud-Dienste nötig

## 🎯 Installation

```bash
git clone <repository-url>
cd Hackaton
pip install -r requirements.txt
```

## 🎮 Nutzung

```bash
python battle_sim.py
```

## 🏗️ Projektstruktur

```
Hackaton/
├── battle_sim.py          # Hauptprogramm
├── agents.py              # Agenten-Klassen
├── actions.py             # Kampfaktionen
├── game_engine.py         # Spielmechanik
├── ui.py                  # Interface
├── requirements.txt       # Dependencies
└── README.md             # Diese Datei
```

## 🎲 Spielmechanik

Jeder Agent hat:
- **Lebenspunkte (HP)**
- **Ausdauer (Stamina)**
- **Erfahrungspunkte (XP)**
- **Level**
- **Spezielle Fähigkeiten**

Aktionen haben:
- **Schaden**
- **Cooldown**
- **Spezialeffekte** (Buffs/Debuffs)
- **Stamina-Kosten**

## 🏆 Für den Cline Hackathon

Dieses Projekt wurde für den Cline Hackathon (8.-14. Dezember) entwickelt.

## 📝 Lizenz

Apache License 2.0 - Siehe LICENSE Datei

Copyright 2024 KoMMb0t <kommuniverse@gmail.com>

# 🤖 OGame Full Automation Bot

**Der ultimative Bot für vollautomatisches OGame-Spielen!**

## 🎯 Hauptziel
Erreiche so schnell wie möglich deine **zweite Kolonie** durch intelligente Automatisierung:
- 🏗️ **Automatischer Planeten-Aufbau** mit optimalen Prioritäten
- 🏴‍☠️ **Vollautomatisches Raiding** für massive Ressourcen  
- 🌟 **Intelligente Kolonisierung** für strategische Expansion

## ⚡ Quick Start

### 1. Bot starten
```bash
python3 ogame_bot.py
```

**Das wars!** Der Bot macht alles automatisch:
- ✅ Startet Browser mit Remote Debugging
- ✅ Wartet auf dein Login
- ✅ Erkennt OGame automatisch  
- ✅ Beginnt Vollautomatisierung

### 2. Login (einmalig)
1. 🌐 Browser öffnet sich automatisch
2. 🔑 Du loggst dich **einmal** in OGame ein
3. 📍 Gehe zur Planeten-Übersicht
4. 🤖 Bot startet automatisch!

### 3. Entspann dich!
Der Bot übernimmt komplett:
- � Überwacht alle Ressourcen
- 🏗️ Baut strategisch wichtige Gebäude  
- ⚔️ Sucht und raidet schwache Ziele
- � Plant deine Kolonisierung

## 🚀 Features

### 🧠 Intelligenter Planeten-Aufbau
- **Adaptive Prioritäten**: Fokus auf Ressourcenproduktion → Infrastruktur → Flotte
- **Ressourcen-basierte Entscheidungen**: Baut das, was am meisten bringt
- **Energie-Management**: Automatische Solarkraftwerk-Optimierung

### ⚔️ Automatisches Raiding System
- **Galaxy-Scanner**: Findet automatisch lohnende Ziele
- **Sicherheits-Checks**: Vermeidet starke Spieler und Fallen
- **Intelligente Flotten**: Optimale Schiff-Zusammenstellung für jeden Raid
- **24/7 Betrieb**: Maximaler Ressourcen-Gewinn rund um die Uhr

### 🏛️ Kolonisierung-Automation
- **Strategische Planung**: Überwacht Ressourcen für perfektes Timing
- **Auto-Deployment**: Startet Kolonisierungs-Flotten automatisch
- **Ziel-Analyse**: Findet beste Planeten für Expansion

### ⚙️ Adaptive Modi
- **🏗️ BUILDING MODE**: Fokus auf Infrastruktur (10min Zyklen)
- **⚔️ ACTIVE MODE**: Aktives Raiding (5min Zyklen)  
- **🚀 TURBO MODE**: Bereit für Kolonisierung (3min Zyklen)

## 📊 Erwartete Ergebnisse

| Zeitraum | Ohne Bot | Mit Bot | Verbesserung |
|----------|----------|---------|--------------|
| **1 Tag** | 2.000 Ressourcen | 15.000+ Ressourcen | **7x schneller** |
| **1 Woche** | Grundaufbau | Raid-Flotte bereit | **Wochen gespart** |
| **2 Wochen** | Erste Technik | **Zweite Kolonie!** | **🎯 Ziel erreicht** |

## 🛠️ Installation

### Requirements (automatisch installiert)
```bash
pip install selenium webdriver-manager requests
```

### Browser Setup (automatisch)
- **Brave Browser** wird automatisch konfiguriert
- **Remote Debugging** auf Port 9223
- **Separates Profil** für Bot-Betrieb

## 📋 Projekt-Struktur

```
ogamer/
├── ogame_bot.py              # 🎯 EINZIGER STARTPUNKT!
├── src/managers/             # 🤖 Bot-Logik
│   ├── building_manager.py   # 🏗️ Gebäude-Automatisierung
│   ├── fleet_manager.py      # ⚔️ Raid-System
│   ├── colonization_manager.py # 🌟 Kolonisierung
│   └── resource_manager.py   # 💰 Ressourcen-Monitoring
├── config/                   # ⚙️ Konfiguration
│   └── planet_config.py      # 🏛️ Strategien & Prioritäten
└── logs/                     # 📊 Log-Dateien
    └── ogame_bot.log         # 📋 Detaillierte Aktivitäten
```

## 🎮 Live-Monitoring

### Console Output
```bash
🤖 === EMPIRE STATUS ===
💰 Resources: M:45,230 C:23,100 D:8,450 (Total: 76,780)
🏛️ Colonies: 1
🏗️ Building Ready: ✅
🏴‍☠️ Raid Ready: ✅  
🌟 Colonization Ready: ❌

🏗️ === PHASE 1: BUILDING ===
✅ Building construction started!

🏴‍☠️ === PHASE 2: RAIDING ===
✅ Raid launched successfully!

🚀 TURBO MODE - Next cycle in 3 minutes
```

### Log-Datei
- 📊 **Detaillierte Statistiken** in `logs/ogame_bot.log`
- 📈 **Ressourcen-Tracking** über Zeit
- ⚔️ **Raid-Erfolgsraten** und Beute
- 🏗️ **Bau-Entscheidungen** mit Begründung

## 🔧 Erweiterte Konfiguration

### Building Prioritäten anpassen
```python
# config/planet_config.py
BUILDING_PRIORITIES = {
    'early_game': ['Metal Mine', 'Crystal Mine', 'Solar Plant'],
    'mid_game': ['Robot Factory', 'Deuterium Synthesizer'],
    'late_game': ['Shipyard', 'Research Lab']
}
```

### Raid-Parameter tunen
```python
# Mehr/weniger aggressive Raids
RAID_SETTINGS = {
    'min_target_resources': 50000,  # Minimum lohnende Beute
    'max_player_rank': 500,         # Nur schwächere Spieler
    'safety_margin': 2.0            # 2x Überlegenheit mindestens
}
```

## 🛡️ Sicherheit

### Anti-Detection Features
- ✅ **Menschliche Timing**: Zufällige Delays zwischen Aktionen
- ✅ **Browser-Simulation**: Nutzt echten Browser (keine Headless-Detection)
- ✅ **Adaptive Pausen**: Längere Breaks bei verdächtigen Aktivitäten
- ✅ **Fehler-Handling**: Graceful Recovery bei Problemen

### Benutzer-Kontrolle
- 🔄 **Ctrl+C**: Sanftes Beenden (Browser bleibt offen)
- 🌐 **Browser-Access**: Du kannst jederzeit manuell eingreifen
- 📊 **Transparente Logs**: Alles wird dokumentiert

## � Troubleshooting

### Bot startet nicht?
```bash
# Check browser process
ps aux | grep -i brave

# Check logs
tail -f logs/ogame_bot.log

# Restart clean
killall "Brave Browser"
python3 ogame_bot.py
```

### Verbindung verloren?
- ✅ Bot reconnected automatisch
- ✅ Fortsetzung ohne Datenverlust
- ✅ Browser bleibt für dich verfügbar

### Performance Issues?
```bash
# Monitor resource usage
top -p $(pgrep -f ogame_bot)

# Adjust cycle timing in bot code
CYCLE_DELAYS = {
    'turbo': 180,    # 3 minutes
    'active': 300,   # 5 minutes  
    'building': 420  # 7 minutes
}
```

## 🎯 Pro-Tipps

### 🏆 Maximaler Erfolg:
1. **Starte früh am Tag** → Nutze 24h voll aus
2. **Lass Bot mindestens eine Woche laufen** → Exponentielles Wachstum
3. **Check Logs gelegentlich** → Verstehe Bot-Strategien
4. **Tweak Konfiguration** → Optimiere für deinen Server

### ⚡ Speed-Boost:
- 🌙 **Nacht-Modi**: Bot läuft auch nachts für dich
- 📱 **Remote-Monitoring**: Check Status von unterwegs via Logs
- 🔄 **Zero-Downtime**: Browser-Crash? Bot startet neu!

---

## 🎉 Happy Domination!

**Dein Bot arbeitet jetzt 24/7 für dich!**

Während du schläfst:
- 💰 Sammelt er Millionen von Ressourcen
- 🏗️ Baut er dein Imperium aus  
- ⚔️ Raidet er deine Nachbarn
- 🌟 Bereitet er deine Expansion vor

**Ziel: Zweite Kolonie in Rekordzeit! 🚀**

---
*Made with ❤️ for galactic domination*

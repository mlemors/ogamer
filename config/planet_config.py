# OGame Bot - Planet Development Configuration

class PlanetDevelopmentConfig:
    """Konfiguration für die Planeten-Entwicklung"""
    
    # === RESOURCE THRESHOLDS ===
    # Mindest-Ressourcen bevor gebaut wird
    MIN_METAL_TO_BUILD = 500
    MIN_CRYSTAL_TO_BUILD = 250
    MIN_DEUTERIUM_TO_BUILD = 100
    
    # === BUILDING STRATEGY ===
    # Prioritäten: 1 = höchste Priorität
    BUILDING_PRIORITY = {
        # Phase 1: Grundlagen (Level 1-10)
        'metallmine': 1,
        'kristallmine': 2,
        'deuteriumsynthetisierer': 3,
        'solarkraftwerk': 4,
        
        # Phase 2: Effizienz (Level 5-15)  
        'roboterfabrik': 5,
        'metallspeicher': 6,
        'kristallspeicher': 7,
        'deuteriumtank': 8,
        
        # Phase 3: Forschung (Level 10+)
        'forschungslabor': 9,
        'nanofabrik': 10,
        
        # Phase 4: Militär (Level 15+)
        'raumschiffwerft': 11,
        'verteidigungsanlagen': 12
    }
    
    # === TARGET LEVELS ===
    # Ziel-Level für verschiedene Entwicklungsphasen
    EARLY_GAME_TARGETS = {
        'metallmine': 12,
        'kristallmine': 10,
        'deuteriumsynthetisierer': 8,
        'solarkraftwerk': 10,
        'roboterfabrik': 6,
        'forschungslabor': 3
    }
    
    MID_GAME_TARGETS = {
        'metallmine': 20,
        'kristallmine': 17,
        'deuteriumsynthetisierer': 15,
        'solarkraftwerk': 18,
        'roboterfabrik': 10,
        'forschungslabor': 8,
        'nanofabrik': 3,
        'raumschiffwerft': 5
    }
    
    LATE_GAME_TARGETS = {
        'metallmine': 30,
        'kristallmine': 25,
        'deuteriumsynthetisierer': 20,
        'solarkraftwerk': 25,
        'roboterfabrik': 15,
        'forschungslabor': 12,
        'nanofabrik': 8,
        'raumschiffwerft': 12
    }
    
    # === SMART BUILDING LOGIC ===
    # Ressourcen-Verhältnis für Entscheidungen
    RESOURCE_RATIOS = {
        'metal_crystal_ratio': 3.0,  # Metal sollte 3x mehr sein als Crystal
        'crystal_deuterium_ratio': 2.0,  # Crystal sollte 2x mehr sein als Deuterium
        'energy_threshold': 0.8  # Baue Kraftwerk wenn Energie < 80%
    }
    
    # === BOT BEHAVIOR ===
    # Wie oft versucht der Bot zu bauen
    BUILD_CHECK_INTERVAL = 300  # Alle 5 Minuten prüfen
    RESOURCE_CHECK_INTERVAL = 60   # Alle 1 Minute Ressourcen prüfen
    
    # Sicherheits-Einstellungen
    MAX_BUILD_ATTEMPTS = 3  # Max 3 Bauversuche pro Zyklus
    BUILD_COOLDOWN = 1800   # 30 Min warten nach erfolgreichem Bau
    
    # === EMERGENCY STOPS ===
    # Stoppe Bot wenn Ressourcen zu niedrig
    EMERGENCY_STOP_METAL = 50
    EMERGENCY_STOP_CRYSTAL = 25
    EMERGENCY_STOP_DEUTERIUM = 10
    
    @classmethod
    def get_target_for_phase(cls, phase="early"):
        """Hole Ziel-Level für bestimmte Spiel-Phase"""
        if phase == "early":
            return cls.EARLY_GAME_TARGETS
        elif phase == "mid":
            return cls.MID_GAME_TARGETS
        elif phase == "late":
            return cls.LATE_GAME_TARGETS
        else:
            return cls.EARLY_GAME_TARGETS
            
    @classmethod
    def should_build_energy(cls, energy_percentage):
        """Entscheide ob Kraftwerk gebaut werden soll"""
        return energy_percentage < cls.RESOURCE_RATIOS['energy_threshold']
        
    @classmethod
    def determine_game_phase(cls, total_building_levels):
        """Bestimme Spiel-Phase basierend auf Gebäude-Leveln"""
        if total_building_levels < 50:
            return "early"
        elif total_building_levels < 150:
            return "mid"
        else:
            return "late"

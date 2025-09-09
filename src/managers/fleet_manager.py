import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FleetManager:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.wait = WebDriverWait(driver, 10)
        
        # Raid-Konfiguration
        self.raid_config = {
            'min_ships_for_raid': 5,  # Mindestanzahl Schiffe für Raid
            'max_raid_distance': 20,  # Max Systeme entfernt
            'preferred_targets': ['inactive', 'weak', 'vacation'],
            'avoid_targets': ['strong', 'alliance', 'admin'],
            'resource_threshold': 10000,  # Min Ressourcen für lohnenswerten Raid
        }
        
        # Kolonisierungs-Ziele
        self.colonization_config = {
            'target_planet_size': 200,  # Min Planetengröße
            'max_colonies': 9,  # Max Anzahl Kolonien
            'required_ships': {'kolonie_schiff': 1, 'kleine_transporter': 10}
        }

    def navigate_to_galaxy(self):
        """Navigiere zur Galaxie-Ansicht"""
        try:
            galaxy_selectors = [
                "//a[contains(@href, 'galaxy')]",
                "//a[contains(@href, 'component=galaxy')]", 
                "//span[contains(text(), 'Galaxie')]/parent::a",
                "#galaxy",
                ".galaxy"
            ]
            
            for selector in galaxy_selectors:
                try:
                    if selector.startswith("//"):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    element.click()
                    time.sleep(3)
                    self.logger.info("🌌 Navigated to galaxy view")
                    return True
                except:
                    continue
                    
            self.logger.warning("⚠️ Could not find galaxy navigation")
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Galaxy navigation error: {e}")
            return False

    def scan_for_raid_targets(self):
        """Scanne nach Raid-Zielen in der Galaxie"""
        self.logger.info("🔍 === SCANNING FOR RAID TARGETS ===")
        
        try:
            if not self.navigate_to_galaxy():
                return []
                
            targets = []
            
            # Scanne mehrere Systeme
            for system_offset in range(-5, 6):  # 10 Systeme scannen
                try:
                    self.navigate_to_system(system_offset)
                    system_targets = self.analyze_system_for_targets()
                    targets.extend(system_targets)
                    time.sleep(2)  # Kurze Pause zwischen Systemen
                except:
                    continue
                    
            # Sortiere Ziele nach Attraktivität
            targets.sort(key=lambda x: x.get('score', 0), reverse=True)
            
            self.logger.info(f"🎯 Found {len(targets)} potential raid targets")
            return targets[:10]  # Top 10 Ziele
            
        except Exception as e:
            self.logger.error(f"❌ Raid scan error: {e}")
            return []

    def navigate_to_system(self, offset=0):
        """Navigiere zu einem anderen System"""
        try:
            # Suche nach System-Eingabefeld oder Navigation
            system_selectors = [
                "input[name='system']",
                "#system",
                ".system-input"
            ]
            
            for selector in system_selectors:
                try:
                    system_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    current_system = int(system_input.get_attribute('value') or '1')
                    new_system = max(1, current_system + offset)
                    
                    system_input.clear()
                    system_input.send_keys(str(new_system))
                    
                    # Submit oder Enter drücken
                    submit_btn = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit'], .submit")
                    submit_btn.click()
                    time.sleep(2)
                    return True
                except:
                    continue
                    
            return False
            
        except Exception as e:
            self.logger.error(f"❌ System navigation error: {e}")
            return False

    def analyze_system_for_targets(self):
        """Analysiere aktuelles System nach Raid-Zielen"""
        targets = []
        
        try:
            # Suche nach Planeten-Reihen in der Galaxie-Ansicht
            planet_selectors = [
                ".row",
                ".planet-row", 
                "[class*='planet']",
                "tr"
            ]
            
            for selector in planet_selectors:
                try:
                    rows = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for row in rows:
                        target_info = self.analyze_planet_row(row)
                        if target_info and self.is_good_raid_target(target_info):
                            targets.append(target_info)
                            
                except:
                    continue
                    
            return targets
            
        except Exception as e:
            self.logger.error(f"❌ System analysis error: {e}")
            return []

    def analyze_planet_row(self, row):
        """Analysiere eine Planeten-Zeile"""
        try:
            # Extrahiere Planet-Informationen
            info = {
                'coordinates': self.extract_coordinates(row),
                'player_name': self.extract_player_name(row),
                'activity': self.extract_activity_status(row),
                'fleet_size': self.estimate_fleet_size(row),
                'estimated_resources': self.estimate_resources(row),
                'score': 0
            }
            
            # Berechne Attraktivitäts-Score
            info['score'] = self.calculate_target_score(info)
            
            return info if info['coordinates'] else None
            
        except:
            return None

    def extract_coordinates(self, row):
        """Extrahiere Koordinaten aus einer Zeile"""
        try:
            coord_text = row.text
            # Suche nach Koordinaten-Muster wie [1:2:3]
            import re
            coord_match = re.search(r'\[(\d+):(\d+):(\d+)\]', coord_text)
            if coord_match:
                return f"{coord_match.group(1)}:{coord_match.group(2)}:{coord_match.group(3)}"
            return None
        except:
            return None

    def extract_player_name(self, row):
        """Extrahiere Spielername"""
        try:
            # Suche nach Spielername-Links oder -Text
            player_elements = row.find_elements(By.CSS_SELECTOR, ".player, .playername, a[href*='player']")
            if player_elements:
                return player_elements[0].text.strip()
            return "Unknown"
        except:
            return "Unknown"

    def extract_activity_status(self, row):
        """Extrahiere Aktivitäts-Status"""
        try:
            # Suche nach Inaktivitäts-Indikatoren
            inactive_indicators = [
                ".inactive", ".vacation", ".long_inactive",
                "[class*='inactive']", "[title*='inactive']"
            ]
            
            for indicator in inactive_indicators:
                if row.find_elements(By.CSS_SELECTOR, indicator):
                    return "inactive"
                    
            # Prüfe auf letzte Aktivität
            activity_text = row.text.lower()
            if any(word in activity_text for word in ['inactive', 'urlaub', 'vacation']):
                return "inactive"
                
            return "active"
        except:
            return "unknown"

    def estimate_fleet_size(self, row):
        """Schätze Flottengröße basierend auf sichtbaren Indikatoren"""
        try:
            # Suche nach Flotten-Indikatoren
            fleet_indicators = row.find_elements(By.CSS_SELECTOR, ".fleet, [class*='fleet']")
            
            if not fleet_indicators:
                return "small"  # Keine sichtbare Flotte
            elif len(fleet_indicators) < 3:
                return "medium"
            else:
                return "large"
        except:
            return "unknown"

    def estimate_resources(self, row):
        """Schätze verfügbare Ressourcen"""
        try:
            # Basiere Schätzung auf Planeten-Größe und Aktivität
            text = row.text
            
            # Suche nach Zahlen die Planetengröße andeuten könnten
            import re
            numbers = re.findall(r'\d+', text)
            
            if numbers:
                # Nimm die größte Zahl als groben Indikator
                max_num = max(int(n) for n in numbers if int(n) < 500)
                return max_num * 100  # Grobe Schätzung
                
            return 5000  # Default-Schätzung
        except:
            return 5000

    def calculate_target_score(self, target_info):
        """Berechne Attraktivitäts-Score für ein Ziel"""
        score = 0
        
        # Inaktive Spieler sind bessere Ziele
        if target_info['activity'] == 'inactive':
            score += 50
        elif target_info['activity'] == 'active':
            score -= 20
            
        # Geschätzte Ressourcen
        score += min(target_info['estimated_resources'] / 1000, 30)
        
        # Flottengröße (kleinere Flotten sind besser)
        if target_info['fleet_size'] == 'small':
            score += 20
        elif target_info['fleet_size'] == 'large':
            score -= 30
            
        return max(0, score)

    def is_good_raid_target(self, target_info):
        """Prüfe ob ein Ziel für Raid geeignet ist"""
        # Mindest-Score erforderlich
        if target_info['score'] < 20:
            return False
            
        # Vermeide starke oder aktive Ziele
        if target_info['fleet_size'] == 'large':
            return False
            
        # Bevorzuge inaktive Spieler
        if target_info['activity'] == 'inactive':
            return True
            
        return target_info['score'] > 40

    def launch_raid(self, target_coords, ship_count):
        """Starte einen Raid auf ein Ziel"""
        self.logger.info(f"🚀 === LAUNCHING RAID TO {target_coords} ===")
        
        try:
            # Navigiere zur Flotten-Seite
            if not self.navigate_to_fleet():
                return False
                
            # Wähle Schiffe aus
            if not self.select_ships_for_raid(ship_count):
                return False
                
            # Setze Ziel-Koordinaten
            if not self.set_target_coordinates(target_coords):
                return False
                
            # Wähle Mission (Angriff)
            if not self.select_mission_type('attack'):
                return False
                
            # Bestätige und starte
            return self.confirm_and_launch_fleet()
            
        except Exception as e:
            self.logger.error(f"❌ Raid launch error: {e}")
            return False

    def navigate_to_fleet(self):
        """Navigiere zur Flotten-Seite"""
        try:
            fleet_selectors = [
                "//a[contains(@href, 'fleet')]",
                "//a[contains(@href, 'component=fleet')]",
                "//span[contains(text(), 'Flotte')]/parent::a",
                "#fleet",
                ".fleet"
            ]
            
            for selector in fleet_selectors:
                try:
                    if selector.startswith("//"):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    element.click()
                    time.sleep(2)
                    self.logger.info("🚀 Navigated to fleet page")
                    return True
                except:
                    continue
                    
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Fleet navigation error: {e}")
            return False

    def select_ships_for_raid(self, ship_count):
        """Wähle Schiffe für den Raid aus"""
        try:
            # Suche nach kleinen Transportern (beste Raid-Schiffe)
            ship_selectors = [
                "input[name*='small']",  # Kleine Transporter
                "input[name*='light']",  # Light Fighter
                ".ship-small",
                "[class*='transport']"
            ]
            
            for selector in ship_selectors:
                try:
                    ship_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    ship_input.clear()
                    ship_input.send_keys(str(ship_count))
                    self.logger.info(f"✅ Selected {ship_count} ships for raid")
                    return True
                except:
                    continue
                    
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Ship selection error: {e}")
            return False

    def set_target_coordinates(self, coords):
        """Setze Ziel-Koordinaten"""
        try:
            # Parse Koordinaten
            galaxy, system, planet = coords.split(':')
            
            # Setze Koordinaten-Felder
            coord_fields = ['galaxy', 'system', 'planet']
            coord_values = [galaxy, system, planet]
            
            for field, value in zip(coord_fields, coord_values):
                try:
                    coord_input = self.driver.find_element(By.CSS_SELECTOR, f"input[name='{field}']")
                    coord_input.clear()
                    coord_input.send_keys(value)
                except:
                    continue
                    
            self.logger.info(f"🎯 Target coordinates set: {coords}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Coordinate setting error: {e}")
            return False

    def select_mission_type(self, mission='attack'):
        """Wähle Missions-Typ"""
        try:
            mission_selectors = [
                "input[value='1']",  # Angriff
                "input[name='mission'][value='1']",
                ".mission-attack"
            ]
            
            for selector in mission_selectors:
                try:
                    mission_radio = self.driver.find_element(By.CSS_SELECTOR, selector)
                    mission_radio.click()
                    self.logger.info("⚔️ Attack mission selected")
                    return True
                except:
                    continue
                    
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Mission selection error: {e}")
            return False

    def confirm_and_launch_fleet(self):
        """Bestätige und starte die Flotte"""
        try:
            # Suche nach Bestätigungs-Button
            confirm_selectors = [
                "input[value='Senden']",
                "input[type='submit']",
                ".send-fleet",
                "#sendFleet"
            ]
            
            for selector in confirm_selectors:
                try:
                    confirm_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    # SICHERHEITS-CHECK: Bestätige nur bei geringer Schiffanzahl
                    if self.safety_check_before_launch():
                        confirm_btn.click()
                        self.logger.info("🚀 Fleet launched successfully!")
                        return True
                    else:
                        self.logger.warning("⚠️ Safety check failed - fleet not launched")
                        return False
                except:
                    continue
                    
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Fleet launch error: {e}")
            return False

    def safety_check_before_launch(self):
        """Sicherheits-Check vor Flotten-Start"""
        try:
            # Prüfe die Seite auf Warnungen oder große Schiffzahlen
            page_text = self.driver.page_source.lower()
            
            # Verhindere versehentliche große Angriffe
            dangerous_keywords = ['destroy', 'vernichten', 'total', 'alle schiffe']
            
            for keyword in dangerous_keywords:
                if keyword in page_text:
                    self.logger.warning(f"⚠️ Dangerous keyword found: {keyword}")
                    return False
                    
            return True
            
        except:
            return True  # Bei Unsicherheit eher erlauben

    def auto_raid_cycle(self):
        """Vollautomatischer Raid-Zyklus"""
        self.logger.info("🏴‍☠️ === AUTO RAID CYCLE ===")
        
        try:
            # 1. Scanne nach Zielen
            targets = self.scan_for_raid_targets()
            
            if not targets:
                self.logger.info("🔍 No suitable raid targets found")
                return False
                
            # 2. Wähle bestes Ziel
            best_target = targets[0]
            self.logger.info(f"🎯 Best target: {best_target['coordinates']} (Score: {best_target['score']})")
            
            # 3. Starte Raid mit kleiner Flotte (sicher)
            success = self.launch_raid(best_target['coordinates'], 5)
            
            if success:
                self.logger.info("✅ Raid launched successfully!")
                # Warte bevor nächster Raid
                time.sleep(300)  # 5 Minuten warten
                return True
            else:
                self.logger.warning("❌ Raid launch failed")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Auto raid cycle error: {e}")
            return False

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class ColonizationManager:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.wait = WebDriverWait(driver, 10)
        
        # Kolonisierungs-Konfiguration
        self.colonization_config = {
            'required_ships': {
                'colony_ship': 1,
                'small_cargo': 20,  # Für Ressourcen-Transport
                'light_fighter': 10  # Für Schutz
            },
            'target_planet_slots': [4, 5, 6, 7, 8],  # Bevorzugte Planeten-Positionen
            'min_planet_size': 150,  # Mindest-Planetengröße
            'max_distance': 50,  # Max Entfernung in Systemen
            'required_resources': {
                'metal': 50000,
                'crystal': 25000, 
                'deuterium': 10000
            }
        }

    def check_colonization_readiness(self, resources):
        """Prüfe ob Kolonisierung möglich ist"""
        self.logger.info("🏛️ === CHECKING COLONIZATION READINESS ===")
        
        try:
            # 1. Prüfe Ressourcen
            if not self.has_sufficient_resources(resources):
                return False, "Insufficient resources"
                
            # 2. Prüfe verfügbare Schiffe
            if not self.has_required_ships():
                return False, "Ships not available"
                
            # 3. Prüfe Kolonie-Slots
            current_colonies = self.count_current_colonies()
            if current_colonies >= 9:
                return False, "Maximum colonies reached"
                
            self.logger.info("✅ Colonization ready!")
            return True, f"Ready with {current_colonies} existing colonies"
            
        except Exception as e:
            self.logger.error(f"❌ Colonization readiness check error: {e}")
            return False, str(e)

    def has_sufficient_resources(self, resources):
        """Prüfe ob genügend Ressourcen vorhanden sind"""
        try:
            metal = int(resources.get('metal', '0') or '0')
            crystal = int(resources.get('crystal', '0') or '0')
            deuterium = int(resources.get('deuterium', '0') or '0')
            
            required = self.colonization_config['required_resources']
            
            if metal >= required['metal'] and crystal >= required['crystal'] and deuterium >= required['deuterium']:
                self.logger.info(f"💰 Resources sufficient: M:{metal} C:{crystal} D:{deuterium}")
                return True
            else:
                self.logger.info(f"💸 Resources insufficient: Need M:{required['metal']} C:{required['crystal']} D:{required['deuterium']}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Resource check error: {e}")
            return False

    def has_required_ships(self):
        """Prüfe ob erforderliche Schiffe vorhanden sind"""
        try:
            # Navigiere zur Flotten-Übersicht
            if not self.navigate_to_fleet_overview():
                return False
                
            # Prüfe verfügbare Schiffe
            available_ships = self.get_available_ships()
            required = self.colonization_config['required_ships']
            
            for ship_type, needed_count in required.items():
                available = available_ships.get(ship_type, 0)
                if available < needed_count:
                    self.logger.info(f"🚢 Ship shortage: {ship_type} - have {available}, need {needed_count}")
                    return False
                    
            self.logger.info("🚢 All required ships available")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Ship check error: {e}")
            return False

    def navigate_to_fleet_overview(self):
        """Navigiere zur Flotten-Übersicht"""
        try:
            fleet_selectors = [
                "//a[contains(@href, 'fleet')]",
                "//a[contains(@href, 'component=fleet')]",
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
                    return True
                except:
                    continue
                    
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Fleet navigation error: {e}")
            return False

    def get_available_ships(self):
        """Hole verfügbare Schiffe"""
        ships = {}
        
        try:
            # Suche nach Schiff-Eingabefeldern oder Anzeigen
            ship_selectors = [
                "input[name*='small']",  # Kleine Transporter
                "input[name*='large']",  # Große Transporter  
                "input[name*='light']",  # Leichte Jäger
                "input[name*='heavy']",  # Schwere Jäger
                "input[name*='colony']", # Kolonieschiff
                ".ship-count",
                "[class*='ship']"
            ]
            
            for selector in ship_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        ship_type, count = self.extract_ship_info(element)
                        if ship_type and count > 0:
                            ships[ship_type] = count
                except:
                    continue
                    
            self.logger.info(f"🚢 Available ships: {ships}")
            return ships
            
        except Exception as e:
            self.logger.error(f"❌ Ship inventory error: {e}")
            return {}

    def extract_ship_info(self, element):
        """Extrahiere Schiff-Typ und Anzahl aus Element"""
        try:
            # Hole verfügbare Anzahl
            max_attr = element.get_attribute('max')
            value_attr = element.get_attribute('value')
            text = element.text
            
            count = 0
            if max_attr and max_attr.isdigit():
                count = int(max_attr)
            elif value_attr and value_attr.isdigit():
                count = int(value_attr)
            elif text and text.isdigit():
                count = int(text)
                
            # Bestimme Schiff-Typ basierend auf Name/ID
            name = element.get_attribute('name') or element.get_attribute('id') or ''
            
            ship_type = None
            if 'small' in name.lower() or 'cargo' in name.lower():
                ship_type = 'small_cargo'
            elif 'large' in name.lower():
                ship_type = 'large_cargo'
            elif 'light' in name.lower() or 'fighter' in name.lower():
                ship_type = 'light_fighter'
            elif 'colony' in name.lower():
                ship_type = 'colony_ship'
                
            return ship_type, count
            
        except:
            return None, 0

    def count_current_colonies(self):
        """Zähle aktuelle Kolonien"""
        try:
            # Suche nach Planeten-Liste oder Dropdown
            planet_selectors = [
                ".planet-list .planet",
                "#planetList option", 
                ".planet-selector option",
                "[class*='planet']"
            ]
            
            colony_count = 0
            
            for selector in planet_selectors:
                try:
                    planets = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if planets:
                        colony_count = len(planets)
                        break
                except:
                    continue
                    
            # Hauptplanet nicht mitzählen
            colony_count = max(0, colony_count - 1)
            
            self.logger.info(f"🏛️ Current colonies: {colony_count}")
            return colony_count
            
        except Exception as e:
            self.logger.error(f"❌ Colony count error: {e}")
            return 0

    def find_colonization_targets(self):
        """Finde geeignete Planeten für Kolonisierung"""
        self.logger.info("🔍 === SEARCHING FOR COLONIZATION TARGETS ===")
        
        try:
            # Navigiere zur Galaxie
            if not self.navigate_to_galaxy():
                return []
                
            targets = []
            
            # Scanne mehrere Systeme nach freien Planeten-Slots
            for system_offset in range(-10, 11):
                try:
                    self.navigate_to_system(system_offset)
                    system_targets = self.scan_system_for_free_slots()
                    targets.extend(system_targets)
                    time.sleep(1)
                except:
                    continue
                    
            # Sortiere nach Attraktivität
            targets.sort(key=lambda x: x.get('score', 0), reverse=True)
            
            self.logger.info(f"🎯 Found {len(targets)} colonization targets")
            return targets[:5]  # Top 5 Ziele
            
        except Exception as e:
            self.logger.error(f"❌ Target search error: {e}")
            return []

    def navigate_to_galaxy(self):
        """Navigiere zur Galaxie"""
        try:
            galaxy_selectors = [
                "//a[contains(@href, 'galaxy')]",
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
                    return True
                except:
                    continue
                    
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Galaxy navigation error: {e}")
            return False

    def navigate_to_system(self, offset=0):
        """Navigiere zu System"""
        try:
            system_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='system'], #system")
            current_system = int(system_input.get_attribute('value') or '1')
            new_system = max(1, current_system + offset)
            
            system_input.clear()
            system_input.send_keys(str(new_system))
            
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit'], .submit")
            submit_btn.click()
            time.sleep(2)
            return True
            
        except Exception as e:
            self.logger.error(f"❌ System navigation error: {e}")
            return False

    def scan_system_for_free_slots(self):
        """Scanne System nach freien Planeten-Slots"""
        targets = []
        
        try:
            # Suche nach Planeten-Positionen
            preferred_slots = self.colonization_config['target_planet_slots']
            
            for slot in preferred_slots:
                try:
                    # Prüfe ob Slot frei ist
                    slot_element = self.driver.find_element(By.XPATH, f"//td[contains(@class, 'position-{slot}') or text()='{slot}']")
                    
                    # Prüfe ob Slot leer ist (kein Planet)
                    if self.is_slot_empty(slot_element):
                        # Hole System-Koordinaten
                        coords = self.get_current_system_coords()
                        target_coords = f"{coords}:{slot}"
                        
                        target_info = {
                            'coordinates': target_coords,
                            'slot': slot,
                            'score': self.calculate_colonization_score(slot, coords),
                            'system_coords': coords
                        }
                        
                        targets.append(target_info)
                        self.logger.info(f"🆓 Found free slot: {target_coords}")
                        
                except:
                    continue
                    
            return targets
            
        except Exception as e:
            self.logger.error(f"❌ System scan error: {e}")
            return []

    def is_slot_empty(self, slot_element):
        """Prüfe ob Planeten-Slot leer ist"""
        try:
            # Suche nach Indikatoren für besetzten Slot
            occupied_indicators = [
                ".planet", ".occupied", 
                "img[src*='planet']",
                "[class*='planet']"
            ]
            
            for indicator in occupied_indicators:
                if slot_element.find_elements(By.CSS_SELECTOR, indicator):
                    return False
                    
            # Prüfe Text-Inhalt
            text = slot_element.text.strip()
            if text and len(text) > 2:  # Wenn Text vorhanden, wahrscheinlich besetzt
                return False
                
            return True
            
        except:
            return False

    def get_current_system_coords(self):
        """Hole aktuelle System-Koordinaten"""
        try:
            # Suche nach Koordinaten-Anzeigen
            coord_selectors = [
                ".coordinates", 
                "#coordinates",
                "input[name='galaxy']",
                "input[name='system']"
            ]
            
            galaxy = "1"
            system = "1"
            
            # Versuche Galaxie zu finden
            try:
                galaxy_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='galaxy']")
                galaxy = galaxy_input.get_attribute('value') or "1"
            except:
                pass
                
            # Versuche System zu finden
            try:
                system_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='system']")
                system = system_input.get_attribute('value') or "1"
            except:
                pass
                
            return f"{galaxy}:{system}"
            
        except Exception as e:
            self.logger.error(f"❌ Coordinate extraction error: {e}")
            return "1:1"

    def calculate_colonization_score(self, slot, system_coords):
        """Berechne Score für Kolonisierungs-Ziel"""
        score = 0
        
        # Bevorzuge bestimmte Slots
        preferred_slots = [4, 5, 6, 7, 8]
        if slot in preferred_slots:
            score += 20
            
        # Bevorzuge mittlere Slots (bessere Temperatur)
        if 4 <= slot <= 9:
            score += 10
            
        # Entfernung zum Haupt-System (näher ist besser)
        try:
            galaxy, system = system_coords.split(':')
            # Annahme: Haupt-Planet ist in System 1-100
            system_distance = abs(int(system) - 50)  # Basis-System als Referenz
            score -= min(system_distance, 30)  # Max 30 Punkte Abzug
        except:
            pass
            
        return max(0, score)

    def launch_colonization_fleet(self, target_coords):
        """Starte Kolonisierungs-Flotte"""
        self.logger.info(f"🚀 === LAUNCHING COLONIZATION TO {target_coords} ===")
        
        try:
            # Navigiere zur Flotte
            if not self.navigate_to_fleet_overview():
                return False
                
            # Wähle Schiffe für Kolonisierung
            if not self.select_colonization_ships():
                return False
                
            # Setze Ziel
            if not self.set_target_coordinates(target_coords):
                return False
                
            # Wähle Kolonisierungs-Mission
            if not self.select_colonization_mission():
                return False
                
            # Bestätige Start
            return self.confirm_colonization_launch()
            
        except Exception as e:
            self.logger.error(f"❌ Colonization launch error: {e}")
            return False

    def select_colonization_ships(self):
        """Wähle Schiffe für Kolonisierung"""
        try:
            required = self.colonization_config['required_ships']
            
            # Kolonieschiff auswählen
            colony_ship_input = self.driver.find_element(By.CSS_SELECTOR, "input[name*='colony']")
            colony_ship_input.clear()
            colony_ship_input.send_keys("1")
            
            # Transporter für Ressourcen
            cargo_input = self.driver.find_element(By.CSS_SELECTOR, "input[name*='small']")
            cargo_input.clear()
            cargo_input.send_keys(str(required['small_cargo']))
            
            # Jäger für Schutz
            try:
                fighter_input = self.driver.find_element(By.CSS_SELECTOR, "input[name*='light']")
                fighter_input.clear()
                fighter_input.send_keys(str(required['light_fighter']))
            except:
                pass  # Jäger optional
                
            self.logger.info("🚢 Colonization fleet selected")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Ship selection error: {e}")
            return False

    def set_target_coordinates(self, coords):
        """Setze Ziel-Koordinaten"""
        try:
            galaxy, system, planet = coords.split(':')
            
            coord_inputs = {
                'galaxy': galaxy,
                'system': system, 
                'planet': planet
            }
            
            for field, value in coord_inputs.items():
                try:
                    coord_input = self.driver.find_element(By.CSS_SELECTOR, f"input[name='{field}']")
                    coord_input.clear()
                    coord_input.send_keys(value)
                except:
                    continue
                    
            self.logger.info(f"🎯 Colonization target set: {coords}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Target setting error: {e}")
            return False

    def select_colonization_mission(self):
        """Wähle Kolonisierungs-Mission"""
        try:
            # Mission 7 ist normalerweise Kolonisierung
            mission_selectors = [
                "input[value='7']",
                "input[name='mission'][value='7']",
                ".mission-colonize"
            ]
            
            for selector in mission_selectors:
                try:
                    mission_radio = self.driver.find_element(By.CSS_SELECTOR, selector)
                    mission_radio.click()
                    self.logger.info("🏛️ Colonization mission selected")
                    return True
                except:
                    continue
                    
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Mission selection error: {e}")
            return False

    def confirm_colonization_launch(self):
        """Bestätige Kolonisierungs-Start"""
        try:
            confirm_selectors = [
                "input[value='Senden']",
                "input[type='submit']",
                ".send-fleet"
            ]
            
            for selector in confirm_selectors:
                try:
                    confirm_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                    confirm_btn.click()
                    self.logger.info("🏛️ Colonization fleet launched!")
                    return True
                except:
                    continue
                    
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Colonization confirmation error: {e}")
            return False

    def auto_colonization_cycle(self, resources):
        """Vollautomatischer Kolonisierungs-Zyklus"""
        self.logger.info("🏛️ === AUTO COLONIZATION CYCLE ===")
        
        try:
            # 1. Prüfe Bereitschaft
            ready, reason = self.check_colonization_readiness(resources)
            
            if not ready:
                self.logger.info(f"🚫 Colonization not ready: {reason}")
                return False
                
            # 2. Finde Ziele
            targets = self.find_colonization_targets()
            
            if not targets:
                self.logger.info("🔍 No colonization targets found")
                return False
                
            # 3. Wähle bestes Ziel
            best_target = targets[0]
            self.logger.info(f"🎯 Best colonization target: {best_target['coordinates']} (Score: {best_target['score']})")
            
            # 4. Starte Kolonisierung
            success = self.launch_colonization_fleet(best_target['coordinates'])
            
            if success:
                self.logger.info("🎉 Colonization fleet launched successfully!")
                return True
            else:
                self.logger.warning("❌ Colonization launch failed")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Auto colonization error: {e}")
            return False

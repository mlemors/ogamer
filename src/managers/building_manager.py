import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BuildingManager:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.wait = WebDriverWait(driver, 10)
        
        # Aufbau-Strategie: Prioritäten der Gebäude
        self.building_priority = {
            # Grundlagen zuerst
            'metallmine': 1,
            'kristallmine': 2, 
            'deuteriumsynthetisierer': 3,
            'solarkraftwerk': 4,
            
            # Dann Infrastruktur
            'roboterfabrik': 5,
            'nanofabrik': 6,
            'forschungslabor': 7,
            'metallspeicher': 8,
            'kristallspeicher': 9,
            'deuteriumtank': 10,
            
            # Militär später
            'raumschiffwerft': 11,
            'raketenwerfer': 12,
            'verteidigungsanlagen': 13
        }
        
        # Mindest-Level für Gebäude
        self.minimum_levels = {
            'metallmine': 15,
            'kristallmine': 12,
            'deuteriumsynthetisierer': 10,
            'solarkraftwerk': 12,
            'roboterfabrik': 8,
            'forschungslabor': 5
        }
        
    def navigate_to_buildings(self):
        """Navigate to buildings page"""
        try:
            # Look for buildings tab/link
            buildings_selectors = [
                "//a[contains(@href, 'buildings')]",
                "//a[contains(@href, 'component=buildings')]",
                "//span[contains(text(), 'Gebäude')]/parent::a",
                "#buildings",
                ".buildings"
            ]
            
            for selector in buildings_selectors:
                try:
                    if selector.startswith("//"):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    element.click()
                    time.sleep(2)
                    self.logger.info("Navigated to buildings page")
                    return True
                except:
                    continue
                    
            self.logger.warning("Could not find buildings navigation")
            return False
            
        except Exception as e:
            self.logger.error(f"Error navigating to buildings: {e}")
            return False
            
    def get_buildable_buildings(self):
        """Get list of buildings that can be built"""
        buildable = []
        
        try:
            # Common selectors for build buttons
            build_selectors = [
                "//a[contains(@class, 'build-it')]",
                "//a[contains(@class, 'build_link')]",
                "//button[contains(@class, 'build')]",
                ".build-it",
                ".fastBuild"
            ]
            
            for selector in build_selectors:
                try:
                    if selector.startswith("//"):
                        elements = self.driver.find_elements(By.XPATH, selector)
                    else:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        
                    for element in elements:
                        building_info = self.extract_building_info(element)
                        if building_info:
                            buildable.append(building_info)
                            
                except:
                    continue
                    
            return buildable
            
        except Exception as e:
            self.logger.error(f"Error getting buildable buildings: {e}")
            return []
            
    def extract_building_info(self, element):
        """Extract building information from element"""
        try:
            # Try to get building name and info
            title = element.get_attribute("title") or ""
            onclick = element.get_attribute("onclick") or ""
            
            # Try to find building name in various ways
            building_name = "Unknown Building"
            
            # Check parent elements for building info
            parent = element.find_element(By.XPATH, "./..")
            grandparent = parent.find_element(By.XPATH, "./..")
            
            # Look for building name in nearby elements
            name_elements = grandparent.find_elements(By.CSS_SELECTOR, ".building_name, .buildingName, h3, .title")
            
            if name_elements:
                building_name = name_elements[0].text.strip()
            elif title:
                building_name = title
                
            return {
                'name': building_name,
                'element': element,
                'title': title,
                'onclick': onclick
            }
            
        except:
            return None
            
    def smart_planet_development(self, resources):
        """Intelligente Planeten-Entwicklung basierend auf Ressourcen und Strategie"""
        self.logger.info("🏗️ === SMART PLANET DEVELOPMENT ===")
        
        try:
            # 1. Prüfe aktuellen Gebäude-Status
            current_buildings = self.get_current_building_levels()
            
            # 2. Bestimme nächstes zu bauendes Gebäude
            next_building = self.determine_next_building(current_buildings, resources)
            
            if next_building:
                self.logger.info(f"🎯 Target building: {next_building}")
                
                # 3. Navigiere zu Gebäuden und baue
                if self.navigate_to_buildings():
                    return self.build_specific_building(next_building)
                else:
                    return self.build_from_overview(next_building)
            else:
                self.logger.info("✅ No immediate building needed")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Smart development error: {e}")
            return False

    def get_current_building_levels(self):
        """Versuche aktuelle Gebäude-Level zu ermitteln"""
        buildings = {}
        
        try:
            # Suche nach Gebäude-Level Anzeigen auf der Übersichtsseite
            level_selectors = [
                ".level",
                ".building-level", 
                "[class*='level']",
                ".lvl"
            ]
            
            for selector in level_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for elem in elements:
                        text = elem.text.strip()
                        if text.isdigit():
                            # Versuche Gebäudename zu finden
                            parent = elem.find_element(By.XPATH, "./..")
                            building_name = self.extract_building_name_from_element(parent)
                            if building_name:
                                buildings[building_name.lower()] = int(text)
                except:
                    continue
                    
            self.logger.info(f"📊 Current buildings: {buildings}")
            return buildings
            
        except Exception as e:
            self.logger.error(f"❌ Error getting building levels: {e}")
            return {}

    def determine_next_building(self, current_buildings, resources):
        """Bestimme das nächste zu bauende Gebäude basierend auf Strategie"""
        
        # Konvertiere Ressourcen zu Zahlen
        metal = int(resources.get('metal', '0') or '0')
        crystal = int(resources.get('crystal', '0') or '0')
        deuterium = int(resources.get('deuterium', '0') or '0')
        
        self.logger.info(f"💰 Available: Metal: {metal}, Crystal: {crystal}, Deuterium: {deuterium}")
        
        # Einfache Logik: Baue basierend auf Ressourcen-Mangel
        if metal < 1000 and crystal < 1000:
            return 'metallmine'  # Mehr Metall brauchen
        elif crystal < 500:
            return 'kristallmine'  # Mehr Kristall brauchen  
        elif deuterium < 200:
            return 'deuteriumsynthetisierer'  # Mehr Deuterium brauchen
        elif metal > 2000 and crystal > 1000:
            # Genug Ressourcen für fortgeschrittene Gebäude
            return 'roboterfabrik'  # Schnellere Bauzeiten
        else:
            return 'solarkraftwerk'  # Mehr Energie
            
    def build_from_overview(self, building_name):
        """Versuche von der Übersichtsseite aus zu bauen"""
        try:
            self.logger.info(f"🔍 Looking for {building_name} on overview page...")
            
            # Suche nach Gebäude-Namen oder Build-Buttons
            name_selectors = [
                f"//span[contains(text(), '{building_name}')]",
                f"//div[contains(text(), '{building_name}')]",
                f"//a[contains(@title, '{building_name}')]"
            ]
            
            for selector in name_selectors:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    
                    # Suche nach Build-Button in der Nähe
                    parent = element.find_element(By.XPATH, "./..")
                    build_button = parent.find_element(By.CSS_SELECTOR, ".build-it, .fastBuild, [onclick*='build']")
                    
                    self.logger.info(f"🔨 Found build button for {building_name}")
                    build_button.click()
                    time.sleep(2)
                    return True
                    
                except:
                    continue
                    
            # Fallback: Baue irgendwas verfügbares
            return self.build_any_available()
            
        except Exception as e:
            self.logger.error(f"❌ Build from overview error: {e}")
            return False

    def build_specific_building(self, building_name):
        """Baue ein spezifisches Gebäude"""
        try:
            buildable = self.get_buildable_buildings()
            
            # Suche nach dem gewünschten Gebäude
            for building in buildable:
                if building_name.lower() in building['name'].lower():
                    self.logger.info(f"🎯 Found target: {building['name']}")
                    return self.build_building(building)
                    
            # Wenn spezifisches Gebäude nicht verfügbar, baue erstes verfügbares
            if buildable:
                self.logger.info(f"⚠️ {building_name} not available, building: {buildable[0]['name']}")
                return self.build_building(buildable[0])
                
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Build specific error: {e}")
            return False

    def build_any_available(self):
        """Baue das erste verfügbare Gebäude"""
        try:
            buildable = self.get_buildable_buildings()
            
            if buildable:
                building = buildable[0]
                self.logger.info(f"🔨 Building first available: {building['name']}")
                return self.build_building(building)
            else:
                self.logger.info("ℹ️ No buildings available to build")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Build any available error: {e}")
            return False

    def build_building(self, building_info):
        """Baue ein Gebäude basierend auf building_info"""
        try:
            self.logger.info(f"🏗️ Starting construction: {building_info['name']}")
            
            # Klicke Build-Button
            building_info['element'].click()
            time.sleep(2)
            
            # Suche nach Bestätigungs-Button
            confirm_selectors = [
                "//input[@value='Bauen']",
                "//button[contains(text(), 'Bauen')]", 
                "//a[contains(text(), 'Bauen')]",
                "//input[contains(@value, 'Build')]",
                ".build_submit",
                ".confirm"
            ]
            
            for selector in confirm_selectors:
                try:
                    if selector.startswith("//"):
                        confirm_btn = self.driver.find_element(By.XPATH, selector)
                    else:
                        confirm_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                    confirm_btn.click()
                    self.logger.info(f"✅ Construction confirmed: {building_info['name']}")
                    time.sleep(3)  # Warte auf Bestätigung
                    return True
                except:
                    continue
                    
            # Kein Bestätigungs-Button gefunden - möglicherweise bereits bestätigt
            self.logger.info(f"✅ Construction initiated: {building_info['name']}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Build building error: {e}")
            return False

    def extract_building_name_from_element(self, element):
        """Extrahiere Gebäude-Namen aus einem Element"""
        try:
            # Verschiedene Wege um Namen zu finden
            name_sources = [
                element.text,
                element.get_attribute("title"),
                element.get_attribute("alt"),
                element.get_attribute("data-building")
            ]
            
            for name in name_sources:
                if name and len(name) > 2:
                    return name.strip()
                    
            return None
            
        except:
            return None

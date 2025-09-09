#!/usr/bin/env python3
"""
🤖 OGame Full Automation Bot
==========================

EINZIGER STARTPUNKT für den kompletten OGame Bot!

Features:
- ✅ Automatischer Planeten-Aufbau
- ✅ Vollautomatisches Raiding
- ✅ Kolonisierung (zweite Kolonie)
- ✅ Intelligente Strategien
- ✅ 24/7 Betrieb möglich

Usage:
    python3 ogame_bot.py

Das wars! Alles andere läuft automatisch.
"""

import os
import sys
import time
import logging
import requests
import signal
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Selenium imports
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.chrome.options import Options
except ImportError:
    print("❌ Selenium not installed!")
    print("Installing selenium...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium", "webdriver-manager", "requests"])
    
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.chrome.options import Options

# Import our managers
try:
    from src.managers.building_manager import BuildingManager
    from src.managers.fleet_manager import FleetManager
    from src.managers.colonization_manager import ColonizationManager
    from src.managers.resource_manager import ResourceManager
except ImportError as e:
    print(f"❌ Manager import error: {e}")
    print("Make sure all files are in the correct folders!")
    sys.exit(1)

class OGameBot:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.setup_logging()
        
    class OGameFullBot:
    """
    🚀 VOLLAUTOMATISCHER OGAME BOT
    
    Der ultimative Bot für:
    - Planeten-Aufbau
    - Ressourcen-Farming durch Raids
    - Automatische Kolonisierung
    """
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.managers = {}
        self.running = True
        
        # Setup logging
        self.setup_logging()
        
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        
        self.logger.info("🤖 OGame Full Automation Bot initialized")

    def setup_logging(self):
        """Setup comprehensive logging"""
        log_dir = project_root / "logs"
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / "ogame_bot.log"
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Setup file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        
        # Setup console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        
        # Setup logger
        self.logger = logging.getLogger('OGameBot')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Clear any existing handlers to avoid duplicates
        self.logger.handlers = [file_handler, console_handler]

    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        self.logger.info("👋 Shutdown signal received...")
        self.running = False

    def find_browser_with_debugging(self):
        """Find browser with remote debugging enabled"""
        self.logger.info("🔍 Searching for browser with remote debugging...")
        
        ports_to_try = [9223, 9222, 9224, 9225]
        
        for port in ports_to_try:
            try:
                response = requests.get(f"http://localhost:{port}/json", timeout=2)
                if response.status_code == 200:
                    tabs = response.json()
                    self.logger.info(f"✅ Found browser on port {port} with {len(tabs)} tabs")
                    
                    # Check for OGame tabs
                    for tab in tabs:
                        url = tab.get('url', '')
                        title = tab.get('title', '')
                        if 'ogame' in url.lower() or 'ogame' in title.lower():
                            self.logger.info(f"🎮 Found OGame tab: {title}")
                            
                    return port
                    
            except requests.exceptions.ConnectionError:
                continue
            except Exception as e:
                self.logger.debug(f"Port {port} check failed: {e}")
                continue
                
        return None

    def start_browser_if_needed(self):
        """Start browser with remote debugging if not running"""
        port = self.find_browser_with_debugging()
        
        if port:
            self.logger.info(f"✅ Browser already running on port {port}")
            return port
            
        self.logger.info("🚀 Starting new browser with remote debugging...")
        
        # Try to start Brave Browser
        brave_cmd = [
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
            "--remote-debugging-port=9223",
            "--user-data-dir=/tmp/ogame-bot-profile",
            "--no-first-run",
            "--disable-features=VizDisplayCompositor"
        ]
        
        try:
            import subprocess
            process = subprocess.Popen(
                brave_cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Wait for browser to start
            time.sleep(5)
            
            # Check if it started successfully
            port = self.find_browser_with_debugging()
            if port:
                self.logger.info("✅ Browser started successfully!")
                return port
            else:
                self.logger.error("❌ Browser started but remote debugging not available")
                return None
                
        except Exception as e:
            self.logger.error(f"❌ Failed to start browser: {e}")
            return None

    def connect_to_browser(self, port):
        """Connect to browser via remote debugging"""
        try:
            options = Options()
            options.add_experimental_option("debuggerAddress", f"localhost:{port}")
            
            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 30)
            
            self.logger.info(f"✅ Connected to browser on port {port}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Browser connection failed: {e}")
            return False

    def initialize_managers(self):
        """Initialize all bot managers"""
        try:
            self.managers = {
                'building': BuildingManager(self.driver, self.logger),
                'fleet': FleetManager(self.driver, self.logger),
                'colonization': ColonizationManager(self.driver, self.logger),
                'resource': ResourceManager(self.driver, self.logger)
            }
            
            self.logger.info("✅ All managers initialized")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Manager initialization failed: {e}")
            return False

    def find_ogame_tab(self):
        """Find and switch to OGame tab"""
        try:
            handles = self.driver.window_handles
            
            for handle in handles:
                self.driver.switch_to.window(handle)
                url = self.driver.current_url
                title = self.driver.title
                
                if any(keyword in url.lower() for keyword in ['ogame', 'gameforge']):
                    self.logger.info(f"🎮 Switched to OGame tab: {title}")
                    return True
                    
            self.logger.warning("⚠️ No OGame tab found")
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Tab switching error: {e}")
            return False

    def wait_for_ogame_login(self):
        """Wait for user to log in to OGame"""
        self.logger.info("⏳ Please log in to OGame and navigate to your planet overview...")
        self.logger.info("   The bot will start automatically when you're in the game!")
        
        while self.running:
            try:
                if self.find_ogame_tab():
                    url = self.driver.current_url
                    if any(indicator in url.lower() for indicator in ['component=overview', 'page=ingame', 'game/index']):
                        self.logger.info("🎮 Game detected! Starting automation...")
                        return True
                        
                time.sleep(3)
                
            except Exception as e:
                self.logger.debug(f"Login check error: {e}")
                time.sleep(3)
                
        return False

    def get_empire_status(self):
        """Get comprehensive empire status"""
        try:
            # Get resources
            resources = self.managers['resource'].get_resources()
            
            metal = int(resources.get('metal', '0') or '0')
            crystal = int(resources.get('crystal', '0') or '0')
            deuterium = int(resources.get('deuterium', '0') or '0')
            total_resources = metal + crystal + deuterium
            
            # Get colonies count
            current_colonies = 0
            if self.managers['colonization']:
                current_colonies = self.managers['colonization'].count_current_colonies()
            
            status = {
                'resources': resources,
                'total_resources': total_resources,
                'colonies': current_colonies,
                'ready_for_building': metal >= 500 or crystal >= 250,
                'ready_for_raids': metal >= 1000 and crystal >= 500,
                'ready_for_colonization': metal >= 50000 and crystal >= 25000 and deuterium >= 10000
            }
            
            self.logger.info("📊 === EMPIRE STATUS ===")
            self.logger.info(f"💰 Resources: M:{metal:,} C:{crystal:,} D:{deuterium:,} (Total: {total_resources:,})")
            self.logger.info(f"🏛️ Colonies: {current_colonies}")
            self.logger.info(f"🏗️ Building Ready: {status['ready_for_building']}")
            self.logger.info(f"🏴‍☠️ Raid Ready: {status['ready_for_raids']}")
            self.logger.info(f"🌟 Colonization Ready: {status['ready_for_colonization']}")
            
            return status
            
        except Exception as e:
            self.logger.error(f"❌ Empire status error: {e}")
            return {}

    def execute_automation_cycle(self):
        """Execute one complete automation cycle"""
        self.logger.info("🤖 === FULL AUTOMATION CYCLE ===")
        
        try:
            # Ensure we're on the right page
            if not self.find_ogame_tab():
                self.logger.warning("⚠️ Lost OGame connection!")
                return False
                
            # Get current status
            empire_status = self.get_empire_status()
            
            if not empire_status:
                self.logger.error("❌ Could not get empire status")
                return False
                
            # === PHASE 1: BUILDING DEVELOPMENT ===
            self.logger.info("🏗️ === PHASE 1: BUILDING ===")
            if empire_status.get('ready_for_building', False):
                try:
                    building_success = self.managers['building'].smart_planet_development(empire_status['resources'])
                    if building_success:
                        self.logger.info("✅ Building construction started!")
                except Exception as e:
                    self.logger.error(f"❌ Building phase error: {e}")
            
            # === PHASE 2: RAIDING ===
            self.logger.info("🏴‍☠️ === PHASE 2: RAIDING ===")
            if empire_status.get('ready_for_raids', False):
                try:
                    raid_success = self.managers['fleet'].auto_raid_cycle()
                    if raid_success:
                        self.logger.info("✅ Raid launched successfully!")
                except Exception as e:
                    self.logger.error(f"❌ Raiding phase error: {e}")
            else:
                self.logger.info("💰 Not enough resources for raiding yet")
            
            # === PHASE 3: COLONIZATION ===
            self.logger.info("🏛️ === PHASE 3: COLONIZATION ===")
            if empire_status.get('ready_for_colonization', False):
                try:
                    colonization_success = self.managers['colonization'].auto_colonization_cycle(empire_status['resources'])
                    if colonization_success:
                        self.logger.info("🌟 Colonization fleet launched!")
                except Exception as e:
                    self.logger.error(f"❌ Colonization phase error: {e}")
            else:
                # Show progress towards colonization
                resources = empire_status['resources']
                metal = int(resources.get('metal', '0') or '0')
                crystal = int(resources.get('crystal', '0') or '0')
                deuterium = int(resources.get('deuterium', '0') or '0')
                
                metal_needed = max(0, 50000 - metal)
                crystal_needed = max(0, 25000 - crystal)
                deuterium_needed = max(0, 10000 - deuterium)
                
                if metal_needed > 0 or crystal_needed > 0 or deuterium_needed > 0:
                    self.logger.info(f"💾 Saving for colonization - Need: M:{metal_needed:,} C:{crystal_needed:,} D:{deuterium_needed:,}")
            
            self.logger.info("✅ === AUTOMATION CYCLE COMPLETE ===")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Automation cycle error: {e}")
            return False

    def calculate_next_cycle_delay(self, empire_status):
        """Calculate adaptive delay for next cycle"""
        if empire_status.get('ready_for_colonization', False):
            return 180  # 3 minutes - aggressive when ready for big moves
        elif empire_status.get('ready_for_raids', False):
            return 300  # 5 minutes - active mode
        elif empire_status.get('ready_for_building', False):
            return 420  # 7 minutes - building mode
        else:
            return 600  # 10 minutes - waiting mode

    def run_main_loop(self):
        """Main automation loop"""
        self.logger.info("🚀 === STARTING MAIN AUTOMATION LOOP ===")
        
        cycle = 1
        
        while self.running:
            try:
                self.logger.info(f"🔄 === CYCLE #{cycle} ===")
                
                # Get empire status
                empire_status = self.get_empire_status()
                
                # Execute automation
                success = self.execute_automation_cycle()
                
                if success:
                    cycle += 1
                    
                    # Calculate adaptive delay
                    delay = self.calculate_next_cycle_delay(empire_status)
                    
                    if empire_status.get('ready_for_colonization', False):
                        self.logger.info(f"🚀 TURBO MODE - Next cycle in {delay//60} minutes")
                    elif empire_status.get('ready_for_raids', False):
                        self.logger.info(f"⚔️ ACTIVE MODE - Next cycle in {delay//60} minutes")
                    else:
                        self.logger.info(f"🏗️ BUILDING MODE - Next cycle in {delay//60} minutes")
                    
                    # Sleep with periodic status updates
                    self.sleep_with_updates(delay)
                else:
                    self.logger.warning("⚠️ Cycle failed, retrying in 5 minutes...")
                    self.sleep_with_updates(300)
                    
            except KeyboardInterrupt:
                self.logger.info("👋 Shutdown requested by user")
                break
            except Exception as e:
                self.logger.error(f"❌ Main loop error: {e}")
                self.logger.info("⏳ Waiting 5 minutes before retry...")
                self.sleep_with_updates(300)

    def sleep_with_updates(self, total_seconds):
        """Sleep with periodic status updates"""
        update_interval = 60  # Update every minute
        elapsed = 0
        
        while elapsed < total_seconds and self.running:
            time.sleep(min(update_interval, total_seconds - elapsed))
            elapsed += update_interval
            
            if elapsed < total_seconds:
                remaining = total_seconds - elapsed
                self.logger.info(f"😴 Sleeping... {remaining//60}m {remaining%60}s remaining")

    def cleanup(self):
        """Clean up resources"""
        try:
            if self.driver:
                self.logger.info("🔚 Bot finished (browser stays open for your use)")
                # Don't quit driver - leave browser open for user
        except:
            pass

    def print_startup_banner(self):
        """Print impressive startup banner"""
        banner = """
🤖 ===================================================================
🚀                     OGAME FULL AUTOMATION BOT                    🚀
🏴‍☠️ ===================================================================

🎯 MISSION: Fastest path to second colony through:
   ✅ Automated planet development
   ✅ Intelligent raiding operations  
   ✅ Strategic colonization planning

📋 FEATURES:
   🏗️  Smart building priorities based on resources
   ⚔️  Automated raid scanning and execution
   🏛️  Colony ship deployment and management
   📊 Adaptive timing based on empire status

⚠️  IMPORTANT:
   🌐 Login to OGame manually after browser opens
   📍 Navigate to your planet overview page
   🤖 Bot will detect game and start automatically

🎮 Expected Results:
   📈 3-5x faster resource growth
   ⏱️  Colony ready in 3-7 days (vs 2-4 weeks)
   🏆 Complete automation 24/7

===================================================================
"""
        print(banner)

    def start(self):
        """Main entry point - start the complete automation"""
        try:
            self.print_startup_banner()
            
            # Step 1: Find or start browser
            port = self.start_browser_if_needed()
            if not port:
                self.logger.error("❌ Could not start or find browser!")
                return False
                
            # Step 2: Connect to browser
            if not self.connect_to_browser(port):
                return False
                
            # Step 3: Initialize managers
            if not self.initialize_managers():
                return False
                
            # Step 4: Wait for OGame login
            if not self.wait_for_ogame_login():
                return False
                
            # Step 5: Start main automation loop
            self.run_main_loop()
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Critical startup error: {e}")
            return False
        finally:
            self.cleanup()

def main():
    """Main function"""
    bot = OGameFullBot()
    success = bot.start()
    
    if not success:
        print("
❌ Bot failed to start properly!")
        print("Check the logs in logs/ogame_bot.log for details.")
        sys.exit(1)
    else:
        print("
✅ Bot finished successfully!")

if __name__ == "__main__":
    main()
        
    def setup_browser(self):
        """Initialize the Chrome browser with optimal settings"""
        self.logger.info("Setting up browser...")
        
        chrome_options = Options()
        
        # Browser settings
        if config.BROWSER_HEADLESS:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument(f"--window-size={config.BROWSER_WINDOW_SIZE[0]},{config.BROWSER_WINDOW_SIZE[1]}")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User agent to avoid detection
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        try:
            # Try to use Brave browser first
            brave_paths = [
                "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
                "/usr/bin/brave-browser",
                "/opt/brave.com/brave/brave-browser"
            ]
            
            brave_found = False
            for brave_path in brave_paths:
                if os.path.exists(brave_path):
                    chrome_options.binary_location = brave_path
                    self.logger.info(f"Found Brave at: {brave_path}")
                    brave_found = True
                    break
            
            if brave_found:
                try:
                    # Try with system chromedriver first
                    self.driver = webdriver.Chrome(options=chrome_options)
                    self.logger.info("✅ Using Brave Browser!")
                except:
                    # Try with ChromeDriverManager
                    service = Service(ChromeDriverManager().install())
                    self.driver = webdriver.Chrome(service=service, options=chrome_options)
                    self.logger.info("✅ Using Brave Browser with downloaded driver!")
            else:
                self.logger.info("Brave not found, trying Chrome...")
                # Fallback to Chrome
                try:
                    self.driver = webdriver.Chrome(options=chrome_options)
                except:
                    service = Service(ChromeDriverManager().install())
                    self.driver = webdriver.Chrome(service=service, options=chrome_options)
                    
        except Exception as e:
            self.logger.error(f"Brave/Chrome failed: {e}")
            self.logger.info("Trying Safari WebDriver as fallback...")
            
            # Ultimate fallback to Safari
            try:
                self.driver = webdriver.Safari()
                self.logger.info("Using Safari WebDriver")
            except Exception as e3:
                self.logger.error(f"Safari also failed: {e3}")
                raise Exception("No working browser found. Please install Brave/Chrome or enable Safari WebDriver.")
        
        # Execute script to remove webdriver property (if supported)
        try:
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except:
            pass  # Some browsers don't support this
        
        self.wait = WebDriverWait(self.driver, config.BROWSER_TIMEOUT)
        self.logger.info("Browser setup completed")
        
    def navigate_to_ogame(self):
        """Navigate to OGame login page"""
        self.logger.info("Navigating to OGame...")
        self.driver.get(config.OGAME_LOGIN_URL)
        time.sleep(3)
        
    def wait_for_manual_login(self):
        """Wait for user to manually log in and navigate to game"""
        self.logger.info("Please log in manually and navigate to the game overview page.")
        self.logger.info("The bot will detect when you're on the overview page and start working.")
        
        # Wait until we're on the game overview page
        while True:
            try:
                current_url = self.driver.current_url
                if "component=overview" in current_url or "page=ingame" in current_url:
                    self.logger.info("Game overview page detected! Starting bot...")
                    break
                else:
                    time.sleep(2)
            except Exception as e:
                self.logger.error(f"Error checking URL: {e}")
                time.sleep(2)
                
    def get_resources(self):
        """Get current resource amounts"""
        try:
            resources = {}
            
            # Try to find resource elements
            metal_elem = self.driver.find_element(By.ID, "resources_metal")
            crystal_elem = self.driver.find_element(By.ID, "resources_crystal")
            deuterium_elem = self.driver.find_element(By.ID, "resources_deuterium")
            energy_elem = self.driver.find_element(By.ID, "resources_energy")
            
            resources['metal'] = metal_elem.text.replace('.', '').replace(',', '')
            resources['crystal'] = crystal_elem.text.replace('.', '').replace(',', '')
            resources['deuterium'] = deuterium_elem.text.replace('.', '').replace(',', '')
            resources['energy'] = energy_elem.text.replace('.', '').replace(',', '')
            
            self.logger.info(f"Resources: Metal: {resources['metal']}, Crystal: {resources['crystal']}, Deuterium: {resources['deuterium']}, Energy: {resources['energy']}")
            return resources
            
        except Exception as e:
            self.logger.error(f"Error getting resources: {e}")
            return None
            
    def check_buildings(self):
        """Check what buildings can be built"""
        try:
            # Navigate to buildings page
            buildings_link = self.driver.find_element(By.XPATH, "//a[contains(@href, 'buildings')]")
            buildings_link.click()
            time.sleep(2)
            
            self.logger.info("Checking available buildings...")
            
            # Find all buildable items
            build_buttons = self.driver.find_elements(By.XPATH, "//a[contains(@class, 'build-it')]")
            
            if build_buttons:
                self.logger.info(f"Found {len(build_buttons)} buildable items")
                for i, button in enumerate(build_buttons[:3]):  # Only check first 3
                    try:
                        building_name = button.get_attribute("title") or f"Building {i+1}"
                        self.logger.info(f"Can build: {building_name}")
                    except:
                        pass
            else:
                self.logger.info("No buildings can be built right now")
                
        except Exception as e:
            self.logger.error(f"Error checking buildings: {e}")
            
    def run_bot_cycle(self):
        """Run one cycle of bot operations"""
        self.logger.info("=== Starting bot cycle ===")
        
        # Get current resources
        resources = self.get_resources()
        
        # Check buildings if auto-build is enabled
        if config.AUTO_BUILD:
            self.check_buildings()
            
        # Add more bot operations here
        
        self.logger.info("=== Bot cycle completed ===")
        
    def start(self):
        """Start the bot"""
        try:
            self.setup_browser()
            self.navigate_to_ogame()
            self.wait_for_manual_login()
            
            # Main bot loop
            while True:
                try:
                    self.run_bot_cycle()
                    self.logger.info(f"Sleeping for {config.CHECK_INTERVAL} seconds...")
                    time.sleep(config.CHECK_INTERVAL)
                    
                except KeyboardInterrupt:
                    self.logger.info("Bot stopped by user")
                    break
                except Exception as e:
                    self.logger.error(f"Error in bot cycle: {e}")
                    time.sleep(10)  # Wait before retrying
                    
        except Exception as e:
            self.logger.error(f"Critical error: {e}")
        finally:
            self.cleanup()
            
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.logger.info("Closing browser...")
            self.driver.quit()

if __name__ == "__main__":
    bot = OGameBot()
    bot.start()

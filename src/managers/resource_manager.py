from selenium.webdriver.common.by import By
import time

class ResourceManager:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        
    def get_resources(self):
        """Get current resource amounts with multiple fallback methods"""
        resources = {}
        
        # Method 1: Try standard OGame resource IDs
        resource_ids = {
            'metal': ['resources_metal', 'metal', 'resource_metal'],
            'crystal': ['resources_crystal', 'crystal', 'resource_crystal'],
            'deuterium': ['resources_deuterium', 'deuterium', 'resource_deuterium'],
            'energy': ['resources_energy', 'energy', 'resource_energy']
        }
        
        for resource_type, ids in resource_ids.items():
            value = None
            
            for id_name in ids:
                try:
                    element = self.driver.find_element(By.ID, id_name)
                    value = self.clean_number(element.text)
                    break
                except:
                    continue
                    
            if value is None:
                # Method 2: Try CSS selectors
                css_selectors = [
                    f".{resource_type}",
                    f"[data-resource='{resource_type}']",
                    f".resource_{resource_type}"
                ]
                
                for selector in css_selectors:
                    try:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        value = self.clean_number(element.text)
                        break
                    except:
                        continue
                        
            resources[resource_type] = value or "0"
            
        return resources
        
    def clean_number(self, text):
        """Clean number string and convert to integer"""
        if not text:
            return "0"
            
        # Remove dots, commas, and other non-numeric characters
        cleaned = ''.join(c for c in text if c.isdigit())
        return cleaned if cleaned else "0"
        
    def get_resource_production(self):
        """Get resource production rates"""
        try:
            production = {}
            
            # Look for production info elements
            prod_selectors = [
                ".production",
                ".prod",
                "[title*='Produktion']",
                "[title*='production']"
            ]
            
            for selector in prod_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for elem in elements:
                        text = elem.text or elem.get_attribute("title") or ""
                        if "Metall" in text or "Metal" in text:
                            production['metal'] = self.extract_production_value(text)
                        elif "Kristall" in text or "Crystal" in text:
                            production['crystal'] = self.extract_production_value(text)
                        elif "Deuterium" in text:
                            production['deuterium'] = self.extract_production_value(text)
                except:
                    continue
                    
            return production
            
        except Exception as e:
            self.logger.error(f"Error getting production: {e}")
            return {}
            
    def extract_production_value(self, text):
        """Extract production value from text"""
        import re
        
        # Look for numbers in the text
        numbers = re.findall(r'[\d,\.]+', text)
        if numbers:
            return self.clean_number(numbers[-1])  # Take the last number found
        return "0"
        
    def log_resources(self):
        """Log current resources and production"""
        resources = self.get_resources()
        production = self.get_resource_production()
        
        self.logger.info("=== RESOURCES ===")
        for resource, amount in resources.items():
            prod = production.get(resource, "Unknown")
            self.logger.info(f"{resource.capitalize()}: {amount} (Production: +{prod}/h)")
            
        return resources, production

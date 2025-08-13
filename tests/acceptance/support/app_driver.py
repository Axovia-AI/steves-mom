"""
Configuration and support utilities for acceptance tests.
"""
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import requests
import time
from urllib.parse import urljoin


class AppDriver:
    """Driver for interacting with the chat application."""
    
    def __init__(self, base_url="http://localhost:3000"):
        self.base_url = base_url
        self.driver = None
        self.wait = None
        
    def start_browser(self):
        """Start the browser instance."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)
        
    def stop_browser(self):
        """Stop the browser instance."""
        if self.driver:
            self.driver.quit()
            self.driver = None
            
    def navigate_to(self, path="/"):
        """Navigate to a specific path."""
        url = urljoin(self.base_url, path)
        self.driver.get(url)
        
    def wait_for_element(self, selector, timeout=30):
        """Wait for an element to be present."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        
    def wait_for_element_clickable(self, selector, timeout=30):
        """Wait for an element to be clickable."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        
    def find_element(self, selector):
        """Find an element by CSS selector."""
        return self.driver.find_element(By.CSS_SELECTOR, selector)
        
    def find_elements(self, selector):
        """Find elements by CSS selector."""
        return self.driver.find_elements(By.CSS_SELECTOR, selector)
        
    def click_element(self, selector):
        """Click an element."""
        element = self.wait_for_element_clickable(selector)
        element.click()
        
    def type_text(self, selector, text):
        """Type text into an element."""
        element = self.wait_for_element(selector)
        element.clear()
        element.send_keys(text)
        
    def get_text(self, selector):
        """Get text from an element."""
        element = self.wait_for_element(selector)
        return element.text
        
    def is_element_present(self, selector):
        """Check if an element is present."""
        try:
            self.driver.find_element(By.CSS_SELECTOR, selector)
            return True
        except:
            return False
            
    def wait_for_api_response(self, timeout=30):
        """Wait for chat API response to complete."""
        # Wait for any loading indicators to disappear
        time.sleep(1)  # Brief wait for request to start
        
        # Wait for specific loading indicators that may appear
        try:
            WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='loading']"))
            )
            # If loading element appears, wait for it to disappear
            WebDriverWait(self.driver, timeout).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='loading']"))
            )
        except:
            # If no loading element found, just wait a bit
            time.sleep(2)


@pytest.fixture
def app_driver():
    """Pytest fixture that provides an app driver instance."""
    driver = AppDriver()
    driver.start_browser()
    yield driver
    driver.stop_browser()


def check_server_health(base_url="http://localhost:3000", timeout=30):
    """Check if the application server is running."""
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{base_url}/ping", timeout=5)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            pass
        time.sleep(1)
    
    return False
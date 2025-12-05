from playwright.sync_api import Page
from datetime import datetime
import os
from config.settings import settings

class BasePage:
    def __init__(self, page: Page):
        self.page = page
    
    def navigate(self, url: str):
        """Navega para URL"""
        self.page.goto(url, wait_until="networkidle")
    
    def click(self, selector: str, timeout: int = None):
        """Clica em elemento"""
        self.page.click(selector, timeout=timeout or settings.TIMEOUT)
    
    def fill(self, selector: str, text: str):
        """Preenche campo"""
        self.page.fill(selector, str(text))
    
    def select_option(self, selector: str, value: str):
        """Seleciona opção em dropdown"""
        self.page.select_option(selector, value)
    
    def wait_for_selector(self, selector: str, timeout: int = None):
        """Aguarda elemento aparecer"""
        self.page.wait_for_selector(selector, timeout=timeout or settings.TIMEOUT)
    
    def wait_for_load(self):
        """Aguarda página carregar"""
        self.page.wait_for_load_state("networkidle")
    
    def screenshot(self, name: str):
        """Captura screenshot"""
        os.makedirs(settings.SCREENSHOTS_DIR, exist_ok=True)
        path = os.path.join(settings.SCREENSHOTS_DIR, name)
        self.page.screenshot(path=path, full_page=True)
        return path
    
    def press_key(self, selector: str, key: str):
        """Pressiona tecla em campo"""
        self.page.press(selector, key)
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from config.settings import settings
import os

class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
    
    def start(self, browser_type: str = "chromium"):
        """Inicia o navegador"""
        self.playwright = sync_playwright().start()
        
        if browser_type == "chromium":
            browser_launcher = self.playwright.chromium
        elif browser_type == "firefox":
            browser_launcher = self.playwright.firefox
        else:
            browser_launcher = self.playwright.chromium
        
        # Inicia o navegador
        self.browser = browser_launcher.launch(
            headless=settings.HEADLESS,
            slow_mo=settings.SLOW_MO
        )
        
        # Cria contexto com downloads
        self.context = self.browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="pt-BR",
            accept_downloads=True,
        )
        
        self.context.set_default_timeout(settings.TIMEOUT)
        self.page = self.context.new_page()
        
        return self.page
    
    def stop(self):
        """Fecha o navegador"""
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
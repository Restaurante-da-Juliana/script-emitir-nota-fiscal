import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Configurações do navegador
    HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"
    SLOW_MO = int(os.getenv("SLOW_MO", "500"))
    TIMEOUT = int(os.getenv("TIMEOUT", "60000"))
    
    BASE_URL = os.getenv("BASE_URL", "https://receita.pr.gov.br/")
    
    # Diretórios
    DOWNLOADS_DIR = "downloads"
    SCREENSHOTS_DIR = "screenshots"
    LOGS_DIR = "logs"
    DATA_DIR = "data"

settings = Settings()
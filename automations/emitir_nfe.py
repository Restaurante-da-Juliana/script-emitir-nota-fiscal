from core.browser_manager import BrowserManager
from pages.receita_federal_page import ReceitaFederalPage
from utils.excel_handler import ExcelHandler
from config.settings import settings
import logging
from datetime import datetime
import os

# Configurar logging
os.makedirs(settings.LOGS_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(
            f'{settings.LOGS_DIR}/emissao_nfe_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
            encoding='utf-8'
        ),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def emitir_nota_fiscal(
    cnpj_emitente: str,
    inscricao_estadual: str,
    produtos: list,
    dados_destinatario: dict = None,
    valor_total: float = None,
    informacoes_adicionais: str = ""
):
    """
    Emite uma nota fiscal com os dados fornecidos
    
    Args:
        cnpj_emitente: CNPJ da empresa emitente
        inscricao_estadual: Inscrição estadual
        produtos: Lista de produtos a serem incluídos
        dados_destinatario: Dicionário com dados do destinatário
        valor_total: Valor total da nota (calculado se não fornecido)
        informacoes_adicionais: Informações complementares
    """
    browser = BrowserManager()
    
    try:
        logger.info("=" * 60)
        logger.info("INICIANDO EMISSÃO DE NOTA FISCAL")
        logger.info("=" * 60)
        
        # Inicia navegador
        page = browser.start()
        receita = ReceitaFederalPage(page)
        
        logger.info("Acessando portal da Receita Federal...")
        receita.acessar_portal()

        logger.info("Logando-se com as credenciais na página da Receita Federal...")
        receita.logar_credenciais()
        
        logger.info("Acessando área de emissão de NF-e...")
        receita.acessar_emissao_nfe()

        logger.info("Preenchendo os dados do emitente...")
        receita.preencher_dados_emitente()

        logger.info("Escolhendo e preenchendo CPF ou CNPJ")
        receita.selecionar_e_preencher_cpf_ou_cnpj()

        logger.info("Preenchendo Inscrição estadual")
        receita.preenchendo_inscricao_estadual()

        logger.info("Preenchendo Dados do destinatário")
        receita.preenchendo_dados_destinatario()
        
        logger.info("Preenchendo Identificação da Nota")
        receita.preenchendo_identificadao_nota()

        logger.info("Avançando Local de Retirada/Entrega")
        receita.local_retirada_entrega()

        logger.info("Preenchendo Produtos")
        receita.preenchendo_produtos()

        
        ##return {
        ##    "sucesso": True,
        ##    "numero_nota": numero_nota,
        ##    "xml_path": xml_path,
        ##    "danfe_path": danfe_path
        ##}
        
    except Exception as e:
        logger.error(f"❌ Erro na emissão: {str(e)}")
        if browser.page:
            error_screenshot = f"erro_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            browser.page.screenshot(path=f"{settings.SCREENSHOTS_DIR}/{error_screenshot}")
            logger.error(f"Screenshot do erro salvo: {error_screenshot}")
        raise
    
    finally:
        logger.info("Fechando navegador...")
        browser.stop()
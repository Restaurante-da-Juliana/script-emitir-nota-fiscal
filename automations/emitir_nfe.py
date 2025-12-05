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
        
        # 6. Adicionar produtos
        logger.info(f"Adicionando {len(produtos)} produto(s)...")
        receita.adicionar_multiplos_produtos(produtos)
        
        # 7. Calcular valor total se não fornecido
        if not valor_total:
            valor_total = sum(p.get("quantidade", 0) * p.get("valor_unitario", 0) for p in produtos)
        
        logger.info(f"Valor total da nota: R$ {valor_total:.2f}")
        
        # 8. Preencher dados de pagamento
        logger.info("Preenchendo dados de pagamento...")
        receita.preencher_dados_pagamento(valor=valor_total)
        
        # 9. Preencher dados de transporte
        logger.info("Preenchendo dados de transporte...")
        receita.preencher_dados_transporte()
        
        # 10. Adicionar informações adicionais
        if informacoes_adicionais:
            logger.info("Adicionando informações complementares...")
            receita.adicionar_informacoes_adicionais(informacoes_adicionais)
        
        # 11. Validar nota
        logger.info("Validando nota fiscal...")
        receita.validar_nota()
        
        # Aguardar confirmação do usuário antes de transmitir
        input("Revise a nota e pressione ENTER para transmitir...")
        
        # 12. Transmitir nota
        logger.info("Transmitindo nota fiscal...")
        receita.transmitir_nota()
        
        # 13. Obter número da nota
        numero_nota = receita.obter_numero_nota()
        logger.info(f"✓ Nota fiscal emitida com sucesso! Número: {numero_nota}")
        
        # 14. Baixar XML e DANFE
        logger.info("Baixando XML e DANFE...")
        xml_path = receita.baixar_xml()
        danfe_path = receita.baixar_danfe()
        
        logger.info(f"XML salvo em: {xml_path}")
        logger.info(f"DANFE salvo em: {danfe_path}")
        
        logger.info("=" * 60)
        logger.info("EMISSÃO CONCLUÍDA COM SUCESSO!")
        logger.info("=" * 60)
        
        return {
            "sucesso": True,
            "numero_nota": numero_nota,
            "xml_path": xml_path,
            "danfe_path": danfe_path
        }
        
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
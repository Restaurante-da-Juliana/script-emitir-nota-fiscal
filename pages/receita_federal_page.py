import os
from pages.base_page import BasePage
from config.settings import settings
from playwright.sync_api import Page
import time

class ReceitaFederalPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = os.getenv("BASE_URL")
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
    
    def acessar_portal(self):
        self.navigate(self.url)
        self.screenshot("01_portal_inicial.png")

    def logar_credenciais(self):
        self.page.get_by_role("textbox", name="Usuário (CPF)").click()
        self.page.get_by_role("textbox", name="Usuário (CPF)").fill(self.user)
        self.page.get_by_role("textbox", name="Senha").click()
        self.page.get_by_role("textbox", name="Senha").fill(self.password)
        self.page.get_by_role("button", name="Login").click()
    
    def acessar_emissao_nfe(self):
        self.page.get_by_role("link", name="NFA-e MEI e NFA-e (Modelo 55)").click()
        self.page.get_by_role("link", name="Emissão").click()
    
    def preencher_dados_emitente(self):
        self.page.get_by_role("button", name="Avançar").click()
    
    def preencher_dados_destinatario(self, dados_destinatario: dict):
        """Preenche dados do destinatário"""
        if dados_destinatario.get("cnpj"):
            self.fill("#txtCNPJDestinatario", dados_destinatario["cnpj"])
        
        if dados_destinatario.get("razao_social"):
            self.fill("#txtRazaoSocial", dados_destinatario["razao_social"])
        
        if dados_destinatario.get("endereco"):
            self.fill("#txtEndereco", dados_destinatario["endereco"])
        
        self.screenshot("06_dados_destinatario.png")
    
    def adicionar_produto(self, produto: dict):
        """Adiciona um produto à nota"""
        # Clicar em adicionar produto
        self.click("text=Adicionar Produto")
        
        # Preencher dados do produto
        if produto.get("codigo"):
            self.fill("#txtCodigoProduto", produto["codigo"])
        
        if produto.get("descricao"):
            self.fill("#txtDescricao", produto["descricao"])
        
        if produto.get("ncm"):
            self.fill("#txtNCM", produto["ncm"])
        
        if produto.get("quantidade"):
            self.fill("#txtQuantidade", str(produto["quantidade"]))
        
        if produto.get("valor_unitario"):
            self.fill("#txtValorUnitario", str(produto["valor_unitario"]))
        
        # Calcular valor total automaticamente
        if produto.get("quantidade") and produto.get("valor_unitario"):
            valor_total = produto["quantidade"] * produto["valor_unitario"]
            self.fill("#txtValorTotal", str(valor_total))
        
        # Confirmar adição
        self.click("button:has-text('Confirmar')")
        self.screenshot(f"07_produto_adicionado_{produto.get('codigo', 'sem_codigo')}.png")
    
    def adicionar_multiplos_produtos(self, produtos: list):
        """Adiciona múltiplos produtos"""
        for i, produto in enumerate(produtos, 1):
            print(f"Adicionando produto {i}/{len(produtos)}: {produto.get('descricao', 'N/A')}")
            self.adicionar_produto(produto)
            time.sleep(1)
    
    def preencher_dados_pagamento(self, forma_pagamento: str = "01", valor: float = None):
        """Preenche dados de pagamento"""
        # 01 = Dinheiro, 03 = Cartão de Crédito, etc.
        self.select_option("#ddlFormaPagamento", forma_pagamento)
        
        if valor:
            self.fill("#txtValorPagamento", str(valor))
        
        self.screenshot("08_dados_pagamento.png")
    
    def preencher_dados_transporte(self, modalidade: str = "9"):
        """Preenche dados de transporte"""
        # 9 = Sem transporte
        self.select_option("#ddlModalidadeFrete", modalidade)
        self.screenshot("09_dados_transporte.png")
    
    def adicionar_informacoes_adicionais(self, informacoes: str):
        """Adiciona informações complementares"""
        if self.page.query_selector("#txtInformacoesComplementares"):
            self.fill("#txtInformacoesComplementares", informacoes)
        self.screenshot("10_informacoes_adicionais.png")
    
    def validar_nota(self):
        """Valida a nota antes de transmitir"""
        self.click("button:has-text('Validar')")
        time.sleep(2)
        self.screenshot("11_nota_validada.png")
    
    def transmitir_nota(self):
        """Transmite a nota fiscal"""
        self.click("button:has-text('Transmitir')")
        time.sleep(3)
        self.screenshot("12_nota_transmitida.png")
    
    def obter_numero_nota(self) -> str:
        """Obtém o número da nota fiscal emitida"""
        # Ajustar seletor conforme site real
        numero = self.page.text_content("#lblNumeroNF")
        return numero
    
    def baixar_xml(self):
        """Baixa o XML da nota"""
        with self.page.expect_download() as download_info:
            self.click("text=Download XML")
        
        download = download_info.value
        os.makedirs(settings.DOWNLOADS_DIR, exist_ok=True)
        file_path = os.path.join(settings.DOWNLOADS_DIR, download.suggested_filename)
        download.save_as(file_path)
        
        return file_path
    
    def baixar_danfe(self):
        """Baixa o DANFE (PDF)"""
        with self.page.expect_download() as download_info:
            self.click("text=Imprimir DANFE")
        
        download = download_info.value
        os.makedirs(settings.DOWNLOADS_DIR, exist_ok=True)
        file_path = os.path.join(settings.DOWNLOADS_DIR, download.suggested_filename)
        download.save_as(file_path)
        
        return file_path
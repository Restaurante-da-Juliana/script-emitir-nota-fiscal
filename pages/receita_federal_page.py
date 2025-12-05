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
        self.cpf = os.getenv("CPF")
        self.cnpj = os.getenv("CNPJ")
        self.ie = os.getenv("IE")
        self.razao_social = os.getenv("RAZAO_SOCIAL")
        self.cep = os.getenv("CEP")
        self.numero = os.getenv("NUMERO")
    
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
        btn = self.page.get_by_role("button", name="Avançar")
        btn.wait_for(state="attached")
        btn.wait_for(state="visible")
        self.page.wait_for_timeout(150)
        btn.click()

    def selecionar_e_preencher_cpf_ou_cnpj(self):
        if self.cpf and len(self.cpf) > 0:
            locator = self.page.locator(".slds-radio_faux").first
            locator.wait_for(state="visible")
            locator.click()
            self.page.get_by_role("textbox").nth(1).click()
            self.page.get_by_role("textbox").nth(1).fill(self.cpf)
        else:
            locator = self.page.locator("span:nth-child(2) > .slds-radio__label > .slds-radio_faux")
            locator.wait_for(state="visible")
            locator.click()
            textbox = self.page.get_by_role("textbox").nth(1)
            textbox.click()
            textbox.fill(self.cnpj)

    def preenchendo_inscricao_estadual(self):
        textbox = self.page.get_by_role("textbox").nth(2)
        textbox.click()
        textbox.fill(self.ie)

    def preenchendo_dados_destinatario(self):
        textbox_razao_social = self.page.get_by_role("textbox").nth(3)
        textbox_razao_social.click()
        textbox_razao_social.fill(self.razao_social)

        textbox_cep = self.page.locator(".slds-input.slds-size_3-of-12")
        textbox_cep.click()
        textbox_cep.fill(self.cep)
        self.page.get_by_text("Endereço").click()

        textbox_numero = self.page.locator(".slds-form-element.slds-col.slds-size_1-of-12 > .slds-form-element__control > .slds-input")
        textbox_numero.click()
        textbox_numero.fill(self.numero)
        self.page.get_by_role("button", name="Avançar").click()

    def preenchendo_identificadao_nota(self):
        self.page.locator("#combobox-id-1").click()
        self.page.locator("span").filter(has_text="Venda").first.click()

        self.page.get_by_role("combobox").nth(1).select_option("1")

        self.page.get_by_role("combobox").nth(3).select_option("1")

        self.page.get_by_role("combobox").nth(4).select_option("1")

        self.page.locator(".slds-form-element.slds-size_6-of-12 > div:nth-child(3) > .slds-form-element > .slds-form-element__control > span > .slds-radio__label > .slds-radio_faux").first.click()

        self.page.get_by_role("button", name="Avançar").click()

    def local_retirada_entrega(self):
        botao = self.page.get_by_role("button", name="Avançar")
        botao.wait_for(state="attached")
        botao.wait_for(state="visible")
        botao.wait_for(state="enabled")
        botao.click()


    def preenchendo_produtos(self):
        campoDescricao = self.page.get_by_role("textbox").nth(1)

        campoDescricao.wait_for(state="visible")
        campoDescricao.wait_for(state="attached")
        campoDescricao.wait_for(state="editable")

        campoDescricao.fill("REFEIÇÃO NO RESTAURANTE DA JULIANA")



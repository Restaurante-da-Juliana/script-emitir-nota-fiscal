import pandas as pd
import os
from config.settings import settings

class ExcelHandler:
    @staticmethod
    def ler_notas_para_emitir(arquivo: str = "notas_para_emitir.xlsx") -> list:
        """Lê arquivo Excel com notas para emitir"""
        caminho = os.path.join(settings.DATA_DIR, arquivo)
        
        if not os.path.exists(caminho):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
        
        df = pd.read_excel(caminho)
        return df.to_dict('records')
    
    @staticmethod
    def ler_produtos(arquivo: str = "produtos.xlsx") -> list:
        """Lê arquivo Excel com produtos"""
        caminho = os.path.join(settings.DATA_DIR, arquivo)
        
        if not os.path.exists(caminho):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
        
        df = pd.read_excel(caminho)
        return df.to_dict('records')
    
    @staticmethod
    def salvar_resultado(dados: list, arquivo: str = "resultado_emissao.xlsx"):
        """Salva resultado da emissão"""
        caminho = os.path.join(settings.DATA_DIR, arquivo)
        df = pd.DataFrame(dados)
        df.to_excel(caminho, index=False)
        return caminho
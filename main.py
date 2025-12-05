import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from automations.emitir_nfe import emitir_nota_fiscal

if __name__ == "__main__":
    # Exemplo 1: Emissão simples
    print("\n" + "="*60)
    print("AUTOMAÇÃO DE EMISSÃO DE NF-e - RECEITA FEDERAL")
    print("="*60 + "\n")
    
    # Dados do emitente
    cnpj_emitente = "12.345.678/0001-90"
    inscricao_estadual = "123456789"
    
    # Dados do destinatário (opcional)
    destinatario = {
        "cnpj": "98.765.432/0001-10",
        "razao_social": "EMPRESA DESTINATÁRIA LTDA",
        "endereco": "Rua Exemplo, 123"
    }
    
    # Produtos
    produtos = [
        {
            "codigo": "PROD001",
            "descricao": "Produto de Teste 1",
            "ncm": "12345678",
            "quantidade": 10,
            "valor_unitario": 50.00
        },
        {
            "codigo": "PROD002",
            "descricao": "Produto de Teste 2",
            "ncm": "87654321",
            "quantidade": 5,
            "valor_unitario": 100.00
        }
    ]
    
    # Informações adicionais
    info_adicional = "Nota fiscal emitida automaticamente via Playwright"
    
    try:
        resultado = emitir_nota_fiscal(
            cnpj_emitente=cnpj_emitente,
            inscricao_estadual=inscricao_estadual,
            produtos=produtos,
            dados_destinatario=destinatario,
            informacoes_adicionais=info_adicional
        )
        
        print("\n✓ Processo concluído!")
        print(f"Nota Fiscal: {resultado['numero_nota']}")
        print(f"XML: {resultado['xml_path']}")
        print(f"DANFE: {resultado['danfe_path']}")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)
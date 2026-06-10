import pandas as pd
import os
import gspread
from datetime import datetime

# Lê o CSV e converte valores financeiros para decimais.
def carregar_e_limpar_dados(caminho_arquivo):
    df = pd.read_csv(caminho_arquivo)
    colunas_financeiras = ['comissão', 'cashback', 'vendas totais']
    for coluna in colunas_financeiras:
        df[coluna] = (
            df[coluna]
            .str.replace('R$', '', regex=False)
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
            .astype(float)
        )
    return df

# Agrupa os dados e calcula a variante com maior lucro.
def calcular_vencedor_ab(df):
    resumo = df.groupby('Grupos de usuários')[['compradores', 'comissão', 'cashback', 'vendas totais']].sum()
    resumo['lucro_meliuz'] = resumo['comissão'] - resumo['cashback']
    resumo['roi'] = resumo['lucro_meliuz'] / resumo['cashback']
    variante_vencedora = resumo['lucro_meliuz'].idxmax()
    return resumo, variante_vencedora

# Cria um texto de instrução (prompt) para a IA gerar o relatório.
def gerar_prompt_relatorio(resumo_df, vencedor, nome_parceiro):
    dados_texto = resumo_df.to_string() 
    prompt = f"""
Você atua como Analista de Growth Sênior no Méliuz.
Acabamos de rodar um Teste A/B com o parceiro {nome_parceiro}. 
Nossa equipe processou os dados e o resumo matemático é este:

{dados_texto}

A variante matematicamente vencedora, com base no maior lucro para o Méliuz (Comissão - Cashback), foi a: {vencedor}.

SUA TAREFA:
Escreva um relatório gerencial de no máximo 3 parágrafos sobre este teste. 
O relatório deve ser focado em negócios, ser direto ao ponto e conter as seguintes seções claras:
1. Resumo do Teste (O que aconteceu e quem foi testado).
2. Resultados Chave (Comparando a vencedora com as perdedoras focando em Lucro e ROI).
3. Decisão Acionável (A recomendação clara de qual variante escalar).

Por favor, gere APENAS o relatório. Sem saudações ou explicações adicionais.
    """
    pasta_relatorios = os.path.join(os.path.dirname(__file__), "..", "relatorios")
    os.makedirs(pasta_relatorios, exist_ok=True)
    caminho_arquivo = os.path.join(pasta_relatorios, f"prompt_{nome_parceiro.replace(' ', '_')}.txt")
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(prompt)
    return caminho_arquivo

# Conecta na planilha do Google
def registrar_no_google_sheets(nome_parceiro, vencedor, lucro, roi):
    try:
        caminho_credenciais = os.path.join(os.path.dirname(__file__), "..", "credentials.json")
        gc = gspread.service_account(filename=caminho_credenciais)
        
        planilha = gc.open_by_url('https://docs.google.com/spreadsheets/d/1jpXBCWaSC4H3O-kYMTA1MyvZ47Gb987zSOA9wFDqOa8/edit').sheet1
        
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
        decisao = f"Escalar {vencedor} para 100% do tráfego"
        lucro_formatado = f"R$ {lucro:,.2f}"
        roi_formatado = f"{roi:.2f}"
        
        linha = [data_atual, nome_parceiro, vencedor, lucro_formatado, roi_formatado, decisao]
        
        planilha.append_row(linha)
        print("☁️ Resultado registrado no Google Sheets com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao salvar no Google Sheets: {e}")
        print("Dica: Verifique se o 'credentials.json' está na pasta raiz e se você compartilhou a planilha com o e-mail correto.")

# Busca parceiros que já foram salvos na planilha
def obter_parceiros_processados():
    try:
        caminho_credenciais = os.path.join(os.path.dirname(__file__), "..", "credentials.json")
        gc = gspread.service_account(filename=caminho_credenciais)
        planilha = gc.open_by_url('https://docs.google.com/spreadsheets/d/1jpXBCWaSC4H3O-kYMTA1MyvZ47Gb987zSOA9wFDqOa8/edit').sheet1
        return set(planilha.col_values(2))
    except Exception:
        return set()

# Processa automaticamente todos os datasets encontrados na pasta.
if __name__ == "__main__":
    
    pasta_datasets = os.path.join(os.path.dirname(__file__), "..", "datasets")
    arquivos = [f for f in os.listdir(pasta_datasets) if f.endswith('.csv')]
    
    if not arquivos:
        print("Nenhum arquivo .csv encontrado na pasta datasets.")
    
    parceiros_processados = obter_parceiros_processados()
    
    for arquivo_atual in sorted(arquivos):
        caminho_teste = os.path.join(pasta_datasets, arquivo_atual)
        nome_parceiro = arquivo_atual.replace(".csv", "")
        
        if nome_parceiro in parceiros_processados:
            continue
            
        print(f"--------------------------------------------------")
        print(f"Iniciando pipeline de análise para: {nome_parceiro}")
        
        try:
            dados_limpos = carregar_e_limpar_dados(caminho_teste)
            tabela_resumo, vencedor = calcular_vencedor_ab(dados_limpos)
            
            caminho_prompt = gerar_prompt_relatorio(tabela_resumo, vencedor, nome_parceiro)
            print("✅ Relatório de IA gerado.")
            
            lucro_vencedor = tabela_resumo.loc[vencedor, 'lucro_meliuz']
            roi_vencedor = tabela_resumo.loc[vencedor, 'roi']
            registrar_no_google_sheets(nome_parceiro, vencedor, lucro_vencedor, roi_vencedor)
            
            print(f"🎉 Pipeline executado com sucesso para {nome_parceiro}!\n")
            
        except Exception as e:
            print(f"❌ Ocorreu um erro ao processar {nome_parceiro}: {e}\n")
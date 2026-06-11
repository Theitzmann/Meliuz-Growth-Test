import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import pandas as pd
import os
import argparse
import gspread
import csv
import anthropic
from dotenv import load_dotenv
from datetime import datetime

# Carrega as variáveis do arquivo .env (onde estará a sua chave da API)
load_dotenv()

# 1. Carrega o CSV e limpa os dados financeiros
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

# 2. Agrupa os dados e calcula a variante com melhor ROI (Visão de Growth)
def calcular_vencedor_ab(df):
    resumo = df.groupby('Grupos de usuários')[['compradores', 'comissão', 'cashback', 'vendas totais']].sum()
    resumo['lucro_meliuz'] = resumo['comissão'] - resumo['cashback']
    
    # Utilizando ROI (Lucro / Cashback) para uma decisão justa independente do tamanho da amostra
    resumo['roi'] = resumo['lucro_meliuz'] / resumo['cashback']
    variante_vencedora = resumo['roi'].idxmax()
    
    return resumo, variante_vencedora

# 3. Cria o prompt estruturado para a IA
def gerar_texto_prompt(resumo_df, vencedor, nome_parceiro):
    dados_texto = resumo_df.to_string() 
    prompt = f"""
Você atua como Analista de Growth Sênior no Méliuz.
Acabamos de rodar um Teste A/B com o parceiro {nome_parceiro}. 
Nossa equipe processou os dados e o resumo matemático é este:

{dados_texto}

A variante matematicamente vencedora, com base no maior ROI e Lucro para o Méliuz, foi a: {vencedor}.

SUA TAREFA:
Escreva um relatório gerencial de no máximo 3 parágrafos sobre este teste. 
O relatório deve ser focado em negócios, ser direto ao ponto e conter as seguintes seções claras:
1. Resumo do Teste (O que aconteceu e quem foi testado).
2. Resultados Chave (Comparando a vencedora com as perdedoras focando em Lucro e ROI).
3. Decisão Acionável (A recomendação clara de qual variante escalar).

Por favor, gere APENAS o relatório formatado em Markdown. Sem saudações ou explicações adicionais.
    """
    return prompt

# 4. Chama a API do Claude e salva o relatório final
def gerar_relatorio_claude(prompt_texto, nome_parceiro):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("⚠️ Chave 'ANTHROPIC_API_KEY' não encontrada no .env. Gerando apenas o prompt em .txt.")
        return False
        
    print("🤖 Enviando dados para a IA analisar...")
    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-haiku-4-5", # Nomenclatura oficial corrigida
            max_tokens=1000,
            temperature=0.2,
            messages=[
                {"role": "user", "content": prompt_texto}
            ]
        )
        
        relatorio = message.content[0].text
        
        pasta_relatorios = os.path.join(os.path.dirname(__file__), "..", "relatorios")
        os.makedirs(pasta_relatorios, exist_ok=True)
        
        caminho_arquivo = os.path.join(pasta_relatorios, f"relatorio_{nome_parceiro}.md")
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(relatorio)
            
        print(f"✨ Relatório gerencial de IA salvo em: relatorios/relatorio_{nome_parceiro}.md")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao chamar a API do Claude: {e}")
        return False

# 5. Registra no Sheets ou faz o fallback para CSV local
def registrar_resultado(nome_parceiro, vencedor, lucro, roi):
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    decisao = f"Escalar {vencedor} para 100% do tráfego"
    lucro_formatado = f"R$ {lucro:,.2f}"
    roi_formatado = f"{roi:.2f}"
    
    linha = [data_atual, nome_parceiro, vencedor, lucro_formatado, roi_formatado, decisao]
    
    try:
        caminho_credenciais = os.path.join(os.path.dirname(__file__), "..", "credentials.json")
        gc = gspread.service_account(filename=caminho_credenciais)
        planilha = gc.open_by_url('https://docs.google.com/spreadsheets/d/1jpXBCWaSC4H3O-kYMTA1MyvZ47Gb987zSOA9wFDqOa8/edit').sheet1
        
        # --- TRAVA DE DUPLICIDADE SILENCIOSA ---
        parceiros_cadastrados = planilha.col_values(2) # Assume que Parceiro é a 2ª coluna (B)
        if nome_parceiro in parceiros_cadastrados:
            return # Sai da função sem registrar novamente
        # ---------------------------------------
        
        planilha.append_row(linha)
        print("☁️ Resultado registrado no Google Sheets com sucesso!")
        
    except FileNotFoundError:
        caminho_csv = os.path.join(os.path.dirname(__file__), "..", "historico_testes_ab.csv")
        arquivo_existe = os.path.isfile(caminho_csv)
        
        # --- TRAVA DE DUPLICIDADE SILENCIOSA NO CSV ---
        if arquivo_existe:
            with open(caminho_csv, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                parceiros_cadastrados = [row[1] for row in reader if len(row) > 1]
            if nome_parceiro in parceiros_cadastrados:
                return # Sai da função sem registrar novamente
        # ----------------------------------------------
        
        with open(caminho_csv, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not arquivo_existe:
                writer.writerow(['Data', 'Parceiro', 'Variante Vencedora', 'Lucro Meliuz', 'ROI', 'Decisão'])
            writer.writerow(linha)
            
        print("⚠️ 'credentials.json' ausente. Resultado salvo localmente em 'historico_testes_ab.csv'.")

# 6. Pipeline de Execução
def main():
    parser = argparse.ArgumentParser(description="Analisa um teste A/B de cashback do Méliuz.")
    parser.add_argument("arquivo", help="Caminho para o arquivo CSV do dataset do teste.")
    args = parser.parse_args()

    caminho_teste = args.arquivo
    if not os.path.exists(caminho_teste):
        print(f"❌ Erro: O arquivo '{caminho_teste}' não foi encontrado.")
        return

    nome_arquivo = os.path.basename(caminho_teste)
    nome_parceiro = nome_arquivo.replace(".csv", "")
    
    print(f"\n--- Iniciando análise de Growth para: {nome_parceiro} ---")
    
    try:
        dados_limpos = carregar_e_limpar_dados(caminho_teste)
        tabela_resumo, vencedor = calcular_vencedor_ab(dados_limpos)
        
        # Gera o texto e aciona o Claude
        prompt = gerar_texto_prompt(tabela_resumo, vencedor, nome_parceiro)
        gerar_relatorio_claude(prompt, nome_parceiro)
        
        lucro_vencedor = tabela_resumo.loc[vencedor, 'lucro_meliuz']
        roi_vencedor = tabela_resumo.loc[vencedor, 'roi']
        
        registrar_resultado(nome_parceiro, vencedor, lucro_vencedor, roi_vencedor)
        print("✅ Pipeline executado com sucesso!\n")
        
    except Exception as e:
        print(f"❌ Ocorreu um erro na análise: {e}\n")

if __name__ == "__main__":
    main()
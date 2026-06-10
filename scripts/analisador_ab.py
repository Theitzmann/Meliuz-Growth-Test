import os
import glob
import pandas as pd

def carregar_e_limpar_dados(pasta_datasets):
    arquivos = glob.glob(os.path.join(pasta_datasets, "*.csv"))
    df = pd.concat([pd.read_csv(arq) for arq in arquivos], ignore_index=True)
    
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

def calcular_vencedor_ab(df):
    resumo = df.groupby('Grupos de usuários')[['compradores', 'comissão', 'cashback', 'vendas totais']].sum()
    resumo['lucro_meliuz'] = resumo['comissão'] - resumo['cashback']
    resumo['roi'] = resumo['lucro_meliuz'] / resumo['cashback']
    variante_vencedora = resumo['lucro_meliuz'].idxmax()
    return resumo, variante_vencedora

def gerar_prompt_relatorio(resumo_df, vencedor, nome_parceiro):
    dados_texto = resumo_df.to_string()
    
    prompt = f"""
Você atua como Analista de Growth Sênior no Méliuz.
Acabamos de rodar um Teste A/B com {nome_parceiro}. 
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

if __name__ == "__main__":
    pasta_teste = os.path.join(os.path.dirname(__file__), "..", "datasets")
    nome_parceiro = "Todos os Parceiros"
    
    try:
        dados_limpos = carregar_e_limpar_dados(pasta_teste)
        tabela_resumo, vencedor = calcular_vencedor_ab(dados_limpos)
        
        caminho_prompt = gerar_prompt_relatorio(tabela_resumo, vencedor, nome_parceiro)
        
        print(f"📄 Abra o arquivo '{caminho_prompt}' e cole o texto na sua IA para obter o relatório.")
        print("\n📊 Resumo de Negócios por Variante:")
        print(tabela_resumo[['lucro_meliuz', 'roi', 'vendas totais']])
        print(f"\n🏆 Decisão acionável: escalar a variante '{vencedor}' para 100% do tráfego.")
        
    except Exception as e:
        print(f"❌ Ocorreu um erro: {e}")
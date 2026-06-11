# 🚀 Méliuz Growth - TESTE TÉCNICO

Solução desenvolvida para o teste técnico da vaga de Estágio em Growth. Este pipeline processa dados brutos de testes A/B, identifica a variante vencedora baseada no Lucro Real e ROI, aciona a API do Claude para redigir um relatório gerencial e registra as decisões em uma planilha do Google Sheets. Como medida de segurança, o arquivo `.gitignore` impede o carregamento das chaves de acesso. Por isso, ao testar em um computador diferente, o sistema fará um fallback automático, salvando um arquivo `.csv` e os prompts em `.txt` na raiz do projeto.

📊 **Acompanhamento de Testes:**
[Acessar Planilha no Google Sheets](https://docs.google.com/spreadsheets/d/1jpXBCWaSC4H3O-kYMTA1MyvZ47Gb987zSOA9wFDqOa8/edit?gid=0#gid=0)

---

## 🛠 Funcionalidades Principais

1. **🧹 Limpeza e formatação inteligente dos datasets:** Converte strings financeiras em números decimais para que os cálculos sejam exatos.
2. **📊 Decisão orientada ao ROI:** Agrupa os dados e calcula matematicamente o vencedor do teste focando no **ROI** e eficiência de capital.
3. **🤖 Integração com IA:** Gera relatório por IA em formato Markdown diretamente na pasta `relatorios/`.
4. **☁️ Integração com Google Sheets:** Conecta de forma segura com o Google Drive/Sheets e alimenta uma planilha em tempo real.
5. **⚙️ Funcionamento em outras máquinas:** Mesmo sem as credenciais do Google Sheets e da IA, o código irá funcionar normalmente, salvando o registro em um arquivo `.csv` local e **prompts estruturados** em `.txt` para copiar e colar em uma IA de preferência (ChatGPT, Claude, Gemini...) para gerar o relatório final.

---

## 📁 Estrutura de Pastas

```text
📦 Meliuz-Growth-Test
 ┣ 📂 datasets/           # Datasets brutos de entrada (.csv)
 ┣ 📂 relatorios/         # Relatórios gerenciais finais gerados pela IA
 ┃ ┣ 📜 relatorio_dataset_01_parceiroA.md
 ┃ ┣ 📜 relatorio_dataset_02_parceiroB.md
 ┃ ┗ 📜 relatorio_dataset_03_parceiroC.md
 ┣ 📂 scripts/
 ┃ ┗ 📜 analisador_ab.py  # Script principal do pipeline
 ┣ 📜 .env                # Chave da API da Anthropic (OMITIDO NO GIT)
 ┣ 📜 credentials.json    # Chave de serviço do Google Cloud (OMITIDO NO GIT)
 ┣ 📜 requirements.txt    # Dependências e bibliotecas do projeto
 ┣ 📜 .gitignore
 ┗ 📜 README.md
```
---

## 📝 Exemplo de Relatório Gerencial (Output da IA)

Abaixo está o exemplo real de relatório gerado de forma 100% autônoma pelo pipeline para o `dataset_01_parceiroA`, demonstrando a entrega visual e analítica que o gestor receberá na pasta `relatorios/`:

> ### Relatório de Teste A/B - Dataset_01_ParceiroA
>
> #### Resumo do Teste
> Realizamos um teste A/B com o parceiro Dataset_01_ParceiroA comparando três grupos de usuários distintos para otimizar a performance de vendas e rentabilidade. O teste envolveu 31.857 compradores distribuídos entre Grupo 1 (9.633), Grupo 2 (10.814) e Grupo 3 (11.410), cada um exposto a diferentes estratégias de comissão e cashback.
>
> #### Resultados Chave
> O **Grupo 1 emergiu como vencedor absoluto**, gerando **R$ 404.711 em lucro** para o Méliuz com um **ROI de 1,73** – significativamente superior aos concorrentes. Em comparação, o Grupo 2 produziu R$ 357.519 em lucro (11,6% menor) com ROI de 0,96, enquanto o Grupo 3, apesar de maior volume de vendas (R$ 6,78M), gerou apenas R$ 264.287 em lucro (34,7% menor) com ROI de 0,52. A estratégia do Grupo 1 demonstrou a melhor eficiência de conversão de investimento em comissão/cashback para lucro líquido.
>
> #### Decisão Acionável
> **Recomendação: Escalar imediatamente a variante do Grupo 1** para toda a base de usuários do parceiro Dataset_01_ParceiroA. Esta estratégia oferece o melhor equilíbrio entre atração de compradores (9.633), controle de custos de comissão (R$ 638.135) e geração de lucro, maximizando o retorno sobre investimento em 79% comparado ao Grupo 2 e 230% comparado ao Grupo 3.

`relatorios/relatorio_dataset_01_parceiroA.md`

---

## ⚙️ Como executar o projeto

**1. Instale as dependências e crie o ambiente virtual:** Abra o terminal na raiz do projeto e execute o comando abaixo:
```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

**2. Execute o pipeline indicando o arquivo:** Rode o script passando o caminho do dataset que deseja analisar.
```bash
.venv/bin/python scripts/analisador_ab.py datasets/NOME_DO_ARQUIVO.csv
```
*(⚠️ ATENÇÃO: Substitua `NOME_DO_ARQUIVO.csv` pelo nome exato do dataset a ser analisado, como por exemplo `dataset_01_parceiroA.csv`).*
Exemplos:
```bash
.venv/bin/python scripts/analisador_ab.py datasets/dataset_01_parceiroA.csv
.venv/bin/python scripts/analisador_ab.py datasets/dataset_02_parceiroB.csv
.venv/bin/python scripts/analisador_ab.py datasets/dataset_03_parceiroC.csv
```
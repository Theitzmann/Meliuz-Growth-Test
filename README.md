# 🚀 Méliuz Growth - Automação de Análise A/B

Este projeto tem como objetivo automatizar a análise financeira de resultados de Testes A/B para múltiplos parceiros. 
O pipeline não apenas calcula a variante vencedora com foco no **Lucro Real e ROI** gerados para o Méliuz, mas também poupa horas de trabalho ao enviar os resultados diretamente para uma planilha na nuvem e preparar a base para relatórios gerenciais feitos por Inteligência Artificial.

---

## 📸 Demonstração do Projeto

Abaixo estão algumas imagens do funcionamento do sistema:

<p align="center">
  <img src="image.png" width="800">
  <br>
  <em>Legenda 1: (Substitua por sua explicação, ex: Pipeline rodando no terminal)</em>
</p>

<p align="center">
  <img src="image%20copy.png" width="800">
  <br>
  <em>Legenda 2: (Substitua por sua explicação, ex: Resultados salvos no Sheets)</em>
</p>

<p align="center">
  <img src="image%20copy%202.png" width="800">
  <br>
  <em>Legenda 3: (Substitua por sua explicação)</em>
</p>

<p align="center">
  <img src="image%20copy%203.png" width="800">
  <br>
  <em>Legenda 4: (Substitua por sua explicação)</em>
</p>
---

## 🛠 Funcionalidades Principais

1. **🚀 Processamento em Lote Automatizado:** O script lê a pasta `datasets/` e processa dezenas de testes A/B (arquivos .csv) de uma só vez.
2. **🧹 Limpeza e Formatação Inteligente:** Limpa as colunas financeiras e converte textos (ex: `R$ 1.000,00`) para valores decimais calculáveis.
3. **📊 Decisão Orientada a Lucro:** Agrupa os dados e calcula matematicamente o vencedor do teste focando no **Lucro** (Comissão - Cashback) e **ROI**.
4. **🤖 Integração com IA:** Gera automaticamente arquivos de texto (`.txt`) na pasta `relatorios/` contendo um "Prompt" pronto. É só copiar e colar no ChatGPT/Claude para receber um relatório gerencial em segundos.
5. **☁️ Integração com Google Sheets:** Conecta de forma segura com o Google Drive/Sheets e alimenta uma planilha em tempo real. E ainda previne duplicidades conferindo se o parceiro já foi salvo!

---

## 📁 Estrutura de Pastas

```text
📦 Meliuz-Growth-Test
 ┣ 📂 datasets/        # Coloque aqui todos os arquivos .csv exportados dos testes A/B
 ┣ 📂 relatorios/      # (Gerado Automaticamente) Prompts prontos para a Inteligência Artificial
 ┣ 📂 scripts/
 ┃ ┗ 📜 analisador_ab.py  # O script principal onde a mágica acontece
 ┣ 📜 credentials.json # (NÃO COMMITAR) Suas chaves de acesso seguras do Google Cloud
 ┣ 📜 .gitignore       # Protege arquivos sensíveis de irem para o GitHub
 ┗ 📜 README.md
```

---

## ⚙️ Como Executar o Projeto

### 1. Pré-requisitos e Segurança (`credentials.json`)
Como este projeto se conecta a uma planilha na nuvem, as chaves de acesso (`credentials.json`) **não foram enviadas para o GitHub** (é uma boa prática de segurança ignorá-las via `.gitignore`).

Mas não se preocupe! **Você não precisa delas para avaliar o código.**
O script foi construído para funcionar perfeitamente em modo local. Se ele não encontrar o arquivo `credentials.json`, ele avisará que vai pular a etapa da nuvem, mas **continuará rodando a análise A/B inteira** e gerará os relatórios de IA localmente na pasta `relatorios/` para você conferir o resultado da lógica!

*(Caso faça questão de ver a integração com o Google Sheets rodando, por favor, me avise que eu lhe envio a minha chave de acesso de forma segura).*

### 2. Ative a Máquina Virtual (Ambiente Python)
Para proteger seu computador de conflitos de versões, os pacotes como `pandas` e `gspread` foram instalados de forma isolada. 

Para rodar, basta executar esse comando no terminal a partir da pasta raiz do projeto:

```bash
.venv/bin/python scripts/analisador_ab.py
```

Pronto! Agora é só acompanhar no terminal os datasets sendo processados e conferir os resultados caindo instantaneamente na sua planilha do Google Sheets.

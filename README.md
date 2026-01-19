# 🏭 Manufacturing Defects

Projeto de análise de dados e visualização de defeitos de fabricação, utilizando **Python** para explorar padrões de qualidade em um processo industrial e apoiar a tomada de decisão baseada em dados.
O repositório reúne uma análise exploratória em notebook e uma aplicação interativa para visualização dos defeitos ao longo do tempo.

# 📌 Objetivo do Projeto

Analisar dados de inspeção de peças fabricadas, identificando:
- Padrões de defeitos ao longo dos dias e amostras;
- Tendências de aumento ou redução de defeitos;
- Possíveis insights para melhoria contínua de processos industriais.

Este projeto tem foco em Análise de Dados aplicada à indústria, servindo também como item de portfólio.

# 🗂️ Estrutura do Projeto
manufacturing-defects/
- .devcontainer/               # Configurações de ambiente (opcional)
- Manufacturing_Defects.ipynb  # Análise exploratória dos dados
- app.py                       # Aplicação para visualização interativa
- defects_data_final.csv       # Dataset de defeitos de fabricação
- requirements.txt             # Dependências do projeto

# 📊 Análise Exploratória

O notebook Manufacturing_Defects.ipynb contém:
- Carregamento e tratamento dos dados;
- Estatísticas descritivas;
- Visualizações para análise de defeitos ao longo do tempo;
- Identificação de padrões e possíveis outliers.

Pode ser executado localmente via Jupyter Notebook ou em ambientes como VS Code e Google Colab.

# 📈 Aplicação Interativa

O arquivo app.py disponibiliza uma aplicação para visualização dos dados, permitindo:
- Exploração visual da quantidade de defeitos;
- Análise temporal;
- Apoio à interpretação dos dados de forma interativa.

Para executar:

streamlit run app.py
(ou conforme a implementação do app)

🛠️ Tecnologias Utilizadas

- Python
- Pandas
- NumPy
- Matplotlib / Seaborn
- Jupyter Notebook
- Streamlit

# 🔮 Próximos Passos

- Implementar detecção de outliers;
- Criar modelos de previsão de defeitos;
- Expandir a aplicação com filtros avançados;
- Adicionar métricas de qualidade do processo.

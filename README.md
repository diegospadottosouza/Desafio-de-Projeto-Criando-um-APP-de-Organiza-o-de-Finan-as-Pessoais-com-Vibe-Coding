📊 Finance Vibe - Organização de Finanças Pessoais

https://img.shields.io/badge/Python-3.13-blue?logo=python
https://img.shields.io/badge/Streamlit-App-red?logo=streamlit
https://img.shields.io/badge/License-MITigreen

Um aplicativo interativo desenvolvido em Python + Streamlit para ajudar na organização das finanças pessoais.
O projeto inclui categorização automática de transações, relatórios visuais, previsão de gastos e exportação de relatórios em Excel e PDF.

🚀 Funcionalidades

- Cadastro de transações (valor, data, descrição e categoria)
- Categorização automática com IA (Naive Bayes + NLP)
- Filtros por período e categoria
- Relatórios visuais:
- Gráfico de barras
- Gráfico de pizza
- Gráfico de linha interativa
- Previsão de gastos futuros (Regressão Linear)
- Metas financeiras com alertas inteligentes
- Exportação de relatórios:
- Excel (.xlsx)
- PDF estilizado com tabela e gráficos

🛠️ Tecnologias utilizadas
- Python 3.13+
- Streamlit
- Pandas
- Matplotlib
- Plotly
- Scikit-learn
- ReportLab
- Kaleido

📂 Estrutura do projeto
finance-app/
│
├── src/
│   └── app.py          # Código principal do aplicativo
├── transacoes.csv      # Base de dados local (gerada automaticamente)
├── requirements.txt    # Lista de dependências
└── README.md           # Documentação do projeto



▶️ Como executar
- Clone este repositório:
git clone https://github.com/seu-usuario/finance-vibe.git
cd finance-vibe/src
- Crie um ambiente virtual (opcional, mas recomendado):
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac
- Instale as dependências:
pip install -r requirements.txt
- Execute o aplicativo:
streamlit run app.py


📦 Dependências (requirements.txt)
streamlit
pandas
matplotlib
plotly
scikit-learn
reportlab
kaleido


📸 Demonstração
- Tela inicial com cadastro de transações
- Relatórios interativos com gráficos
- Exportação para Excel e PDF
(adicione prints ou GIFs aqui para mostrar o funcionamento do app)

👨‍💻 Autor
Projeto desenvolvido por Diego Spadotto de Souza durante o desafio da DIO com Vibe Coding.

📜 Licença
Este projeto está sob a licença MIT.
Sinta-se livre para usar, modificar e compartilhar.

import streamlit as st
import pandas as pd
import os
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Image
from reportlab.lib import colors

st.title("📊 Finance Vibe - Organização de Finanças Pessoais")

csv_path = "transacoes.csv"

def carregar_dados():
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        return pd.DataFrame(columns=["Valor", "Categoria", "Data", "Descricao"])

def salvar_transacao(valor, categoria, data, descricao):
    nova = pd.DataFrame([[valor, categoria, data, descricao]], 
                        columns=["Valor", "Categoria", "Data", "Descricao"])
    dados = carregar_dados()
    dados = pd.concat([dados, nova], ignore_index=True)
    dados.to_csv(csv_path, index=False)

# Função para gerar PDF com tabela + gráficos
def gerar_pdf(dados_filtrados):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "Relatório Financeiro")

    # Converter dados para tabela
    if not dados_filtrados.empty:
        data_table = [dados_filtrados.columns.tolist()] + dados_filtrados.values.tolist()
        table = Table(data_table)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.grey),
            ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0,0), (-1,0), 12),
            ("BACKGROUND", (0,1), (-1,-1), colors.beige),
        ]))
        table.wrapOn(c, 50, 600)
        table.drawOn(c, 50, 600)

        # --- Gráfico de Pizza ---
        fig, ax = plt.subplots()
        dados_filtrados.groupby("Categoria")["Valor"].sum().plot.pie(
            autopct='%1.1f%%', ax=ax, startangle=90, cmap="Set3"
        )
        ax.set_ylabel("")
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format="png")
        plt.close(fig)
        img_buffer.seek(0)
        img = Image(img_buffer, width=300, height=300)
        img.drawOn(c, 150, 250)

        # --- Gráfico de Linha ---
        fig_line = px.line(dados_filtrados, x="Data", y="Valor", color="Categoria", markers=True,
                           title="Gastos ao longo do tempo")
        fig_line.write_image(img_buffer, format="png")
        img_buffer.seek(0)
        img2 = Image(img_buffer, width=400, height=250)
        img2.drawOn(c, 100, 50)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
# Entrada de dados
descricao = st.text_input("Descrição da transação (ex.: Uber, Pizza, Mercado)")
valor = st.number_input("Digite o valor da transação:")
data = st.date_input("Data da transação")

# 🔮 Categorização automática
dados = carregar_dados()
categoria_sugerida = "Outros"
if not dados.empty and "Descricao" in dados.columns and dados["Descricao"].notnull().any():
    try:
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(dados["Descricao"].astype(str))
        y = dados["Categoria"]

        modelo_cat = MultinomialNB()
        modelo_cat.fit(X, y)

        if descricao:
            X_novo = vectorizer.transform([descricao])
            categoria_sugerida = modelo_cat.predict(X_novo)[0]
    except Exception as e:
        categoria_sugerida = "Outros"

categoria = st.selectbox(
    "Categoria", 
    ["Alimentação", "Transporte", "Lazer", "Outros"], 
    index=["Alimentação","Transporte","Lazer","Outros"].index(categoria_sugerida)
)

if st.button("Adicionar"):
    salvar_transacao(valor, categoria, data, descricao)
    st.success(f"Transação salva com sucesso! Categoria sugerida: {categoria}")

# 📅 Filtros
dados = carregar_dados()
if not dados.empty:
    st.subheader("Filtros de Análise")

    # Filtro por período
    data_inicio = st.date_input("Data inicial", value=pd.to_datetime("2025-01-01"))
    data_fim = st.date_input("Data final", value=pd.to_datetime("today"))

    # Filtro por categoria
    categoria_filtro = st.selectbox("Filtrar por categoria", ["Todas"] + dados["Categoria"].unique().tolist())

    # Aplicar filtros
    dados["Data"] = pd.to_datetime(dados["Data"])
    dados_filtrados = dados[(dados["Data"] >= pd.to_datetime(data_inicio)) & (dados["Data"] <= pd.to_datetime(data_fim))]

    if categoria_filtro != "Todas":
        dados_filtrados = dados_filtrados[dados_filtrados["Categoria"] == categoria_filtro]

    # 📊 Relatório
    st.subheader("Resumo das Transações")
    st.dataframe(dados_filtrados)

    # Gráfico de barras
    st.bar_chart(dados_filtrados.groupby("Categoria")["Valor"].sum())

    # 📊 Gráfico de Pizza
    st.subheader("Distribuição de Gastos por Categoria")
    fig, ax = plt.subplots()
    dados_filtrados.groupby("Categoria")["Valor"].sum().plot.pie(
        autopct='%1.1f%%', ax=ax, startangle=90, cmap="Set3"
    )
    ax.set_ylabel("")
    st.pyplot(fig)

    # 📈 Evolução dos Gastos ao longo do tempo
    st.subheader("Evolução dos Gastos")
    fig_line = px.line(dados_filtrados, x="Data", y="Valor", color="Categoria", markers=True,
                       title="Gastos ao longo do tempo")
    st.plotly_chart(fig_line)

    # 🔮 Previsão de gastos futuros
    st.subheader("Previsão de Gastos")
    try:
        dados_filtrados["Dias"] = (dados_filtrados["Data"] - dados_filtrados["Data"].min()).dt.days

        X = dados_filtrados[["Dias"]]
        y = dados_filtrados["Valor"]

        modelo = LinearRegression()
        modelo.fit(X, y)

        futuro = np.array(range(dados_filtrados["Dias"].max()+1, dados_filtrados["Dias"].max()+8)).reshape(-1,1)
        previsao = modelo.predict(futuro)

        previsao_df = pd.DataFrame({
            "Dia Futuro": range(1, 8),
            "Valor Previsto": previsao
        })

        st.line_chart(previsao_df.set_index("Dia Futuro"))
        st.write(previsao_df)
    except Exception as e:
        st.warning("Não foi possível gerar previsão. Adicione mais dados para treinar o modelo.")

    # 🎯 Metas financeiras
    st.subheader("Metas Financeiras")
    meta = st.number_input("Defina sua meta mensal de gastos (R$):", min_value=0.0, step=100.0)

    if meta > 0:
        gasto_total = dados_filtrados["Valor"].sum()
        st.write(f"Gasto total até agora: R${gasto_total:.2f}")
        if gasto_total >= meta:
            st.error("⚠️ Atenção! Você já atingiu ou ultrapassou sua meta de gastos.")
        elif gasto_total >= meta * 0.8:
            st.warning("⚠️ Você está perto de atingir sua meta (80%).")
        else:
            st.success("✅ Você está dentro da meta. Continue assim!")

    # 📤 Exportação dos relatórios
    st.subheader("Exportar Relatórios")

    # Exportar para Excel
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        dados_filtrados.to_excel(writer, sheet_name="Relatório", index=False)
    st.download_button(
        label="📥 Baixar Excel",
        data=buffer.getvalue(),
        file_name="relatorio_financeiro.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Exportar para PDF estilizado com gráficos
    pdf_buffer = gerar_pdf(dados_filtrados)
    st.download_button(
        label="📥 Baixar PDF com Gráficos",
        data=pdf_buffer,
        file_name="relatorio_financeiro.pdf",
        mime="application/pdf"
    )
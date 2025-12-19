import streamlit as st
from groq import Groq
from tavily import TavilyClient
from datetime import datetime

# --- CONFIGURAÇÃO ---
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]

client = Groq(api_key=GROQ_API_KEY)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

st.set_page_config(page_title="Agente de Viagens Global", page_icon="🌍", layout="wide")

with st.sidebar:
    st.header("💰 Câmbio e Datas")
    moeda_final = st.selectbox("Minha moeda:", ["BRL", "USD", "EUR"])
    data_ida = st.date_input("Data de Ida", datetime.now())
    st.info("O agente buscará preços reais e gerará links de reserva.")

st.title("✈️ Busca de Passagens e Preços Reais")

c1, c2 = st.columns([2, 1])
with c1:
    origem = st.text_input("Cidade de Origem (Ex: São Paulo):", "São Paulo")
    destino = st.text_input("Cidade de Destino:", "Roma")
with c2:
    passageiros = st.number_input("Passageiros:", min_value=1, value=1)

if st.button("🚀 Pesquisar Passagens e Preços"):
    with st.spinner(f"Varrendo a web por voos de {origem} para {destino}..."):
        
        # 1. Pesquisa focada em voos e preços atuais
        query_voos = f"passagens aéreas de {origem} para {destino} em {data_ida} preços reais 2024 2025"
        busca = tavily.search(query=query_voos, search_depth="advanced", max_results=5)
        contexto = "\n".join([f"Site: {r['url']} - Info: {r['content']}" for r in busca['results']])
        
        # 2. Prompt para extrair preços e links
        prompt = f"""
        Você é um buscador de passagens aéreas.
        DADOS ATUAIS DA WEB: {contexto}
        
        TAREFA:
        1. Liste os preços de voos encontrados de {origem} para {destino} para {passageiros} passageiro(s).
        2. Converta os valores para {moeda_final}.
        3. Crie uma seção chamada "🔗 Links Rápidos de Busca" com links diretos para o Google Flights e Skyscanner usando estes termos: {origem} para {destino}.
        4. Cite as companhias aéreas que aparecem nos resultados.
        """
        
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        
        resultado = chat.choices[0].message.content
        
        # 3. Exibição
        st.subheader(f"🎫 Opções de Voos: {origem} ➡️ {destino}")
        st.markdown(resultado)
        
        link_google = f"https://www.google.com/travel/flights?q=Flights%20to%20{destino}%20from%20{origem}%20on%20{data_ida}"
        
        st.divider()
        st.subheader("🔗 Atalhos de Reserva")
        st.link_button("Ver no Google Flights", link_google)
import streamlit as st
import google.generativeai as genai
import pandas as pd
import json

# 1. Configurações Visuais
st.set_page_config(page_title="AdSaver Pro", layout="wide")
st.title("🚀 AdSaver: Performance Engineering Engine")

# 2. Conexão Segura
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Erro: Configure a GEMINI_API_KEY nos Secrets.")
    st.stop()

# --- BARRA LATERAL (SIMULAÇÃO DE PLANOS) ---
st.sidebar.header("💎 Configuração da Conta")
plano_escolhido = st.sidebar.radio(
    "Selecione o Plano Ativo:",
    ("Basic (Econômico)", "Pro (High-Performance)")
)

# Lógica de seleção do Modelo
if "Basic" in plano_escolhido:
    modelo_atual = 'gemini-1.5-flash'
    st.sidebar.info("⚡ Plano Basic: Usando motor Flash (Rápido e Custo Zero).")
else:
    modelo_atual = 'gemini-1.5-pro'
    st.sidebar.warning("🔥 Plano Pro: Usando motor 1.5 Pro (Máxima inteligência BoF).")

st.markdown("---")

# 3. Interface Limpa
col1, col2 = st.columns(2)
with col1:
    url_final = st.text_input("🔗 URL da Landing Page", placeholder="Ex: https://seusite.com.br/oferta")
    camp_name = st.text_input("🏷️ Nome da Campanha", placeholder="Ex: [VENDAS] - Produto - BoF")
with col2:
    contexto = st.text_area("📝 Briefing de Contexto", placeholder="Diferenciais, dores e público-alvo...")

# 4. Motor de Geração
if st.button("CONSTRUIR CAMPANHA ROI-FOCUS"):
    if not url_final or not contexto:
        st.warning("Preencha URL e Briefing para continuar.")
    else:
        with st.spinner(f"Processando com IA Senior ({modelo_atual})..."):
            try:
                # Instancia o modelo escolhido no plano
                model = genai.GenerativeModel(modelo_atual)
                
                # Prompt de Engenharia
                prompt = f"""
                Aja como Senior Performance Engineer. Analise: {url_final} e {contexto}.
                Gere estrutura Google Ads BoF.
                RESPONDA APENAS JSON ESTRITO:
                {{
                "ads": [{{ "Campaign": "{camp_name}", "Ad Group": "BoF_Principal", "Headline 1": "...", "Headline 2": "...", "Description 1": "...", "Final URL": "{url_final}" }}],
                "keywords": [{{ "Campaign": "{camp_name}", "Ad Group": "BoF_Principal", "Keyword": "...", "Match Type": "Exact" }}],
                "extensions": [{{ "Campaign": "{camp_name}", "Text": "...", "URL": "{url_final}" }}]
                }}
                Regras: Títulos < 30 chars, Descrições < 90 chars.
                """
                
                response = model.generate_content(prompt)
                text_clean = response.text.strip().replace('```json', '').replace('```', '')
                data = json.loads(text_clean)
                
                st.success(f"✅ Sucesso! Gerado com o motor: {modelo_atual}")
                
                # Botões de Download
                c1, c2, c3 = st.columns(3)
                with c1:
                    df1 = pd.DataFrame(data.get('ads', []))
                    st.download_button("📥 Anúncios", df1.to_csv(index=False).encode('utf-8'), "ads.csv")
                with c2:
                    df2 = pd.DataFrame(data.get('keywords', []))
                    st.download_button("📥 Keywords", df2.to_csv(index=False).encode('utf-8'), "keys.csv")
                with c3:
                    df3 = pd.DataFrame(data.get('extensions', []))
                    st.download_button("📥 Extensões", df3.to_csv(index=False).encode('utf-8'), "ext.csv")

            except Exception as e:
                st.error(f"Erro técnico: {str(e)}")
                st.info("Nota: Se estiver usando o modelo Pro e der erro 404, verifique o requirements.txt ou mude para o Basic.")

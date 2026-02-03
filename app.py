import streamlit as st
import google.generativeai as genai
import pandas as pd
import json

# Título e Configuração
st.set_page_config(page_title="AdSaver Pro", layout="wide")
st.title("🚀 AdSaver: Performance Engineering BoF")

# 1. SEGURANÇA: Busca a chave nos Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Configure a GEMINI_API_KEY nos Secrets do Streamlit.")
    st.stop()

# 2. INTERFACE DE INPUT
col1, col2 = st.columns(2)
with col1:
    url_final = st.text_input("🔗 URL da Landing Page", value="https://seusite.com.br/planejador-financeiro")
    camp_name = st.text_input("🏷️ Nome da Campanha", value="[VENDAS] - Software Financeiro - BoF")
with col2:
    contexto = st.text_area("📝 Briefing do Produto", value="Software de planejamento financeiro mensal... R$ 14,99/mês.")

# 3. LÓGICA DE GERAÇÃO
if st.button("CONSTRUIR ESTRUTURA ROI-FOCUS"):
    with st.spinner("Gerando estrutura BoF e Extensões..."):
        try:
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            # Prompt Senior focado em 3 CSVs
            prompt = f"""
            Aja como um Senior Performance Engineer. Analise a URL {url_final} e o contexto {contexto}.
            Gere uma estrutura de Google Ads Fundo de Funil (BoF).
            RESPONDA APENAS UM JSON ESTRITO com as chaves:
            - "ads": [{{ "Campaign": "{camp_name}", "Ad Group": "BoF_Principal", "Headline 1": "...", (até 15), "Description 1": "...", (até 4), "Final URL": "{url_final}" }}]
            - "keywords": [{{ "Campaign": "{camp_name}", "Ad Group": "BoF_Principal", "Keyword": "...", "Match Type": "Exact" }}]
            - "extensions": [{{ "Campaign": "{camp_name}", "Type": "Sitelink", "Sitelink Text": "...", "Sitelink Desc 1": "...", "Sitelink URL": "{url_final}/oferta" }}]
            
            Regras de Caracteres: Headlines máx 28, Descrições máx 85.
            """
            
            response = model.generate_content(prompt)
            texto_limpo = response.text.strip().replace('```json', '').replace('```', '')
            data = json.loads(texto_limpo)
            
            st.success("✅ Estrutura BoF Gerada com Sucesso!")
            
            # 4. BOTÕES DE DOWNLOAD (Os 3 CSVs)
            c1, c2, c3 = st.columns(3)
            with c1:
                df_ads = pd.DataFrame(data['ads'])
                st.download_button("📥 CSV Anúncios (RSA)", df_ads.to_csv(index=False).encode('utf-8'), "1_ads.csv")
            with c2:
                df_keys = pd.DataFrame(data['keywords'])
                st.download_button("📥 CSV Palavras-Chave", df_keys.to_csv(index=False).encode('utf-8'), "2_keywords.csv")
            with c3:
                df_ext = pd.DataFrame(data['extensions'])
                st.download_button("📥 CSV Extensões (Sitelinks)", df_ext.to_csv(index=False).encode('utf-8'), "3_extensions.csv")
                
        except Exception as e:
            st.error(f"Erro técnico: {str(e)}")

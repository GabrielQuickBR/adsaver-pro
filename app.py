import streamlit as st
import google.generativeai as genai
import pandas as pd
import json

# 1. Configurações Iniciais do App
st.set_page_config(page_title="AdSaver Pro - BoF Engine", layout="wide")
st.title("🚀 AdSaver: Performance Engineering Engine")
st.markdown("---")

# 2. Conexão Segura com a API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Erro: GEMINI_API_KEY não encontrada nos Secrets.")
    st.stop()

# 3. Interface de Trabalho (Inputs)
col1, col2 = st.columns(2)
with col1:
    url_final = st.text_input("🔗 URL da Landing Page", placeholder="https://seusite.com.br")
    camp_name = st.text_input("🏷️ Nome da Campanha", placeholder="[VENDAS] - Produto - BoF")
with col2:
    contexto = st.text_area("📝 Briefing de Contexto", placeholder="Diferenciais, dores e o que o produto resolve...")

# 4. Motor de Geração ROI-FOCUS
if st.button("CONSTRUIR CAMPANHA ROI-FOCUS"):
    if not url_final or not contexto:
        st.warning("Preencha a URL e o Briefing para continuar.")
    else:
        with st.spinner("IA Senior processando estrutura BoF..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-pro')
                
                # Prompt de Engenharia para 3 CSVs Separados
                prompt = f"""
                Você é um Senior Performance Engineer. Gere uma estrutura de Google Ads para:
                URL: {url_final}
                Contexto: {contexto}

                RESPONDA APENAS UM JSON ESTRITO com as seguintes chaves:
                - "ads": [{{ "Campaign": "{camp_name}", "Ad Group": "BoF_Principal", "Headline 1": "...", "Headline 2": "...", (até 15), "Description 1": "...", (até 4), "Final URL": "{url_final}" }}]
                - "keywords": [{{ "Campaign": "{camp_name}", "Ad Group": "BoF_Principal", "Keyword": "...", "Match Type": "Exact" }}]
                - "extensions": [{{ "Campaign": "{camp_name}", "Sitelink Text": "...", "Sitelink Desc 1": "...", "Sitelink URL": "{url_final}/oferta" }}]

                REGRAS: Títulos < 30 caracteres. Descrições < 90 caracteres. Foco exclusivo em Fundo de Funil (BoF).
                """
                
                response = model.generate_content(prompt)
                # Limpa a resposta para garantir que seja apenas JSON
                json_data = response.text.strip().replace('```json', '').replace('```', '')
                data = json.loads(json_data)
                
                st.success("✅ Estrutura gerada com sucesso!")
                
                # 5. Entrega dos 3 CSVs para Download
                st.subheader("📥 Exportar para Google Ads Editor")
                d1, d2, d3 = st.columns(3)
                
                with d1:
                    df_ads = pd.DataFrame(data['ads'])
                    st.download_button("Anúncios (RSA)", df_ads.to_csv(index=False).encode('utf-8'), "1_ads_rsa.csv", "text/csv")
                
                with d2:
                    df_keys = pd.DataFrame(data['keywords'])
                    st.download_button("Palavras-Chave", df_keys.to_csv(index=False).encode('utf-8'), "2_keywords.csv", "text/csv")
                
                with d3:
                    df_ext = pd.DataFrame(data['extensions'])
                    st.download_button("Extensões (Sitelinks)", df_ext.to_csv(index=False).encode('utf-8'), "3_extensions.csv", "text/csv")

            except Exception as e:
                st.error(f"Erro na análise técnica: {str(e)}")

st.markdown("---")
st.caption("Pronto para importação via Google Ads Editor.")

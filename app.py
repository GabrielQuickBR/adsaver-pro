import streamlit as st
import google.generativeai as genai
import pandas as pd
import json

# Configuração da página
st.set_page_config(page_title="AdSaver Pro - BoF Engine", layout="wide")
st.title("🚀 AdSaver: Performance Engineering BoF")

# Puxa a chave automaticamente do "Cofre" (Secrets)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Erro: API Key não encontrada nos Secrets.")
    st.stop()

# Interface Limpa (Sem barra lateral)
col1, col2 = st.columns(2)
with col1:
    url_final = st.text_input("🔗 URL da Landing Page", placeholder="https://seusite.com.br")
    camp_name = st.text_input("🏷️ Nome da Campanha", placeholder="[VENDAS] - Produto - BoF")
with col2:
    contexto = st.text_area("📝 Briefing do Produto", placeholder="Descreva o diferencial ou a dor que o produto resolve...")

if st.button("CONSTRUIR CAMPANHA ROI-FOCUS"):
    with st.spinner("Gerando estrutura BoF infalível..."):
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Super Prompt calibrado para o Ads Editor
        prompt = f"""
        Aja como um Senior Performance Engineer. Analise a URL {url_final} e o contexto {contexto}.
        Gere uma campanha de Google Ads Fundo de Funil (BoF).
        Responda APENAS com um JSON estrito:
        {{
          "ads": [{{"Campaign": "{camp_name}", "Ad Group": "BoF_Principal", "Headline 1": "...", "Description 1": "...", "Final URL": "{url_final}"}}],
          "keywords": [{{"Campaign": "{camp_name}", "Ad Group": "BoF_Principal", "Keyword": "...", "Match Type": "Exact"}}]
        }}
        Regras: Títulos < 30 char, Descrições < 90 char.
        """
        
        try:
            response = model.generate_content(prompt)
            data = json.loads(response.text.replace('```json', '').replace('```', ''))
            
            st.success("Estrutura Gerada!")
            # Botões de Download
            df_ads = pd.DataFrame(data['ads'])
            st.download_button("📥 Baixar CSV de Anúncios", df_ads.to_csv(index=False).encode('utf-8'), "ads.csv")
            
            df_keys = pd.DataFrame(data['keywords'])
            st.download_button("📥 Baixar CSV de Palavras-Chave", df_keys.to_csv(index=False).encode('utf-8'), "keywords.csv")
            
        except:
            st.error("Erro na geração. Tente novamente.")

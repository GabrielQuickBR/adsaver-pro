import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
import io

# Configuração visual do SaaS
st.set_page_config(page_title="Performance Engine - BoF", layout="wide")
st.title("🚀 Performance Engineering Engine: Google Ads")
st.markdown("---")

# Sidebar para a chave da API (Segurança inicial)
api_key = st.sidebar.text_input("Insira sua Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)

# Interface de Input
col1, col2 = st.columns(2)
with col1:
    url_final = st.text_input("🔗 URL da Landing Page", placeholder="https://seusite.com.br")
    camp_name = st.text_input("🏷️ Nome da Campanha", placeholder="[VENDAS] - Produto - BoF")
with col2:
    contexto = st.text_area("📝 Briefing/Dores do Produto", placeholder="Descreva o diferencial ou a dor que o produto resolve...")

# Botão de Ação
if st.button("CONSTRUIR CAMPANHA ROI-FOCUS"):
    if not api_key or not url_final or not contexto:
        st.warning("Por favor, preencha todos os campos.")
    else:
        with st.spinner("IA analisando URL e gerando estrutura BoF..."):
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            # Prompt de Engenharia Senior
            prompt = f"""
            Aja como um Senior Performance Engineer focado em Fundo de Funil (BoF).
            Analise: URL {url_final} e Contexto {contexto}.
            Gere uma estrutura pronta para Google Ads Editor.
            
            SAÍDA OBRIGATÓRIA EM JSON ESTRITO:
            {{
              "ads": [{{"Campaign": "{camp_name}", "Ad_Group": "BoF_Principal", "Headline_1": "...", "Description_1": "...", "Final_URL": "{url_final}"}}],
              "keywords": [{{"Campaign": "{camp_name}", "Ad_Group": "BoF_Principal", "Keyword": "...", "Match_Type": "Exact"}}],
              "extensions": [{{"Campaign": "{camp_name}", "Type": "Sitelink", "Text": "...", "Desc1": "...", "Desc2": "...", "Final_URL": "{url_final}/oferta"}}]
            }}
            REGRAS: Headlines < 30 char. Descriptions < 90 char. Ignore termos informacionais.
            """
            
            try:
                response = model.generate_content(prompt)
                # Limpeza e conversão do JSON
                clean_json = response.text.replace('```json', '').replace('```', '')
                data = json.loads(clean_json)
                
                # Exibição e Botões de Download
                st.success("Estrutura gerada com sucesso!")
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    df_ads = pd.DataFrame(data['ads'])
                    st.download_button("📥 CSV Anúncios", df_ads.to_csv(index=False).encode('utf-8'), "1_campanha_ads.csv")
                with c2:
                    df_keys = pd.DataFrame(data['keywords'])
                    st.download_button("📥 CSV Palavras-Chave", df_keys.to_csv(index=False).encode('utf-8'), "2_keywords.csv")
                with c3:
                    df_ext = pd.DataFrame(data['extensions'])
                    st.download_button("📥 CSV Extensões", df_ext.to_csv(index=False).encode('utf-8'), "3_extensoes.csv")
                
            except Exception as e:
                st.error("Erro na geração. Tente ser mais específico no briefing.")

st.markdown("---")
st.caption("Foco em Prontidão para Importação no Google Ads Editor.")

import streamlit as st
import google.generativeai as genai
import pandas as pd
import json

# 1. Configurações Visuais
st.set_page_config(page_title="AdSaver Pro", layout="wide")
st.title("🚀 AdSaver Pro")
st.markdown("---")

# 2. Conexão Segura (Busca a chave nos Secrets)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Erro: Configure a GEMINI_API_KEY nos Secrets.")
    st.stop()

# 3. Interface de Trabalho (Campos Limpos com Placeholder)
col1, col2 = st.columns(2)
with col1:
    url_final = st.text_input(
        "🔗 URL da Landing Page", 
        placeholder="Ex: https://seusite.com.br/produto-venda"
    )
    camp_name = st.text_input(
        "🏷️ Nome da Campanha", 
        placeholder="Ex: [VENDAS] - Nome do Produto - Fundo de Funil"
    )
with col2:
    contexto = st.text_area(
        "📝 Briefing de Contexto", 
        placeholder="Descreva os diferenciais, a dor que o produto resolve e o público-alvo..."
    )

# 4. Geração da Campanha
if st.button("CONSTRUIR CAMPANHA ROI-FOCUS"):
    if not url_final or not contexto:
        st.warning("Por favor, insira a URL e o Briefing para continuar.")
    else:
        with st.spinner("IA Senior processando estrutura BoF..."):
            try:
                # Modelo Flash para maior estabilidade e velocidade
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                Aja como um Senior Performance Engineer focado em Fundo de Funil (BoF).
                Analise a URL {url_final} e o contexto {contexto}.
                Gere uma estrutura de Google Ads pronta para o Editor.
                
                RESPONDA APENAS UM JSON ESTRITO com as chaves:
                - "ads": [{{ "Campaign": "{camp_name}", "Ad Group": "BoF_Principal", "Headline 1": "...", "Description 1": "...", "Final URL": "{url_final}" }}]
                - "keywords": [{{ "Campaign": "{camp_name}", "Ad Group": "BoF_Principal", "Keyword": "...", "Match Type": "Exact" }}]
                - "extensions": [{{ "Campaign": "{camp_name}", "Text": "...", "URL": "{url_final}" }}]

                Regras: Headlines < 30 char, Descriptions < 90 char.
                """
                
                response = model.generate_content(prompt)
                texto_json = response.text.strip().replace('```json', '').replace('```', '')
                data = json.loads(texto_json)
                
                st.success("✅ Estrutura gerada com sucesso!")
                
                # 5. Entrega dos CSVs
                c1, c2, c3 = st.columns(3)
                with c1:
                    df_ads = pd.DataFrame(data['ads'])
                    st.download_button("📥 Baixar Anúncios", df_ads.to_csv(index=False).encode('utf-8'), "1_ads.csv")
                with c2:
                    df_keys = pd.DataFrame(data['keywords'])
                    st.download_button("📥 Baixar Keywords", df_keys.to_csv(index=False).encode('utf-8'), "2_keywords.csv")
                with c3:
                    df_ext = pd.DataFrame(data['extensions'])
                    st.download_button("📥 Baixar Extensões", df_ext.to_csv(index=False).encode('utf-8'), "3_extensoes.csv")
                    
            except Exception as e:
                st.error(f"Erro na análise técnica: {str(e)}")

st.markdown("---")
st.caption("Pronto para importação via Google Ads Editor.")

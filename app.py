import streamlit as st
import pandas as pd
import joblib
import os
import numpy as np

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="JusDataPredict",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- FUNÇÕES DE CARREGAMENTO (COM CACHE) ---
# O cache do Streamlit evita recarregar os modelos a cada interação do usuário
@st.cache_resource
def load_artifacts():
    """Carrega todos os artefatos necessários (modelo, dataframes, etc.)."""
    try:
        model_path = os.path.join('models', 'risk_prediction_model.joblib')
        df_path = os.path.join('models', 'jurisprudencia_df.joblib')
        vectorizer_path = os.path.join('models', 'similarity_vectorizer.joblib')
        matrix_path = os.path.join('models', 'cosine_similarity_matrix.joblib')

        model = joblib.load(model_path)
        df = joblib.load(df_path)
        similarity_vectorizer = joblib.load(vectorizer_path)
        cosine_sim_matrix = joblib.load(matrix_path)
        return model, df, similarity_vectorizer, cosine_sim_matrix
    except FileNotFoundError:
        st.error("Arquivos de modelo não encontrados. Por favor, execute o script 'train_model.py' primeiro.")
        return None, None, None, None

# --- CARREGAMENTO DOS DADOS ---
model, df, similarity_vectorizer, cosine_sim_matrix = load_artifacts()

# Se o carregamento falhar, interrompe a execução
if model is None:
    st.stop()


# --- FUNÇÕES AUXILIARES ---
def predict_risk(tese, juizo, model):
    """Faz a predição da probabilidade de êxito."""
    # Combina as features da mesma forma que no treinamento
    input_features = f"{tese} {juizo}"
    # O modelo espera uma lista ou array
    prediction_proba = model.predict_proba([input_features])
    # A coluna 1 corresponde à classe 'Procedente'
    success_probability = prediction_proba[0][1]
    return success_probability

def get_risk_level(probability):
    """Categoriza o risco com base na probabilidade."""
    if probability < 0.30:
        return "Alto Risco", "error"
    elif probability < 0.60:
        return "Risco Médio", "warning"
    else:
        return "Baixo Risco", "success"

def find_similar_cases(tese, df, vectorizer, sim_matrix, top_n=5):
    """Encontra os casos mais similares à tese informada."""
    # Vetoriza a nova tese
    tese_vector = vectorizer.transform([tese])
    
    # Vetoriza todas as teses do dataset para garantir dimensionalidade consistente
    all_teses_vectors = vectorizer.transform(df['tese_juridica'])
    
    # Calcula similaridade entre a nova tese e todas as teses existentes
    cosine_similarities = (tese_vector * all_teses_vectors.T).toarray().flatten()
    
    # Obtém os índices dos 'top_n' casos mais similares
    similar_indices = cosine_similarities.argsort()[:-top_n-1:-1]
    
    # Retorna o subset do dataframe com os casos similares
    similar_cases = df.iloc[similar_indices]
    return similar_cases

# --- INTERFACE DO USUÁRIO (UI) ---

# Título e Descrição
st.title("⚖️ JusDataPredict")
st.markdown("##### Sistema de Análise Preditiva de Risco e Consistência Jurisprudencial")
st.markdown("---")

# Sidebar para inputs
st.sidebar.header("Analisar Novo Caso")
juizos_list = sorted(df['juizo'].unique().tolist())
selected_juizo = st.sidebar.selectbox("Selecione o Juízo", juizos_list)
input_tese = st.sidebar.text_area("Descreva a Tese Jurídica Principal", height=150,
                                  placeholder="Ex: Negativação indevida do nome do consumidor por dívida já paga.")

analyze_button = st.sidebar.button("Analisar Risco e Consistência", type="primary")

# --- LÓGICA DA APLICAÇÃO ---
if analyze_button:
    if input_tese and selected_juizo:
        with st.spinner('Analisando dados e jurisprudência...'):
            # 1. Módulo de Predição de Risco
            probability = predict_risk(input_tese, selected_juizo, model)
            risk_level, risk_color = get_risk_level(probability)
            
            # 2. Módulo de Análise de Consistência Jurisprudencial
            similar_cases = find_similar_cases(input_tese, df, similarity_vectorizer, cosine_sim_matrix)

            # --- EXIBIÇÃO DOS RESULTADOS ---
            st.header("Resultados da Análise Preditiva")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(label="**Probabilidade de Êxito (P(G))**",
                          value=f"{probability:.1%}")

            with col2:
                st.metric(label="**Nível de Risco da Causa**",
                          value=risk_level)
            
            # Alerta visual de risco
            st.markdown(f"**Análise de Risco:** A probabilidade de um resultado 'Procedente' para uma tese similar neste juízo é estimada em **{probability:.1%}**, classificando a causa como de **{risk_level}**.")

            st.markdown("---")

            st.header("Análise de Consistência Jurisprudencial")
            st.markdown("As 5 decisões mais similares encontradas em nosso banco de dados para a tese apresentada são:")
            
            # Calcular a taxa de sucesso das 5 mais similares
            success_rate_similar = similar_cases['resultado'].value_counts(normalize=True).get('Procedente', 0)
            
            st.info(f"**Taxa de Sucesso Histórica (Top 5):** Das 5 decisões mais relevantes, **{success_rate_similar:.0%}** foram julgadas como 'Procedentes'.")
            
            for index, row in similar_cases.iterrows():
                with st.expander(f"**Caso {index}** | Juízo: {row['juizo']} | **Resultado: {row['resultado']}**"):
                    st.markdown(f"**Tese Registrada:** *{row['tese_juridica']}*")
                    st.markdown("**Fundamento da Decisão (Snippet):**")
                    st.write(f"_{row['texto_decisao']}_")
    else:
        st.sidebar.warning("Por favor, preencha a tese jurídica e selecione um juízo.")

else:
    st.info("Preencha os dados do caso na barra lateral e clique em 'Analisar' para ver os resultados.")

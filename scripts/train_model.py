import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
import os

print("Iniciando o processo de treinamento do modelo...")

# Caminho para o arquivo de dados
DATA_PATH = os.path.join('..', 'data', 'jurisprudencia.csv')

# Carregar o dataset
try:
    df = pd.read_csv(DATA_PATH)
    print("Dataset carregado com sucesso.")
    print(f"Número de registros: {len(df)}")
except FileNotFoundError:
    print(f"Erro: Arquivo de dados não encontrado em '{DATA_PATH}'.")
    print("Certifique-se de que o arquivo 'jurisprudencia.csv' está na pasta 'data'.")
    exit()

# 1. PREPARAÇÃO DOS DADOS

# Combinar as características de texto para o modelo de predição
df['features'] = df['tese_juridica'] + " " + df['juizo']

# Codificar a variável alvo ('Procedente' -> 1, 'Improcedente' -> 0)
le = LabelEncoder()
df['resultado_encoded'] = le.fit_transform(df['resultado'])
print("Variável alvo 'resultado' codificada.")
print(le.classes_) # Mostra as classes ['Improcedente' 'Procedente']

# 2. TREINAMENTO DO MODELO DE PREDIÇÃO DE RISCO

# Definir as variáveis X e y
X = df['features']
y = df['resultado_encoded']

# Criar um pipeline com TF-IDF e Regressão Logística
# TF-IDF converte texto em vetores numéricos
# Regressão Logística é um modelo de classificação simples e eficaz
model_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words=['de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um'])),
    ('clf', LogisticRegression(random_state=42))
])

# Treinar o modelo
model_pipeline.fit(X, y)
print("Modelo de predição de risco treinado com sucesso.")

# 3. CRIAÇÃO DO SISTEMA DE ANÁLISE DE CONSISTÊNCIA JURISPRUDENCIAL

# Usaremos um vetorizador separado para a similaridade de teses, focado apenas no texto da tese
tfidf_vectorizer_similarity = TfidfVectorizer(stop_words=['de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um'])
tfidf_matrix_similarity = tfidf_vectorizer_similarity.fit_transform(df['tese_juridica'])

# Calcular a matriz de similaridade de cossenos
# Isso cria uma matriz onde cada tese é comparada com todas as outras
cosine_sim_matrix = cosine_similarity(tfidf_matrix_similarity, tfidf_matrix_similarity)
print("Matriz de similaridade de cossenos calculada.")

# 4. SALVAR OS ARTEFATOS

# Criar o diretório para salvar os modelos se não existir
output_dir = os.path.join('..', 'models')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Salvar o pipeline do modelo de predição
joblib.dump(model_pipeline, os.path.join(output_dir, 'risk_prediction_model.joblib'))
print("Modelo de predição salvo em 'models/risk_prediction_model.joblib'")

# Salvar o vetorizador para a análise de similaridade
joblib.dump(tfidf_vectorizer_similarity, os.path.join(output_dir, 'similarity_vectorizer.joblib'))
print("Vetorizador de similaridade salvo em 'models/similarity_vectorizer.joblib'")

# Salvar a matriz de similaridade
joblib.dump(cosine_sim_matrix, os.path.join(output_dir, 'cosine_similarity_matrix.joblib'))
print("Matriz de similaridade salva em 'models/cosine_similarity_matrix.joblib'")

# Salvar o dataframe e o encoder para uso no app
joblib.dump(df, os.path.join(output_dir, 'jurisprudencia_df.joblib'))
joblib.dump(le, os.path.join(output_dir, 'label_encoder.joblib'))
print("DataFrame e LabelEncoder salvos.")

print("\nProcesso de treinamento concluído com sucesso!")

# OBJETIVO
"""
Quais gêneros de filme dão o maior Retorno sobre Investimento (ROI)
e quais fatores (duração, ano, orçamento) estão mais correlacionados
com a nota do público?"""

# ROI = (revenue - budget) / budget 
# %% [1. Carregamento]
import ast
from pathlib import Path

import pandas as pd
import plotly.express as px

DATA_PATH = Path('/home/cavalcantz/projects/tmdb_movies/data/tmdb_5000_movies.csv')

movies_raw_df = pd.read_csv(DATA_PATH, sep=',')
print(movies_raw_df.shape)
movies_raw_df.head()

# %% [2. Limpeza]
# Sempre parte de `df_raw`, nunca de si mesma — assim é reproduzível
# independente de quantas vezes essa célula for rodada.
movies_clean_df = (
    movies_raw_df
    .drop(columns=['homepage', 'overview', 'tagline'])
    .dropna(subset=['release_date', 'budget', 'revenue'])
    .copy()
)

# orçamento e receita zerados/negativos inviabilizam o cálculo de ROI
# (divisão por zero ou números sem sentido de negócio) -> removidos
n_antes = len(movies_clean_df)
movies_clean_df = movies_clean_df.query('budget > 0 and revenue > 0')
print(f'Removidas {n_antes - len(movies_clean_df)} linhas com budget/revenue <= 0')

movies_clean_df['release_date'] = pd.to_datetime(movies_clean_df['release_date'], errors='coerce')
movies_clean_df['release_year'] = movies_clean_df['release_date'].dt.year

movies_clean_df.info()
movies_clean_df.head()

# %% [3. Feature engineering]
# Cria as colunas derivadas: lucro, ROI e gênero principal.

movies_feat_df = movies_clean_df.copy()

movies_feat_df['profit'] = movies_feat_df['revenue'] - movies_feat_df['budget']
movies_feat_df['roi'] = (movies_feat_df['revenue'] - movies_feat_df['budget']) / movies_feat_df['budget']


def main_primary_extract(genres_str: str) -> str:
    """Extrai o nome do primeiro gênero da coluna 'genres' (string de lista de dicts)."""
    if pd.isna(genres_str):
        return 'Other'
    try:
        generos = ast.literal_eval(genres_str)
    except (ValueError, SyntaxError):
        return 'Other'
    if not generos:
        return 'Other'
    return generos[0]['name']


movies_feat_df['main_genre'] = movies_feat_df['genres'].apply(main_primary_extract)

print(movies_feat_df['main_genre'].value_counts())
movies_feat_df[['title', 'budget', 'revenue', 'roi', 'main_genre', 'release_year', 'runtime', 'vote_average']].head(10)

# %% [markdown]
# ## 4. Análise / agrupamentos

# ### 4.1 ROI médio por gênero

roi_by_genre = (
    movies_feat_df
    .groupby('main_genre')['roi']
    .agg(avg_roi='mean', median_roi='median', movies_qnt='count')
    .sort_values('avg_roi', ascending=False)
)

roi_by_genre

# > Nota: avg_roi é bastante sensível a outliers (um único filme de
# > baixíssimo orçamento e alta bilheteria pode inflar a média do gênero).
# > median_roi costuma ser uma leitura mais confiável do "gênero típico".

# %% ### 4.2 Correlação com a nota do público (vote_average)
numerics_columns = ['runtime', 'release_year', 'budget', 'revenue', 'roi', 'vote_average']

score_correlation = (
    movies_feat_df[numerics_columns]
    .corr(numeric_only=True)['vote_average']
    .drop('vote_average')
    .sort_values(key=abs, ascending=False)
)
score_correlation

# %% [markdown]
# ## 5. Gráficos
plot_df = (
    roi_by_genre
    .sort_values("median_roi")
    .reset_index()
)

fig = px.bar(
    plot_df,
    x="median_roi",
    y="main_genre",
    orientation="h",
    text="median_roi",
    color="median_roi",
    color_continuous_scale="Blues"
)

fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")

fig.update_layout(
    title="ROI Mediano por Gênero",
    xaxis_title="ROI Mediano",
    yaxis_title="Gênero",
    template="simple_white",
    showlegend=False
)

fig.show()

# %% [6. Scratch]
# Zona livre pra testar coisas pontuais
vote_by_genre = (
    movies_feat_df
    .groupby('main_genre')['vote_average']
    .agg(avg_vote='mean', median_vote='median', desvio='std', movies_qnt='count')
    .sort_values('avg_vote')
)

vote_by_genre

plot_vote_df = (
    vote_by_genre
    .sort_values("avg_vote")
    .reset_index()
)

fig = px.bar(
    plot_vote_df,
    x="avg_vote",
    y="main_genre",
    orientation="h",
    text="avg_vote",
    color="avg_vote",
    color_continuous_scale="Blues"
)

fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")

fig.update_layout(
    title=" Média de votos por Gênero",
    xaxis_title="Média de votos",
    yaxis_title="Gênero",
    template="simple_white",
    showlegend=False
)

roi_by_genre.to_csv("/home/cavalcantz/projects/tmdb_movies/outputs/roi_por_genero.csv")

# %%

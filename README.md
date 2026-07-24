# 🎬 Análise de ROI e Avaliação de Filmes (TMDB 5000)

## Objetivo
Quais gêneros de filme dão o maior Retorno sobre Investimento (ROI) e quais
fatores (duração, ano, orçamento) estão mais correlacionados com a nota do
público?

## Fonte dos dados
[TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) (Kaggle).

> Baixe o arquivo `tmdb_5000_movies.csv` e coloque em `data/` antes de rodar
> o projeto (a pasta `data/` não é versionada neste repositório).

## Estrutura do projeto
```
tmdb_movies/
├── data/           # dataset bruto (não versionado)
├── notebooks/      # versão final da análise, com storytelling
├── outputs/        # gráficos e tabelas exportados
├── scripts/        # analysis.py com o pipeline de análise
├── requirements.txt
└── README.md
```

## Como rodar
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scripts/analysis.py
```

## Metodologia
1. **Limpeza**: remoção de linhas sem data, orçamento ou receita, e de
   registros com budget/revenue ≤ 0 (inviabilizam o cálculo de ROI).
2. **Feature engineering**: cálculo de `profit`, `roi` e extração do
   gênero principal de cada filme.
3. **Análise**: ROI médio/mediano por gênero e correlação entre variáveis
   numéricas e a nota do público (`vote_average`).
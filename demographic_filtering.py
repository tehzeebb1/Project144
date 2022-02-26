import pandas as pd
import numpy as np

df = pd.read_csv('final.csv',encoding="utf-8")

C = df['vote_average'].mean()
m = df['vote_count'].quantile(0.9)
q_articles = df.copy().loc[df['vote_count'] >= m]

def weighted_rating(x, m=m, C=C):
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+m) * R) + (m/(m+v) * C)

q_articles['score'] = q_articles.apply(weighted_rating, axis=1)

q_articles = q_articles.sort_values('score', ascending=False)

output = q_articles[['title', 'poster_link', 'release_date', 'runtime', 'vote_average', 'overview']].head(20).values.tolist()


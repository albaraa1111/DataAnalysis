import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1 — Load data
df = pd.read_csv("medical_examination.csv")

# 2 — Add overweight (BMI > 25 ⇒ 1 else 0)
bmi = df['weight'] / ((df['height'] / 100) ** 2)
df['overweight'] = (bmi > 25).astype(int)

# 3 — Normalize cholesterol and gluc (1 if >1, else 0)
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc']        = (df['gluc'] > 1).astype(int)

# 4
def draw_cat_plot():
    # 5 — Melt the categorical features keeping cardio as id
    df_cat = pd.melt(
        df,
        id_vars=['cardio'],
        value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']
    )

    # 6 — Group and count to get totals per (cardio, variable, value)
    df_cat = (
        df_cat
        .groupby(['cardio', 'variable', 'value'], as_index=False)
        .size()
        .rename(columns={'size': 'total'})
    )

    # 7 — Draw the categorical plot
    g = sns.catplot(
        data=df_cat,
        x='variable',
        y='total',
        hue='value',
        col='cardio',
        kind='bar',
        height=5,
        aspect=1
    )

    # 8 — Get the matplotlib Figure object
    fig = g.fig

    # 9 — Save and return
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11 — Clean the data
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # 12 — Compute correlation matrix
    corr = df_heat.corr(numeric_only=True)

    # 13 — Upper-triangle mask
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14 — Figure/axis
    fig, ax = plt.subplots(figsize=(12, 12))

    # 15 — Heatmap
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt='.1f',
        linewidths=.5,
        square=True,
        cbar_kws={'shrink': .5},
        center=0
    )

    # 16 — Save and return
    fig.savefig('heatmap.png')
    return fig

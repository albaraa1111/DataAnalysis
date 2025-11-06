import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# --- Import data (parse dates, set index) ---
df = pd.read_csv(
    "fcc-forum-pageviews.csv",
    parse_dates=["date"],
    index_col="date"
)

# --- Clean data (remove top/bottom 2.5% outliers) ---
df = df[
    (df["value"] >= df["value"].quantile(0.025)) &
    (df["value"] <= df["value"].quantile(0.975))
]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df["value"], color="red", linewidth=1)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["Year"] = df_bar.index.year
    df_bar["Month"] = df_bar.index.month_name()

    # Group by Year/Month and pivot months to columns
    monthly_mean = (
        df_bar.groupby(["Year", "Month"])["value"]
              .mean()
              .reset_index()
    )

    # Ensure month order Jan..Dec
    month_order = ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"]
    monthly_mean["Month"] = pd.Categorical(monthly_mean["Month"], categories=month_order, ordered=True)
    monthly_mean = monthly_mean.sort_values(["Year", "Month"])

    pivot = monthly_mean.pivot(index="Year", columns="Month", values="value")

    # Draw bar plot
    fig = pivot.plot(kind="bar", figsize=(15, 8)).get_figure()
    ax = plt.gca()
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title="Months")

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(18, 6))

    # Year-wise box plot
    sns.boxplot(data=df_box, x="year", y="value", ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise box plot (ensure correct month order)
    month_abbrev_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    df_box["month"] = pd.Categorical(df_box["month"], categories=month_abbrev_order, ordered=True)
    sns.boxplot(data=df_box, x="month", y="value", ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

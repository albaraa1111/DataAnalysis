import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # Read data from file
    df = pd.read_csv("epa-sea-level.csv")

    # Create scatter plot
    plt.figure(figsize=(12, 6))
    plt.scatter(df["Year"], df["CSIRO Adjusted Sea Level"])

    # Create first line of best fit (use all data → extend to 2050)
    res_all = linregress(df["Year"], df["CSIRO Adjusted Sea Level"])
    x_all = pd.Series(range(1880, 2051))
    y_all = res_all.intercept + res_all.slope * x_all
    plt.plot(x_all, y_all, label="Best fit (all data)")

    # Create second line of best fit (use data from year 2000 → extend to 2050)
    df_2000 = df[df["Year"] >= 2000]
    res_2000 = linregress(df_2000["Year"], df_2000["CSIRO Adjusted Sea Level"])
    x_2000 = pd.Series(range(2000, 2051))
    y_2000 = res_2000.intercept + res_2000.slope * x_2000
    plt.plot(x_2000, y_2000, label="Best fit (2000+)")

    # Add labels and title
    plt.title("Rise in Sea Level")
    plt.xlabel("Year")
    plt.ylabel("Sea Level (inches)")
    plt.legend()

    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()

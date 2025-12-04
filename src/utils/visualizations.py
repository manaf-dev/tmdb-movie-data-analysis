"""
Visualization utilities for movie data analysis.
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_revenue_vs_budget(df):
    """
    Create scatter plot of revenue vs budget with trend line.

    Args:
        df: Movie DataFrame with 'budget_musd' and 'revenue_musd' columns
    """
    plt.figure(figsize=(10, 6))

    # Get data without missing values
    plot_data = df[["budget_musd", "revenue_musd"]].dropna()

    # Scatter plot
    plt.scatter(
        plot_data["budget_musd"],
        plot_data["revenue_musd"],
        alpha=0.6,
        s=100,
        edgecolors="black",
        linewidth=0.5,
    )

    plt.xlabel("Budget (Million USD)", fontsize=12)
    plt.ylabel("Revenue (Million USD)", fontsize=12)
    plt.title("Revenue vs Budget Trends", fontsize=14, fontweight="bold")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_roi_by_genre(df):
    """
    Create bar chart of average ROI by genre.

    Args:
        df: Movie DataFrame with 'genres' and 'roi' columns
    """
    plt.figure(figsize=(10, 6))

    # Explode genres and calculate mean roi
    genre_df = df.assign(Genre=df["genres"].str.split("|")).explode("Genre")
    genre_roi = genre_df.groupby("Genre")["roi"].mean().sort_values(ascending=False)

    # Create bar chart
    plt.bar(genre_roi.index, genre_roi.values, edgecolor="black")

    plt.xlabel("Genre", fontsize=12)
    plt.ylabel("Average ROI", fontsize=12)
    plt.title("ROI Distribution by Genre", fontsize=14, fontweight="bold")
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_franchise_comparison(df):
    """
    Create multi-panel comparison of franchise vs standalone performance.

    Args:
        df: Movie DataFrame with franchise indicators
    """
    # get franchise and standalone movies
    franchise = df[df["belongs_to_collection"].notna()]
    standalone = df[df["belongs_to_collection"].isna()]

    # calculate metrics
    metrics = {
        "Revenue": [
            franchise["revenue_musd"].mean(),
            standalone["revenue_musd"].mean(),
        ],
        "ROI": [franchise["roi"].mean(), standalone["roi"].mean()],
        "Budget": [franchise["budget_musd"].mean(), standalone["budget_musd"].mean()],
        "Rating": [franchise["vote_average"].mean(), standalone["vote_average"].mean()],
    }

    # Create subplots
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(
        "Franchise vs Standalone Movie Performance", fontsize=14, fontweight="bold"
    )

    categories = ["Franchise", "Standalone"]
    colors = ["#2E86AB", "#A23B72"]

    # Revenue comparison
    axs[0, 0].bar(categories, metrics["Revenue"], color=colors, edgecolor="black")
    axs[0, 0].set_title("Average Revenue (M USD)")
    axs[0, 0].set_ylabel("Million USD")
    axs[0, 0].grid(True, axis="y", alpha=0.3)

    # ROI comparison
    axs[0, 1].bar(categories, metrics["ROI"], color=colors, edgecolor="black")
    axs[0, 1].set_title("Average ROI")
    axs[0, 1].set_ylabel("ROI Multiplier")
    axs[0, 1].grid(True, axis="y", alpha=0.3)

    # Budget comparison
    axs[1, 0].bar(categories, metrics["Budget"], color=colors, edgecolor="black")
    axs[1, 0].set_title("Average Budget (M USD)")
    axs[1, 0].set_ylabel("Million USD")
    axs[1, 0].grid(True, axis="y", alpha=0.3)

    # Rating comparison
    axs[1, 1].bar(categories, metrics["Rating"], color=colors, edgecolor="black")
    axs[1, 1].set_title("Average Rating")
    axs[1, 1].set_ylabel("Rating (out of 10)")
    axs[1, 1].set_ylim(0, 10)
    axs[1, 1].grid(True, axis="y", alpha=0.3)

    plt.tight_layout()
    plt.show()


def plot_popularity_vs_rating(df):
    """
    Create scatter plot of popularity vs rating.

    Args:
        df: Movie DataFrame
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(
        df["vote_average"], df["popularity"], alpha=0.6, s=100, edgecolors="black", linewidth=0.5
    )

    plt.xlabel("Rating", fontsize=12)
    plt.ylabel("Popularity", fontsize=12)
    plt.title("Popularity vs. Rating", fontsize=14, fontweight="bold")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_yearly_trends(df):
    """
    Plot yearly trends in box office performance.

    Args:
        df: Movie DataFrame
    """
    # Extract year from release date
    df_copy = df.copy()
    df_copy["release_year"] = df_copy["release_date"].dt.year

    # Group by year and calculate metrics
    yearly_stats = df_copy.groupby("release_year").agg(
        {"revenue_musd": ["count", "mean"], "budget_musd": "mean", "roi": "mean"}
    )

    yearly_stats.columns = ["Movie Count", "Mean Revenue", "Mean Budget", "Mean ROI"]

    # Create subplots
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Yearly Box Office Performance Trends", fontsize=16, fontweight="bold")

    # Movie Count per Year
    axs[0, 0].plot(yearly_stats.index, yearly_stats["Movie Count"], marker="o")
    axs[0, 0].set_title("Number of Movies Released per Year")
    axs[0, 0].set_ylabel("Count")

    # Average Revenue per Year
    axs[0, 1].plot(
        yearly_stats.index, yearly_stats["Mean Revenue"], marker="o", color="green"
    )
    axs[0, 1].set_title("Average Revenue per Year (M USD)")
    axs[0, 1].set_ylabel("Revenue (M USD)")

    # Average Budget per Year
    axs[1, 0].plot(
        yearly_stats.index, yearly_stats["Mean Budget"], marker="o", color="orange"
    )
    axs[1, 0].set_title("Average Budget per Year (M USD)")
    axs[1, 0].set_ylabel("Budget (M USD)")

    # Average ROI per Year
    axs[1, 1].plot(
        yearly_stats.index, yearly_stats["Mean ROI"], marker="o", color="purple"
    )
    axs[1, 1].set_title("Average ROI per Year")
    axs[1, 1].set_ylabel("ROI")

    for ax in axs.flat:
        ax.set_xlabel("Year")
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

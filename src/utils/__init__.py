"""
Utility modules for TMDB Movie Data Analysis.
"""

from .analysis import analyze_franchise_vs_standalone, rank_movies
from .data_cleaner import clean_movie_data
from .data_fetcher import fetch_movies_from_api
from .visualizations import (
    plot_franchise_comparison,
    plot_revenue_vs_budget,
    plot_roi_by_genre,
)

__all__ = [
    "fetch_movies_from_api",
    "clean_movie_data",
    "rank_movies",
    "analyze_franchise_vs_standalone",
    "plot_revenue_vs_budget",
    "plot_roi_by_genre",
    "plot_franchise_comparison",
]

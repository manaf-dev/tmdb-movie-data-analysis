"""
Data fetching utilities for TMDB API.
"""

import logging
import os

import pandas as pd
import requests
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Setup logging
logger = logging.getLogger(__name__)


def fetch_movies_from_api(movie_ids):
    """
    Fetch movies from TMDB API.

    Args:
        movie_ids: List of TMDB movie IDs

    Returns:
        pandas DataFrame with raw movie data
    """
    base_url = "https://api.themoviedb.org/3/movie/"
    access_token = os.getenv("TMDB_API_KEY")
    headers = {"accept": "application/json", "Authorization": f"Bearer {access_token}"}

    movies = []
    logger.info("Fetching movies from TMDB API")

    for movie_id in movie_ids:
        url = f"{base_url}{movie_id}?append_to_response=credits"
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                movies.append(response.json())
            else:
                logger.error(
                    f"Failed to fetch movie ID {movie_id}: {response.status_code}"
                )
        except Exception as e:
            logger.error(f"Error fetching movie {movie_id}: {e}")

    logger.info(f"Successfully fetched {len(movies)} movies")

    return pd.DataFrame(movies)

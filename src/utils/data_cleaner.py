"""
Data cleaning and preprocessing utilities.
"""

import logging

import pandas as pd

logger = logging.getLogger(__name__)


def clean_movie_data(df):
    """
    Clean and preprocess movie data.

    Args:
        df: Raw movie DataFrame

    Returns:
        Cleaned DataFrame with derived metrics
    """
    logger.info("Starting data cleaning...")
    movies_df = df.copy()

    # Drop irrelevant columns
    columns_to_drop = [
        "adult",
        "imdb_id",
        "original_title",
        "video",
        "homepage",
        "backdrop_path",
    ]
    movies_df.drop(columns=columns_to_drop, inplace=True, errors="ignore")

    # Extract collection name
    movies_df["belongs_to_collection"] = movies_df["belongs_to_collection"].apply(
        lambda x: x["name"] if isinstance(x, dict) and "name" in x else None
    )

    # Extract genres
    movies_df["genres"] = movies_df["genres"].apply(
        lambda x: "|".join([g["name"] for g in x]) if isinstance(x, list) else ""
    )

    # Extract other list fields
    movies_df["spoken_languages"] = movies_df["spoken_languages"].apply(
        lambda x: (
            "|".join([lang["english_name"] for lang in x])
            if isinstance(x, list)
            else ""
        )
    )
    movies_df["production_countries"] = movies_df["production_countries"].apply(
        lambda x: "|".join([c["name"] for c in x]) if isinstance(x, list) else ""
    )
    movies_df["production_companies"] = movies_df["production_companies"].apply(
        lambda x: "|".join([c["name"] for c in x]) if isinstance(x, list) else ""
    )

    # Extract cast and crew
    movies_df["cast"] = movies_df["credits"].apply(
        lambda x: (
            "|".join([m["name"] for m in x["cast"]]) if isinstance(x, dict) else ""
        )
    )
    movies_df["cast_size"] = movies_df["credits"].apply(
        lambda x: len(x["cast"]) if isinstance(x, dict) else 0
    )
    movies_df["directors"] = movies_df["credits"].apply(
        lambda x: (
            "|".join([m["name"] for m in x["crew"] if m["job"] == "Director"])
            if isinstance(x, dict)
            else ""
        )
    )
    movies_df["crew_size"] = movies_df["credits"].apply(
        lambda x: len(x["crew"]) if isinstance(x, dict) else 0
    )
    movies_df.drop(columns=["credits"], inplace=True, errors="ignore")

    # Convert data types
    movies_df["budget"] = pd.to_numeric(movies_df["budget"], errors="coerce")
    movies_df["revenue"] = pd.to_numeric(movies_df["revenue"], errors="coerce")
    movies_df["runtime"] = pd.to_numeric(movies_df["runtime"], errors="coerce")
    movies_df["release_date"] = pd.to_datetime(
        movies_df["release_date"], errors="coerce"
    )

    # Handle unrealistic values
    movies_df.loc[movies_df["budget"] <= 0, "budget"] = pd.NA
    movies_df.loc[movies_df["revenue"] <= 0, "revenue"] = pd.NA
    movies_df.loc[movies_df["runtime"] <= 0, "runtime"] = pd.NA

    # Convert to millions USD
    movies_df["budget_musd"] = movies_df["budget"] / 1_000_000
    movies_df["revenue_musd"] = movies_df["revenue"] / 1_000_000
    movies_df.drop(columns=["budget", "revenue"], inplace=True)

    # Clean ratings
    movies_df.loc[movies_df["vote_count"] == 0, "vote_average"] = pd.NA

    # Remove duplicates and invalid rows
    movies_df.drop_duplicates(subset=["id"], keep="first", inplace=True)
    movies_df.dropna(subset=["id", "title"], inplace=True)
    movies_df = movies_df[movies_df.notna().sum(axis=1) >= 10]

    # Filter released movies only
    if "status" in movies_df.columns:
        movies_df = movies_df[movies_df["status"] == "Released"]
        movies_df.drop(columns=["status"], inplace=True)

    # Add calculated metrics
    movies_df["profit"] = movies_df["revenue_musd"] - movies_df["budget_musd"]
    movies_df["roi"] = movies_df["revenue_musd"] / movies_df["budget_musd"]

    # Reorder columns
    column_order = [
        "id",
        "title",
        "tagline",
        "release_date",
        "genres",
        "belongs_to_collection",
        "original_language",
        "budget_musd",
        "revenue_musd",
        "profit",
        "roi",
        "production_companies",
        "production_countries",
        "vote_count",
        "vote_average",
        "popularity",
        "runtime",
        "overview",
        "spoken_languages",
        "poster_path",
        "cast",
        "cast_size",
        "directors",
        "crew_size",
    ]
    available_cols = [c for c in column_order if c in movies_df.columns]
    movies_df = movies_df[available_cols]
    movies_df.reset_index(drop=True, inplace=True)

    # Save cleaned data
    try:
        movies_df.to_csv("notebooks/cleaned_movies_data.csv", index=False)
        logger.info("Saved cleaned data to notebooks/cleaned_movies_data.csv")
    except Exception as e:
        logger.warning(f"Could not save cleaned data: {e}")

    logger.info(
        f"Cleaned data: {len(movies_df)} movies, {len(movies_df.columns)} columns"
    )

    return movies_df

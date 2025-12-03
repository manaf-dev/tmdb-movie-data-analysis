import logging

import pandas as pd

logger = logging.getLogger(__name__)


def join_names(names, key):
    """Helper function to join names from a list of dicts."""
    return "|".join([name[key] for name in names]) if isinstance(names, list) else ""

def extract_cast(credits):
    """Helper function to extract cast names from credits dictionary."""
    return "|".join([m["name"] for m in credits.get("cast", [])]) if isinstance(credits, dict) else ""

def extract_directors(credits):
    """Helper function to extract director names from credits dictionary."""
    return "|".join([m["name"] for m in credits.get("crew", []) if m.get("job") == "Director"]) if isinstance(credits, dict) else ""

def count_items(credits, key):
    """Helper function to count items in a list within credits dictionary."""
    return len(credits.get(key, [])) if isinstance(credits, dict) else 0        


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

    # STEP 1: Drop irrelevant columns
    columns_to_drop = [
        "adult",
        "imdb_id",
        "original_title",
        "video",
        "homepage",
        "backdrop_path",
    ]
    movies_df.drop(columns=columns_to_drop, inplace=True, errors="ignore")

    # STEP 2: Extract nested data
    # Extract collection name
    movies_df["belongs_to_collection"] = movies_df["belongs_to_collection"].apply(
        lambda x: x["name"] if isinstance(x, dict) and "name" in x else None
    )

    # Extract genres
    movies_df["genres"] = movies_df["genres"].apply(
        lambda x: join_names(x, "name")
    )

    # Extract spoken languages
    movies_df["spoken_languages"] = movies_df["spoken_languages"].apply(
        lambda x: join_names(x, "english_name")
    )

    # Extract production countrie
    movies_df["production_countries"] = movies_df["production_countries"].apply(
        lambda x: join_names(x, "name")
    )

    # Extract production companies
    movies_df["production_companies"] = movies_df["production_companies"].apply(
        lambda x: join_names(x, "name")
    )

    # Extract cast and crew
    movies_df["cast"] = movies_df["credits"].apply(
        lambda x: extract_cast(x)
    )
    movies_df["cast_size"] = movies_df["credits"].apply(
        lambda x: count_items(x, "cast")
    )
    movies_df["directors"] = movies_df["credits"].apply(
        lambda x: extract_directors(x)
    )
    movies_df["crew_size"] = movies_df["credits"].apply(
        lambda x: count_items(x, "crew")
    )

    # Remove credits column after extractions
    movies_df.drop(columns=["credits"], inplace=True, errors="ignore")

    # STEP 3: Inspect extracted columns using value_counts() to identify anomalies.
    for col in ["belongs_to_collection", "genres", "spoken_languages", "production_countries", "production_companies", "cast", "directors"]:
        if col in movies_df.columns:
            logger.info(f"Value counts for {col}:\n{movies_df[col].value_counts(dropna=False).head(10)}\n")

    # STEP 4: Convert data types
    # Convert budget, revenue, runtime to numeric 
    for col in ["budget", "revenue", "runtime"]:
        movies_df[col] = pd.to_numeric(movies_df[col], errors="coerce")

    # Convert release_date to datetime
    movies_df["release_date"] = pd.to_datetime(
        movies_df["release_date"], errors="coerce"
    )

    # STEP 5: Replace unrealistic values
    # Set budget, revenue, runtime <= 0 to NaN
    for col in ["budget", "revenue", "runtime"]:
        movies_df.loc[movies_df[col] <= 0, col] = pd.NA

    # Convert budget and revenue to millions USD
    for col in ["budget", "revenue"]:
        movies_df[f"{col}_musd"] = movies_df[col] / 1_000_000
    
    # Drop original budget and revenue columns
    movies_df.drop(columns=["budget", "revenue"], inplace=True)

    # Set vote_average to NaN where vote_count is 0
    movies_df.loc[movies_df["vote_count"] == 0, "vote_average"] = pd.NA

    # STEP 6: Remove duplicates and invalid rows
    movies_df.drop_duplicates(subset=["id"], keep="first", inplace=True)
    movies_df.dropna(subset=["id", "title"], inplace=True)

    # Keep rows with at least 10 non-NA values
    movies_df = movies_df[movies_df.notna().sum(axis=1) >= 10]

    # STEP 7: Filter released movies only and drop status column
    if "status" in movies_df.columns:
        movies_df = movies_df[movies_df["status"] == "Released"]
        movies_df.drop(columns=["status"], inplace=True)

    # STEP 8: Add calculated metrics for profit and roi
    movies_df["profit"] = movies_df["revenue_musd"] - movies_df["budget_musd"]
    movies_df["roi"] = movies_df["revenue_musd"] / movies_df["budget_musd"]

    # STEP 9: Reorder columns
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
    movies_df = movies_df[available_cols].reset_index(drop=True, inplace=True)

    logger.info(
        f"Cleaned data: {len(movies_df)} movies, {len(movies_df.columns)} columns"
    )

    return movies_df

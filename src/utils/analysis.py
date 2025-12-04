import pandas as pd


def rank_movies(df, metric, top_n=5, ascending=False, min_budget=None, min_votes=None):
    """
    Rank movies by a metric with optional filters.

    Args:
        df: Movie DataFrame
        metric: Column to rank by (e.g., 'revenue_musd', 'roi', 'profit')
        top_n: Number of results to return
        ascending: Sort direction (False = highest first)
        min_budget: Minimum budget filter in millions USD
        min_votes: Minimum vote count filter

    Returns:
        Filtered and sorted DataFrame
    """
    data = df.copy()

    # Filter based on budget and votes
    if min_budget:
        data = data[data["budget_musd"] >= min_budget]
    if min_votes:
        data = data[data["vote_count"] >= min_votes]

    # Sort and return top N
    return data.sort_values(by=metric, ascending=ascending).head(top_n)


def analyze_franchise_vs_standalone(df):
    """
    Compare franchise vs standalone movie performance.

    Args:
        df: Movie DataFrame

    Returns:
        Comparison DataFrame with key metrics
    """
    # get franchise and standalone movies
    franchise = df[df["belongs_to_collection"].notna()]
    standalone = df[df["belongs_to_collection"].isna()]

    # calculate comparison metrics
    comparison = pd.DataFrame(
        {
            "Metric": [
                "Mean Revenue (M USD)",
                "Mean ROI",
                "Mean Budget (M USD)",
                "Mean Popularity",
                "Mean Rating",
                "Movie Count",
            ],
            "Franchise": [
                franchise["revenue_musd"].mean(),
                franchise["roi"].mean(),
                franchise["budget_musd"].mean(),
                franchise["popularity"].mean(),
                franchise["vote_average"].mean(),
                len(franchise),
            ],
            "Standalone": [
                standalone["revenue_musd"].mean(),
                standalone["roi"].mean(),
                standalone["budget_musd"].mean(),
                standalone["popularity"].mean(),
                standalone["vote_average"].mean(),
                len(standalone),
            ],
        }
    )

    return comparison.round(2)


def get_successful_franchises(df):
    """
    Analyze franchise performance.

    Args:
        df: Movie DataFrame

    Returns:
        DataFrame with franchise statistics
    """
    franchise_movies = df[df["belongs_to_collection"].notna()]
    grouped = franchise_movies.groupby("belongs_to_collection")

    performance = grouped.agg(
        {
            "id": "count",
            "budget_musd": ["sum", "mean"],
            "revenue_musd": ["sum", "mean"],
            "vote_average": "mean",
        }
    ).round(2)

    performance.columns = [
        "Total Movies",
        "Total Budget",
        "Mean Budget",
        "Total Revenue",
        "Mean Revenue",
        "Mean Rating",
    ]

    return performance.sort_values(by=["Total Movies", "Total Revenue"], ascending=False)


def get_successful_directors(df):
    """
    Analyze director performance.

    Args:
        df: Movie DataFrame

    Returns:
        DataFrame with director statistics
    """
    # Explode directors column as a movie can have multiple directors
    # directors are pipe-separated strings
    directors_df = df[["id", "directors", "revenue_musd", "vote_average"]].copy()
    directors_df["director"] = directors_df["directors"].str.split("|")
    directors_df = directors_df.explode("director")

    # group by director name
    performance = (
        directors_df.groupby("director")
        .agg(
            {
                "id": "count",
                "revenue_musd": "sum",
                "vote_average": "mean",
            }
        )
        .round(2)
    )

    performance.columns = [
        "Total Movies",
        "Total Revenue",
        "Mean Rating",
    ]

    return performance.sort_values(by=["Total Movies", "Total Revenue"], ascending=False)


def search_movies(df, cast_member=None, director=None, genres=None, sort_by=None, ascending=False):
    """
    Search movies based on cast, director, and genres.

    Args:
        df: Movie DataFrame
        cast_member: Name of cast member to search for
        director: Name of director to search for
        genres: List of genres to include (all must be present)
        sort_by: Column to sort by
        ascending: Sort order

    Returns:
        Filtered and sorted DataFrame
    """
    data = df.copy()

    if cast_member:
        data = data[data["cast"].str.contains(cast_member, na=False, case=False)]
    
    if director:
        data = data[data["directors"].str.contains(director, na=False, case=False)]
        
    if genres:
        for genre in genres:
            data = data[data["genres"].str.contains(genre, na=False, case=False)]
            
    if sort_by:
        data = data.sort_values(by=sort_by, ascending=ascending)
        
    return data

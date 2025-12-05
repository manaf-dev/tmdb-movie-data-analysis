import pandas as pd

from src.utils.analysis import rank_movies


def test_rank_movies():
    df = pd.DataFrame({"title": ["A", "B", "C"], "revenue": [10, 50, 20]})

    ranked = rank_movies(df, "revenue", ascending=False, top_n=1)

    assert ranked.iloc[0]["title"] == "B"
    assert len(ranked) == 1

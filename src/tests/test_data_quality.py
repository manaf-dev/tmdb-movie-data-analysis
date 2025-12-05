import pandas as pd

from ..utils.data_quality import check_duplicates, check_outliers


def test_check_duplicates_with_duplicates():

    data = {"id": [1, 2, 2, 3], "name": ["Movie A", "Movie B", "Movie B", "Movie C"]}
    df = pd.DataFrame(data)

    duplicates = check_duplicates(df)
    assert duplicates == [2]


def test_check_duplicates_no_duplicates():

    data = {"id": [1, 2, 3], "name": ["Movie A", "Movie B", "Movie C"]}
    df = pd.DataFrame(data)

    duplicates = check_duplicates(df)
    assert duplicates == []


def test_check_outliers():

    data = {
        "id": [1, 2, 3, 4, 5, 6],
        "revenue": [1230.257, 1010.123, 1200.234, 1100.345, 55500, 4],
    }
    df = pd.DataFrame(data)

    outliers = check_outliers(df, "revenue")
    assert len(outliers) == 2
    assert outliers.iloc[0]["id"] == 5
    assert outliers.iloc[1]["id"] == 6


def test_check_outliers_no_outliers():

    data = {
        "id": [1, 2, 3, 4, 5],
        "budget": [1000, 1100, 1200, 1300, 1400],
    }
    df = pd.DataFrame(data)

    outliers = check_outliers(df, "budget")
    assert len(outliers) == 0

from src.utils.data_cleaner import (
    count_items,
    extract_cast,
    extract_directors,
    join_names,
)


def test_extract_cast():
    data = {"cast": [{"name": "Keanu Reeves"}]}
    assert extract_cast(data) == "Keanu Reeves"


def test_count_items():
    data = {"cast": [{"name": "Keanu Reeves"}, {"name": "Laurence Fishburne"}]}
    assert count_items(data, "cast") == 2


def test_extract_directors():
    data = {"crew": [{"name": "Christopher Nolan", "job": "Director"}]}
    assert extract_directors(data) == "Christopher Nolan"


def test_join_names():
    data = [{"name": "Action"}, {"name": "Adventure"}]
    assert join_names(data, "name") == "Action|Adventure"

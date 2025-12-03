# tmdb-movie-data-analysis
Lab for building a movie data analysis pipeline using Python and Pandas.

## Data Dictionary
| Column                | Description                   | Type     | Notes                                  |
| --------------------- | ----------------------------- | -------- | -------------------------------------- |
| id                    | TMDB movie ID                 | int      | Unique identifier                      |
| title                 | Movie title                   | string   | Cleaned text                           |
| tagline               | Marketing tagline             | string   | May contain missing values             |
| release_date          | Official release date         | datetime | Converted from string                  |
| genres                | Pipe-separated list of genres | string   | Extracted from JSON                    |
| belongs_to_collection | Franchise name                | string   | None = standalone movie                |
| budget_musd           | Budget in millions            | float    | Cleaned and normalized                 |
| revenue_musd          | Revenue in millions           | float    | Zero → NaN                             |
| profit                | revenue - budget              | float    | Derived                                |
| roi                   | revenue / budget              | float    | Derived                                |
| production_companies  | Joined company names          | string   | Extracted                              |
| production_countries  | Country list                  | string   | Extracted                              |
| spoken_languages      | English names of languages    | string   | Extracted                              |
| cast                  | Cast list                     | string   | Extracted, exploded                    |
| directors             | Director names                | string   | Extracted                              |
| crew_size             | Number of crew members        | int      | Derived                                |
| cast_size             | Number of cast members        | int      | Derived                                |
| popularity            | TMDB popularity score         | float    | Provided by API                        |
| vote_average          | Average rating                | float    | Set to NaN if vote_count=0             |
| vote_count            | Number of votes               | int      | Useful for filtering low-signal movies |

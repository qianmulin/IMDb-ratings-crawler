# IMDb ratings crawler
It can crawl the top 10,000 items (including movies, TV series, games, etc.) of the number of IMDb ratings.

The crawled information includes id, title, date, rating, different rating ratios, and ratings based on gender and age, etc.

Run `IMDb_ratings_crawler.py` to start crawling, and the crawl data will be saved to `imbd_ratings.csv` in the current folder. Attached is the deduplicated data crawled on May 3, 2021 (incomplete).

The start and end page can be configured in `config.py`(50 items per page).

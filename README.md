# IMDb ratings crawler（IMDb评分爬虫）
可爬取IMDb评分数前10000的条目（包含电影，电视剧，游戏等）。

爬取的信息有id，标题，日期，评分，不同评分比例，按性别年龄划分评分等。

运行IMDb_ratings_crawler.py即可开始爬虫，爬取数据会保存到当前文件夹的imbd_ratings.csv中。

可在config.py中配置开始结束页，每页50个条目。

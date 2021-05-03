import re
import requests
import time
import csv
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

def generate_list_url(page):
    list_url = "https://www.imdb.com/search/title/?adult=include&sort=num_votes,desc&start="+str((page-1)*50+1)+"&ref_=adv_nxt"
    return  list_url

def generate_ratings_list_url(list_url):
    try:
        response = requests.get(list_url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html,'lxml')
            items = soup.select('.lister-item-content')
            ratings_url_list = [[0] * 2 for j in range(50)]
            i = 0
            for item in items:
                header = item.select_one('.lister-item-header')
                # 链接
                link = header.select_one('a')['href']                     
                id_pattern = re.compile(r'(?<=tt)\d+(?=/?)')
                # id
                id = str(id_pattern.search(link).group())           
                ratings_url = "https://www.imdb.com/title/tt"+str(id)+"/ratings?ref_=tt_ov_rt"
                ratings_url_list[i] = ratings_url
                i += 1
                # time.sleep(1)
            return ratings_url_list
        else:
            print("Request list url Failed", response.status_code)
    except RequestException:
        print("Request list url Failed")
        return None

def parse_data(data, table, row, column):
    rating_pattern = re.compile(r'\d.\d')
    result = rating_pattern.search(data[table].iloc[row, column])
    if result:
        return result.group()
    else:
        return None

def parse_ratings(ratings_url):
    try:
        response = requests.get(ratings_url, timeout=60)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html,'lxml') 

            # 匹配评分
            rating_pattern = re.compile(r'\d.\d') 

            # id
            id_pattern = re.compile(r'(tt)\d+')
            id = id_pattern.search(ratings_url).group()

            # 标题
            title = soup.select('div.parent > h3 > a')[0].get_text()

            # 上映日期
            date_text = soup.select('span.nobr')[0].get_text()
            date_pattern = re.compile(r'((?<=\()\d{4})')
            date = date_pattern.search(date_text).group()

            # 加权评分
            weighted_average = soup.select('div.ipl-rating-widget > div.ipl-rating-star > span.ipl-rating-star__rating')[0].get_text()

            # 算术评分
            try:
                mean_text = soup.select('div.allText > div.allText > div.allText[align=center]')[0].get_text()
            except:
                mean_text = soup.select('div#ratings-content > div.allText')[0].get_text()
            arithmetic_mean = rating_pattern.search(mean_text).group()

            # 详细评分数据
            data = pd.read_html(html)

            # 不同评分比例
            rating_10 = data[0].iloc[0, 1]
            rating_9  = data[0].iloc[1, 1]
            rating_8  = data[0].iloc[2, 1]
            rating_7  = data[0].iloc[3, 1]
            rating_6  = data[0].iloc[4, 1]
            rating_5  = data[0].iloc[5, 1]
            rating_4  = data[0].iloc[6, 1]
            rating_3  = data[0].iloc[7, 1]
            rating_2  = data[0].iloc[8, 1]
            rating_1  = data[0].iloc[9, 1]

            # 按性别，年龄分评分
            all_all_ages     = parse_data(data, 1, 0, 1)
            all_18           = parse_data(data, 1, 0, 2)
            all_18_29        = parse_data(data, 1, 0, 3) 
            all_30_44        = parse_data(data, 1, 0, 4) 
            all_45           = parse_data(data, 1, 0, 5) 
            males_all_ages   = parse_data(data, 1, 1, 1) 
            males_18         = parse_data(data, 1, 1, 2)
            males_18_29      = parse_data(data, 1, 1, 3)  
            males_30_44      = parse_data(data, 1, 1, 4) 
            males_45         = parse_data(data, 1, 1, 5) 
            females_all_ages = parse_data(data, 1, 2, 1) 
            females_18       = parse_data(data, 1, 2, 2) 
            females_18_29    = parse_data(data, 1, 2, 3) 
            females_30_44    = parse_data(data, 1, 2, 4) 
            females_45       = parse_data(data, 1, 2, 5) 

            # 按地区分评分
            top_1000    = parse_data(data, 2, 0, 0)
            us_user     = parse_data(data, 2, 0, 1)
            non_us_user = parse_data(data, 2, 0, 2)

            csvwriter.writerow([id, title, date, weighted_average, 
                arithmetic_mean, rating_10, rating_9, rating_8, rating_7, 
                rating_6, rating_5, rating_4, rating_3, rating_2, rating_1, 
                all_all_ages, all_18, all_18_29, all_30_44, all_45, 
                males_all_ages, males_18, males_18_29, males_30_44, males_45, 
                females_all_ages, females_18, females_18_29, females_30_44, 
                females_45, top_1000, us_user, non_us_user,])
        else:
            print("Request ratings url Failed", response.status_code)
    except RequestException:
        print("Request ratings url Failed")
        return None

if __name__ == '__main__':
    page = 156
    count = 0
    with open('imbd_ratings.csv', 'w', newline="", encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile, dialect=("excel"))
        csvwriter.writerow(['id', 'title', 'date', 'weighted_average', 
            'arithmetic_mean', 'rating_10', 'rating_9', 'rating_8', 'rating_7', 
            'rating_6', 'rating_5', 'rating_4', 'rating_3', 'rating_2', 
            'rating_1', 'all_all_ages', 'all_18', 'all_18_29', 'all_30_44', 
            'all_45', 'males_all_ages', 'males_18', 'males_18_29', 'males_30_44', 
            'males_45', 'females_all_ages', 'females_18', 'femaels_18_29', 
            'females_30_44', 'females_45', 'top_1000', 'us_user', 
            'non_us_user',])
        while (page < 200):
             print("Page " + str(page+1))
             list_url = generate_list_url(page + 1)
             ratings_url_list =  generate_ratings_list_url(list_url)
             i = 0
             while (i < 50):
                url = ratings_url_list[i]
                print(url)
                parse = parse_ratings(url)
                i += 1
                count += 1
             page += 1

    print("爬虫完毕，共爬取"+str(count)+"个评价")

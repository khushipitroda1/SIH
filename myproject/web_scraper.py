# Source : https://www.youtube.com/results?search_query=website+crawler+python
# Soruce : https://www.youtube.com/watch?v=XVv6mJpFOb0

# For ERROR-less life, Create a file named "scraped_data.csv" in the same folder where you keep this file

from bs4 import BeautifulSoup
import requests,csv
import pandas as pd

def web_scrapping():

    print("hello web")

    url = 'http://www.ptinews.com/'

    html_text = requests.get(url).text

    soup = BeautifulSoup(html_text, 'lxml')

    all_news = soup.find_all('li', class_ = 'catNameLi')

    all_big_news = soup.find_all('li', class_ = 'clsBigHead')

    all_recents = soup.find_all('a', class_ = 'catLatestHeadli')

    blogs = []

    for big_news_data in all_big_news:
        big_news = big_news_data.find('a')
        title = big_news.text
        news_url = url+(big_news.get_attribute_list('href')[0])
        blogs.append({
            'title' : title,
            'url' : news_url
        })


    for recents in all_recents:
        title = recents.text
        news_url = url + (recents.get_attribute_list('href')[0])
        blogs.append({
            'title' : title,
            'url' : news_url
        })

    for news in all_news:
        title_tag = news.find('a')
        title = title_tag.text
        news_url = url+(title_tag.get_attribute_list('href')[0])
        blogs.append({
            'title' : title,
            'url' : news_url
        })

    len = 0

    for blog in blogs:
        len=len+1
        blog_html_text = requests.get(blog['url']).text
        blog_soup = BeautifulSoup(blog_html_text, 'lxml')
        subject = blog_soup.find('span', class_ = 'cNodeCSS').text
        full_blog = blog_soup.find('div', class_ = 'fullstorydivstory')
        publish_time = full_blog.find('font').text
        publishes = full_blog.find('p', class_ = 'fulstorytext')
        publish_date = publishes.find('b').text
        
        pdate = publish_date.split(',')[1].split('(')[0].strip()

        story = full_blog.find('p').text.replace('  ','')
        blog.update({
            'story' : story,
            'subject':subject,
            'time' : pdate + publish_time,
        })
    
    # blogs.append({
    #     'title':"asdfghjm",
    #     'url':"http://www.ptinews.com//news/13650764_UP-police-constable-killed-after-truck-hits-his-bike.html",
    #     'story':"sdfgnm,mnbvcasdf",
    #     'subject':"National",
    #     "time": "Jun 15 12:37 HRS IST"
    # })

    idb = []
    for x in blogs:
        idb.append(x['url'])
        # print(idb)
    

    df = pd.read_csv('scraped_data.csv')
    urls = df['url'].to_list()
   

    did = [x for x in idb if x not in urls]
    # print(did)
    
    new_blogs = []
    for i in blogs:
        if i['url'] in did:
            new_blogs.append(i)
    # new_blogs=[x for x in blogs if did not in idb]
    # print(new_blogs)



    fields = ['title','url','story','subject','time']

    filename = 'scraped_data.csv'

    with open(filename, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fields)
        # writer.writeheader()
        writer.writerows(new_blogs)

    
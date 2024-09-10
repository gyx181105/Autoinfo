import requests

def fetch_news(url):
    response = requests.get(url)
    data = response.json()
    
    # 提取文章的标题、链接和发布时间
    news_list = []
    for item in data['items']:
        title = item.get('title', '无标题')
        link = item.get('url', '无链接')
        date_published = item.get('date_published', '无发布时间')
        news_list.append({
            'title': title,
            'link': link,
            'date_published': date_published
        })
    
    return news_list

# 调用函数并打印结果
url = "https://www.inoreader.com/stream/user/1005254904/tag/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD/view/json"
news = fetch_news(url)

for article in news:
    print(f"标题: {article['title']}\n链接: {article['link']}\n发布时间: {article['date_published']}\n")
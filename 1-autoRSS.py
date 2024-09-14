import requests
import datetime
import os
import re
import random

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

def sanitize_filename(filename):
    # 移除或替换不允许在文件名中使用的字符
    return re.sub(r'[\\/*?:"<>|]', "", filename)

# 将新闻内容写入txt文件
def save_news_to_txt(news_list):
    # 定义RSS文件夹路径
    folder_name = "RSS"
    
    # 如果文件夹不存在，创建文件夹
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    for article in news_list:
        # 获取当前日期作为时间戳
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        
        # 生成随机的5位数
        random_number = str(random.randint(10000, 99999))
        
        # 生成文件名：时间戳_随机数_标题.txt
        safe_title = sanitize_filename(article['title'])
        file_name = f"{today}_{random_number}_{safe_title[:40]}.txt"  # 限制标题长度为40个字符
        
        # 生成完整的文件路径
        file_path = os.path.join(folder_name, file_name)
        
        # 写入txt文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"标题: {article['title']}\n")
            file.write(f"链接: {article['link']}\n")
            file.write(f"发布时间: {article['date_published']}\n")
        
        print(f"新闻已保存到 {file_path} 文件中")

# 调用函数并保存结果
url = "https://www.inoreader.com/stream/user/1005255007/tag/crypto/view/json"
#url = "https://www.inoreader.com/stream/user/1005255007/tag/%E6%96%B0%E6%99%BA%E5%85%83/view/json" --新智源
news = fetch_news(url)
save_news_to_txt(news)

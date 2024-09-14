import requests
import os
import re
import html2text  # type: ignore
import datetime
import random

# 用于清理文件名，去掉不合法的字符
def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

# 从txt文件中读取标题和链接
def read_urls_from_file(file_path):
    urls = []
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        current_title = None
        for line in f:
            line = line.strip()
            if line.startswith(('标题:', '标题：')):
                current_title = re.split(':|：', line, 1)[1].strip()
            elif line.startswith(('链接:', '链接：')):
                url = re.split(':|：', line, 1)[1].strip()
                urls.append((current_title, url))
    return urls

# 使用本地FireCrawl获取网页内容，并增加调试信息
def fetch_content_with_firecrawl(title, url, firecrawl_url):
    payload = {"url": url}
    
    # 模拟真实的浏览器请求
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Referer": "https://news.google.com/",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Cookie": "_ga=GA1.1.423594254.1725944138; usprivacy=1N--; __qca=P0-2055733827-1725944140027; mailerlite:forms:shown:131107283436308164=310095; _ga_TK72K7QTSN=GS1.1.1725947277.2.1.1725947548.60.0.0"
    }

    try:
        # 发送请求到FireCrawl
        response = requests.post(firecrawl_url, json=payload, headers=headers)
        response.raise_for_status()  # 如果请求失败，抛出HTTPError
        
        # 打印完整返回的数据以调试
        data = response.json()
        print(f"抓取 {url} 返回的数据: {data}")

        # 检查返回的数据是否包含 'content' 字段
        if 'data' in data and 'content' in data['data']:
            return data['data']
        else:
            print(f"未抓取到有效内容: {url}")
            return None
    except requests.RequestException as e:
        print(f"请求失败: {url} - 错误: {e}")
        return None

# 转换HTML到Markdown
def convert_to_markdown(title, url, content):
    # 使用 html2text 将 HTML 转换为 Markdown
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    markdown_content = h.handle(content)
    
    # 将 \n\n 替换为换行符 \n
    markdown_content = markdown_content.replace('\n\n', '\n')

    return title, url, markdown_content

# 保存Markdown文件
def save_markdown(title, content, url, folder="MD"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    # 获取当前日期
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # 生成随机的5位数
    random_number = str(random.randint(10000, 99999))
    
    # 生成文件名：时间戳_随机数_标题.md
    safe_title = sanitize_filename(title)
    filename = f"{today}_{random_number}_{safe_title[:40]}.md"  # 限制标题长度为40个字符
    
    file_path = os.path.join(folder, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"原文链接: {url}\n\n")
        f.write(content)

    print(f"已保存: {file_path}")

# 主逻辑
firecrawl_url = "http://localhost:3002/v0/scrape"  # FireCrawl服务地址
rss_folder = "RSS"

for file in os.listdir(rss_folder):
    if file.endswith(".txt"):
        file_path = os.path.join(rss_folder, file)
        print(f"\n正在处理文件: {file_path}")
        try:
            urls = read_urls_from_file(file_path)  # 读取文件中的标题和URL
            for title, url in urls:
                print(f"处理文章: {title} - {url}")
                
                # 第一步：通过 FireCrawl 抓取文章页面内容
                data = fetch_content_with_firecrawl(title, url, firecrawl_url)
                if not data:
                    continue
                
                # 第二步：将HTML内容转换为Markdown
                content = data.get('content', '未抓取到内容')
                markdown_title, markdown_url, markdown_content = convert_to_markdown(title, url, content)
                
                # 第三步：保存为Markdown文件
                save_markdown(markdown_title, markdown_content, markdown_url)
                    
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")

print("处理完成")

import os
import re
from langchain_community.document_loaders import FireCrawlLoader
import html2text

# 用于清理文件名，去掉不合法的字符
def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

# 从txt文件中读取标题和链接
def read_urls_from_file(file_path):
    urls = []
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if line.startswith(('链接:', '链接：')):
                urls.append(re.split(':|：', line, 1)[1].strip())
    return urls

# 获取网页内容并转换为Markdown格式
def fetch_content_with_firecrawl(url, api_key):
    loader = FireCrawlLoader(
        api_key=api_key,
        url=url,
        mode="scrape",
    )
    data = loader.load()
    return data

def convert_to_markdown(item):
    title = item.metadata.get('title', '无标题')
    url = item.metadata.get('source', '无链接')
    content = item.page_content

    # 使用html2text转换HTML到Markdown
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    markdown_content = h.handle(content)
    
    return title, url, markdown_content

# 保存Markdown文件
def save_markdown(title, content, url, folder="MD"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    safe_title = sanitize_filename(title)
    filename = os.path.join(folder, f"{safe_title}.md")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"原文链接: {url}\n\n")
        f.write(content)
    print(f"已保存: {filename}")

api_key = "fc-f653a17b13bd400780c5099493c0c082"
rss_folder = "RSS"

for file in os.listdir(rss_folder):
    if file.endswith(".txt"):
        file_path = os.path.join(rss_folder, file)
        print(f"\n正在处理文件: {file_path}")
        try:
            urls = read_urls_from_file(file_path)
            for url in urls:
                print(f"处理URL: {url}")
                data = fetch_content_with_firecrawl(url, api_key)
                for item in data:
                    title, link, markdown_content = convert_to_markdown(item)
                    save_markdown(title, markdown_content, link)
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")

print("处理完成")

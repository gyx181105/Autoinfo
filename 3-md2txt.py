import os
import re

def convert_markdown_to_txt(md_file_path, txt_file_path):
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 保留图片和链接格式
    # 不需要修改，因为我们要保留原始格式

    # 2. 确保标题前后有空行
    content = re.sub(r'(\n|^)#', r'\n\n#', content)
    content = re.sub(r'#(.*?)\n', r'#\1\n\n', content)

    # 3. 确保作者和日期信息前后有空行
    content = re.sub(r'\n(by.*?)\n', r'\n\n\1\n\n', content)
    content = re.sub(r'\n([A-Z][a-z]+\.? \d{1,2}, \d{4})\n', r'\n\n\1\n\n', content)

    # 4. 移除多余的空行，最多保留两个连续的空行
    content = re.sub(r'\n{3,}', '\n\n', content)

    # 5. 确保文件以换行符结束
    if not content.endswith('\n'):
        content += '\n'

    with open(txt_file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def process_md_folder(md_folder, txt_folder):
    if not os.path.exists(txt_folder):
        os.makedirs(txt_folder)

    for filename in os.listdir(md_folder):
        if filename.endswith('.md'):
            md_file_path = os.path.join(md_folder, filename)
            txt_file_path = os.path.join(txt_folder, filename[:-3] + '.txt')
            print(f"正在处理文件: {md_file_path}")
            convert_markdown_to_txt(md_file_path, txt_file_path)
            print(f"已转换并保存为: {txt_file_path}")

# 使用示例
md_folder = "MD"  # Markdown 文件所在的文件夹
txt_folder = "TXT"  # 转换后的 txt 文件将保存在这个文件夹

process_md_folder(md_folder, txt_folder)
print("所有 Markdown 文件已转换为 TXT 格式")

import os
import requests
import json

def read_txt_file(file_path, max_chars=4000):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read(max_chars)

# def read_txt_file(file_path, max_chars=4000):
#     try:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             content = file.read(max_chars)
#         return content
#     except UnicodeDecodeError:
#         # 如果 UTF-8 解码失败，尝试使用 GBK 编码
#         try:
#             with open(file_path, 'r', encoding='gbk') as file:
#                 content = file.read(max_chars)
#             return content
#         except Exception as e:
#             print(f"无法读取文件 {file_path}: {e}")
#             return None

def generate_summary_with_ollama(content):
    ollama_url = "http://localhost:11434/api/generate"
    prompt = f"请为以下内容生成一个简洁的摘要：\n\n{content}\n\n摘要："
    
    payload = {
        "model": "llama2",
        "prompt": prompt,
        "stream": True
    }
    
    try:
        response = requests.post(ollama_url, json=payload, stream=True, timeout=120)
        response.raise_for_status()
        summary = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if 'response' in data:
                    summary += data['response']
                    print(data['response'], end='', flush=True)  # 实时打印输出
                if 'done' in data and data['done']:
                    break
        print("\n--- 摘要生成完成 ---")
        return summary
    except requests.exceptions.RequestException as e:
        print(f"Ollama API 请求失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"响应内容: {e.response.text}")
        return None
# def process_txt_folder(input_folder="TXT"):
#     for filename in os.listdir(input_folder):
#         if filename.endswith(".txt"):
#             file_path = os.path.join(input_folder, filename)
#             print(f"\n正在处理文件: {file_path}")
            
#             content = read_txt_file(file_path)
#             if content:
#                 print(f"文件内容 (前500个字符):\n{content[:500]}...")
#                 print(f"文件总字符数: {len(content)}")
#             else:
#                 print(f"无法读取文件 {filename} 的内容")

# if __name__ == "__main__":
#     process_txt_folder()
#     print("所有文件处理完成")


def process_txt_folder(input_folder="TXT"):
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_folder, filename)
            print(f"\n正在处理文件: {file_path}")
            
            content = read_txt_file(file_path)
            summary = generate_summary_with_ollama(content)
            
            if summary:
                print(f"\n文件 {filename} 的摘要已生成")
            else:
                print(f"无法为文件 {filename} 生成摘要")

if __name__ == "__main__":
    process_txt_folder()
    print("所有文件处理完成")

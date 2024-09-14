import os
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

def load_and_split_document(file_path):
    print(f"开始加载文件: {file_path}")
    loader = TextLoader(file_path, encoding='utf-8')
    documents = loader.load()
    print(f"文件加载完成，总字符数: {len(documents[0].page_content)}")
    
    print("开始分割文档")
    text_splitter = CharacterTextSplitter(chunk_size=4000, chunk_overlap=0)
    splits = text_splitter.split_documents(documents)
    print(f"文档分割完成，共分成 {len(splits)} 个片段")
    return splits

def generate_summary_with_ollama(content):
    print("初始化 Ollama 模型")
    llm = Ollama(model="llama2")
    
    prompt_template = """请为以下内容生成一个简洁的摘要：

    {content}

    摘要："""
    
    print("创建提示模板")
    prompt = PromptTemplate(template=prompt_template, input_variables=["content"])
    chain = LLMChain(llm=llm, prompt=prompt)
    
    try:
        print("开始生成摘要")
        summary = chain.run(content=content)
        print("摘要生成完成，内容如下：")
        print(summary)
        print("\n--- 摘要生成完成 ---")
        return summary
    except Exception as e:
        print(f"生成摘要时出错: {e}")
        return None

def process_txt_folder(input_folder="TXT"):
    print(f"开始处理文件夹: {input_folder}")
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_folder, filename)
            print(f"\n开始处理文件: {file_path}")
            
            try:
                docs = load_and_split_document(file_path)
                for i, doc in enumerate(docs):
                    print(f"\n处理文档片段 {i+1}/{len(docs)}")
                    print(f"片段内容预览 (前100个字符):\n{doc.page_content[:100]}...")
                    summary = generate_summary_with_ollama(doc.page_content)
                    if summary:
                        print(f"\n文件 {filename} 片段 {i+1} 的摘要已生成")
                    else:
                        print(f"无法为文件 {filename} 片段 {i+1} 生成摘要")
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {e}")

if __name__ == "__main__":
    print("程序开始执行")
    process_txt_folder()
    print("所有文件处理完成")
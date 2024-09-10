
from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field
import json
from langchain_community.document_loaders import FireCrawlLoader
api_key="fc-f653a17b13bd400780c5099493c0c082"
loader = FireCrawlLoader(
    api_key=api_key,
    url="https://firecrawl.dev",
    mode="scrape",
)

data = loader.load()

print(data)
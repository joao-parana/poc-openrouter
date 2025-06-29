## Usage

# Below are some code snippets that show you how to interact with our search API. The different steps and components of this code are explained in more detail in the API Methods section further down.

# ### Getting and printing the full Search API response

# ```python
import os
from datetime import datetime, timezone
from tavily import TavilyClient

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY") # Tavily API Key

start_time = datetime.now(timezone.utc)

# Step 1. Instantiating your TavilyClient
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# Step 2. Executing a simple search query
response = tavily_client.search("Who is Leo Messi?")

# Step 3. That's it! You've done a Tavily Search!
print(f"\n\n01 - {response}", flush=True)
# ```

# This is equivalent to directly querying our REST API.

# ### Generating context for a RAG Application

# ```python
from tavily import TavilyClient

# Step 1. Instantiating your TavilyClient
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# Step 2. Executing a context search query
context = tavily_client.get_search_context(query="What happened during the Burning Man floods?")

# Step 3. That's it! You now have a context string that you can feed directly into your RAG Application
print(f"\n\n02 - {context}", flush=True)
# ```

# This is how you can generate precise and fact-based context for your RAG application in one line of code.

# ### Getting a quick answer to a question

# ```python
from tavily import TavilyClient

# Step 1. Instantiating your TavilyClient
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# Step 2. Executing a Q&A search query
answer = tavily_client.qna_search(query="Who is Leo Messi?")

# Step 3. That's it! Your question has been answered!
print(f"\n\n03 - {answer}", flush=True)
# ```

# This is how you get accurate and concise answers to questions, in one line of code. Perfect for usage by LLMs!

# # Tavily Extract
# Extract web page content from one or more specified URLs.

# ## Usage

# Below are some code snippets that demonstrate how to interact with our Extract API. Each step and component of this code is explained in greater detail in the API Methods section below.

# ### Extracting Raw Content from Multiple URLs using Tavily Extract API

# ```python
from tavily import TavilyClient

# Step 1. Instantiating your TavilyClient
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# Step 2. Defining the list of URLs to extract content from
urls = [
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://en.wikipedia.org/wiki/Machine_learning",
    "https://en.wikipedia.org/wiki/Data_science",
    "https://en.wikipedia.org/wiki/Quantum_computing",
    "https://en.wikipedia.org/wiki/Climate_change"
] # You can provide up to 20 URLs simultaneously

# Step 3. Executing the extract request
response = tavily_client.extract(urls=urls, include_images=True)

print(f"\n\n04 - {len(response)}", flush=True)

# Step 4. Printing the extracted raw content
for result in response["results"]:
    print(f"URL: {result['url']}")
    print(f"Raw Content: {result['raw_content']}")
    print(f"Images: {result['images']}\n")

# Note that URLs that could not be extracted will be stored in response["failed_results"]
# ```

# # Tavily Crawl (Open-Access Beta)

# Crawl lets you traverse a website's content starting from a base URL.

# > **Note**: Crawl is currently available on an invite-only basis. For more information, please visit [crawl.tavily.com](https://crawl.tavily.com)

# ## Usage

# Below are some code snippets that demonstrate how to interact with our Crawl API. Each step and component of this code is explained in greater detail in the API Methods section below.

# ### Crawling a website with instructions

# ```python
from tavily import TavilyClient

# Step 1. Instantiating your TavilyClient
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# Step 2. Defining the starting URL
start_url = "https://wikipedia.org/wiki/Lemon"

# Step 3. Executing the crawl request with instructions to surface only pages about citrus fruits
response = tavily_client.crawl(
    url=start_url,
    max_depth=3,
    limit=50,
    instructions="Find all pages on citrus fruits"
)

# Step 4. Printing pages matching the query

print(f"\n\n05 - {len(response)}", flush=True)

for result in response["results"]:
    print(f"URL: {result['url']}")
    print(f"Snippet: {result['raw_content'][:200]}...\n")

# ```

# # Tavily Map (Open-Access Beta)

# Map lets you discover and visualize the structure of a website starting from a base URL.

# ## Usage

# Below are some code snippets that demonstrate how to interact with our Map API. Each step and component of this code is explained in greater detail in the API Methods section below.

# ### Mapping a website with instructions

# ```python
from tavily import TavilyClient

# Step 1. Instantiating your TavilyClient
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# Step 2. Defining the starting URL
start_url = "https://wikipedia.org/wiki/Lemon"

# Step 3. Executing the map request with parameters to focus on specific pages
response = tavily_client.map(
    url=start_url,
    max_depth=2,
    limit=30,
    instructions="Find pages on citrus fruits"
)

print(f"\n\n06 - {len(response["results"])}", flush=True)

# Step 4. Printing the site structure
for result in response["results"]:
    if 'url' in result:
        print(f"URL: {result['url']}")
    else:
        if isinstance(result, str):
            print(f"URL = {result}")

# ```

# ## Documentation

# For a complete guide on how to use the different endpoints and their parameters, please head to our [Python API Reference](https://docs.tavily.com/sdk/python/reference).

# ## Cost

# Tavily is free for personal use for up to 1,000 credits per month.
# Head to the [Credits & Pricing](https://docs.tavily.com/documentation/api-credits) in our documentation to learn more about how many API credits each request costs.

end_time = datetime.now(timezone.utc)
exec_time = (end_time - start_time).seconds
print(f"exec_time = {exec_time} segundos", flush=True)

import requests
import json
import os

OR_KEY = os.getenv("OR_KEY") # OpenRouter API Key
response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {OR_KEY}",
    # "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    # "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  data=json.dumps({
    "model": "deepseek/deepseek-r1-0528:free",  # Optional
    "messages": [
      {
        "role": "user",
        "content": "Qual é o significado da vida?"
      }
    ]
  })
)
print(response.json())

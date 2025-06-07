import requests
import json
import os

DS_KEY = os.getenv("DS_KEY") # DeepSeek API Key
response = requests.post(
  url="https://api.deepseek.com/chat/completions",
  headers={
    "Authorization": f"Bearer {DS_KEY}",
    "Content-Type": "application/json",
    # "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    # "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  data=json.dumps({
    # Optional deepseek-reasoner or deepseek-chat
    "model": "deepseek-reasoner",
    "messages": [
      {
        "role": "user",
        "content": "Qual é o significado da vida?"
      }
    ]
  })
)
print(response.json())

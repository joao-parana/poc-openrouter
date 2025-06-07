# Please install OpenAI SDK first: `python3 -m pip install -e .
import os
from datetime import datetime, timedelta, timezone
from openai import OpenAI

start_time = datetime.now(timezone.utc)
DS_KEY = os.getenv("DS_KEY") # DeepSeek API Key
client = OpenAI(api_key=DS_KEY, base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    # Optional deepseek-reasoner or deepseek-chat
    model="deepseek-reasoner",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Qual é o significado da vida?"},
    ],
    stream=False
)

print(response.choices[0].message.content)
end_time = datetime.now(timezone.utc)
exec_time = (end_time - start_time).seconds #.total_seconds()
print(f"exec_time = {exec_time} segundos")

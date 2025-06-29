# Please install OpenAI SDK first: `python3 -m pip install -e .
import os
from datetime import datetime, timedelta, timezone
from openai import OpenAI

start_time = datetime.now(timezone.utc)
OR_KEY = os.getenv("OR_KEY") # OpenRouter API Key
client = OpenAI(api_key=OR_KEY, base_url="https://openrouter.ai/api/v1/")

response = client.chat.completions.create(
    model="deepseek/deepseek-r1-0528:free",
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

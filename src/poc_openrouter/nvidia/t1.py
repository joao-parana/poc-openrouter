import os
from openai import OpenAI

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY") # NVidia API Key
client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = NVIDIA_API_KEY
)

completion = client.chat.completions.create(
  model="meta/llama-3.3-70b-instruct",
  messages=[
      {
          "role":"user",
          "content":"Qual é o significado da vida?"
      }
  ],
  temperature=0.1,
  top_p=0.7,
  max_tokens=1024,
  stream=True
)

ctrl_msgs = []
max_size = -1
counter = 0
for chunk in completion:
  counter = counter + 1
  if chunk.choices[0].delta.content is not None:
    size = len(chunk.choices[0].delta.content)
    if size > max_size:
      max_size = size
    ctrl_msgs.append(f"{counter}: {size} ")
    print(f"{chunk.choices[0].delta.content}", end="")

print(f"\n\nmax_size = {max_size}, chunk_sizes: \n{ctrl_msgs}")

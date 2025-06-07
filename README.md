# PoC OpenRouter

> LLM Proof of Concept using [deepseek-r1-0528:free model](https://openrouter.ai/deepseek/deepseek-r1-0528:free) from **openrouter.ai**

You can use this language model to test your application providing **LLM Agent** functionality without spending a single cent.

Create an account at [https://openrouter.ai/](https://openrouter.ai/) and add US $10 in credit and you will be able to use any available model. Many of them **have costs** that are debited from your account, however **you can use several free models** including the **"deepseek/deepseek-r1-0528:free"** model which has great performance with a high latency, but is sufficient for application testing.

The alternative would be to have a reasonable amount of money to use models from OpenAI or Google in your tests, which is sometimes not possible due to budget issues in the project.

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
python3 -m pip install -e .
```

## Example

```python
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
        "content": "Qual é o sentido da vida?"
      }
    ]
  })
)
print(response.json())
```

## License

`poc-openrouter` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

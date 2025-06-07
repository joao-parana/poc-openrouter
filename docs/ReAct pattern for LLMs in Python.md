# **ReAct pattern for LLMs in Python**

A popular nightmare scenario for AI is giving it access to tools, so it can make API calls and execute its own code and generally break free of the constraints of its initial environment.
Let's do that now!
The ReAct pattern (for Reason+Act) is [described in this paper](https://react-lm.github.io/). It's a pattern where you implement additional actions that an LLM can take - searching Wikipedia or running calculations for example - and then teach it how to request that those actions are run, then feed their results back into the LLM.
See also my post [Could you train a ChatGPT-beating model for $85,000 and run it in a browser?](https://simonwillison.net/2023/Mar/17/beat-chatgpt-in-a-browser/#react-pattern).
Matt Webb wrote a great piece about that here: [The surprising ease and effectiveness of AI in a loop](https://interconnected.org/home/2023/03/16/singularity). In it Matt points out that the 1/10 price reduction on ChatGPT compared to GPT-3 makes it an ideal candidate for cheaply implementing this pattern.
Matt used [langchain](https://github.com/hwchase17/langchain) for his implementation. I decided to try building it from scratch on top of my [tiny Python wrapper](https://til.simonwillison.net/gpt3/chatgpt-api) for the ChatGPT API.
Here's my first attempt at a very rough implementation. It gains access to three new actions:

- `wikipedia: <search term>` - search Wikipedia and returns the snippet of the first result
- `simon_blog_search: <search term>` - search my blog and return the truncated text of the first result
- `calculate: <expression>` - evaluate an expression using Python's `eval()` function (so dangerous! This should absolutely use something like [a WebAssembly sandbox](https://til.simonwillison.net/webassembly/python-in-a-wasm-sandbox) instead)

## **Some examples [#](https://til.simonwillison.net/llms/python-react-pattern#user-content-some-examples)**

Here are some (very cherry-picked) examples of my `query()` function running, showing the underlying deliberations of the LLM:

### **What does England share borders with? [#](https://til.simonwillison.net/llms/python-react-pattern#user-content-what-does-england-share-borders-with)**

query("What does England share borders with?")

Thought: I should list down the neighboring countries of England

Action: wikipedia: England

PAUSE

-- running wikipedia England

Observation: <span class="searchmatch">England</span> is a country that is part of the United Kingdom. It shares land borders with Wales to its west and Scotland to its north. The Irish Sea lies northwest

Answer: England shares borders with Wales and Scotland.

### **Has Simon been to Madagascar? [#](https://til.simonwillison.net/llms/python-react-pattern#user-content-has-simon-been-to-madagascar)**

query("Has Simon been to Madagascar?")

Thought: I can try and search on Simon's blog or look up Madagascar on Wikipedia to see if Simon has mentioned it in any of his writings.

Action: simon_blog_search: Madagascar

PAUSE

-- running simon_blog_search Madagascar

Observation: Weeknotes: More releases, more museums: Lots of small releases this week.

Datasette

I released two bug fix releases for Datasette - 0.30.1 and 0.30.2. Changelog here. My Dogsheep personal analytics project means I&#39;m using Datasette for my own data analysis every day, which inspires me to fix small but annoying bugs much more aggressively.

I&#39;ve also set myself a Streak goal to land a commit to Datasette every day.

I landed a tiny new feature to master yesterday: a ?column**notin=x,y,z filter, working as an inverse of the existing ?column**in=x,y,z filter. See issue #614 for details.

More Niche Museums

I&#39;ve been keeping up my streak of adding at least one new museum to www.niche-museums.com every day. This week I added the Pirates Museum in Antananarivo, Madagascar, the David Rumsey Map Center at Stanford, Galerie de Paléontologie et d’Anatomie comparée in Paris, DEVIL-ish Little Things in Vancouver, Washington, Mardi Gras World in New Orleans, Environmental Volunteers EcoCenter in Palo Alto, the Evergreen A

Observation: According to the blog post searched on Simon's blog, he has visited the Pirates Museum in Antananarivo, Madagascar which is listed as a niche museum on www.niche-museums.com.

Answer: Yes, Simon has been to Madagascar and visited the Pirates Museum located in Antananarivo.

### **Fifteen - twenty five [#](https://til.simonwillison.net/llms/python-react-pattern#user-content-fifteen--twenty-five)**

query("Fifteen - twenty five")

Thought: The action required is a calculation

Action: calculate: 15 - 25

PAUSE

-- running calculate 15 - 25

Observation: 375

Answer: Fifteen times twenty five equals 375.

## **The code [#](https://til.simonwillison.net/llms/python-react-pattern#user-content-the-code)**

```python
# This code is Apache 2 licensed:
# https://www.apache.org/licenses/LICENSE-2.0
import openai
import re
import httpx
openai.api_key = "sk-..."

class ChatBot:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result


    def execute(self):
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)
        # Uncomment this to print out token usage each time, e.g.
        # {"completion_tokens": 86, "prompt_tokens": 26, "total_tokens": 112}
        # print(completion.usage)
        return completion.choices[0].message.content
prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.
Your available actions are:
calculate:
e.g. calculate: 4 - 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary
wikipedia:
e.g. wikipedia: Django
Returns a summary from searching Wikipedia
simon_blog_search:
e.g. simon_blog_search: Django
Search Simon's blog for that term
Always look things up on Wikipedia if you have the opportunity to do so.
Example session:
Question: What is the capital of France?
Thought: I should look up France on Wikipedia
Action: wikipedia: France
PAUSE
You will be called again with this:
Observation: France is a country. The capital is Paris.
You then output:
Answer: The capital of France is Paris
""".strip()
action_re = re.compile('^Action: (w+): (.*)$')
def query(question, max_turns=5):
    i = 0
    bot = ChatBot(prompt)
    next_prompt = question
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        print(result)
        actions = [action_re.match(a) for a in result.split('n') if action_re.match(a)]
        if actions:
            # There is an action to run
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception("Unknown action: {}: {}".format(action, action_input))
            print(" -- running {} {}".format(action, action_input))
            observation = known_actions[action](action_input)
            print("Observation:", observation)
            next_prompt = "Observation: {}".format(observation)
        else:
            return
def wikipedia(q):
    return httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    }).json()["query"]["search"][0]["snippet"]
def simon_blog_search(q):
    results = httpx.get("https://datasette.simonwillison.net/simonwillisonblog.json", params={
        "sql": """
        select
          blog_entry.title || ': ' || substr(html_strip_tags(blog_entry.body), 0, 1000) as text,
          blog_entry.created
        from
          blog_entry join blog_entry_fts on blog_entry.rowid = blog_entry_fts.rowid
        where
          blog_entry_fts match escape_fts(:q)
        order by
          blog_entry_fts.rank
        limit
          1""".strip(),
        "_shape": "array",
        "q": q,
    }).json()
    return results[0]["text"]
def calculate(what):
    return eval(what)
known_actions = {
    "wikipedia": wikipedia,
    "calculate": calculate,
    "simon_blog_search": simon_blog_search
}
```

This is not a very robust implementation at all - there's a ton of room for improvement. But I love how simple it is - it really does just take a few dozen lines of Python to make these extra capabilities available to the LLM and have it start to use them.

### **Related**

- gpt3 [A simple Python wrapper for the ChatGPT API](https://til.simonwillison.net/gpt3/chatgpt-api) - 2023-03-02
- llms [Using llama-cpp-python grammars to generate JSON](https://til.simonwillison.net/llms/llama-cpp-python-grammars) - 2023-09-12
- llms [Summarizing Hacker News discussion themes with Claude and LLM](https://til.simonwillison.net/llms/claude-hacker-news-themes) - 2023-09-09
- llms [Exploring ColBERT with RAGatouille](https://til.simonwillison.net/llms/colbert-ragatouille) - 2024-01-27
- gpt3 [GPT-4 for API design research](https://til.simonwillison.net/gpt3/gpt4-api-design) - 2023-04-06
- llms [Running LLaMA 7B and 13B on a 64GB M2 MacBook Pro with llama.cpp](https://til.simonwillison.net/llms/llama-7b-m2) - 2023-03-10
- llms [Expanding ChatGPT Code Interpreter with Python packages, Deno and Lua](https://til.simonwillison.net/llms/code-interpreter-expansions) - 2023-04-30
- llms [Running OpenAI's large context models using llm](https://til.simonwillison.net/llms/larger-context-openai-models-llm) - 2023-06-13
- httpx [Logging OpenAI API requests and responses using HTTPX](https://til.simonwillison.net/httpx/openai-log-requests-responses) - 2024-01-26
- datasette [Interactive row selection prototype with Datasette](https://til.simonwillison.net/datasette/row-selection-prototype) - 2023-03-30

Updated 2023-03-20T15:18:43

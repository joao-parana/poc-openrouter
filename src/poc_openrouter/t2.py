
import openai as open_router
import re
import os
import httpx

OR_KEY = os.getenv("OR_KEY") # OpenRouter API Key

# 1. Configurar a base_url para a API da OpenRouter.ai
# 2. Configurar a chave da API da OpenRouter.ai e usar em openai.api_key pois são compatíveis
open_router.api_base = "https://openrouter.ai/api/v1"
open_router.api_key = OR_KEY # Substitua "sk-or-..." pela sua chave de API da OpenRouter.ai

print(f"api_base = {open_router.api_base}, api_key ~ {open_router.api_key[0:9]}...", flush=True)
# Adicione cabeçalhos específicos para a OpenRouter.ai, incluindo o User-Agent
# O User-Agent é obrigatório para algumas chamadas da OpenRouter.ai
headers = {
    "HTTP-Referer": "https://example.com", # Substitua pelo seu domínio ou URL de origem
    "X-Title": "My Awesome App",           # Substitua pelo nome da sua aplicação
}

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
        # A chamada para ChatCompletion.create é similar à da OpenAI, mas com o modelo da OpenRouter.ai
        model="deepseek/deepseek-r1-0528:free"
        print(f"Executing ChatCompletion.create() using {model} model")
        completion = open_router.ChatCompletion.create(
            model=model,
            messages=self.messages,
            headers=headers # Passar os cabeçalhos personalizados
        )
        # Uncomment this to print out token usage each time, e.g.
        # {"completion_tokens": 86, "prompt_tokens": 26, "total_tokens": 112}
        # print(completion.usage)
        print(f"completion.usage = {completion.usage}, content = {completion.choices[0].message.content}")
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
    print(f"what = {what}")
    return eval(what)

known_actions = {
    "wikipedia": wikipedia,
    "calculate": calculate,
    "simon_blog_search": simon_blog_search
}

# # Realizar a chamada à API
# # Adapte self.messages para uma lista de dicionários no formato esperado:
# # messages = [{"role": "user", "content": "Seu prompt aqui"}]
# # Por exemplo:
# messages = [
#     {"role": "user", "content": "Olá, qual é a capital da França?"}
# ]

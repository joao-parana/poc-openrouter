#!/usr/bin/env python
# coding: utf-8
# # Lesson 1: Simple ReAct Agent from Scratch
# based on https://til.simonwillison.net/llms/python-react-pattern Blog post
import sys
import openai
import re
import httpx
import os
# from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from openai import OpenAI

# dot_env_loaded = load_dotenv()
# if not dot_env_loaded:
#     raise RuntimeError("Arquivo .env não encontrado ou não carregado. Interrompendo a execução do Notebook")

DS_KEY = os.getenv("DS_KEY") # DeepSeek API Key

SMOKE_TEST = False
start_time = datetime.now(timezone.utc)
client = OpenAI(api_key=DS_KEY, base_url="https://api.deepseek.com")

if SMOKE_TEST:
    chat_completion = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Qual é o significado da vida?"},
        ],
    )
    chat_completion.choices[0].message.content

class Agent:
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
        completion = client.chat.completions.create(
                        model="deepseek-reasoner",
                        temperature=0,
                        messages=self.messages)
        return completion.choices[0].message.content

prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

average_dog_weight:
e.g. average_dog_weight: Collie
returns average weight of a dog when given the breed

Example session:

Question: How much does a Bulldog weigh?
Thought: I should look the dogs weight using average_dog_weight
Action: average_dog_weight: Bulldog
PAUSE

You will be called again with this:

Observation: A Bulldog weights 51 lbs

You then output:

Answer: A bulldog weights 51 lbs
""".strip()

def calculate(what):
    return eval(what)

def average_dog_weight(name):
    if name in "Scottish Terrier":
        return("Scottish Terriers average 20 lbs")
    elif name in "Border Collie":
        return("a Border Collies average weight is 37 lbs")
    elif name in "Toy Poodle":
        return("a toy poodles average weight is 7 lbs")
    else:
        return("An average dog weights 50 lbs")

known_actions = {
    "calculate": calculate,
    "average_dog_weight": average_dog_weight
}

my_agent = Agent(prompt)

result = my_agent("How much does a toy poodle weigh?")
print(result)
result = average_dog_weight("Toy Poodle")
next_prompt = "Observation: {}".format(result)
my_agent(next_prompt)
my_agent.messages
my_agent = Agent(prompt)
question = """I have 2 dogs, a border collie and a scottish terrier. \
What is their combined weight"""
my_agent(question)
next_prompt = "Observation: {}".format(average_dog_weight("Border Collie"))
print(next_prompt)
my_agent(next_prompt)
next_prompt = "Observation: {}".format(average_dog_weight("Scottish Terrier"))
print(next_prompt)
my_agent(next_prompt)
next_prompt = "Observation: {}".format(eval("37 + 20"))
print(next_prompt)
result = my_agent(next_prompt)
print(f"result = {result}")

end_time = datetime.now(timezone.utc)
exec_time = (end_time - start_time).seconds #.total_seconds()
print(f"exec_time = {exec_time} segundos")

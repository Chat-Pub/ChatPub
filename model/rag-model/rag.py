import os
from dotenv import load_dotenv
import openai
import json

from functions import *
from prompts import *

load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")

k = 3
knowledge_source_path = 'knowledge_source.json'
MODEL_NAME = 'gpt-3.5-turbo'

# load knowledge source
with open(knowledge_source_path, "r") as st_json:
     data_list = json.load(st_json)
index = set_index(data_list)


# get input
query = input("문의 사항을 입력하세요: ")

context, title_url_lists = get_context(index=index, query=query, k=k, data_list=data_list)

# get response
response = openai.ChatCompletion.create(
    model=MODEL_NAME,
    messages=[{"role":"system", "content":chat_system_prompt},
                {"role":"user", "content":chat_user_prompt_template.format(context=context, query=query)}],
    temperature = 0,
    frequency_penalty=0.0,
    presence_penalty=0.0
    )['choices'][0]['message']['content']

# get the only referenced context
referenced_context = get_valid_references(response = response,
                                            title_url_lists=title_url_lists)


print('Response:', response)
print('Referenced Context:', referenced_context)
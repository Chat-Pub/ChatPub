import os
from dotenv import load_dotenv
import openai
import json

from functions import *

load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")

context_cnt = 3
buffer_size = 2
knowledge_source_path = 'knowledge_source.json'
MODEL_NAME = 'gpt-3.5-turbo'

# load knowledge source
with open(knowledge_source_path, "r") as st_json:
     data_list = json.load(st_json)
index = set_index(data_list)

# set buffer memory
buffer_memory = BufferMemory(buffer_size)

# EXAMPLES for debugging
buffer_memory.save({'Human':'안녕?',
                    'AI':'안녕하세요! 저는 여러분이 받을 수 있는 정책 혜택을 알려주는 챗봇입니다! 무엇을 도와드릴까요?'})
buffer_memory.save({'Human':'고양시 청년이 받을 수 있는 정책 정보를 알려줘',
                    'AI':'고양시에서 청년들을 지원하는 정책 중 하나는 "고양청년 창업 재정지원 프로그램"입니다. 이 프로그램은 창신한 아이디어와 사업성을 가진 고양시 청년들의 창업 성공 가능성을 높이기 위해 무담보 신용보증과 최대 5천만 원 대출을 지원합니다. 이 프로그램은 상시로 신청 가능하며, 자세한 신청 방법은 경기신용보증재단 고양지점을 방문하거나 온라인으로 신청할 수 있습니다. 자세한 내용은 경기신용보증재단 고양지점의 전화번호 1577-5900로 문의하시거나, 고양시 홈페이지에서 확인하실 수 있습니다.'})

# get input
query = input("문의 사항을 입력하세요: ")

# for checking the results
print('\n=== RESULTS ===')
print('Query:', query)
print('Before Chat History:\n', buffer_memory.load())
print()

# get stand-alone question using memory saving the chat history
stand_alone_question = condense_question(model_name=MODEL_NAME, memory=buffer_memory, question=query)

# get context for answering question using stand_alone question
context, title_url_lists = get_context(index=index, query=stand_alone_question, context_cnt=context_cnt, data_list=data_list)

# get response
response = get_response(model_name=MODEL_NAME, context=context, query=stand_alone_question)

# save the current chat in memory
buffer_memory.save({"Human":stand_alone_question, "AI":response})

# get the only referenced context
referenced_context = get_valid_references(response=response,
                                            title_url_lists=title_url_lists)


print('Stand-alone Question', stand_alone_question)
print('After Chat History:\n', buffer_memory.load())
print()

print('Response:', response)
print('Referenced Context:', referenced_context)
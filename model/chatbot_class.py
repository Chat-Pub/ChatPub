from transformers import AutoTokenizer
from transformers import AutoModel
import torch
import openai
import faiss


condense_question_system = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question in Korean."""

condense_question_user_template = """
Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question: """

chat_system_prompt = """You are a Korean chatbot that tells you the policy benefits users can receive based on the given information.
Use the provided Context to answer questions.
Answer in as much detail and kindness as possible using the given context.

If the answer cannot be found in the context, just say that you don't know, don't try to make up an answer.
If you are asked a question that has nothing to do with the policy, say that you are a chatbot informing of the policy benefits the user can receive."""

chat_user_prompt_template = """Context:
{context}

User Question: {query}
Helpful Korean Response: """

def mean_pool(token_embeds, attention_mask):
    # reshape attention_mask to cover 768-dimension embeddings
    in_mask = attention_mask.unsqueeze(-1).expand(
        token_embeds.size()
    ).float()
    # perform mean-pooling but exclude padding tokens (specified by in_mask)
    pool = torch.sum(token_embeds * in_mask, 1) / torch.clamp(
        in_mask.sum(1), min=1e-9
    )
    return pool


def compute_similarity(response, title):
    preprocessed_response = response.replace('"','').replace("'",'').replace('\n', ' ').replace('  ', ' ')
    preprocessed_title = title.replace('"','').replace("'",'').replace('\n', ' ').replace('  ', ' ')
    tokenized_response = set(preprocessed_response.split(' '))
    tokenized_title = set(preprocessed_title.split(' '))

    return len(tokenized_title.intersection(tokenized_response)) / len(tokenized_title)


def condense_question(model_name, memory, question):
    chat_history = memory.load()

    messages = [{"role":"system", 
                 "content":condense_question_system},
                 {"role":"user",
                  "content":condense_question_user_template.format(chat_history=chat_history, question=question)}]
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        temperature = 0
    )

    return response.choices[0]['message']['content']


class SentenceTransformers(torch.nn.Module):
    def __init__(self, model_name):
        super(SentenceTransformers, self).__init__()
        self.model = AutoModel.from_pretrained(model_name)

    def forward(self, **inputs):
        embed_vec= self.model(**inputs)[0]
        outputs = mean_pool(
            token_embeds=embed_vec,
            attention_mask=inputs['attention_mask']
        )

        return outputs
    
    
class BufferMemory():
    def __init__(self, buffer_size):
        # chat history storage
        self.chat_history = []
        self.buffer_size = buffer_size

    def save(self, curr_chat: dict):
        # save the current chat history in memory

        # chat format:
        # {'Human':str,
        #   'AI': str}
        self.chat_history.append(curr_chat)

        if len(self.chat_history) > self.buffer_size:
            self.chat_history = self.chat_history[-self.buffer_size:]
    
    def load(self) -> str:
        chat_history_str = ""

        for chat in self.chat_history:
            for key, value in chat.items():
                chat_history_str += f'{key}: {value}\n'
        
        return chat_history_str

    def clear(self):
        self.chat_history = []
    
# TODO
# 서버에 띄어진 faiss index
INDEX = None

# INDEX가 포함하는 각 벡터에 대한 인덱스를 index 값으로 갖는 database list
# value 값은 정책 정보 dict.

# 중요!!
# '링크'의 key는 'url' 로 설정. 
# '제목'의 key는 'title' 로 설정.
# e.g. [{'title': '수원시행복주택', 'age': '청년', 'url': 'www.~'}, {"..."}, ...]
DATABASE = None

# buffer memory 선언 필요:
# buffer_memory = BufferMemory(3)

class ChatBot:
    def __init__(self, model_path:str = "", buffer:BufferMemory = None):
        self.base_model = "klue/roberta-base"
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.base_model, use_fast=True)
        self.retrieval = SentenceTransformers(self.base_model)
        if model_path != "":
            self.retrieval.load_state_dict(torch.load(model_path))
        self.retrieval.eval()
        self.buffer = buffer
        
    def forward(self, user_info:str = "", user_question:str = "") -> dict:
        stand_alone_question = condense_question(model_name='gpt-3.5-turbo', 
                                                 memory=self.buffer, 
                                                 question=user_question)

        retrieval_input_str = user_info + stand_alone_question
        llm_input = f"유저정보: {user_info}\n유저질문: {stand_alone_question}"

        tokenized_retrieval_input = self.tokenizer(
            retrieval_input_str, return_tensors='pt'
        )
        retrieval_input = {
            'input_ids': tokenized_retrieval_input['input_ids'],
            'attention_mask': tokenized_retrieval_input['attention_mask']
        }
        query_vector = self.retrieval(**retrieval_input)        

        # retrieve context using faiss
        distance, index = INDEX.search(query_vector, 3)
        context = ''
        title_list = [] # used for represent reference
        url_list = [] # used for represent reference

        # index shape: (1, 3)
        for i in index[0]:
            context_item = ''
            for key, value in DATABASE[i].items():
                if key == 'url':
                    url_list.append(value)
                    continue
                if key == 'title':
                    title_list.append(value)
                context_item += f'{key}: {value}\n'
            
            context += context_item
            context += "\n==============\n" # seperator
        
        # get response 
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role":"system", "content":chat_system_prompt},
                        {"role":"user", "content":chat_user_prompt_template.format(context=context, query=llm_input)}],
            temperature = 0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )['choices'][0]['message']['content']

        # validate references
        references = []
        for title, url in zip(title_list, url_list):
            sim = compute_similarity(response, title)
            if sim >= 0.5:
                references.append(f'제목: {title}\n링크: {url}\n')
    
        # key 값 고정
        result_dict = {
            "answer": response,
            "references":references # 길이 가변 (0 ~ 3), 각 원소는 string
        }

        # buffer에 history 저장
        self.buffer.save({
            "Human":stand_alone_question,
            "AI":response
        })

        return result_dict
        



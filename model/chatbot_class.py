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


class ChatBot:
    def __init__(self, model_path:str = ""):
        self.base_model = "klue/roberta-base"
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.base_model, use_fast=True)
        self.retrieval = SentenceTransformers(self.base_model)
        if model_path != "":
            self.retrieval.load_state_dict(torch.load(model_path))
        self.retrieval.eval()
        
    def forward(self, user_info:str = "", user_question:str = "") -> dict:
        retrieval_input_str = user_info + user_question
        llm_input = f"유저정보: {user_info}\n유저질문: {user_question}"

        tokenized_retrieval_input = self.tokenizer(
            retrieval_input_str, return_tensors='pt'
        )
        retrieval_input = {
            'input_ids': tokenized_retrieval_input['input_ids'],
            'attention_mask': tokenized_retrieval_input['attention_mask']
        }
        query_vector = self.retrieval(**retrieval_input)        

        # TODO: retrieve context using faiss
        
        # TODO: ADD LLM

        # key 값 고정
        result_dict = {
            "answer": "챗봇이 출력하는 답", # string
            "references":["참조한 텍스트 1", "참조한 텍스트 2", "참조한 텍스트 3"] # 길이 가변 (0 ~ 3), 각 원소는 string
        }

        return result_dict
        



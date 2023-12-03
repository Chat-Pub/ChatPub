from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from prompts import *
import openai


def get_response(model_name, context, query, is_baseline):
    if is_baseline == True:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[{"role":"system", "content":chat_system_prompt_baseline},
                        {"role":"user", "content":chat_user_prompt_template_baseline.format(context=context, query=query)}],
            temperature = 0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        return response['choices'][0]['message']['content']
    
    elif is_baseline == False:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[{"role":"system", "content":chat_system_prompt},
                        {"role":"user", "content":chat_user_prompt_template.format(context=context, query=query)}],
            temperature = 0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        return response['choices'][0]['message']['content']

def get_eval(model_name, question, passage, baseline_response, prompted_response, is_comparison):
    if is_comparison:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[{"role":"system", "content":eval_system_prompt_comparison},
                        {"role":"user", "content":eval_user_prompt_template_comparison.format(question=question, answer_ref=passage,
                                                                                answer_a=baseline_response,
                                                                                answer_b=prompted_response)}],
            temperature = 0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        return response['choices'][0]['message']['content']

    else:
        results = []
        # baseline
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[{"role":"system", "content":eval_system_prompt_grading},
                        {"role":"user", "content":eval_user_prompt_template_grading.format(question=question, answer_ref=passage,
                                                                                answer=baseline_response)}],
            temperature = 0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        results.append(response['choices'][0]['message']['content'])

        # prompted
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[{"role":"system", "content":eval_system_prompt_grading},
                        {"role":"user", "content":eval_user_prompt_template_grading.format(question=question, answer_ref=passage,
                                                                                answer=prompted_response)}],
            temperature = 0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        results.append(response['choices'][0]['message']['content'])

        return results
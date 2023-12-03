import os
from dotenv import load_dotenv
import openai
import json
from collections import defaultdict
import argparse
from tqdm import tqdm
from functions import *
import time

# Argument parser


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--have_baseline', type=str,
                        default='true')
    parser.add_argument('--have_prompt', type=str,
                        default='true')
    parser.add_argument('--is_comparison', type=str,
                        default='true')


    args = parser.parse_args()

    config = defaultdict()
    for arg, value in args._get_kwargs():
        config[arg] = value

    return args

def main():
     args = get_args()
     load_dotenv()
     openai.api_key = os.getenv("OPENAI_KEY")

     train_data_path = 'data/train.json'
     #MODEL_NAME = 'gpt-3.5-turbo'
     MODEL_NAME = 'gpt-4-1106-preview'
     JUDGE_MODEL_NAME = 'gpt-4-1106-preview'

     with open(train_data_path, "r") as data_json:
          train_dataset = json.load(data_json)['data']

     # baseline 결과 없는 경우, 베이스라인에 대한 추론 수행
     if args.have_baseline == 'false':
          baseline_results = []
          print('============= Get Results on Baseline Model =============')
          for data in tqdm(train_dataset):
               query = data['question']
               context = data['passage']
               
               # get response
               response = get_response(model_name=MODEL_NAME, context=context, query=query, is_baseline=True)
               baseline_results.append({
                    "question":query,
                    "passage":context,
                    "response":response
               })
               time.sleep(20)
          with open(f'results/base_line.json', 'w') as outfile:
               json.dump(baseline_results, outfile, indent=4, ensure_ascii=False)

      # prompt 결과 없는 경우, prompt engineering 수행된 프롬프트에 추론 수행
     if args.have_prompt == 'false':
          prompted_results = []
          print('============= Get Results on Prompted Model =============')
          for data in tqdm(train_dataset):
               query = data['question']
               context = data['passage']
          
               # get response
               response = get_response(model_name=MODEL_NAME, context=context, query=query, is_baseline=False)
               prompted_results.append({
                    "question":query,
                    "passage":context,
                    "response":response
               })
               time.sleep(20)
               with open(f'results/prompted.json', 'w') as outfile:
                    json.dump(prompted_results, outfile, indent=4, ensure_ascii=False)

     with open("results/base_line.json", "r") as data_json:
          baseline_results = json.load(data_json)
     with open("results/prompted.json", "r") as data_json:
          prompted_results = json.load(data_json)

     # 둘 결과 비교
     evals=[]
     print('============= Get Evals =============')
     for b_r, p_r in zip(tqdm(baseline_results), prompted_results):
          question = b_r['question']
          passage = b_r['passage']
          basline_response = b_r['response']
          prompted_response = p_r['response']

          if args.is_comparison == 'true':
               eval_result = get_eval(model_name=JUDGE_MODEL_NAME, question=question, passage=passage,
                                   baseline_response=basline_response, prompted_response=prompted_response,
                                   is_comparison=True)
               
               evals.append({
                    "question":question,
                    "passage":passage,
                    "baseline_response":basline_response,
                    "prompted_response":prompted_response,
                    "eval_result":eval_result
               })
               time.sleep(20)
          
          else:
               eval_result = get_eval(model_name=JUDGE_MODEL_NAME, question=question, passage=passage,
                                   baseline_response=basline_response, prompted_response=prompted_response,
                                   is_comparison=False)
               
               evals.append({
                    "question":question,
                    "passage":passage,
                    "baseline_response":basline_response,
                    "prompted_response":prompted_response,
                    "baseline_eval_result":eval_result[0],
                    "prompted_eval_result":eval_result[1],
               })

               time.sleep(40)
          
     if args.is_comparison == 'true':
          with open(f'results/eval_comparison.json', 'w') as outfile:
               json.dump(evals, outfile, indent=4, ensure_ascii=False)
     else:
          with open(f'results/eval_grading.json', 'w') as outfile:
               json.dump(evals, outfile, indent=4, ensure_ascii=False)
if __name__ == '__main__':
    main()

import os
import json
import argparse
from collections import defaultdict

import torch
import numpy as np
from tqdm.auto import tqdm
import random

from model_class import SentenceTransformers
from utils import collate_fn,  Dataset, get_tokenizer, mean_pool, metrics, NoDuplicatesDataLoader


# Argument parser


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str,
                        default='prajjwal1/bert-tiny')
    parser.add_argument('--max_length', type=int, default=128)
    parser.add_argument('--model_path', type=str, default="")
    parser.add_argument('--eval_batch_size', type=int, default=16)
    parser.add_argument('--test_data', type=str)

    args = parser.parse_args()

    config = defaultdict()
    for arg, value in args._get_kwargs():
        config[arg] = value

    return args

def main():
    random_seed = 42
    random.seed(random_seed)
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    np.random.seed(random_seed)
    torch.manual_seed(random_seed)

    args = get_args()
    tokenizer = get_tokenizer(args)
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    model_name = args.model_name.split('/')[-1]
    data_name = args.test_data.split('/')[-2]
    result_path = f'model/sentence_transformers/output/{model_name}_pre-trained_{data_name}.json'

    with open(args.test_data, 'r') as f:
        test_dataset = json.load(f)

    test_dataset = Dataset(
            tokenizer, args.max_length, test_dataset)
    test_sample = test_dataset.get_list()
    test_loader = NoDuplicatesDataLoader(
            test_sample,
            batch_size=args.eval_batch_size,
            collate_fn=collate_fn,
            tokenizer=tokenizer
        )

    model = SentenceTransformers(args.model_name)
    if args.model_path != "":
        model.load_state_dict(torch.load(args.model_path))
        result_path = f'model/sentence_transformers/output/{args.model_path.split("/")[-1].replace(".pth","")}_{data_name}.json'

    cos_sim = torch.nn.CosineSimilarity()
    
    # move layers to device
    cos_sim.to(device)
    model.to(device)  

    # Validation Steps
    with torch.no_grad():
        model.eval()
        predictions = []
        target_labels = []
        with tqdm(test_loader, unit="batch", desc='Eval') as tepoch:
            for anchor_ids, anchor_mask, positive_ids, positive_mask, labels in tepoch:
                anchor_ids = anchor_ids.to(device)
                anchor_mask = anchor_mask.to(device)
                positive_ids = positive_ids.to(device)
                positive_mask = positive_mask.to(device)
                labels = labels.to(device)

                anchor_inputs = {
                    "input_ids":anchor_ids,
                    "attention_mask":anchor_mask
                }
                positive_inputs = {
                    "input_ids":positive_ids,
                    "attention_mask":positive_mask
                }
                a = model(**anchor_inputs)[0]  # all token embeddings
                p = model(**positive_inputs)[0]

                # get the mean pooled vectors
                a = mean_pool(a, anchor_mask)
                p = mean_pool(p, positive_mask)

                # calculate the cosine similarities
                scores = torch.stack([
                    cos_sim(
                        a_i.reshape(1, a_i.shape[0]), p
                    ) for a_i in a])
                
                batch_predictions = [int(torch.argmax(score).cpu()) for score in scores]
                batch_labels = [int(example) for example in labels]

                predictions += batch_predictions
                target_labels += batch_labels
                
    acc, precision, recall, f1 = metrics(predictions, target_labels, 'macro')
    result = {
        "Acc":acc,
        "Precision":precision,
        "Recall":recall,
        "F1":f1
    }

    for key, value in result.items():
        print(key,value)

    with open(result_path, 'w') as outfile:
        json.dump(result, outfile, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()

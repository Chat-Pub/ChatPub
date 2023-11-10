import os
import json
import argparse
from collections import defaultdict

import torch
import numpy as np
from tqdm.auto import tqdm
import random

from transformers import AdamW
from transformers import get_linear_schedule_with_warmup

from model_class import SentenceTransformers
from utils import collate_fn,  Dataset, get_tokenizer, mean_pool


# Argument parser


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str,
                        default='prajjwal1/bert-tiny')
    parser.add_argument('--max_length', type=int, default=128)
    parser.add_argument('--train_batch_size', type=int, default=16)
    parser.add_argument('--learning_rate', type=float, default=0.00001)
    parser.add_argument('--epoch', type=int, default=5)

    '''
    parser.add_argument('--eval_batch_size', type=int, default=16)
    parser.add_argument('--train_data', type=str)
    parser.add_argument('--valid_data', type=str)
    parser.add_argument('--test_data', type=str)
    '''

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


    """
    with open(args.train_data, 'r') as f:
        train_dataset = json.load(f)
    with open(args.valid_data, 'r') as f:
        valid_dataset = json.load(f)
    with open(args.test_data, 'r') as f:
        test_dataset = json.load(f)
    """
    with open("model/sentence_transformers/data/test_data.json", 'r') as f:
        train_dataset = json.load(f)

    train_dataset = Dataset(
            tokenizer, args.max_length, train_dataset)
    train_loader = torch.utils.data.DataLoader(
            train_dataset,
            batch_size=args.train_batch_size,
            collate_fn=collate_fn,
            shuffle=True,
            num_workers=4,
            drop_last=True
        )

    model = SentenceTransformers(args.model_name)

    cos_sim = torch.nn.CosineSimilarity()
    loss_func = torch.nn.CrossEntropyLoss()
    scale = 20.0  # we multiply similarity score by this scale value
    
    # move layers to device
    cos_sim.to(device)
    loss_func.to(device)
    model.to(device)

    # initialize Adam optimizer
    optim = torch.optim.Adam(model.parameters(), lr=2e-5)

    # setup warmup for first ~10% of steps
    total_steps = int(len(train_dataset) / args.train_batch_size)
    warmup_steps = int(0.1 * total_steps)
    scheduler = get_linear_schedule_with_warmup(
        optim, num_warmup_steps=warmup_steps,
        num_training_steps=total_steps-warmup_steps
    )

    from tqdm.auto import tqdm

    for epoch in range(1, args.epoch+1):
        train_losses = []
        with tqdm(train_loader, unit="batch") as tepoch:
            for iteration,\
                (anchor_ids, anchor_mask,
                positive_ids, positive_mask,
                    labels
                    ) in enumerate(tepoch):

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
                
                loss = loss_func(scores*scale, labels)
                # using loss, calculate gradients and then optimize
                loss.backward()
                optim.step()
                # update learning rate scheduler
                scheduler.step()
                
                train_losses.append(loss.item())
                
if __name__ == '__main__':
    main()

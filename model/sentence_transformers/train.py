import os
import json
import argparse
from collections import defaultdict

import torch
import numpy as np
from tqdm.auto import tqdm
import random

from transformers import get_linear_schedule_with_warmup

from model_class import SentenceTransformers
from utils import collate_fn,  Dataset, get_tokenizer, mean_pool, metrics


# Argument parser


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str,
                        default='prajjwal1/bert-tiny')
    parser.add_argument('--max_length', type=int, default=128)
    parser.add_argument('--train_batch_size', type=int, default=16)
    parser.add_argument('--learning_rate', type=float, default=0.00001)
    parser.add_argument('--epoch', type=int, default=5)
    parser.add_argument('--eval_batch_size', type=int, default=16)
    parser.add_argument('--train_data', type=str)
    parser.add_argument('--valid_data', type=str)

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

    with open(args.train_data, 'r') as f:
        train_dataset = json.load(f)
    with open(args.valid_data, 'r') as f:
        valid_dataset = json.load(f)

    train_dataset = Dataset(
            tokenizer, args.max_length, train_dataset)
    valid_dataset = Dataset(
            tokenizer, args.max_length, valid_dataset)
    train_loader = torch.utils.data.DataLoader(
            train_dataset,
            batch_size=args.train_batch_size,
            collate_fn=collate_fn,
            shuffle=True,
            num_workers=4,
            drop_last=True
        )
    valid_loader = torch.utils.data.DataLoader(
            valid_dataset,
            batch_size=args.eval_batch_size,
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

    lowest_valid_loss = 99999.

    for epoch in range(1, args.epoch+1):
        train_losses = []
        model.train()
        with tqdm(train_loader, unit="batch", desc='Train') as tepoch:
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
                
                loss = loss_func(scores*scale, labels)
                # using loss, calculate gradients and then optimize
                loss.backward()
                optim.step()
                # update learning rate scheduler
                scheduler.step()
                
                train_losses.append(loss.item())

        # Validation Steps
        with torch.no_grad():
            model.eval()
            valid_losses = []
            predictions = []
            target_labels = []
            with tqdm(valid_loader, unit="batch", desc='Eval') as tepoch:
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
                    
                    loss = loss_func(scores*scale, labels)
                    valid_losses.append(loss.item())

                    batch_predictions = [int(torch.argmax(score).cpu()) for score in scores]
                    batch_labels = [int(example) for example in labels]

                    predictions += batch_predictions
                    target_labels += batch_labels
                   
        train_loss = sum(train_losses) / len(train_losses)
        valid_loss = sum(valid_losses) / len(valid_losses)
        acc, precision, recall, f1 = metrics(predictions, target_labels, 'macro')

        print(f"\nEpoch{epoch}")
        print(f"Train Loss: {train_loss}")
        print(f"Vald Loss: {valid_loss}")
        print(f"Acc: {acc}")
        print(f"Precision: {precision}")
        print(f"Recall: {recall}")
        print(f"F1: {f1}\n")

        if lowest_valid_loss > valid_loss:
            model_path = os.path.join(
                    'model/sentence_transformers/model_params',
                    f'{model_name}_{args.learning_rate}.pth'
                )
            torch.save(model.state_dict(), model_path)
            
            lowest_valid_loss = valid_loss
            print("The Best Model Is Updated!")
            print('Acc for model which have lower valid loss: ', acc)
            print('F1 for model which have lower valid loss: ', f1)
                
if __name__ == '__main__':
    main()

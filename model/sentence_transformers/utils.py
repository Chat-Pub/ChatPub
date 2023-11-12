from torch.nn.utils.rnn import pad_sequence
from transformers import AutoTokenizer
import torch
import numpy as np
import evaluate


PAD_VALUE = 0

def compute_acc(predictions, target_labels):
    return (np.array(predictions) == np.array(target_labels)).mean()


class Dataset(object):
    def __init__(self, tokenizer, max_length, dataset):
        questions = []
        passages=[]

        for example in dataset['data']:
            question = example['question'].strip()
            passage = example['passage'].strip()

            if question != "" and passage != "":
                questions.append(question)
                passages.append(passage)

        tokenized_questions = tokenizer(questions,
                                       max_length=max_length,
                                       truncation=True)
        tokenized_passages = tokenizer(passages,
                                       max_length=max_length,
                                       truncation=True)
        
        self.anchor_ids = tokenized_questions['input_ids']
        self.positive_ids = tokenized_passages['input_ids']

    def __len__(self):
        return len(self.anchor_ids)

    def __getitem__(self, index):
        return self.anchor_ids[index], self.positive_ids[index]
    

def collate_fn(samples):
    anchor_ids, positive_ids = zip(*samples)

    anchor_max_len = max(len(input_id) for input_id in anchor_ids)
    positive_max_len = max(len(input_id) for input_id in positive_ids)
    len_inputs = range(len(anchor_ids))

    anchor_mask = torch.tensor(
        [[1] * len(anchor_ids[index]) + [0] * (anchor_max_len - len(anchor_ids[index]))
         for index in len_inputs])
    positive_mask = torch.tensor(
        [[1] * len(positive_ids[index]) + [0] * (positive_max_len - len(positive_ids[index]))
         for index in len_inputs])
    
    anchor_ids = pad_sequence(
        [torch.tensor(anchor_ids[index]) for index in len_inputs],
        batch_first=True, padding_value=PAD_VALUE)
    positive_ids = pad_sequence(
        [torch.tensor(positive_ids[index]) for index in len_inputs],
        batch_first=True, padding_value=PAD_VALUE)
    
    labels = torch.tensor(len_inputs, dtype=torch.long)

    return anchor_ids, anchor_mask, positive_ids, positive_mask, labels


def get_tokenizer(args):
    global PAD_VALUE
    if args.model_name:
        tokenizer = AutoTokenizer.from_pretrained(
            args.model_name, use_fast=True)
        PAD_VALUE = tokenizer.pad_token_id
        return AutoTokenizer.from_pretrained(args.model_name, use_fast=True)
    

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

def metrics(predictions, target_labels, average):
    f1_metric = evaluate.load("f1")
    precision_metric = evaluate.load("precision")
    recall_metric = evaluate.load("recall")

    acc = compute_acc(predictions, target_labels)
    precision = precision_metric.compute(
        predictions=predictions, references=target_labels, average=average)['precision']
    recall = recall_metric.compute(
        predictions=predictions, references=target_labels, average=average)['recall']
    f1 = f1_metric.compute(
        predictions=predictions, references=target_labels, average=average)['f1']

    return acc, precision, recall, f1
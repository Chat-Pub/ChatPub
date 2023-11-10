import torch
from transformers import AutoModel

class SentenceTransformers(torch.nn.Module):
    def __init__(self, model_name):
        super(SentenceTransformers, self).__init__()
        self.model = AutoModel.from_pretrained(model_name)

    def forward(self, **inputs):
        outputs = self.model(**inputs)

        return outputs
    
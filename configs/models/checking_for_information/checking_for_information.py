import numpy as np
import torch 

from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer

import warnings
warnings.simplefilter('ignore')



tokenizer = AutoTokenizer.from_pretrained("configs/models/checking_for_information/tokenizer_")
id2label = {0: "нет", 1: "да"}
label2id = {"нет": 0, "да": 1}

model_is_relevant = AutoModelForSequenceClassification.from_pretrained(
    "configs/models/checking_for_information/model_is_relevant_96", num_labels=2, id2label=id2label, label2id=label2id
)


def is_informative(text):
    l = [0,0]

    for j, i in enumerate(text):
        s = tokenizer.encode(i, return_tensors='pt')
        x = model_is_relevant(s).logits[0].detach().numpy()
        x = np.exp(x)/sum(np.exp(x))
        l[0] += x[0]
        l[1] += x[1]
    print('inf', l)
    return l

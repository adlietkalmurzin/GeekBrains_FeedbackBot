import numpy as np
import torch 

from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer

import warnings
warnings.simplefilter('ignore')



tokenizer = AutoTokenizer.from_pretrained("configs/models/identify_object/tokenizer")
id3label = {0: "вебинар", 1: "программа", 2: "преподаватель"}
label3id = {"вебинар": 0, "программа": 1, 'преподаватель': 2}
model_object = AutoModelForSequenceClassification.from_pretrained(
    "configs/models/identify_object/model_object_1", num_labels=3, id2label=id3label, label2id=label3id, ignore_mismatched_sizes=True
)

def identify_object(text):
    l = [0,0,0]

    for i in text:
        s = tokenizer.encode(i, return_tensors='pt')
        x = model_object(s).logits[0].detach().numpy()
        x = np.exp(x)/sum(np.exp(x))
        l[0] += x[0]
        l[1] += x[1]
        l[2] += x[2]
    print('obj', l)
    return int(np.argmax(l))

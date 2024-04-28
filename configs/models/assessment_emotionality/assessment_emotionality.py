import numpy as np
import torch 

from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer

import warnings
warnings.simplefilter('ignore')




tokenizer = AutoTokenizer.from_pretrained("configs/models/assessment_emotionality/tokenizer_em")
id2label = {0: "нет", 1: "да"}
label2id = {"нет": 0, "да": 1}

model_is_positive = AutoModelForSequenceClassification.from_pretrained(
    "configs/models/assessment_emotionality/model_is_positive_1", num_labels=2, id2label=id2label, label2id=label2id
)
def assessment_emotionality(text):
    s = tokenizer.encode(text, return_tensors='pt')
    x = model_is_positive(s).logits[0].detach().numpy()
    return int(np.argmax(np.exp(x)/sum(np.exp(x))))

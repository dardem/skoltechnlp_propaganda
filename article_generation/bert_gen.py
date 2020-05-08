
import torch
import time


import logging

from tools.generate_all_articles_ids import *
from tools.tokenization import *
from tools.vector_expansion_bert import *
from tools.conll_convertor import CONLLConvertor
from tqdm import tqdm

import sys
sys.path.append('generative_ie_master/src/')
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '6' # Choose your CUDA device


from transformers import BertForMaskedLM
from transformers.tokenization_bert import BertTokenizer
from predict import analyze_tagged_text
from masked_token_predictor_bert import MaskedTokenPredictorBert
from ling_parse import create_parsers

print('I work!')

model = BertForMaskedLM.from_pretrained('bert-large-cased', cache_dir='./cache')
res = model.cuda()
bpe_tokenizer = BertTokenizer.from_pretrained('bert-large-cased', do_lower_case=False, cache_dir='./cache')
ppl = create_parsers()
predictor = MaskedTokenPredictorBert(model, bpe_tokenizer, max_len=250)


analyze_bert = lambda tagged_text: list(zip(*analyze_tagged_text(tagged_text, predictor, ppl, 
                                                                         n_top=6,
                                                                         n_units=1,
                                                                         n_tokens=[1],
                                                                         max_multiunit=50,
                                                                         fix_multiunit=False,
                                                                         multiunit_lookup=200)[:2]))

CONLL_DATASET_PATH = 'data/dataset_conll/si'

print('Bert loaded successfully.')


data_exp = CONLLConvertor.convert_train_offset_to_conll()
print('Data converted successfully.')

MODEL_DICT = {'bert' : analyze_bert}
with open('extended_stopwords', 'r') as file:
    stop_words = file.read().split('\n') + ['\n', ' ', '\t', "'", '“', '”', '/', '\\', ']', '[']
    
stop_words = set(stop_words)

postype_arr = [['n', 'adj', 'adv', 'v'], ['n', 'adj', 'adv'], ['n', 'adj'], ['n']]
print('Starting real work.')

expander = ArticleGenerator(model_dict = MODEL_DICT, stopwords = stop_words, model_name='bert', strat='all',
                                    label='all', postype=['n', 'adj', 'adv', 'v'], word_percent = 1, closest=1, num_copies=4)
expander.get_bert_superdict(data_exp)

superdict = expander.bert_superdict
print('Superdict generated. Expanding.')
i=0
for target in ['neutral', 'propaganda', None]:
    for postype in postype_arr:
        i += 1
        start = time.time()
        new_expander = ArticleGenerator(model_dict = MODEL_DICT, stopwords = stop_words, model_name='bert', strat='all',
                                    label=target, postype=postype, word_percent = 0.73, 
                                        closest=1, num_copies=9, bert_superdict=superdict)
        data_new = new_expander.transform_dataset_bert(data_exp)
        fig = '-'.join(postype)
        if target == None:
            target = 'all'
        f = open('new_modified_datasets/'+f'bert_{target}_{fig}_70.txt', 'w')
        for article in data_new:
            f.write('--DOCSTART--')
            f.write('\n')
            for sentence in article:
                for word in sentence:
                    token, label = word.split()
                    f.write(f'{token} {label}\n')
                f.write('\n')
        f.close()
        end = time.time()
        m = (end - start)//60
        s = (end - start)%60
        print(f'Number {i} out of 12 ready in {m} minutes {s} seconds')
                    
                    
                    
                    
                            
                            
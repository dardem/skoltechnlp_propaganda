import torch
import time


import logging

from tools.generate_all_articles_ids import *
from tools.tokenization import *
from tools.vector_expansion_bert import *
from tools.conll_convertor import CONLLConvertor
from tqdm import tqdm


CONLL_DATASET_PATH = 'data/dataset_conll/si'

print('I work!')

# pretrained GloVe
glove_model = gensim.models.KeyedVectors.load_word2vec_format('gensim_glove_vectors.txt')  
print('Glove loaded successfully.')

data_exp = CONLLConvertor.convert_train_offset_to_conll()
print('Data converted successfully.')

MODEL_DICT = {'glove' : glove_model}
with open('extended_stopwords', 'r') as file:
    stop_words = file.read().split('\n') + ['\n', ' ', '\t', "'", '“', '”', '/', '\\', ']', '[']
    
stop_words = set(stop_words)

postype_arr = [['n', 'adj', 'adv', 'v'], ['n', 'adj', 'adv'], ['n', 'adj'], ['n']]

print('Starting real work.')
i=0
for target in ['neutral', 'propaganda']:
    for postype in postype_arr:
        i += 1
        start = time.time()
        expander = ArticleGenerator(model_dict = MODEL_DICT, stopwords = stop_words, model_name='glove', strat='all',
                                    label=target, postype=postype, word_percent = 0.7, closest=1, num_copies=9)
        data_new = expander.transform_dataset(data_exp)
        fig = '-'.join(postype)
        if target == None:
            target = 'all'
        f = open('new_modified_datasets/'+f'glove_{target}_{fig}_70.txt', 'w')
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
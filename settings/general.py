import os
from settings import ROOT_DIR

TRAIN_ARTICLES_PATH = os.path.join(ROOT_DIR, 'data/datasets/train-articles')
DEV_ARTICLES_PATH = os.path.join(ROOT_DIR, 'data/datasets/dev-articles')

TRAIN_ARTICLES_SI_LABELS_PATH = os.path.join(ROOT_DIR, 'data/datasets/train-labels-task1-span-identification')
TRAIN_ARTICLES_TC_LABELS_PATH = os.path.join(ROOT_DIR, 'data/datasets/train-labels-task2-technique-classification')

CONLL_DATASET_PATH = os.path.join(ROOT_DIR, 'data/dataset_conll')
TRAIN_CONLL_DATASET_PATH = os.path.join(ROOT_DIR, 'data/dataset_conll/train.txt')
TEST_CONLL_DATASET_PATH = os.path.join(ROOT_DIR, 'data/dataset_conll/test.txt')
DEV_CONLL_DATASET_PATH = os.path.join(ROOT_DIR, 'data/dataset_conll/dev.txt')

COMPETITION_DEV_DATASET_PATH = os.path.join(ROOT_DIR, 'data/dataset_conll/competition_dev.txt')
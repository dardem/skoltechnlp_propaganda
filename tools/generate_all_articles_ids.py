from settings.general import TRAIN_ARTICLES_PATH, DEV_ARTICLES_PATH
import os


def generate_all_train_ids():
    articles_ids = []
    for filename in os.listdir(TRAIN_ARTICLES_PATH):
        articles_ids.append(filename[7:-4])

    return articles_ids


def generate_all_dev_ids():
    articles_ids = []
    for filename in os.listdir(DEV_ARTICLES_PATH):
        articles_ids.append(filename[7:-4])

    return articles_ids

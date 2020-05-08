from settings.general import *
from settings.tc_labels import TC2IDX, TC_BANNED
import os


def inside_span(position, article_labels):
    for period in article_labels:
        if (position >= period[1]) and (position < period[2]):
            return period[0]
    return 0


def tokenize_train(article_id, task_type='SI', by_sentence=True, joint_sentence=1):
    tokens = []
    positions = []
    classes = []

    with open(os.path.join(TRAIN_ARTICLES_PATH, 'article' + article_id + '.txt'), 'r') as file:
        text = file.read()
    span_indexes = []
    if task_type == 'SI':
        with open(os.path.join(TRAIN_ARTICLES_SI_LABELS_PATH, 'article' + article_id + '.task1-SI.labels'), 'r') as file:
            for line in file.readlines():
                indexes = line.strip().split('\t')
                span_indexes.append((1, int(indexes[1]), int(indexes[2])))
    else:
        with open(os.path.join(TRAIN_ARTICLES_TC_LABELS_PATH, 'article' + article_id + '.task2-TC.labels'), 'r') as file:
            for line in file.readlines():
                indexes = line.strip().split('\t')
                if indexes[1] not in TC_BANNED:
                    span_indexes.append((TC2IDX[indexes[1]], int(indexes[2]), int(indexes[3])))

    article_labels = span_indexes.copy()
    word = text[0]
    position = 0
    sentences = []

    for i, symbol in enumerate(text[1:]):
        word_class = inside_span(position, article_labels)

        if (not word.isalpha()) and (not word.isdigit()):
            tokens.append(word)
            classes.append(word_class)
            positions.append(position - len(word) + 1)
            word = symbol
        else:
            if not ((symbol.isalpha()) or (symbol.isdigit() or (symbol == '-') or (symbol == "'"))):
                tokens.append(word)
                classes.append(word_class)
                positions.append(position - len(word) + 1)
                word = symbol
            else:
                word += symbol

        if word == '\n':
            if by_sentence:
                sentences.append([tokens, positions, classes])
                tokens = []
                positions = []
                classes = []
                word = symbol

        position += 1

    if by_sentence:
        if joint_sentence > 1:
            cleaned_sentences = []
            for sentence in sentences:
                if len(sentence[0]) == 1:
                    continue
                cleaned_sentences.append(sentence)

            result = []
            for i in range(len(cleaned_sentences)-joint_sentence):
                new_sentence = [[], [], []]
                for j in range(joint_sentence):
                    new_sentence[0] += sentences[i+j][0]
                    new_sentence[1] += sentences[i+j][1]
                    new_sentence[2] += sentences[i+j][2]
                result.append(new_sentence)
            return result
        else:
            return sentences
    else:
        return tokens, positions, classes


def tokenize_dev(article_id, by_sentence=True):
    tokens = []
    positions = []
    sentences = []

    with open(os.path.join(DEV_ARTICLES_PATH, 'article' + article_id + '.txt'), 'r') as file:
        text = file.read()

    word = text[0]
    position = 0

    for i, symbol in enumerate(text[1:]):
        if (not word.isalpha()) and (not word.isdigit()):
            tokens.append(word)
            positions.append(position)
            word = symbol
        else:
            if not ((symbol.isalpha()) or (symbol.isdigit() or (symbol == '-') or (symbol == "'"))):
                tokens.append(word)
                positions.append(position)
                word = symbol
            else:
                word += symbol

        if word == '\n':
            if by_sentence:
                sentences.append([tokens, positions])
                tokens = []
                positions = []

                word = symbol

        position += 1
    if by_sentence:
        return sentences
    else:
        return tokens, positions

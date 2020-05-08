from tools.tokenization import *
from settings.tc_labels import IDX2TCLABEL
from tools.generate_all_articles_ids import *
from tqdm import tqdm
from nltk.corpus import stopwords
from random import shuffle
en_stopwords = stopwords.words('english')


def correct(token):
    stop_symbols = ['\n', '\t', ' ']
    if (len([symbol for symbol in stop_symbols if symbol in token]) > 0): #or (len(token) == 1) or (token in en_stopwords):
        return False
    return True

class CONLLConvertor:

    @staticmethod
    def convert_article_offset_to_conll(article_id, by_sentence=True, context=1, task_type='SI-BIO', keep_position=False, delimeter=' '):
        def get_biluo_tag(index, tags, result_tags, task_type='SI'):
            tag = tags[index]
            if task_type == 'SI':
                if tag == 1:
                    if (index == 0) or (len(result_tags) == 1):
                        return 'B-SPAN'
                    elif result_tags[-2] == 1:
                        if (index == len(tags)-1) or (tags[index + 1] == 0):
                            return 'L-SPAN'
                        else:
                            return 'I-SPAN'
                    elif result_tags[-2] == 0:
                        if (index == len(tags)-1) or (tags[index + 1] == 0):
                            return 'U-SPAN'
                        else:
                            return 'B-SPAN'
                else:
                    return 'O'
            else:
                if tag != 0:
                    tag_name = IDX2TCLABEL[tag]
                    if (index == 0) or (len(result_tags) == 1):
                        return 'B-'+tag_name
                    elif (result_tags[-2] != 0) and (result_tags[-2] == tag):
                        if (index == len(tags)-1) or (tags[index + 1] == 0):
                            return 'L-'+tag_name
                        else:
                            return 'I-'+tag_name
                    else:
                        if (index == len(tags)-1) or (tags[index + 1] == 0):
                            return 'U-'+tag_name
                        else:
                            return 'B-'+tag_name
                else:
                    return 'O'

        result = []
        result_tags = []

        if by_sentence:
            sentences = tokenize_train(article_id, task_type=task_type[:2], by_sentence=by_sentence, joint_sentence=context)
            for sentence in sentences:
                sentence_res = []
                for index, (token, position, _tag) in enumerate(zip(sentence[0], sentence[1], sentence[2])):
                    if correct(token):
                        result_tags.append(sentence[2][index])
                        tag = get_biluo_tag(index, sentence[2], result_tags, task_type=task_type[:2])

                        if 'BILUO' in task_type:
                            res_tag = tag
                        elif ('BIO' in task_type):
                            if (tag[0] == 'U') or (tag[0] == 'L'):
                                res_tag = 'I' + tag[1:]
                            else:
                                res_tag = tag

                            if 'BIO-wd' in task_type:
                                if res_tag[0] == 'B':
                                    res_tag = res_tag[2:] + '-B'
                                elif res_tag[0] == 'I':
                                    res_tag = res_tag[2:] + '-I'

                        if keep_position:
                            sentence_res.append(token + delimeter + str(position) + delimeter + res_tag)
                        else:
                            sentence_res.append(token + delimeter + res_tag)

                if len(sentence_res) > 0:
                    result.append('\n'.join(sentence_res))
        else:
            tokens, positions, tags = tokenize_train(article_id, by_sentence=by_sentence)

            for index, (token, position, _tag) in enumerate(zip(tokens, positions, tags)):
                if correct(token):
                    result_tags.append(tags[index])
                    tag = get_biluo_tag(index, tags, result_tags, task_type=task_type[:2])

                    if 'BILUO' in task_type:
                        res_tag = tag
                    elif ('BIO' in task_type):
                        if (tag[0] == 'U') or (tag[0] == 'L'):
                            res_tag = 'I' + tag[1:]
                        else:
                            res_tag = tag

                        if 'BIO-wd' in task_type:
                            if res_tag[0] == 'B':
                                res_tag = res_tag[2:] + '-B'
                            elif res_tag[0] == 'I':
                                res_tag = res_tag[2:] + '-I'

                    if keep_position:
                        result.append(token + delimeter + str(position) + delimeter + res_tag)
                    else:
                        result.append(token + delimeter + res_tag)

        if by_sentence:
            return '\n\n'.join(result)

        return '\n'.join(result)


    @staticmethod
    def convert_train_offset_to_conll(task_type='SI-BIO', by_sentence=True, context=1, keep_position=False,
                                      delimeter=' ', test_dev=False):
        article_ids = generate_all_train_ids()

        articles_tagged = []
        for article_id in tqdm(article_ids):
            articles_tagged.append(CONLLConvertor.convert_article_offset_to_conll(article_id = article_id,
                                                                                  by_sentence=by_sentence,
                                                                                  context=context,
                                                                                  keep_position=keep_position,
                                                                                  delimeter=delimeter,
                                                                                  task_type=task_type))

        if not test_dev:
            with open(TRAIN_CONLL_DATASET_PATH, 'w') as file:
                #file.write('-DOCSTART- -X- O O\n\n' + '\n\n-DOCSTART- -X- O O\n\n'.join(articles_tagged))
                file.write('\n\n'.join(articles_tagged))
        else:
            shuffle(articles_tagged)
            train_df = articles_tagged[:-50]
            #test_df = articles_tagged[-75:-50]
            dev_df = articles_tagged[-50:]

            with open(TRAIN_CONLL_DATASET_PATH, 'w') as file:
                #file.write('-DOCSTART- -X- O O\n\n' + '\n\n-DOCSTART- -X- O O\n\n'.join(train_df))
                file.write('\n\n'.join(train_df))
            #with open(TEST_CONLL_DATASET_PATH, 'w') as file:
                #file.write('-DOCSTART- -X- O O\n\n' + '\n\n-DOCSTART- -X- O O\n\n'.join(test_df))
            #    file.write('\n\n'.join(test_df))
            with open(DEV_CONLL_DATASET_PATH, 'w') as file:
                #file.write('-DOCSTART- -X- O O\n\n' + '\n\n-DOCSTART- -X- O O\n\n'.join(dev_df))
                file.write('\n\n'.join(dev_df))

        return articles_tagged


    @staticmethod
    def convert_article_dev_to_conll(article_id, by_sentence=True, delimeter=' '):
        result = []

        if by_sentence:
            sentences = tokenize_dev(article_id, by_sentence=by_sentence)
            for sentence in sentences:
                sentence_res = []
                for index, (token, position) in enumerate(zip(sentence[0], sentence[1])):
                    if correct(token):
                        sentence_res.append(token + delimeter + str(position))

                if len(sentence_res) > 0:
                    result.append('\n'.join(sentence_res))
        else:
            tokens, positions = tokenize_train(article_id, by_sentence=by_sentence)

            for index, (token, position) in enumerate(zip(tokens, positions)):
                if correct(token):
                    result.append(token + delimeter + str(position))

        if by_sentence:
            return '\n\n'.join(result)

        return '\n'.join(result)

    @staticmethod
    def convert_dev_to_conll(by_sentence = True):
        article_ids = generate_all_dev_ids()

        articles_tagged = []

        for article_id in tqdm(article_ids):
            articles_tagged.append(
                CONLLConvertor.convert_article_dev_to_conll(article_id=article_id, by_sentence=by_sentence) + '\n')

        with open(COMPETITION_DEV_DATASET_PATH, 'w') as file:
            file.write('\n'.join(articles_tagged))


#CONLLConvertor.convert_train_offset_to_conll(task_type='SI-BIO', by_sentence=True, context=1, test_dev=True, delimeter=' ')
#CONLLConvertor.convert_dev_to_conll(by_sentence=True)

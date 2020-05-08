import os
from IPython.display import HTML
from settings.markup_visualizer import *
from settings.general import *
from ast import literal_eval


class MarkUpVisualizer:

    @staticmethod
    def request_color_legend(classes_hightlights, task_type='SI'):
        if task_type == 'SI':
            classes_names = CLASSES_NAMES_SI
        elif task_type == 'SI-BILUO':
            classes_names = CLASSES_NAMES_SI_BILUO
        else:
            classes_names = CLASSES_NAMES_TC
        lenend = '<h3> Легенда: </h3>'
        for i in classes_hightlights.keys():
            lenend += '<br>' + str(i) + ' : ' + classes_hightlights[i]('test') + ' : ' + classes_names[i]
        return lenend

    @staticmethod
    def highlight_markup(tokens, classes, classes_hightlights):
        return ' '.join([classes_hightlights[class_label](tokens[i]) for i, class_label in enumerate(classes)])

    @staticmethod
    def visualize_markup(tokens, classes, task_type='SI'):
        if task_type == 'SI':
            classes_highlights_html = CLASSES_HIGHLIGHTS_SI_HTML
        elif task_type == 'SI-BILUO':
            classes_highlights_html = CLASSES_HIGHLIGHTS_SI_BILUO_HTML
        else:
            classes_highlights_html = CLASSES_HIGHLIGHTS_TC_HTML

        result = '<h3> Article: </h3>'
        result += '<br>' + MarkUpVisualizer.highlight_markup(tokens,
                                            classes,
                                            classes_highlights_html)

        result += '<br>'
        result += MarkUpVisualizer.request_color_legend(classes_highlights_html, task_type)

        return HTML(result)

    @staticmethod
    def visualize_article_si_idx(article_id):
        def inside_span(position, span_indexes):
            for period in span_indexes:
                if (position >= period[0]) and (position < period[1]):
                    return 1
            return 0

        with open(os.path.join(TRAIN_ARTICLES_PATH, 'article' + article_id + '.txt'), 'r') as file:
            text = file.read()

        span_indexes = []
        with open(os.path.join(TRAIN_ARTICLES_SI_LABELS_PATH, 'article' + article_id + '.task1-SI.labels'), 'r') as file:
            for line in file.readlines():
                indexes = line.strip().split('\t')
                span_indexes.append((int(indexes[1]), int(indexes[2])))

        tokens = []
        classes = []

        for position, symbol in enumerate(text):
            tokens.append(symbol)
            classes.append(inside_span(position, span_indexes))

        return MarkUpVisualizer.visualize_markup(tokens, classes)

    @staticmethod
    def visualize_article_si_conll(article_path, task_type='SI'):
        tokens = []
        classes = []
        if task_type == 'SI':
            classes2idx = CLASSES_NAMES_SI2IDX
        elif task_type == 'SI-BILUO':
            classes2idx = CLASSES_NAMES_SI_BILUO2IDX

        with open(article_path, 'r') as file:
            for line in file.readlines():
                token, pos, cls = line.strip().split(' ')
                tokens.append(literal_eval(token))
                classes.append(classes2idx[cls])

        return MarkUpVisualizer.visualize_markup(tokens, classes, task_type)

    @staticmethod
    def visualize_article_tc_idx(article_id):
        def inside_span(position, span_indexes):
            for period in span_indexes:
                if (position >= period[1]) and (position < period[2]):
                    return CLASSES_NAMES_TC2IDX[period[0]]
            return 0

        with open(os.path.join(TRAIN_ARTICLES_PATH, 'article' + article_id + '.txt'), 'r') as file:
            text = file.read()

        span_indexes = []
        with open(os.path.join(TRAIN_ARTICLES_TC_LABELS_PATH, 'article' + article_id + '.task2-TC.labels'), 'r') as file:
            for line in file.readlines():
                indexes = line.strip().split('\t')
                span_indexes.append((indexes[1], int(indexes[2]), int(indexes[3])))

        tokens = []
        classes = []

        for position, symbol in enumerate(text):
            tokens.append(symbol)
            classes.append(inside_span(position, span_indexes))

        return MarkUpVisualizer.visualize_markup(tokens, classes, 'TC')
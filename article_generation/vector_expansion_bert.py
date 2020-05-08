import gensim
from tqdm import tqdm
import stanfordnlp
import nltk
from multi_rake import Rake
import numpy as np


class ArticleGenerator():

    def __init__(self, model_dict, stopwords, model_name = 'glove', strat = 'keywords', 
                      label = None, postype =None, closest = 1, 
                      article_percent= 1,
                      word_percent = 1, num_copies=1, bert_superdict = {}):
        """
    
        :params:
        model_dict, dict -- contains the models which will be used for
        synonimizing
          
        model_name, str, values = 'glove', 'word2vec', 'fasttext' or other
        
        strat: str, values are "keywords", "all" -- strategy of synonimizing, 
        rather to choose keywords or all words respectively
        
        label, str or NoneType, values = 'neutral', 'propaganda', None if choose all
        
        postype, list of strings or NoneType, 
        values = 'adj', 'adv', 'v', 'n' -- preferred parts of speech to be 
        included in the synonimization, None for all types
        Example: speechpart = ['adj', 'v', 'adv']
        
        closest, int -- closeness of a synonym to find, the bigger the less similar.
        
        article_percent, int 0 < x <=1 -- percentage of articles to transform
        
        word_percent, int 0 < x <= 1 -- percentage of words to change
        
        word_replace, bool -- calculate word_percent randomly with or without replacement,
                            only relevant when word_percent < 1
        """
        self.model_dict = model_dict
        self.model_name = model_name
        self.strat = strat
        self.label = label
        self.postype = postype
        self.closest = closest
        self.word_percent = word_percent
        self.num_copies = num_copies
        self.model = self.model_dict[self.model_name]
        self.stopwords = stopwords
        self.bert_superdict = bert_superdict
        
        


    def get_text(self, article):
        text = str()
        for sentence in article:
            for comb in sentence:
                word, label = comb.split()
                text += (word +' ')
        return text


    def get_keywords(self, article):
        """
        Find the keywords in article and return them in a convenient way.
        :params:
            article, list of sentences, sentences are lists of strings 
        :returns:
            keywords, list of strings -- extracted keywords
        """
        #here we save the labels that will NOT be changed
        labeltype = set()
        if self.label is not None:
            if self.label == 'neutral':
                labeltype.add('B-SPAN')
                labeltype.add('I-SPAN')
            elif self.label == 'propaganda':
                labeltype.add('0')
            
        #additional variable that holds parts of speech that will NOT be changed
        pos_shortcuts = {
        'NN': 'n',
        'JJ': 'adj',
        'RB': 'adv',
        'VB': 'v'
        }

        wordtypes = set()
        if self.postype is not None:
            wordtypes = {'n', 'adj', 'adv', 'v'}
            for fig in self.postype:
                wordtypes.discard(fig)

        text = self.get_text(article)
        text = ''.join(c for c in text if c not in '\'\"')
        rake = Rake()
        try:
            fig = rake.apply(text)
        except:
            print('Couldn\'t find keywords, falling back to all words.' )
            fig = self.get_words(article)
            return fig

        raw_keywords = []
        for string, _ in fig:
            raw_keywords += string.split()


        raw_keywords = set(raw_keywords)

        keywords = {}

        for i in range(len(article)):
            sentence = article[i]
            for comb in sentence:
                word, label = comb.split()
                word = word.lower()
                pos = nltk.pos_tag([word])[0][1]
                if pos in pos_shortcuts:
                    pos = pos_shortcuts[pos]
                if word in raw_keywords and label not in labeltype and pos not in wordtypes:
                    keywords[word] = i
        return keywords


 #  def get_tokens(self, article):
 #      """
 #      Get list of all words in the text.
 #      :params:
 #          article, list of sentences, sentences are lists of strings--
 #          element of the dataset
 #      :returns:
 #          tokens, list of strings
 #      """
 #      tokens = []
 #      for sentence in article:
 #          for comb in sentence:
 #              word, label = comb.split()
 #              tokens.append(word.lower())
 #      return tokens

    def get_words(self, article):
        """
        Create a list of words that are to be changed.

        :params:
            article, list of sentences, sentences are lists of strings--
            element of the dataset

        :returns:
            words, list of words that are to be changed
        """
        labeltype = set()
        if self.label is not None:
            if self.label == 'neutral':
                labeltype.add('B-SPAN')
                labeltype.add('I-SPAN')
            elif self.label == 'propaganda':
                labeltype.add('0')
            
        #additional variable that holds parts of speech that would NOT be changed
        pos_shortcuts = {
        'NN': 'n',
        'JJ': 'adj',
        'RB': 'adv',
        'VB': 'v'
        }
        wordtypes = set()
        if self.postype is not None:
            wordtypes = {'n', 'adj', 'adv', 'v'}
            for fig in self.postype:
                wordtypes.discard(fig)

        words = {}

        for i in range(len(article)):
            sentence = article[i]
            for comb in sentence:
                word, label = comb.split()
                word = word.lower()
                pos = nltk.pos_tag([word])[0][1]
                if pos in pos_shortcuts:
                    pos = pos_shortcuts[pos]
                if label not in labeltype and pos not in wordtypes and word not in self.stopwords:
                    words[word] = i
        return words


    def get_changes(self, words):
        """
        Creates a dict object to be later used for synonimization. 
        :params: 
            words, dict of strings:ints -- words that are to be changed
            
        :returns:
            chagedict, dict, words (str) : synonims (str) -- dictionary to be used for
            synonimization
        
        """
        words = list(words.keys())

        changedict = {}
        if self.word_percent < 1:
            words = list(np.random.choice(np.array(words), size = int(len(words)*self.word_percent)))
            
        closest_array = list(np.random.choice(np.array([self.closest, self.closest + 1, 
                                                        self.closest + 2, self.closest + 3]), size = int(len(words))))
            
        for comb, closest in zip(words,closest_array):
            a = comb.split() #очень часто слов в одной строке более одного, поэтому будем заменять каждое
            for word in a:
                try:
                    #если модель знает такое слово, заменяем его
                    alt = self.model.most_similar(positive = ['{}'.format(word)])[closest][0] 
                except:
                    alt = word #если модель не знает такого слова, мы его просто оставляем

                changedict[word] = alt #запись слова и синонима в словарь

        return changedict


    #def get_bert_changes(self, words, article):
    #    """
    #    Creates a dict object to be later used for synonimization with Bert.
    #    :params:
    #        words, dict of strings:ints -- words that are to be changed and
    #        indices of sentences
    #
    #    :returns:
    #        changedict, dict, words (str): synonimns (str) -- dictionary to be used 
    #        for synonimization
    #    """
    #    changedict = {}
    #    closest_array = list(np.random.choice(np.array([self.closest, self.closest + 1, 
    #                                                    self.closest + 2]), size = int(len(words))))
    #    for pair, closest in zip(words.items(), closest_array):
    #        word, index = pair
    #        sentence = article[index]
    #        clear_sentence = list([comb.split()[0] for comb in sentence])
    #        raw_sentence = list([b.lower()+ ' ' if b.lower()!= word else '__'+b.lower()+'__ ' for b in clear_sentence])
    #        text_sentence = "".join(raw_sentence)
    #        #print('Step1')
    #        #print(word)
    #        #print(text_sentence)
    #        try:
    #            synonyms = self.model(text_sentence)
    #            #print('Step 2')
    #            #print(synonyms)
    #            for i in range(closest, closest+3):
    #                alt = synonyms[i][0]
    #                alt = alt.lower()
    #                if not alt.isalnum() or alt in self.stopwords:
    #                    if i == closest+2:
    #                        alt = word
    #                    else:
    #                        continue
    #                else:
    #                    break
    #                    
    #        except:
    #            alt = word
    #        #print('Step 3')
    #        #print(alt)
    #        changedict[word] = alt
    #    
    #    
    #    self.bert_changedict = changedict
    #    
    #    
    #    return changedict

    def get_bert_superdict(self, dataset):
        for i in range(len(dataset)):
            self.bert_superdict[i] = {}
            article = dataset[i]
            for j in range(len(article)):
                self.bert_superdict[i][j] = {}
                sentence = article[j]
                clear_sentence = list([comb.split()[0] for comb in sentence])
                for comb in sentence:
                    word, label = comb.split()
                    word = word.lower()
                    if word.isalnum() and word not in self.stopwords:
                        raw_sentence = list([b.lower()+ ' ' if b.lower()!= word else '__'+b.lower()+'__ ' for b in clear_sentence])
                        text_sentence = "".join(raw_sentence)
                        synonyms = self.model(text_sentence)
                        synonyms = list([pair[0].lower() for pair in synonyms])
                        synonyms += [word]
                        self.bert_superdict[i][j][word] = synonyms[:7]



    def synonimize(self, article, changedict):
        """
        Transform the article according to the previously constructed dictionary.
        :params:
            article, list of sentences, sentence is a list of strings 

            chagedict, dict, words (str) : synonyms (str) -- dictionary to be used for
            synonimization
            
        :returns:
            synonimized_article, list of sentences, sentence is a list of strings

        """
        
        #additional variable that holds labels that would NOT be changed
        
        labeltype = set()
        if self.label is not None:
            if self.label == 'neutral':
                labeltype.add('B-SPAN')
                labeltype.add('I-SPAN')
            elif self.label == 'propaganda':
                labeltype.add('0')
            
        #additional variable that holds parts of speech that would NOT be changed
        pos_shortcuts = {
        'NN': 'n',
        'JJ': 'adj',
        'RB': 'adv',
        'VB': 'v'
        }
        wordtypes = set()
        if self.postype is not None:
            wordtypes = {'n', 'adj', 'adv', 'v'}
            for fig in self.postype:
                wordtypes.discard(fig)
        
        synonimized_article = []
        for sentence in article:
            synonimized_sentence = []
            for comb in sentence:
                word, label = comb.split()
                word = word.lower()
                pos = nltk.pos_tag([word])[0][1]
                if pos in pos_shortcuts:
                    pos = pos_shortcuts[pos]
                if word in changedict and label not in labeltype and pos not in wordtypes and word not in self.stopwords:
                    new_word = changedict[word]
                else:
                    new_word = word
                new_comb = new_word + " " + label
                synonimized_sentence.append(new_comb)
            synonimized_article.append(synonimized_sentence)
        return synonimized_article


    def synonimize_sentence(self, sentence, changedict):
        """
        Transform the sentence according to the previously constructed dictionary.
        :params:
            sentence, a list of strings 

            chagedict, dict, words (str) : synonyms (str) -- dictionary to be used for
            synonimization
            
        :returns:
            synonimized_sentenc, list of strings

        """
        labeltype = set()
        if self.label is not None:
            if self.label == 'neutral':
                labeltype.add('B-SPAN')
                labeltype.add('I-SPAN')
            elif self.label == 'propaganda':
                labeltype.add('0')
            
        #additional variable that holds parts of speech that would NOT be changed
        pos_shortcuts = {
        'NN': 'n',
        'JJ': 'adj',
        'RB': 'adv',
        'VB': 'v'
        }
        wordtypes = set(self.postype)
        if self.postype is not None:
            wordtypes = {'n', 'adj', 'adv', 'v'}
            for fig in self.postype:
                wordtypes.discard(fig)
        
        
        synonimized_sentence = []
        for comb in sentence:
            word, label = comb.split()
            word = word.lower()
            pos = nltk.pos_tag([word])[0][1]
            if pos in pos_shortcuts:
                pos = pos_shortcuts[pos]
            trigger = np.random.binomial(1,self.word_percent)
            changetrigger = 0
            if word in changedict and label not in labeltype and pos not in wordtypes and word not in self.stopwords and trigger == 1:
                synonyms = changedict[word]
                np.random.shuffle(synonyms)
                for syn in synonyms:
                    new_word = syn
                    if not syn.isalnum() or syn in self.stopwords:
                        continue
                    else:
                        changetrigger = 1
                        break
                if changetrigger == 0:
                    new_word = word

            else:
                new_word = word
            new_comb = new_word + " " + label
            synonimized_sentence.append(new_comb)
        
        return synonimized_sentence




    def transform_article(self, article):
        """
        :params:
            article, article, list of sentences, sentences are lists of strings
            
        """
        if self.strat == 'keywords':
            words = self.get_keywords(article)
        else:
            words = self.get_words(article)

        if self.model_name == 'bert':
            changedict = self.get_bert_changes(words=words, article=article)
        else:
            changedict = self.get_changes(words = words)
    
        transformed_article = self.synonimize(article=article, changedict=changedict)
    
        return transformed_article


    def transform_dataset(self, dataset):
        """
        :params:
            dataset, list of articles, articles are list of sentences, 
            sentences are lists of strings   
        """        

        #производим замену

        dataset_new = []
        for i in range(self.num_copies):
            for article in dataset:
                new_article = self.transform_article(article=article)
                dataset_new.append(new_article)
        dataset_expanded = dataset + dataset_new
    
        return dataset_expanded


    def transform_dataset_bert(self, dataset):
        """
        :params:
            dataset, list of articles, articles are list of sentences, 
            sentences are lists of strings   
        """      
        dataset_new = []  
        for num_copy in range(self.num_copies):
            for i in range(len(dataset)):
                article = dataset[i]
                new_article = []
                for j in range(len(article)):
                    sentence = article[j]
                    changedict = self.bert_superdict[i][j]
                    new_sentence = self.synonimize_sentence(sentence=sentence, changedict=changedict)
                    new_article.append(new_sentence)
                dataset_new.append(new_article)
        dataset_expanded = dataset + dataset_new

        return dataset_expanded



        



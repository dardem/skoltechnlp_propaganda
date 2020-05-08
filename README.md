# SkoltechNLP Propaganda 2020 solution

Repository for SkoltechNLP team solving SemEval 2020 Task 11 "Detection of Propaganda Techniques in News Articles": https://propaganda.qcri.org/semeval2020-task11/

Our final submission is based on BERT for NER implementation from https://github.com/IINemo/bert_sequence_tagger.

## Tools
Main tools for
- tokenization;
- converting from character-level to token-level markup (CoNLL format);
- markup visualization.

## Article generation
Scripts for augemented data generation. Grid based on:
- models for verctor representations: Glove, Fasttext, BERT (https://github.com/uhh-lt/generative-ie);
- POS: for example, you can use nouns, adjectives, adverbs and verbs (n, adj, adv, v);
- classes: only propaganda class, only neutral, or both;
- times of data expansion: for example, the dataset can be increased in two (x2) or five (x5) times.

## Notebooks 
Here you can find example of markup visualization.

#!/usr/bin/python3
# -*- coding: utf-8 -*-

# nltk.download('stopwords')
# nltk.download('wordnet')

from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from leasingapi.models import LegalPosition
from nltk import ngrams
import string


class LegalPositionPreprocessor:
    """
    Class used to preprocess the legal positions data
    into a valuable information that is needed in
    our further execution of caluse number extraction process
    """

    def __init__(self, legal_position_id, *args, **kwargs):
        self.legal_position_instance = LegalPosition.objects.get(
            id=legal_position_id)
        self.descriptions = self.legal_position_instance.clause_name.order_by(
            'id')
        self.key_texts = self.legal_position_instance.text.order_by('id')
        self.meta_dict = {'descriptions': self.descriptions,
                          'key_texts': self.key_texts,
                          'preprocessed_descriptions': [],
                          'preprocessed_key_texts': []}
        self.locked = True

        # begin data preprocessing
        self.__preprocess_data__()

    def __preprocess_data__(self):
        """
        Internal/private method that will initiate
        the default functionality of this class
        it call other private and public methods
        the belongs to this class
        """
        self.__tokenize_data__()
        self.__normalize_data__()
        self.locked = False

    def __tokenize_data__(self):
        """
        function used for tokenization of clause name and
        key text of self.legal_position instance
        """
        # # closure definition begins
        # def remove_punctuation(input_string):
        #     """
        #     closure to remove the puntuation form the text
        #     and return a puntuation removed version of the
        #     input string
        #     """
        #     punctuations = string.punctuation
        #     no_punct = ""
        #     for char in input_string:
        #         if char not in punctuations:
        #             no_punct = no_punct + char
        #     return no_punct

        # closure ends and parent method block begins here
        temp_tokenized_descriptions = []
        temp_tokenized_key_texts = []
        for description in self.descriptions:
            temp_tokenized_description = {'tokens': [],
                                          "id": description.id,
                                          'n-grams': [],
                                          'N': None}
            temp_tokenized_description['tokens'] = word_tokenize(description.text)
            temp_tokenized_description['N'] = len(temp_tokenized_description['tokens'])
            temp_tokenized_description['n-grams'] = self.__get_ngrams__(temp_tokenized_description['tokens'])
            temp_tokenized_descriptions.append(temp_tokenized_description)

        for key_text in self.key_texts:
            temp_tokenized_key_text = {'tokens': [],
                                       'id': key_text.id,
                                       'n-grams': [],
                                       'N': None}
            temp_tokenized_key_text['tokens'] = word_tokenize(key_text.content)
            temp_tokenized_key_text['N'] = len(temp_tokenized_key_text['tokens'])
            temp_tokenized_key_text['n-grams'] = self.__get_ngrams__(temp_tokenized_key_text['tokens'])
            temp_tokenized_key_texts.append(temp_tokenized_key_text)

        self.meta_dict['preprocessed_key_texts'] = temp_tokenized_key_texts
        self.meta_dict['preprocessed_descriptions'] = temp_tokenized_descriptions

    def __normalize_data__(self):
        """
        function used to normalize the data
        using leminization
        """
        lem = WordNetLemmatizer()
        stop_words = set(stopwords.words("english"))
        for data in self.meta_dict['preprocessed_descriptions']:
            ext = [lem.lemmatize(word) for word in data['tokens'] if (not word in stop_words) and (not word in string.punctuation)]
            data['leminized_description'] = ext

        for data in self.meta_dict['preprocessed_key_texts']:
            ext = [lem.lemmatize(word) for word in data['tokens'] if (not word in stop_words) and (not word in string.punctuation)]
            data['leminized_key_text'] = ext

    def __get_ngrams__(self, tokenized_content):
        """
        Internal method used to associate the all feasible ngrams
        of the legalpostions key_texts and descriptions
        """
        min_n = 1
        max_n = len(tokenized_content)
        Ngrams = []
        for n in range(1, max_n + 1):
            grams = ngrams(tokenized_content, n)
            for gram in grams:
                print(gram)
                Ngrams.append(tuple([t.lower() for t in gram]))
        return Ngrams

    def get_data(self):
        """
        safe instance Method to return the data
        or self.meta_dict with Django models instance key/values removed
        """
        if not self.locked:
            return {'preprocessed_descriptions': self.meta_dict['preprocessed_descriptions'],
                    'preprocessed_key_texts': self.meta_dict['preprocessed_key_texts']}
        else:
            raise Exception("%s class instance is still processing. Please wait untill lock is released" % self.__class__.__name__)

"""
This file generate a sentimental analysis model class. it preprocess data, predict the sentiment of each data and return the label of the data in format 0 or 1 (respectfully, negative and positive)
"""

import pickle

import pandas as pd

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from nltk import pos_tag

nltk.download('averaged_perceptron_tagger_eng')
nltk.download("universal_tagset")

import re
import string

from lib import model_file_path, vector_file_path


class Model:
    
    def __init__(self):
        """
        retrieve and store model and vector trought pickle
        """

        pkfile = open(model_file_path, 'rb')
        vecfile = open(vector_file_path, 'rb')
        self.model = pickle.load(pkfile)
        self.vector = pickle.load(vecfile)

    def getModel(self):
        """
        return the model instance (already trained)
        """
        return self.model
    
    def predict(self, reviews) -> list:
        """
        return a list containing the sentiment analysis of the given data (in format 0 for neg and 1 for pos)
        must get a list of string as parameter
        """

        data = pd.DataFrame(reviews, columns=['Reviews'])
        tokenized = self.tokenizer(data)

        without_stopwords = self.stopwords_remover(tokenized)    
        without_punctuation = self.punctuation_remover(without_stopwords)    
        tagged_words = self.pos_tagger(without_punctuation)
        lemmatized_words = self.lemmatizer(tagged_words)

        # transform the comments column into a list. each of its element is a list of words
        list_of_rows = lemmatized_words.Reviews.tolist()
        text = [" ".join(str(elm) for elm in doc) for doc in list_of_rows] # concat the el of each inner list into a string  

        # encode the string into a vector based on existing vocabulary
        vectorized = self.vector.transform(text)        
        predictions = self.model.predict(vectorized.toarray())

        return predictions


    def tokenizer(self, dataset):
        """
        tokenise dataframe data and return the new dataframe
        must get a dataframe as parameter
        """
        new_dataset = dataset.copy(deep=True)
        new_dataset["Reviews"] = new_dataset.Reviews.map(lambda x: word_tokenize(x.lower() if isinstance(x, str) else str(x) ))
        return new_dataset

    def stopwords_remover(self, dataset):
        """
        Remove stopwords from dataframe data and return the new dataframe
        must get a dataframe as parameter
        """

        with open("data/stopwords.txt") as file:
            custom_stopwords = file.read().split(",")
            
        stop_words = set(stopwords.words('english') + custom_stopwords + ["footnote", "sidenote", "project", "gutenberg"])

        regex = r"^\w+$"

        dataset["Reviews"] = dataset.Reviews.map(lambda x: [word for word in x if (word not in stop_words and re.match(regex, word))])
        return dataset

    def punctuation_remover(self, dataset):
        """
        Remove punctuations from dataframe data and return the new dataframe
        must get a dataframe as parameter
        """
        punctuation = string.punctuation + "``" + "''" + "--" + "_" + "(" + ")" + '""' + "|" + "“" + "”" + "’" + "‘" + "___"
        dataset["Reviews"] = dataset.Reviews.map(lambda x: [word for word in x if word not in punctuation])
        return dataset

    def pos_tagger(self, dataset):
        """
        transform each data in the dataframe into a tuple containing the data and its nature
        must get a dataframe as parameter
        """

        dataset["Reviews"] = dataset.Reviews.map(lambda x: [tagged for tagged in pos_tag(x,tagset='universal') if tagged[1] not in ["NUM"] ])
        return dataset

    def lemmatizer(self, dataset):
        """
        Transform each data from dataframe in its base form and return the new dataframe. It does not store duplicate data
        must get a dataframe as parameter
        """

        lem = WordNetLemmatizer()
        dataset["Reviews"] = dataset.Reviews.map(lambda row: [ lem.lemmatize(word[0], pos = self.get_pos_tag(word[1])) for word in row ])
        return dataset    

    def get_pos_tag(self, pos):  
        """
        convert universal tagset to WordNetLemmatizer() format
        must get a string as parameter
        """

        match pos:
            case "NOUN":
                result = "n"
            case "VERB":
                result = "v"
            case "ADJ":
                result = "a"
            case "ADV":
                result = "r"
            case _:
                result = "s"
        return result
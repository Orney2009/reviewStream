import pickle
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from nltk import pos_tag
import re
import string
import numpy as np


class Model:
    
    def __init__(self):
        pkfile = open('data/models/model.pkl', 'rb')
        vecfile = open('data/models/vectorized.pkl', 'rb')
        self.model = pickle.load(pkfile)
        self.vector = pickle.load(vecfile)

    def getModel(self):
        return self.model
    
    def predict(self, reviews):
        data = pd.DataFrame(reviews, columns=['Reviews'])
        tokenized = self.tokenizer(data)
        without_stopwords = self.stopwords_remover(tokenized)    
        without_punctuation = self.punctuation_remover(without_stopwords)    
        tagged_words = self.pos_tagger(without_punctuation)
        lemmatized_words = self.lemmatizer(tagged_words)
        list_of_rows = lemmatized_words.Reviews.tolist()
        text = [" ".join(str(elm) for elm in doc) for doc in list_of_rows]        
        vectorized = self.vector.transform(text)        
        predictions = self.model.predict(vectorized.toarray())
        return predictions


    def tokenizer(self, dataset):
        new_dataset = dataset.copy(deep=True)
        new_dataset["Reviews"] = new_dataset.Reviews.map(lambda x: word_tokenize(x.lower() if isinstance(x, str) else str(x) ))
        return new_dataset

    def stopwords_remover(self, dataset):    
        with open("data/stopwords.txt") as file:
            custom_stopwords = file.read().split(",")
            
        stop_words = set(stopwords.words('english') + custom_stopwords + ["footnote", "sidenote", "project", "gutenberg"])

        regex = r"^\w+$"

        dataset["Reviews"] = dataset.Reviews.map(lambda x: [word for word in x if (word not in stop_words and re.match(regex, word))])
        return dataset

    def punctuation_remover(self, dataset):
        punctuation = string.punctuation + "``" + "''" + "--" + "_" + "(" + ")" + '""' + "|" + "“" + "”" + "’" + "‘" + "___"
        dataset["Reviews"] = dataset.Reviews.map(lambda x: [word for word in x if word not in punctuation])
        return dataset

    def pos_tagger(self, dataset):
        dataset["Reviews"] = dataset.Reviews.map(lambda x: [tagged for tagged in pos_tag(x,tagset='universal') if tagged[1] not in ["NUM"] ])
        return dataset

    def lemmatizer(self, dataset):
        lem = WordNetLemmatizer()
        dataset["Reviews"] = dataset.Reviews.map(lambda row: [ lem.lemmatize(word[0], pos = self.get_pos_tag(word[1])) for word in row ])
        return dataset    

    def get_pos_tag(self, pos):    
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
    


# test = Model()
# results = test.predict(["Avoid this movie at all costs, everything about it is bad", "I love it", "It's a great movie !"])

# for result in results:
#     print(result)
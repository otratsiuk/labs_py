import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class Search:
    def __init__(self):
        self.documents = []
        self.documents_clean = []
        self.links = []
        self.dataframe = pd.DataFrame
        self.vectorizer = TfidfVectorizer()

    def get_links(self):

        r = requests.get('https://www.freecodecamp.org/news')
        soup = BeautifulSoup(r.content, 'html.parser')

        for article in soup.find_all('article'):
            url = article.find('a', href=True)
            if url:
                self.link = url['href']
                self.links.append(str('https://www.freecodecamp.org') + str(self.link))


    def get_documents(self):
        for article in self.links:
            r = requests.get(article)
            soup = BeautifulSoup(r.content, 'html.parser')

            sen = []
            for i in soup.find_all("p"):
                sen.append(i.text)
            
            self.documents.append(' '.join(sen))    


    def clean_documents(self):
        for d in self.documents:
            # Remove Unicode
            document_test = re.sub(r'[^\x00-\x7F]+', ' ', d)
            # Remove Mentions
            document_test = re.sub(r'@\w+', '', document_test)
            # Lowercase the document
            document_test = document_test.lower()
            # Remove punctuations
            document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)
            # Lowercase the numbers
            document_test = re.sub(r'[0-9]', '', document_test)
            # Remove the doubled space
            document_test = re.sub(r'\s{2,}', ' ', document_test)
            self.documents_clean.append(document_test)   


    def create_dataframe(self):
        X = self.vectorizer.fit_transform(self.documents_clean)
        X = X.T.toarray()
        self.dataframe = pd.DataFrame(X, index=self.vectorizer.get_feature_names_out()) 
        print(self.dataframe)


    def prepare_texts(self):
        self.get_links()
        self.get_documents()
        self.clean_documents()
        self.create_dataframe()


    def get_similar_articles(self, query):
        print("query:", query)
        # Convert the query become a vector
        
        query = [query]
        q_vec = self.vectorizer.transform(query).toarray().reshape(self.dataframe.shape[0],)
        sim = {}

        # Calculate the similarity
        for i in range(25):
            sim[i] = np.dot(self.dataframe.loc[:, i].values, q_vec) / np.linalg.norm(self.dataframe.loc[:, i]) * np.linalg.norm(q_vec)
        
        # Sort the values 
        sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)

        for k, v in sim_sorted:
            if v != 0.0:
                return (v, self.links[k], self.documents[k])

        return None        

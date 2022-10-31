import math
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import nltk
from collections import Counter
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


nltk.download('stopwords')


class Search:
    def __init__(self):
        self.document_index = 0
        self.documents = []
        self.documents_clean = []
        self.sentences_clean = []
        self.sentence_tokens = []
        self.search_document_tokens = []
        self.search_document = ''
        self.search_document_sentences = []
        self.sentence_scores = {}
        self.key_words = {}
        self.links = []
        self.dataframe_sum = pd.DataFrame
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


    def get_sentences(self):
        self.search_document = self.search_document.split('If you read this far, tweet to the author to show them you care. Tweet a thanks', 1)[0]
        self.search_document_sentences = nltk.tokenize.sent_tokenize(self.search_document)


    def clean_sentences(self):
        self.stop_words = nltk.corpus.stopwords.words('english')
        self.stop_words.extend(['org', 'youtube', 'anil', 'freecodecamp', 'n'])
        self.stop_words = set(self.stop_words)
        sentences = self.clean_document(self.search_document_sentences) 
        for i in sentences:
            tokens = nltk.word_tokenize(i)
            tokens = [w for w in tokens if not w in self.stop_words]
            self.search_document_tokens.append(tokens)
            self.sentence_tokens.append(tokens)
            self.sentences_clean.append(" ".join(tokens))

        self.search_document_tokens = sorted(sum(self.search_document_tokens, [])) 


    def clean(self):
        self.documents_clean = []
        self.sentences_clean = []
        self.sentence_tokens = []
        self.search_document_tokens = []
        self.search_document = ''
        self.search_document_sentences = []
        self.dataframe_sum = pd.DataFrame
        self.sentence_scores = {}


    def summarizing_dataframe(self):
        self.dataframe_sum = pd.DataFrame(0, index=list(dict.fromkeys(self.search_document_tokens)), 
                        columns=(list(range(0, len(self.sentences_clean), 1))))
        print(self.dataframe_sum)                


    def word_frequency_in_sentence(self):
        for i in range(len(self.sentence_tokens)):
            freqs = Counter(self.sentence_tokens[i])
            for f in freqs.keys():
                self.dataframe_sum[i][f] = freqs[f]


    def word_frequency_in_text(self):
        freqs = Counter(self.search_document_tokens)
        self.dataframe_sum['document'] = 0
        self.dataframe_sum['max'] = self.dataframe_sum.values.max(1)

        for f in freqs.keys():
            self.dataframe_sum['document'][f] = freqs[f]    


    def sentences_score(self):
        self.sentence_scores = {}

        columns = self.dataframe_sum.columns.to_list()[:-2]
        db = self.dataframe.shape[1]
        df = pd.DataFrame(self.dataframe.astype(bool).sum(axis=1))
        
        for (sen, words) in self.dataframe_sum.iteritems():
            self.sentence_scores[sen] = 0
            words_in_sen = pd.DataFrame({'words': self.dataframe_sum.index.tolist(), 'freq': words.tolist()})
            words_in_sen = words_in_sen.set_index(['words'])

            for w in words_in_sen.index.tolist():
                tfSi = words_in_sen['freq'][w]
                tfD = self.dataframe_sum['document'][w]
                tfmaxD = self.dataframe_sum['max'][w]
                dft = df[0][w]
                self.sentence_scores[sen] += tfSi * 0.5 * (1 + tfD / tfmaxD) * math.log(db / dft)
            if sen == len(columns) - 1:
                break    


    def get_key_words(self):
        words = self.dataframe.index.tolist()
        freqs = self.dataframe[self.document_index]
        key_words = dict(zip(words, freqs))
        key_words = dict(sorted(key_words.items(), key=lambda item: item[1], reverse=True))
        
        return list(key_words.keys())[:7]


    def summarize(self):
        self.get_sentences()
        self.clean_sentences()
        self.summarizing_dataframe()
        self.word_frequency_in_sentence()
        self.word_frequency_in_text()
        self.sentences_score()
        self.get_key_words()

        self.sentence_scores = dict(sorted(self.sentence_scores.items(), key=lambda item: item[1], reverse=True))
        indexes = list(self.sentence_scores.keys())[:5]

        summarization = []
        for i in range(len(self.search_document_sentences)):
            if i in indexes:
                print(str(self.search_document_sentences[i]) + ' (' + str(self.sentence_scores[i]) + ' )')
                summarization.append(str(self.search_document_sentences[i]))

        return " ".join(str(x) for x in summarization)      


    def clean_document(self, document):
        clean = []
        for d in document:
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
            self.stop_words = nltk.corpus.stopwords.words('english')
            self.stop_words.extend(['org', 'youtube', 'anil', 'freecodecamp', 'n'])
            tokens = nltk.word_tokenize(document_test)
            tokens = [w for w in tokens if not w in self.stop_words]
            document_test = ' '.join(tokens)
            clean.append(document_test) 

        return clean      


    def create_dataframe(self):
        X = self.vectorizer.fit_transform(self.documents_clean)
        X = X.T.toarray()
        self.dataframe = pd.DataFrame(X, index=self.vectorizer.get_feature_names_out())
        print(self.dataframe) 


    def prepare_texts(self):
        self.get_links()
        self.get_documents()
        self.documents_clean = self.clean_document(self.documents)
        self.create_dataframe()


    def get_similar_articles(self, query):
        print("query:", query)
        query = [query]
        q_vec = self.vectorizer.transform(query).toarray().reshape(self.dataframe.shape[0],)
        sim = {}

        for i in range(self.dataframe.shape[1]):
            sim[i] = np.dot(self.dataframe.loc[:, i].values, q_vec) / np.linalg.norm(self.dataframe.loc[:, i]) * np.linalg.norm(q_vec)
        
        sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)

        for k, v in sim_sorted:
            if v != 0.0:
                self.search_document = self.documents[k]
                self.document_index = k
                return (v, self.links[k], self.documents[k])

        return None        

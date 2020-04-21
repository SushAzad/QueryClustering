from gensim.models import Word2Vec
from gensim.test.utils import common_texts, get_tmpfile
from sklearn.cluster import KMeans
from sklearn import preprocessing
import re
import nltk
import itertools
import numpy as np
import sys
import pandas as pd
import pickle
import csv

# get SQL keywords for embeddings
keywords=set()
with open('sql_reserved_words.csv') as words:
    reader = csv.reader(words)
    for row in reader:
        keywords.add(row[0])

def keywordize_query(query):
    t = nltk.word_tokenize(query)
    filtered=[]
    dic={}
    for w in t: 
        word=w.upper()
        if word in keywords:
            filtered.append(word)
            if word in dic:
                dic[word]+=1
            else:
                dic[word]=1
    
    # can also return dic for a dictionary with wordcounts 
    return filtered



def tokenize(ql):
    returning = []
    for contents in ql:
        lol = nltk.word_tokenize(contents)
        returning.append(lol)
    return returning

def get_document_embeddings(df, model, isTokenized = False):
    corpus = df['queryText'].str.lower().tolist()
    ids=df['queryID'].tolist()
    document_embeddings = []
    doc_emb = dict()
    non_vocab = set()
    for i,document in enumerate(corpus):
        word_counts = {}
#         document = document.decode('utf-8', 'ignore')
        if not isTokenized:
            # print("Since isToeknized parameter is not set, document is being tokenized by NLTK")
            document = nltk.word_tokenize(document)
        for word in document:
            if word not in word_counts:
                word_counts[word] = 0
            word_counts[word] += 1
        this_document_embeddings = np.zeros(100)
        total_words = 0 
        for word in word_counts:
#             print(word)
            try:
                this_document_embeddings += word_counts[word] * model.wv.__getitem__(word)
                total_words += word_counts[word]
            except KeyError:
                non_vocab.add(word)
        this_document_embeddings /= total_words
        document_embeddings.append(this_document_embeddings)
        doc_emb[ids[i]]=this_document_embeddings
    return document_embeddings, doc_emb, non_vocab


def createWordEmb(df, isTokenized=False):
    queries =  df['queryText'].str.lower().tolist()
    if not isTokenized:
        print("Since isToeknized parameter is not set, queries are being tokenized by NLTK")
        queries = tokenize(queries)
    qModel = Word2Vec(queries, size=100, window=5, workers=12, negative=0, hs=1, sample=1e-3)
    qModel.save("word2vecQueries.model")
    qModel.wv.save_word2vec_format("QueriesNon-embedded.txt", binary=False)
    print("Printing a random index2Word to check for garbage:", qModel.wv.index2word[90])
    phrasal = open("QueriesNon-embedded.txt", "r")
    vocab = []
    embeddings = []
    both = []
    new = []
    for idx, word in enumerate(qModel.wv.index2word):
            sentence = ""
            vocab.append(word)
            sentence += word+" "
            embeddings.append(qModel.wv.vectors[idx])
            for vector in qModel.wv.vectors[idx]:
                sentence += str(vector) + " "
            tup = (word, qModel.wv.vectors[idx])
            both.append(tup)
            new.append(sentence)
    m = open("FA19QueryEmbeddings.txt", "w")
    m.write(str(embeddings))
    n = open("FA19QueryPhraseEmbeddings.txt", "w")
    n.write(str(both))
    n = open("FormattedFA19Queries.txt", "w")
    n.write(str(new))
    return qModel

if (len(sys.argv) < 3):
	print("Please input a csv file to use i.e. python createEmbeddings.py [file] [True/False]. File needs queryText and queryID as cols. True or False indicates pre-tokenized input")
else:
    filename = sys.argv[1]
    df = pd.read_csv(filename)
    preTok = False
    if sys.argv[2] == "True" or sys.argv[2] == "true":
        preTok = True
    # Pass True as parameter to both functions below if queryText in df is tokenized.
    model = createWordEmb(df, preTok)
    doc_emb_list, doc_emb_dict, non_vocab = get_document_embeddings(df, model, preTok)
    with open('NewQueryEmbeddings.pickle', 'wb') as handle:
        pickle.dump(doc_emb_dict, handle)

    with open('data/non_vocab_words.csv', 'w') as outfile:
        writer = csv.writer(outfile)
        for row in list(non_vocab):
            writer.writerow(row)

    print("Embeddings have been written to NewQueryEmbeddings.pickle! All words that were not found in the vocabulary have been recorded in non_vocab_words.csv")
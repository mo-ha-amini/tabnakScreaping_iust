import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import math

def tokenize(allnews):
    tokens = []
    for news in allnews:
        words = [word for word in news.split(' ')]
        for word in words:
            word = word_clean(word)
            if word not in tokens and len(word)>1:
                tokens.append(word)
    tokens = set(tokens)
    # print(len(tokens))
    return tokens

def convert_news_to_array_of_tokrns(allnews):
    news_words = []
    for news in allnews:
        newsArr = []
        words = [word for word in news.split(' ')]
        for word in words:
            word = word_clean(word)
            if len(word) > 1:
                newsArr.append(word)
        news_words.append(newsArr)
    return news_words 

def word_clean(word):
    word = word.strip().translate({ord(i): None for i in '.،()؛؟!'})
    return word

def get_index_tokens(tokens ,word):
    tokens_index = {}
    for i, token in enumerate(tokens):
        tokens_index[token] = i
    return tokens_index[word]
    
def term_ferquecny(news_Arr, word):
    tf_arr = []
    for news in news_Arr:
        d_count = len(news)
        count_t_in_d = len([t for t in news if t == word])
        tf = count_t_in_d / d_count
        tf_arr.append(tf)
    return tf_arr

def inverse_doc_ferquency(news_Arr, word):
    N = len(news_Arr)
    df = 0
    for news in news_Arr:
        if word in news:
            df+=1
    idf = math.log((1+ N / df))
    return idf

def tf_idf(tokens, news_arr):
    tf_idf_arr = []
    for token in tokens:
        temp = [token]
        idf = inverse_doc_ferquency(news_arr, token)
        tfs = term_ferquecny(news_arr, token)
        for tf in tfs:
            tfidf = tf * idf
            temp.append(tfidf)
        tf_idf_arr.append(temp)
    print(tf_idf_arr)

def main():
    with open('textArr1.txt', 'r', encoding = 'utf-8') as f:
        allnews = f.read()
    allnews = [news for news in allnews.split('\n')]
    
    newsArr = convert_news_to_array_of_tokrns(allnews)
    tokens = tokenize(allnews)
    tf_idf(tokens, newsArr)

        
    # vectorizer = TfidfVectorizer()
    # X = vectorizer.fit_transform(allnews)
    # print(X)

main()
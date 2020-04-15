import pandas as pd
import sys, re
from tensorflow.python.keras.preprocessing import text


def is_response_tweet(tweet):
    return '@' in tweet

# load Wikipedia dataset
def load_wiki_data():
    train = pd.read_csv('data/toxic_train.csv')
    test = pd.read_csv('data/toxic_test.csv')
    X_train = train["comment_text"].fillna("fillna").values
    X_test = test["comment_text"].fillna("fillna").values
    y_train = train[["toxic"]].values

    return X_train, y_train, X_test


# load Twitter dataset
def load_twitter_data():
    twitter_df = pd.read_csv('data/sample_with_label.csv')
    twitter_text = twitter_df["TweetText"].fillna("fillna").values
    twitter_y = twitter_df["WasDeleted"].fillna("fillna").values

    return twitter_df, twitter_text, twitter_y

# initializes text tokenizer
def initialize_tokenizer(word_list, max_features=30000):
    tokenizer = text.Tokenizer(num_words=max_features)
    tokenizer.fit_on_texts(word_list)
    return tokenizer


# computes lists of n-grams for n=1,2,3
def get_ngrams(data, toxic_data):
    words = {}
    bigrams = {}
    trigrams = {}
    n = len(data)

    for i in range(n):
        s = data[i]
        tokens = [string for string in re.split('[\s\?!\.,():/]', s.lower()) if string != ""]
        for j in range(len(tokens)):
            word = tokens[j]
            if not word in words:
                words[word] = [0,0]
            words[word][1] += 1
            if toxic_data[i] == 1:
                words[word][0] += 1
            if j < (len(tokens) - 1):
                bigram = tokens[j] + ' ' + tokens[j+1]
                if not bigram in bigrams:
                    bigrams[bigram] = [0,0]
                bigrams[bigram][1] += 1
                if toxic_data[i] == 1:
                    bigrams[bigram][0] += 1
            if j < (len(tokens) - 2):
                trigram = tokens[j] + ' ' + tokens[j+1] + ' ' + tokens[j+2]
                if not trigram in trigrams:
                    trigrams[trigram] = [0,0]
                trigrams[trigram][1] += 1
                if toxic_data[i] == 1:
                    trigrams[trigram][0] += 1
        if i % 1000 == 0 or i == n-1:
            sys.stdout.write('\r')
            sys.stdout.write("Progress: %d / %d" % (i+1,n))
            sys.stdout.flush()
    return words, bigrams, trigrams

# computes n-gram frequencies
def get_frequencies(words, threshold):
    freqs = {}
    for word in words:
        if words[word][1] > threshold:
            freqs[word] = float(words[word][0])/words[word][1]
    return freqs
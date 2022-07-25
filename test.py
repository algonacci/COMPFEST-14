import tweepy
from dotenv import dotenv_values
import re
from nltk.tokenize import WordPunctTokenizer
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
import tqdm
from gensim.models import Word2Vec
import pandas as pd
import numpy as np

config = dotenv_values(".env")

consumer_key = config["consumer_key"]
consumer_key_secret = config["consumer_key_secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

tok = WordPunctTokenizer()
pat1 = r'@[A-Za-z0-9]+'
pat2 = r'https?://[A-Za-z0-9./]+'
pat3 = r'^RT[\s]+'
combined_pat = r'|'.join((pat1, pat2, pat3))


def tweet_cleaner(text):
    soup = BeautifulSoup(text, 'html.parser')
    souped = soup.get_text()
    stripped = re.sub(combined_pat, '', souped)
    try:
        clean = stripped.decode("utf-8").replace(u"\ufffd", "?")
    except:
        clean = stripped
    letters_only = re.sub("[^a-zA-Z]", " ", clean)
    lower_case = letters_only.lower()
    words = tok.tokenize(lower_case)
    return (" ".join(words)).strip()

username = input("Username: ")

tweets = api.user_timeline(screen_name=username, count=200, tweet_mode='extended')

list_of_tweets = []
for tweet in tweets:
    list_of_tweets.append(tweet.full_text)

cleaned_tweet = []
for tweet in list_of_tweets:
    cleaned_tweet.append(tweet_cleaner(tweet))

print(cleaned_tweet)

df = pd.DataFrame({
    'cleaned_tweet': cleaned_tweet
})

sentences = [word_tokenize(t) for t in df['cleaned_tweet']]

print(sentences[:5])

model = Word2Vec(sentences=sentences,
                 size=300,
                 window=20, 
                 min_count=2, 
                 workers=10,
                 iter=1000)

print(model.vector_size)
print(model.similar_by_word("model", topn=10))

words = list(model.wv.vocab)
print(words)

X=model[model.wv.vocab]

df=pd.DataFrame(X)
df.head()

X_corr=df.corr()
values,vectors=np.linalg.eig(X_corr)

args = (-values).argsort()
values = vectors[args]
vectors = vectors[:, args]

new_vectors=vectors[:,:2]

neww_X=np.dot(X,new_vectors)

import matplotlib.pyplot as plt
plt.figure(figsize=(13,7))
plt.scatter(neww_X[:,0],neww_X[:,1],linewidths=10,color='blue')
plt.title("Word Embedding",size=20)
plt.axis('off')
vocab=list(model.wv.vocab)
for i, word in enumerate(vocab):
  plt.annotate(word,xy=(neww_X[i,0],neww_X[i,1]))
plt.show()
import tweepy
from dotenv import dotenv_values
import re
from nltk.tokenize import WordPunctTokenizer
from bs4 import BeautifulSoup

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
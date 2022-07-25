import time
import re
from bs4 import BeautifulSoup
from gensim.models import Word2Vec
import tweepy
from dotenv import dotenv_values
from transformers import pipeline
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.tokenize import WordPunctTokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from xlwt import Workbook
from PIL import Image

plt.rcParams.update({
    "lines.color": "white",
    "patch.edgecolor": "white",
    "text.color": "white",
    "axes.facecolor": "black",
    "axes.edgecolor": "white",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "grey",
    "figure.facecolor": "black",
    "figure.edgecolor": "black",
    "savefig.facecolor": "black",
    "savefig.edgecolor": "black"})

config = dotenv_values(".env")

consumer_key = config["consumer_key"]
consumer_key_secret = config["consumer_key_secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

pretrained_name = "w11wo/indonesian-roberta-base-indolem-sentiment-classifier-fold-0"

stop_words = set(stopwords.words('indonesian'))
data = 'https://raw.githubusercontent.com/Braincore-id/stopwords_twitter_indo/main/stopwords_twitter.csv'
df_stopwords = pd.read_csv(data, names=['stopword'])
new_stopwords = []

for data in df_stopwords['stopword']:
    new_stopwords.append(data)
stop_words.update(new_stopwords)

english_stop_words = set(stopwords.words('english'))
stop_words.update(english_stop_words)

nlp = pipeline(
    "sentiment-analysis",
    model=pretrained_name,
    tokenizer=pretrained_name
)

le = LabelEncoder()


def analyze_sentiment(text):
    data = []
    predicted_label = []
    confidence = []

    for i in text:
        data.append(nlp(i))

    for my_list in data:
        for item in my_list:
            predicted_label.append(item["label"])
            confidence.append(item["score"])

    return predicted_label, confidence


def get_analysis(score):
    if score == 0:
        return 'Negative'
    else:
        return 'Positive'


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


def visualize_wordcloud(data, topic):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    visualize_wordcloud.wordcloud_visualization_filename = 'Topic_' + topic + '_' + timestamp
    text = str(data).replace("'", "")
    wordcloud = WordCloud(width=3000, height=2000,
                          font_path='C:\\Users\\Client\\Documents\\GitHub\\COMPFEST-14\\static\\font\\PlusJakartaSans-Regular.ttf',
                          max_words=200, colormap='Set3',
                          background_color="black",
                          stopwords=stop_words).generate(text)
    plt.figure(figsize=(15, 10), facecolor='k')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(fname='static/output/sentiment_analysis/topic/' +
                visualize_wordcloud.wordcloud_visualization_filename + '.png')


def visualize_wordcloud_username(data, username):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    visualize_wordcloud.wordcloud_visualization_filename = 'Username_' + \
        username + '_' + timestamp
    text = str(data).replace("'", "")
    wordcloud = WordCloud(width=3000, height=2000,
                          font_path='C:\\Users\\Client\\Documents\\GitHub\\COMPFEST-14\\static\\font\\PlusJakartaSans-Regular.ttf',
                          max_words=200, colormap='Set3',
                          background_color="black",
                          stopwords=stop_words).generate(text)
    plt.figure(figsize=(15, 10), facecolor='k')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(fname='static/output/sentiment_analysis/username/' +
                visualize_wordcloud.wordcloud_visualization_filename + '.png')


def visualize_sentiment_countplot(topic):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    visualize_sentiment_countplot.sentiment_countplot_filename = 'Sentiment_' + \
        topic + '_' + timestamp
    plt.figure(figsize=(15, 10), facecolor='k')
    plt.title('Sentiment Analysis {}'.format(topic), fontsize=40, pad=20)
    plt.xlabel('Sentiment', fontsize=30, labelpad=20)
    plt.ylabel('Count', fontsize=30, labelpad=20)

    # make a count plot using matplotlib
    sns.countplot(x=scraping_tweets_with_any_topic.sentiment,
                  data=scraping_tweets_with_any_topic.sentiment)

    plt.savefig(fname='static/output/sentiment_analysis/topic_sentiment/' +
                visualize_sentiment_countplot.sentiment_countplot_filename + '.png')


def visualize_sentiment_countplot_username(username):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    visualize_sentiment_countplot_username.sentiment_countplot_filename = 'Sentiment_Username_' \
        + username + '_' + timestamp
    plt.figure(figsize=(15, 10), facecolor='k')
    plt.title('Sentiment Analysis from {}'.format(
        username), fontsize=40, pad=20)
    plt.xlabel('Sentiment', fontsize=30, labelpad=20)
    plt.ylabel('Count', fontsize=30, labelpad=20)

    # make a count plot using matplotlib
    sns.countplot(x=scraping_tweets_from_user_account.sentiment,
                  data=scraping_tweets_from_user_account.sentiment)

    plt.savefig(fname='static/output/sentiment_analysis/user_sentiment/' +
                visualize_sentiment_countplot_username.sentiment_countplot_filename + '.png')


def scraping_tweets_with_any_topic(topic):
    user = []
    tweets = []
    likes = []
    followers = []
    retweets = []

    for tweet in tweepy.Cursor(api.search_tweets, q=topic, lang="id", tweet_mode='extended').items(100):
        user.append(tweet.user.screen_name)
        tweets.append(tweet.full_text)
        likes.append(tweet.favorite_count)
        followers.append(tweet.user.followers_count)
        retweets.append(tweet.retweet_count)

    print(tweets)

    predicted_label, confidence = analyze_sentiment(tweets)

    temporary_df = pd.DataFrame({
        'sentiment': le.fit_transform(predicted_label),
    })

    df = pd.DataFrame({"Username": user,
                       "Tweet": tweets,
                       "Likes": likes,
                       "Followers": followers,
                       "Retweets": retweets,
                       "Sentiment": temporary_df['sentiment'].apply(get_analysis),
                       "Confidence": confidence})

    scraping_tweets_with_any_topic.sentiment = df['Sentiment']
    scraping_tweets_with_any_topic.data_tweet = []

    for data in df['Tweet']:
        scraping_tweets_with_any_topic.data_tweet.append(tweet_cleaner(data))

    df_for_excel = df.copy()
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    scraping_tweets_with_any_topic.df_excel = df_for_excel.to_excel(
        'static/output/sentiment_analysis/excel/' + topic + '_' + timestamp + '.xlsx',
        index=False
    )
    scraping_tweets_with_any_topic.path_excel = 'static/output/sentiment_analysis/excel/' \
        + topic + '_' + timestamp + '.xlsx'

    scraping_tweets_with_any_topic.df = df.to_html(
        index=False, classes='table table-hover')
    return scraping_tweets_with_any_topic.df


def scraping_tweets_from_user_account(username):
    list_of_tweets = []

    tweets = api.user_timeline(
        screen_name=username, count=60, tweet_mode='extended')

    for tweet in tweets:
        list_of_tweets.append(tweet.full_text)

    cleaned_tweet = []

    for data in list_of_tweets:
        cleaned_tweet.append(tweet_cleaner(data))

    print(cleaned_tweet)

    predicted_label, confidence = analyze_sentiment(cleaned_tweet)

    temporary_df = pd.DataFrame({
        'sentiment': le.fit_transform(predicted_label),
    })

    df = pd.DataFrame({
        "Tweet": cleaned_tweet,
        "Retweets": [tweet.retweet_count for tweet in tweets],
        "Likes": [tweet.favorite_count for tweet in tweets],
        "Sentiment": temporary_df['sentiment'].apply(get_analysis),
        "Confidence": confidence
    })

    scraping_tweets_from_user_account.sentiment = df['Sentiment']
    scraping_tweets_from_user_account.data_tweet = df['Tweet']

    df_for_excel = df.copy()
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    scraping_tweets_from_user_account.df_excel = df_for_excel.to_excel(
        'static/output/sentiment_analysis/excel/' + username + '_' + timestamp + '.xlsx',
        index=False)
    scraping_tweets_from_user_account.path_excel = 'static/output/sentiment_analysis/excel/' \
         + username + '_' + timestamp + '.xlsx'

    df = df.to_html(index=False, classes='table table-hover')
    
    return df


def visualize_word_embedding(data, topic):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    visualize_word_embedding.word_embedding_filename = 'Word_Embedding_' + \
        topic + '_' + timestamp
    df = pd.DataFrame({
        'cleaned_tweet': data,
    })
    sentences = [word_tokenize(sent) for sent in df['cleaned_tweet']]
    print(sentences[:5])
    model = Word2Vec(sentences, size=100, window=5,
                     min_count=1, workers=4, seed=42,)
    words = list(model.wv.vocab)
    X = model[words]
    new_df = pd.DataFrame(X)
    X_corr = new_df.corr()
    values, vectors = np.linalg.eig(X_corr)
    args = (-values).argsort()
    values = vectors[args]
    vectors = vectors[:, args]
    new_vectors = vectors[:,:2]
    new_X = np.dot(X, new_vectors)

    plt.figure(figsize=(15, 10), facecolor='k')
    plt.scatter(new_X[:, 0], new_X[:, 1], s=100)
    plt.axis('off')
    vocab = list(model.wv.vocab)
    for i, word in enumerate(vocab):
        plt.annotate(word, xy=(new_X[i,0] ,new_X[i,1]))
    plt.savefig(fname='static/output/sentiment_analysis/word_embedding/' +
                visualize_word_embedding.word_embedding_filename + '.png')

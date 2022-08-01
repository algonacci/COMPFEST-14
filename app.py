import os
from flask import Flask, render_template, request, send_file
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
import locale
import utils.flight_fare_predictor as predictor
import utils.sentiment as sentiment
import utils.landmark_detection as ld
import warnings
import pandas as pd
warnings.filterwarnings('ignore')

app = Flask(__name__)

app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['DOWNLOAD_FOLDER'] = 'static/output/landmark_detection/downloads/'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')


def rupiah_format(number, with_prefix=False, decimal=0):
    locale.setlocale(locale.LC_NUMERIC, 'id_ID.utf8')
    rupiah = locale.format("%.*f", (decimal, number), True)
    if with_prefix:
        return "Rp. {}".format(rupiah)
    return rupiah


@app.route('/flight-fare-predictor', methods=['GET', 'POST'])
@cross_origin()
def flight_fare_predictor():
    if request.method == 'POST':
        output = predictor.flight_fare_prediction(request=request)
        get_data = request.form.to_dict()
        df = pd.DataFrame({
            'Departure Time': get_data['Dep_Time'].replace('T', ' '),
            'Arrival Time': get_data['Arrival_Time'].replace('T', ' '),
            'Source': get_data['Source'],
            'Destination': get_data['Destination'],
            'Total Transit': get_data['stops'],
            'Airline': get_data['airline']
        }, index=[0])
        table_data = df.to_html(index=False, classes='table table-hover')
        return render_template('flight-fare-predictor.html',
                               predicted_data=table_data,
                               predicted_price="Your flight price is Rp{}".format(rupiah_format(output)))
    else:
        return render_template('flight-fare-predictor.html')


@app.route('/sentiment-analysis')
@cross_origin()
def sentiment_analysis_page():
    return render_template('sentiment-analysis.html')


@app.route('/sentiment-analysis/topic', methods=['GET', 'POST'])
@cross_origin()
def topic_sentiment_analysis():
    if request.method == 'POST':
        topic = request.form['topic']
        if topic:
            table = sentiment.scraping_tweets_with_any_topic(topic=topic)
            cleaned_tweet = sentiment.scraping_tweets_with_any_topic.data_tweet
            sentiment.visualize_wordcloud(data=cleaned_tweet, topic=topic)
            wordcloud_plot = '../static/output/sentiment_analysis/topic/' + \
                sentiment.visualize_wordcloud.wordcloud_visualization_filename
            sentiment.visualize_sentiment_countplot(topic=topic)
            sentiment_countplot = '../static/output/sentiment_analysis/topic_sentiment/' + \
                sentiment.visualize_sentiment_countplot.sentiment_countplot_filename
            sentiment.visualize_word_embedding(data=cleaned_tweet, topic=topic)
            word_embedding = '../static/output/sentiment_analysis/word_embedding/' + \
                sentiment.visualize_word_embedding.word_embedding_filename
            return render_template('topic-sentiment-analysis.html',
                                   table=table, text='{}'.format(topic),
                                   wordcloud_plot=wordcloud_plot,
                                   sentiment_countplot=sentiment_countplot,
                                   word_embedding=word_embedding)
        else:
            return render_template('topic-sentiment-analysis.html', no_topic="Please enter a topic")
    else:
        return render_template('topic-sentiment-analysis.html')


@app.route('/sentiment-analysis/user', methods=['GET', 'POST'])
@cross_origin()
def user_sentiment_analysis():
    if request.method == 'POST':
        username = request.form['username']
        if username:
            table = sentiment.scraping_tweets_from_user_account(
                username=username)
            cleaned_tweet = sentiment.scraping_tweets_from_user_account.data_tweet
            sentiment.visualize_wordcloud_username(
                data=cleaned_tweet, username=username)
            wordcloud_plot = '../static/output/sentiment_analysis/username/' + \
                sentiment.visualize_wordcloud.wordcloud_visualization_filename
            sentiment.visualize_sentiment_countplot_username(username=username)
            sentiment_countplot = '../static/output/sentiment_analysis/user_sentiment/' + \
                sentiment.visualize_sentiment_countplot_username.sentiment_countplot_filename
            sentiment.visualize_word_embedding(
                data=cleaned_tweet, topic=username)
            word_embedding = '../static/output/sentiment_analysis/word_embedding/' + \
                sentiment.visualize_word_embedding.word_embedding_filename
            return render_template('user-sentiment-analysis.html',
                                   table=table, text='{}'.format(username),
                                   wordcloud_plot=wordcloud_plot,
                                   sentiment_countplot=sentiment_countplot,
                                   word_embedding=word_embedding)
        else:
            return render_template('topic-sentiment-analysis.html', no_topic="Please enter an username")
    else:
        return render_template('user-sentiment-analysis.html')


@app.route('/download_excel_user')
@cross_origin()
def download_excel_user():
    excel = sentiment.scraping_tweets_from_user_account.path_excel
    return send_file(excel, as_attachment=True)


@app.route('/download_excel_topic')
@cross_origin()
def download_excel_topic():
    excel = sentiment.scraping_tweets_with_any_topic.path_excel
    return send_file(excel, as_attachment=True)


@app.route('/landmark-detection', methods=['GET', 'POST'])
@cross_origin()
def landmark_detection():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            processed_image = ld.detect_landmark(image=file, filename=filename)
            return render_template('landmark-detection.html',
                                    label=ld.detect_landmark.label.replace('_', ' '),
                                    processed_image=processed_image)
    else:
        return render_template('landmark-detection.html')


@app.errorhandler(404)
@cross_origin()
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
@cross_origin()
def internal_server_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

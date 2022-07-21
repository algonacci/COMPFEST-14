from flask import Flask, render_template, request
from flask_cors import cross_origin
import locale
import utils
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)


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
        output = utils.flight_fare_prediction(request=request)
        return render_template('flight-fare-predictor.html',
                               predicted_price="Your flight price is Rp{}".format(rupiah_format(output)))
    else:
        return render_template('flight-fare-predictor.html')


@app.route('/sentiment-analysis')
@cross_origin()
def sentiment_analysis_page():
    return render_template('sentiment-analysis.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

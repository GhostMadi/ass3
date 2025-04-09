from flask import Flask, render_template, request, send_from_directory
from forecast_model import forecast_prices
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    coin = 'bitcoin'
    if request.method == 'POST':
        coin = request.form.get('coin')
    forecast_df = forecast_prices(coin_id=coin)
    return render_template('index.html', coin=coin.capitalize())

# Route to download the plot image
@app.route('/download')
def download_plot():
    return send_from_directory(os.getcwd() + '/static', 'plot.png', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
#http://localhost:5000

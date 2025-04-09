
import pandas as pd
import requests
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

def fetch_data(coin_id='bitcoin', days='365'):
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart'
    params = {'vs_currency': 'usd', 'days': days, 'interval': 'daily'}
    r = requests.get(url, params=params)
    data = r.json()
    prices = data['prices']
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('date', inplace=True)
    return df[['price']]

def forecast_prices(coin_id='bitcoin', forecast_days=265):
    df = fetch_data(coin_id)
    model = ARIMA(df['price'], order=(5, 1, 0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=forecast_days)

    future_dates = pd.date_range(df.index[-1] + pd.Timedelta(days=1), periods=forecast_days, freq='D')
    forecast_df = pd.DataFrame(forecast.values, index=future_dates, columns=['forecast_price'])

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(df['price'], label='Historical')
    plt.plot(forecast_df['forecast_price'], color='red', label='Forecast')
    plt.title(f'{coin_id.capitalize()} Price Forecast')
    plt.xlabel('Date')
    plt.ylabel('USD')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('static/plot.png')
    plt.close()

    return forecast_df
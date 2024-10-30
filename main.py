import requests
import pandas as pd
import plotly.express as px
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
import os

load_dotenv()

class CryptoDataFetcher:
    def __init__(self):
        self.api_url = 'https://api.coingecko.com/api/v3/'
        self.api_key = os.getenv('API_KEY')
        self.headers = {'x_cg_pro_api_key': self.api_key}

    def get_supported_cryptocurrencies(self):
        response = requests.get(f'{self.api_url}coins/list', headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('Failed to fetch cryptocurrency list.')

    def get_historical_data(self, coin_id, days=30):
        url = f'{self.api_url}coins/{coin_id}/market_chart'
        params = {'vs_currency': 'usd', 'days': days}
        response = requests.get(url, params=params, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            prices = data['prices']
            df = pd.DataFrame(prices, columns=['Timestamp', 'Price'])
            df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')
            return df
        else:
            raise Exception('Failed to fetch historical data.')

class CryptoTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-time Cryptocurrency Tracker")
        self.data_fetcher = CryptoDataFetcher()
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack()
        title_label = tk.Label(main_frame, text="Real-time Cryptocurrency Tracker", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)
        crypto_frame = tk.Frame(main_frame)
        crypto_frame.pack(pady=5)
        tk.Label(crypto_frame, text="Select Cryptocurrency:", font=("Helvetica", 12)).pack(side=tk.LEFT)
        self.crypto_var = tk.StringVar(value='Bitcoin')
        supported_coins = ['Bitcoin', 'Ethereum', 'Ripple', 'Litecoin', 'Cardano']
        tk.OptionMenu(crypto_frame, self.crypto_var, *supported_coins).pack(side=tk.LEFT)
        plot_button = tk.Button(
            main_frame,
            text="Show Price Trend",
            command=self.show_price_trend,
            font=("Helvetica", 12),
            relief="raised",
            activebackground="lightblue",
            padx=10, pady=5
        )
        plot_button.pack(pady=10)
        footer_label = tk.Label(self.root, text="Made by Yasin Oruc", font=("Helvetica", 10), fg="gray")
        footer_label.pack(side=tk.BOTTOM, pady=5)

    def show_price_trend(self):
        coin_id = self.crypto_var.get().lower()
        try:
            df = self.data_fetcher.get_historical_data(coin_id)
            fig = px.line(df, x='Date', y='Price', title=f'{coin_id.capitalize()} Price over Time')
            fig.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = CryptoTrackerApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()

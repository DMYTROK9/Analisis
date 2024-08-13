pip install matplotlib

import yfinance as yf
import matplotlib.pyplot as plt

# Download Tesla stock data
tesla_data = yf.download('TSLA', start='2020-01-01', end='2023-01-01')

# Reset the index
tesla_data.reset_index(inplace=True)

def make_graph(data, title):
    """
    Plots the closing price of stock data.

    Parameters:
    data (DataFrame): The stock data with 'Date' and 'Close' columns.
    title (str): The title for the graph.
    """
    plt.figure(figsize=(14, 7))
    plt.plot(data['Date'], data['Close'], label='Closing Price', color='b')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Closing Price (USD)')
    plt.grid(True)
    plt.legend()
    plt.show()

# Plot the graph for Tesla stock data
make_graph(tesla_data, 'Tesla Stock Closing Prices (2020-2022)')
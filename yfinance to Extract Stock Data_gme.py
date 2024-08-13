pip install yfinance

import yfinance as yf

# Download GameStop stock data
gme_data = yf.download('GME', start='2020-01-01', end='2023-01-01')

# Reset the index
gme_data.reset_index(inplace=True)

# Display the first five rows
print(gme_data.head())

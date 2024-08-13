pip install yfinance

import yfinance as yf

# Descargar los datos de Tesla
tesla_data = yf.download('TSLA', start='2020-01-01', end='2023-01-01')

# Restablecer el índice
tesla_data.reset_index(inplace=True)

# Mostrar las cinco primeras filas
print(tesla_data.head())
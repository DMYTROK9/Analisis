pip install requests
pip install beautifulsoup4

import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL de la página con los datos de ingresos de Tesla
url = 'https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue'

# Hacer una solicitud GET a la página web
response = requests.get(url)

# Parsear el contenido de la página
soup = BeautifulSoup(response.text, 'html.parser')

# Encontrar la tabla con los datos de ingresos
tables = soup.find_all('table')

# Buscar la tabla que contiene los ingresos
for table in tables:
    if 'Tesla Quarterly Revenue' in str(table):
        revenue_table = table
        break

# Extraer las filas de la tabla
rows = revenue_table.find_all('tr')

# Extraer los datos de las filas
data = []
for row in rows:
    cols = row.find_all('td')
    cols = [col.text.strip() for col in cols]
    if cols:
        data.append(cols)

# Crear un DataFrame de Pandas
tesla_revenue = pd.DataFrame(data, columns=['Date', 'Revenue'])

# Limpiar los datos: eliminar comas y signos de dólar, y convertir a numérico
tesla_revenue['Revenue'] = tesla_revenue['Revenue'].replace({'\$': '', ',': ''}, regex=True)
tesla_revenue['Revenue'] = pd.to_numeric(tesla_revenue['Revenue'], errors='coerce')

# Mostrar las cinco últimas filas
print(tesla_revenue.tail())
pip install requests
pip install beautifulsoup4

import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the webpage with GameStop revenue data
url = 'https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue'

# Make a GET request to the webpage
response = requests.get(url)

# Parse the webpage content
soup = BeautifulSoup(response.text, 'html.parser')

# Find all tables on the webpage
tables = soup.find_all('table')

# Search for the table containing revenue data
for table in tables:
    if 'GameStop Quarterly Revenue' in str(table):
        revenue_table = table
        break

# Extract all rows from the table
rows = revenue_table.find_all('tr')

# Extract the data from each row
data = []
for row in rows:
    cols = row.find_all('td')
    cols = [col.text.strip() for col in cols]
    if cols:
        data.append(cols)

# Create a Pandas DataFrame from the extracted data
gme_revenue = pd.DataFrame(data, columns=['Date', 'Revenue'])

# Clean the data: remove commas and dollar signs, and convert to numeric
gme_revenue['Revenue'] = gme_revenue['Revenue'].replace({'\$': '', ',': ''}, regex=True)
gme_revenue['Revenue'] = pd.to_numeric(gme_revenue['Revenue'], errors='coerce')

# Display the last five rows
print(gme_revenue.tail())
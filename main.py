import mechanicalsoup
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)

# 1 Grabbing Excel file directly and parsing
parcel_numbers = pd.read_excel("http://cosl.org/negexcel/BENTON.xls")['Parcel #']

# (or) 2 Loading the website and scraping
browser = mechanicalsoup.StatefulBrowser()
browser.open("http://cosl.org/postauctionlist.aspx?ID=BENT&CTY=BENT&CN=BENTON")
page = browser.get_current_page()
table = page.find("table", {"id": "GridView1"})
rows = table.find_all("tr")

parcel_list = []
for row in rows:
    cols = row.find_all("td")
    if len(cols) == 0:
        # Try to grab headers
        headers = [ele.text.strip() for ele in row.find_all('th')]
        continue  # No valid cells in this row (header row?)
    text = [ele.text.strip() for ele in cols]  # Get texts from elements
    parcel_list.append(text[5])

print(parcel_numbers)
print(parcel_list)

# Do searches using the data above on another website
# This website tracks state between pages so you need to navigate between the
# different pages before trying a search
browser = mechanicalsoup.StatefulBrowser()
# Go here https://www.arcountydata.com/county.asp?county=Benton&s=R
browser.open("https://www.arcountydata.com/county.asp?county=Benton&s=R")

# Then here /sponsored.asp
browser.open("https://www.arcountydata.com/sponsored.asp")

# Then fill out search_form
page = browser.get_current_page()

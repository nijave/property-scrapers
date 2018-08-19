import mechanicalsoup
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)

parcel_numbers = pd.read_excel("http://cosl.org/negexcel/BENTON.xls")['Parcel #']

browser = mechanicalsoup.StatefulBrowser()
browser.open("http://cosl.org/postauctionlist.aspx?ID=BENT&CTY=BENT&CN=BENTON")
page = browser.get_current_page()
table = page.find("table", {"id": "GridView1"})
rows = tbody.find_all("tr")

for row in rows:
    cols = row.find_all("td")
    if len(cols) == 0:
        continue  # No valid cells in this row (header row?)
    text = [ele.text.strip() for ele in cols]  # Get texts from elements
    print("ok")

print(browser)

browser = mechanicalsoup.StatefulBrowser()
# Go here https://www.arcountydata.com/county.asp?county=Benton&s=R
browser.open("https://www.arcountydata.com/county.asp?county=Benton&s=R")

# Then here /sponsored.asp
browser.open("https://www.arcountydata.com/sponsored.asp")

# Then fill out search_form
page = browser.get_current_page()
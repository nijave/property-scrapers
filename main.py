import mechanicalsoup
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)


# 1 Grabbing Excel file directly and parsing
parcels = pd.read_excel("http://cosl.org/negexcel/BENTON.xls")['Parcel #']

# (or) 2 Loading the website and scraping
browser = mechanicalsoup.StatefulBrowser(soup_config={'features': 'lxml'})
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
    parcel_list.append(text[4])

# Do searches using the data above on another website
# This website tracks state between pages so you need to navigate between the
# different pages before trying a search
# This might not work for multiple pages of results
browser = mechanicalsoup.StatefulBrowser()
# Go here https://www.arcountydata.com/county.asp?county=Benton&s=R
browser.open("https://www.arcountydata.com/county.asp?county=Benton&s=R")

# Then here /sponsored.asp
browser.open("https://www.arcountydata.com/sponsored.asp")

# Then fill out search_form
browser.select_form("#search_form")
params = {"Subdivision": "",
          "OBYIType": "",
          "occupancyType": "",
          "searchCounties": "",
          "ParcelNumberModifier": "begins",
          "ParcelNumber": "16-12473-000",
          "OwnerModifier": "starts",
          "OwnerName": "",
          "StreetNumber": "",
          "siteDirection": "",
          "StreetName": "",
          "City": "",
          "ParcelParcelType": "",
          "search": "Search"}

for k, v in params.items():
    browser[k] = v

browser.submit_selected("search")
table = browser.get_current_page().find("form", {"id": "parcel_report"}).find("table")
# Convert beautifulsoup resultset of links to "linkName linkAddress" items
parcel_links = ["%s %s" % (ele.text, ele.attrs["href"]) for ele in table.find_all('a')]

print("""
Parcels using Pandas:
{parcels}

Parcels using mechanicalsoup:
{parcel_list}

Parcel links:
{parcel_links}
""".format(parcels="\n".join(parcels.tolist()), parcel_list="\n".join(parcel_list), parcel_links="\n".join(parcel_links)))

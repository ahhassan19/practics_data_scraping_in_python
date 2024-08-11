import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

base_url = "https://www.ebay.com/sch/i.html?from=R40&_nkw=ear+buds&_sacat=0&_pgn="
page_num = 1
Names = []
Brands = []
Prices = []
Ships = []
Locations = []
Watchers = []
Links = []

# while True:
for i in range(1,3):
    print(f"Scraping Page {page_num}")
    url = base_url + str(page_num)
    print(url)
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        data = soup.find_all("div", {"class": "s-item__info clearfix"})
        
        for item in data:
            try:
                Name = item.find('h3', {"class": "s-item__title"}).text.strip()
                Names.append(Name)
            except:
                Names.append("")
                
            try:
                Brand = item.find('span', {"class": "s-item__dynamic"}).text.strip()
                Brands.append(Brand)
            except:
                Brands.append("")
                
            try:
                price = item.find('span', {"class": "s-item__price"}).text.strip()
                Prices.append(price)
            except:
                Prices.append("")
                
            try:
                ship = item.find('span', {"class": "s-item__shipping s-item__logisticsCost"}).text.strip()
                Ships.append(ship)
            except:
                Ships.append("")
                
            try:
                location = item.find('span', {"class": "s-item__location s-item__itemLocation"}).text.strip()
                Locations.append(location)
            except:
                Locations.append("")
                
            try:
                watch = item.find('span', {"class": "s-item__dynamic s-item__watchCount"}).text.strip()
                Watchers.append(watch)
            except:
                Watchers.append("")
                
            try:
                link = item.find('a', {"class": "s-item__link"})['href']
                Links.append(link)
            except:
                Links.append("")

        next_page = soup.find('a', {"class": "pagination__next"})
        if next_page:
            page_num += 1
            time.sleep(2)
        else:
            break
    else:
        break

# Save data to a CSV file
df = pd.DataFrame({
    'Name': Names,
    'Brand': Brands,
    'Price': Prices,
    'Shipping': Ships,
    'Location': Locations,
    'Watchers': Watchers,
    'Link': Links
})

df.to_csv("ebay.csv", index=False)

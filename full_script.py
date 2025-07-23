# Full Script Example (with CSV saving)
import requests
from bs4 import BeautifulSoup
import csv
import time

# Set Python output encoding
import sys
sys.stdout.reconfigure(encoding='utf-8')

base_url = "https://books.toscrape.com/"
page_url = "https://books.toscrape.com/catalogue/page-{}.html"

# Rating converter
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

# Prepare CSV file
with open("full_script.csv", "w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price", "Rating", "Stock", "Image URL", "Detail Link"])

    # Loop through pages 1 to 50
    for page in range(1, 51):
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        response = requests.get(url)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        books = soup.find_all("article", class_="product_pod")

        for book in books:
            # Title, Price & Stock
            title = book.h3.a["title"]
            price_text = book.find("p", class_="price_color").text
            price = float(price_text[1:])
            #price = float(price_text.replace("£", ""))  # Clean £
            stock = book.find("p", class_="instock availability").text.strip()
           
            # Rating
            rating_class = book.find("p", class_="star-rating")["class"]
            rating_word = rating_class[1]  # e.g., "Three"
            rating = rating_map.get(rating_word, 0)  # Convert to number

            # Image & Detail Link
            img_url = base_url + book.find("img")["src"].replace("../", "")
            link = base_url + "catalogue/" + book.h3.a["href"].replace("../", "")
            
            # Book image URL (add base_url)
            #img_src = book.find("img")["src"]
            #img_url = base_url + img_src.replace("../", "")
            # Book detail page link
            #partial_link = book.h3.a["href"]
            #book_url = base_url + "catalogue/" + partial_link.replace("../", "")
            
            #Write to CSV
            writer.writerow([title, price, rating, stock, img_url, link])


        print(f"✅ Page {page} scraped successfully")
        time.sleep(1)  # Be polite to the server

print("✅ All pages done. Data saved to all_books.csv")        
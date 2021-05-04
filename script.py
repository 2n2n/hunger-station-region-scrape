#! /usr/bin/python3
import argparse
import os
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="Scrape data from hunger station website.")
parser.add_argument('--output', default="./output", type=str, help="output path (default is output folder of current script location.)" )

args = parser.parse_args()

if os.path.exists(args.output) == False:
    os.makedirs(args.output)

# 1st pass. page 1
    # get the english version
    # get arabic version
# combine two arrays [...] [...]

locale = { 
    "en": "https://hungerstation.com/sa-en/regions?page=", 
    "ar": "https://hungerstation.com/sa-ar/المناطق?page="
} 

regions = []
for page in range(1,6):
    print('executing pass :' + str(page))
    page_regions = []
    websites = {
        "en": [],
        "ar": []
    }
    for lang in locale: 
        print("Scanning ", lang + str(page))
        websites[lang] = requests.get(locale[lang] + str(page))
        soup = BeautifulSoup(websites[lang].content, 'html.parser')
        results = soup.find_all('div', class_="Title-kEkEAm iQqayg")
        websites[lang] = [elem.text.strip() for elem in results]
    
    for idx, english_name in enumerate(websites["en"]):
        arabic_name = websites["ar"][idx]
        page_regions.append((english_name, arabic_name))
    
    regions = regions + page_regions

df = pd.DataFrame(regions)

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(args.output + "/" + 'cities.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Regions')

# Close the Pandas Excel writer and output the Excel file.
writer.save()


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

po = []
for page in range(5):
    print("Scanning ", "https://hungerstation.com/sa-en/regions?page="+str(page + 1))
    page = requests.get("https://hungerstation.com/sa-en/regions?page="+str(page + 1))
    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find_all('div', class_="Title-kEkEAm iQqayg")

    po = [elem.text.strip() for elem in results] + po

df = pd.DataFrame(po)

# # Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('cities.xlsx', engine='xlsxwriter')

# # Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Regions')

# # Close the Pandas Excel writer and output the Excel file.
writer.save()
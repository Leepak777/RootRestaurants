#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 11:09:29 2023

@author: kevinhua
"""

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json
import ssl
import urllib

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'} # set the headers
ssl._create_default_https_context = ssl._create_unverified_context

a = {}
x = {}

url = "https://www.ubereats.com/ca/city/vancouver-bc" 
req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
page = urlopen(req).read()
soup = BeautifulSoup(page, 'html.parser')

for restaurant in soup.findAll('h3'): # find the name of the restaurant
    name = restaurant.text.strip()
    print(name)
    delivery_info = restaurant.findNext('div')
    if delivery_info is not None:
        delivery_time = delivery_info.findNext('span').text
        delivery_time = delivery_time.replace("–"," to ")
        delivery_cost = delivery_info.text
        #print(delivery_time, delivery_cost)
        print(delivery_cost)
        
        a[name] = {
            #'Delivery Time' : delivery_time,
            name_location_rating, attributes = delivery.split("A top-rated restaurant with")
            name, location, rating = name_location_rating.split("(")
            rating = rating.strip(")")
            attributes = [a.strip() for a in attributes.split("•")]
        }
    else:
        print('Delivery information not found')
    print("\n")

x['restaurants'] = a

with open('final_result.json', 'w+', encoding='utf-8') as out: # writing the final file
    json.dump(x, out, indent=4, ensure_ascii=False)

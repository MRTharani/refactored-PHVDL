import asyncio
import requests
from bs4 import BeautifulSoup
import json
import time
import random 
from database import *
import logging
from config import * 


logging.basicConfig(level=logging.INFO)




def fetch_video_links():
    proxy_url = "https://cf-proxy.mrspidyxd.workers.dev/?host="
    base_url = "https://www.pornhub.com"
    url = ["https://www.pornhub.com","https://www.pornhub.com/video?o=mv","https://www.pornhub.com/video?o=ht","https://www.pornhub.com/video?o=tr","https://www.pornhub.com/video?o=cm"]
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(proxy_url+random.choice(url), headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    return [div.find('a', class_='thumbnailTitle')['href'].replace("https://cf-proxy.mrspidyxd.workers.dev",base_url).split("&")[0] for div in soup.find_all('div', class_='vidTitleWrapper') if div.find('a', class_='thumbnailTitle')]

#will convert into Channel Search
def search_video_links(query):
    base_url = "https://cf-proxy.mrspidyxd.workers.dev/?host="
    search_url = "https://www.pornhub.com/video/search?search="
    url = "https://www.pornhub.com"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(base_url + search_url + query, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    return [div.find('a', class_='thumbnailTitle')['href'].replace("https://cf-proxy.mrspidyxd.workers.dev", url).split("&")[0] for div in soup.find_all('div', class_='vidTitleWrapper') if div.find('a', class_='thumbnailTitle')]



def extract_urls(url):
    temp_file = "dump.txt"
    os.system(f"yt-dlp --flat-playlist -j {url} > {temp_file}")
    urls = []
    with open(temp_file) as file:
            for line in file:
                parts = line.strip().split()
                for i in range(len(parts)):
                    if '"url":' == parts[i]:
                        # Extract and write the URL to the output file
                        urls.append(parts[i + 1].strip('"",'))
    os.remove(temp_file)
    return urls    



def fetch_models():
    try:
        url = ["https://www.pornhub.com/pornstars?performerType=amateur#subFilterListVideos","https://www.pornhub.com/pornstars?o=mp&t=a&gender=female&performerType=amateur",'https://www.pornhub.com/pornstars?o=t#subFilterListVideos',"https://www.pornhub.com/pornstars?gender=female&performerType=amateur","https://www.pornhub.com/pornstars?gender=female","https://www.pornhub.com/pornstars?gender=female&performerType=pornstar","https://www.pornhub.com/pornstars?o=mv&performerType=pornstar#subFilterListVideos","https://www.pornhub.com/pornstars?performerType=amateur#subFilterListVideos","https://www.pornhub.com/pornstars?o=t&performerType=amateur#subFilterListVideos","https://www.pornhub.com/pornstars?o=r","https://www.pornhub.com/pornstars?o=ms#subFilterListVideos","https://www.pornhub.com/pornstars?o=ms&performerType=amateur"]
        base_url = "https://www.pornhub.com"
        response = requests.get(random.choice(url))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        hrefs = set(link.get('href') for link in soup.find_all('a') if link.get('href'))
        return random.sample([base_url+href for href in hrefs if "/model/" in href or "/pornstar/" in href or "/channel/" in href],5)
    except requests.RequestException as e:
        print(f"An error occurred: {e}")


def fetch_links():
  logging.info("Started link_gen")
  if True:
    urls = []
    for ph in fetch_models():
        logging.info(ph)
        urls.extend(extract_urls(ph))
    logging.info("Some Recommended Videos")
    urls.extend(fetch_video_links())
    length = len(urls)
    logging.info(f"Total Videos:{length}")
    if db is not None:
      data = get_raw_url()
      urls = [url for url in urls if url not in data]
    filtered = len(urls)
    logging.info(f"Filtered Videos:{filtered}")
    urls = random.sample(urls,100)
    return urls

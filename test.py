import requests
from bs4 import BeautifulSoup
# from flask import Flask, make_response, request, jsonify

from model import model

# animeName = model.predict_anime_by_name(name="date a live", return_only_titles=True)

# print(animeName[0])
# for i in animeName:
    # print()
images = []

word = "chainsaw man"
url = "https://www.google.com/search?q={0}&tbm=isch".format(word)
with requests.Session() as s:
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'lxml')
    product_links = [item.select_one('a')['href'] for item in soup.select('.product-wrapper') if item.select_one('[src]:not(.woocommerce-placeholder)')]

    for link in product_links:
            r = s.get(link)
            soup = BeautifulSoup(r.content, 'lxml')
            images.append(soup.select_one('[data-large_image]')['data-large_image'])
# images = soup.findAll('img')
# image = images[0]
# # print("compiler Complete")
print(images)

# image = []
# url = "https://www.google.com/search?q={0}&tbm=isch".format("chainsaw Man")
# images = BeautifulSoup(requests.get(url).content, 'lxml').findAll('img')
# image.append(images[1].get('src'))

# url = "https://www.google.com/search?q={0}&tbm=isch".format("Spy x Family Part 2")
# images = BeautifulSoup(requests.get(url).content, 'lxml').findAll('img')
# image.append(images[1].get('src'))

# url = "https://www.google.com/search?q={0}&tbm=isch".format("Mob Psycho 100 III")
# images = BeautifulSoup(requests.get(url).content, 'lxml').findAll('img')
# image.append(images[1].get('src'))

# url = "https://www.google.com/search?q={0}&tbm=isch".format("Boku no Hero Academia 6th Season")
# images = BeautifulSoup(requests.get(url).content, 'lxml').findAll('img')
# image.append(images[1].get('src'))

# url = "https://www.google.com/search?q={0}&tbm=isch".format("Bleach Senen Kessen-hen")
# images = BeautifulSoup(requests.get(url).content, 'lxml').findAll('img')
# image.append(images[1].get('src'))

# for i in image:
#     print(i)
# header_flex = [
#     {
#         "type": "image",
#         "originalContentUrl": image.get('src'),
#         "previewImageUrl": image.get('src')
#     }
# ]
# response = make_response(jsonify({'line_payload': header_flex}) , 200)
# response.headers['Response-Type'] = "object"
# print(response)
# for image in images:
#     print(image.get('src'))

# from serpapi import GoogleSearch
# search = GoogleSearch({
#     "q":"chainsaw man",
#     "location": "Thailand",
#     "tbm": "isch",#image
#     "ijn": "0",#page image
#     # "num": "1",
#     "api_key": "428305627c283cfdcab204064335e2443066df8f0b335949fcb8b15df4cdb57d"
# })
# result = search.get_dict()
# image_results = result["images_results"]
# # origin = image_results[0]["original"]
# print(image_results)

#https://gist.github.com/brickellis/a19dd7a5789f60fa5e3972047e0277e4
# import argparse
# import urllib
# import json

# def get_soup(url,header):
#     return BeautifulSoup(url,'html.parser')

# parser = argparse.ArgumentParser(description='Scrape Google images')
# parser.add_argument('-s', '--search', default='bananas', type=str, help='search term')
# parser.add_argument('-n', '--num_images', default=10, type=int, help='num images to save')
# parser.add_argument('-d', '--directory', default='/Users/gene/Downloads/', type=str, help='save directory')
# args = parser.parse_args()
# query = args.search#raw_input(args.search)
# max_images = args.num_images
# save_directory = args.directory
# image_type="Action"
# query= query.split()
# query='+'.join(query)
# url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
# header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
# soup = get_soup(url,header)
# ActualImages=[]# contains the link for Large original images, type of  image
# for a in soup.find_all("div",{"class":"rg_meta"}):
#     link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
#     ActualImages.append((link,Type))
# print(ActualImages)
from __future__ import print_function
from flask import Flask, make_response, request, jsonify
import numpy as np

import requests
from bs4 import BeautifulSoup

import model.model as model

app = Flask(__name__)

@app.route("/")
def home():
     return "helloworld"

@app.route("/genre",  methods=["GET"])
def genre():
     #!separate with , and
     genre = request.args.get("genre")
     more = request.args.get("more")
     exits = request.args.get("exit")


     genre_check = model.vectorize_classes(model.tokenizer(input=genre))
     if(np.count_nonzero(genre_check) == 0):
          # wrong output
          header_flex ={ [
               
                    {
                         "type":"text",
                         "text": "ไม่พบการค้นหา "+ genre +" ค่ะ"
                    },
                    {
                         "type":"text",
                         "text": "กรุณาใส่ใหม่อีกครั้งค่ะ"
                    }
          ]
                    }
          response = make_response(jsonify({'line_payload': header_flex}) , 200)
          response.headers['Response-Type'] = "object"
     elif(np.count_nonzero(genre_check) != 0):

          if (more == None):
               more = 0
          elif(exits != None):
               print("แล้วเจอกันนะคะ")
               exit()
          else :
               more = int(more)
               more *= 5

          predict = model.predict(genre_check, return_only_titles=True, n=15)

          image = []
          for i in range(5):
               url = "https://www.google.com/search?q={0}&source=lnms&tbm=isch".format(predict[i + more])
               images = BeautifulSoup(requests.get(url).content, 'lxml').findAll('img')
               image.append(images[1].get('src'))
          
     
          header_flex = [     
               {
               "type": "template",
               "altText": "this is a image carousel template",
               "template": {
               "type": "image_carousel",
               "columns": [
               {
                    "imageUrl": image[0],
                    "action": {
                         "type": "postback",
                         "label": "Detail",
                         "data": predict[0+ more]
               }
               },
               {
                    "imageUrl": image[1],
                    "action": {
                         "type": "postback",
                         "label": "Detail",
                         "data": predict[1+ more]
               }
               },
               {
                    "imageUrl":  image[2],
                    "action": {
                         "type": "postback",
                         "label": "Detail",
                         "data": predict[2+ more]
               }
               },
               {
                    "imageUrl":  image[3],
                    "action": {
                         "type": "postback",
                         "label": "Detail",
                         "data": predict[3+ more]
               }
               },
               {
                    "imageUrl":  image[4],
                    "action": {
                         "type": "postback",
                         "label": "Detail",
                         "data": predict[4 + more]
               }
               }
          ]
          }
          },
                {
                         "type":"text",
                         "text": "ผลการค้นหา "+ genre +" ค่ะ"
                    }
          ]
     

         
     response = make_response(jsonify({'line_payload': header_flex}) , 200)
     response.headers['Response-Type'] = "object"

     return response

#Seasonal anime plaintext
@app.route("/anichan", methods=["GET"])
def anichan():
     seasonal = ["chainsaw Man", "Spy x Family Part 2", "Mob Psycho 100 III", "Boku no Hero Academia 6th Season", "Bleach Senen Kessen-hen"]
     more = request.args.get("more")

     
     if more == None:
          more = 0

     image = []
     link = []
     for i in range(5):
          url = "https://www.google.com/search?q={0}&tbm=isch".format(seasonal[i])
          images = BeautifulSoup(requests.get(url).content, 'html.parser').findAll('img')
          image.append(images[1].get('src'))

     header_flex = [     
          {
     "type": "template",
     "altText": "this is a image carousel template",
     "template": {
     "type": "image_carousel",
     "columns": [
          {
               "imageUrl": image[0],
               "action": {
                    "type": "postback",
                    "label": "Detail",
                    "data": seasonal[0]
          }
          },
          {
               "imageUrl": image[1],
               "action": {
                    "type": "postback",
                    "label": "Detail",
                    "data": seasonal[1]
          }
          },
          {
               "imageUrl":  image[2],
               "action": {
                    "type": "postback",
                    "label": "Detail",
                    "data": seasonal[2]
          }
          },
          {
               "imageUrl":  image[3],
               "action": {
                    "type": "postback",
                    "label": "Detail",
                    "data": seasonal[3]
          }
          },
          {
               "imageUrl":  image[4],
               "action": {
                    "type": "postback",
                    "label": "Detail",
                    "data": seasonal[4]
          }
          }
     ]
     }
     }
     ]
     
     response = make_response(jsonify({'line_payload': header_flex}) , 200)
     response.headers['Response-Type'] = "object"
     return response


@app.route("/aniname", methods=["GET"])
def name():
     name = request.args.get("name")
     more = request.args.get("more")
     if(more == None):
          more = 0
     else:
          more = int(more)
          more *= 5

     predict = model.predict_anime_by_name(name=name, return_only_titles=True, n=15)
     print("more Is:",more)

     image = []
     for i in range(5):
          url = "https://www.google.com/search?q={0}&tbm=isch".format(predict[i + more])
          images = BeautifulSoup(requests.get(url).content, 'lxml').findAll('img')
          image.append(images[1].get('src'))

          
     header_flex = [     
               {
               "type": "template",
               "altText": "this is a image carousel template",
               "template": {
               "type": "image_carousel",
               "columns": [
               {
                    "imageUrl": image[0],
                    "action": {
                         "type": "postback",
                         "label": "Detail",
                         "data": predict[0+ more]
               }
               },
               {
                    "imageUrl": image[1],
                    "action": {
                         "type": "postback",
                         "label": "Detail",
                         "data": predict[1+ more]
               }
               },
               {
                    "imageUrl":  image[2],
                    "action": {
                         "type": "postback",
                         "label": "Detail",
                         "data": predict[2+ more]
               }
               },
               {
                    "imageUrl":  image[3],
                    "action": {
                         "type": "postback",
                         "label": "Detail",
                         "data": predict[3+ more]
               }
               },
               {
                    "imageUrl":  image[4],
                    "action": {
                         "type": "postback",
                         "label": "Detail",
                         "data": predict[4 + more]
               }
               }
          ]
          }
          },
           {
                         "type":"text",
                         "text": "ผลการค้นหา เรื่องที่ใกล้เคียง "+ name +" มากที่สุดค่ะ"
                    }
          ]
     
     response = make_response(jsonify({'line_payload': header_flex}) , 200)
     response.headers['Response-Type'] = "object"

     return response



if __name__ == "__main__":
     app.run(port=5000)
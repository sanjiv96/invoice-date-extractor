#!flask/bin/python

'''
@author: Sanjiv Purohit

This is python flask based REST Server to parse the invoice images and extract the transaction date.  
This server uses Google Cloud Vision API for text detection  and dateutil to validate the extracted dates. 

'''
from flask import Flask, abort, jsonify
from flask import request
from google.cloud import vision
import base64
import re
import dateutil.parser
    
app = Flask(__name__)

# POST method accepts json content base_64_image_content . 
@app.route('/extract_date', methods=['POST'])
def extract_date():
    if not request.json or not 'base_64_image_content' in request.json:
        # No Key found in payload
        abort(400)

    # creating Google Client  
    client = vision.ImageAnnotatorClient()
    data = base64.b64decode(request.json['base_64_image_content'])
    image = vision.types.Image(content=data)
    response = client.text_detection(image=image)
    date_string = 'null'

    # date extraction and validation
    for text in response.text_annotations:
        print (text.description)
        patn = re.compile(r'[\d|\w]+[/|\-|.|\\][\d|\w]+[/|\-|.|\\]\d+')
        matches = patn.findall(text.description)
        # find the first match of the date 
        for match in matches:
            try:
                date = dateutil.parser.parse(match, dayfirst=True)
                date_string = str(date).split()
                date_string = date_string[0]
                break
            except ValueError:
                pass
        break

    # get response
    return jsonify({'date': date_string}), 201

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)

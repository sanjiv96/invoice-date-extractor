# -*- coding: utf-8 -*-
"""
@author Sanjeev
The client file to encode image to base64 format and make post request to the 
Rest server endpoint  
"""
import requests
import base64
url = 'http://44.225.44.65:5000/extract_date'
image_path = "Add full path of image here"
with open(image_path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    myobj = {"base_64_image_content": encoded_string}       
    x = requests.post(url, json=myobj)
    print(x.content)     

#!/usr/bin/python3
import requests
import json

def printContent(request):
  print(json.dumps(r.json(), indent=3))

r = requests.get("http://127.0.0.1:5000/")
r.status_code           # Should be 200
r.json()                # The json body of the request as a Python dictionary
printContent(r)         # Prints the json body of the request
r.headers               # A dictionary of the provided headers

## Write your code in what follows. You can include comments describing what you are doing.

## NUMBER 1
## This block of code uses GET requests to pull our list of users,
## and then pulls out the correct user that we want.
user = requests.get("http://127.0.0.1:5000/user")
user_dict = user.json()
temp_url = user_dict['users'][0]['link']
recip_address = user_dict['users'][0]['username']
url = "http://127.0.0.1:5000/" + temp_url
user = requests.get(url)

## NUMBER 2
data = {"first": "Benedict", "last": "Cumberbatch"}
url = "http://127.0.0.1:5000/user"
user_post = requests.post(url, json = data)
header = user_post.headers['Location']

## NUMBER 3
data = {"text": "The Imitation Game", "recipient" : recip_address}
r = requests.post(header + "/message", json = data)
print(r.text)
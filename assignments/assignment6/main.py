from flask import Flask, request, make_response, json, url_for, abort
from db import Db   # See db.py
import utils

app = Flask(__name__)
db = Db()
app.debug = True # Comment out when not testing
app.url_map.strict_slashes = False   # Allows for a trailing slash on routes

#### ERROR HANDLERS

@app.errorhandler(500)
def server_error(e):
   return make_json_response({ 'error': 'unexpected server error' }, 500)

@app.errorhandler(404)
def not_found(e):
   return make_json_response({ 'error': e.description }, 404)

@app.errorhandler(403)
def forbidden(e):
   return make_json_response({ 'error': e.description }, 403)

@app.errorhandler(400)
def client_error(e):
   return make_json_response({ 'error': e.description }, 400)


#### MAIN ROUTES

@app.route('/', methods = ['GET'])
def bucket_list():
   pass

@app.route('/<bucketId>', methods = ['GET'])
def bucket_contents(bucketId):
   pass

@app.route('/', methods = ['POST'])
def bucket_create():
   pass

@app.route('/<bucketId>', methods = ['PUT'])
def bucket_create_with_id(bucketId):
   pass

@app.route('/<bucketId>', methods = ['DELETE'])
def bucket_delete(bucketId):
   pass

@app.route('/<bucketId>/<hash>', methods = ['GET'])
def shortcut_get_link(bucketId, hash):
   pass

@app.route('/<bucketId>/<hash>', methods = ['PUT'])
def shortcut_create_with_hash(bucketId, hash):
   pass

@app.route('/<bucketId>', methods = ['POST'])
def shortcut_create(bucketId):
   pass

@app.route('/<bucketId>/<hash>', methods = ['DELETE'])
def shortcut_delete(bucketId, hash):
   pass


## Helper method for creating JSON responses
def make_json_response(content, response = 200, headers = {}):
   headers['Content-Type'] = 'application/json'
   return make_response(json.dumps(content), response, headers)



# Starts the application
if __name__ == "__main__":
   app.run()
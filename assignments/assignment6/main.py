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
   buckets = db.getBuckets()
   return make_json_response({
      "buckets": [
         {
            "link": url_for('bucket_contents', link=bucket.link),
            "description": bucket.description
         }
         for bucket in buckets
      ]
   })

@app.route('/<bucketId>', methods = ['GET'])
def bucket_contents(bucketId):
   password = getPasswordFromQuery()
   bucket = getBucketAndCheckPassword(bucketId, password)
   return make_json_response({
      "id": bucket.id,
      "link": url_for('bucket_contents'),
      "description": bucket.description,
      "shortcuts": [
         {
            "linkHash": shortcut.linkHash,
            "link": url_for('shortcut_get_link', link=shortcut.link),
            "description": shortcut.description
         } 
         for shortcut in bucket.shortcuts
      ]
   })

@app.route('/', methods = ['POST'])
def bucket_create():
   pass

@app.route('/<bucketId>', methods = ['PUT'])
def bucket_create_with_id(bucketId):
   checkBucketIdAvailable(bucketId)
   password = getPasswordFromContents()
   passHash = utils.getHash(password) 
   description = checkForDescription()
   db.addBucket(bucketId, description, passHash)
   db.commit()
   headers = { "Location": url_for('bucket_contents', id=bucketId) }
   return make_json_response({ 'ok': 'bucket created' }, 201, headers)

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



## HELPER METHODS FOR BUCKET_CONTENTS
# Check if password is in the args of the request
def getPasswordFromQuery():
   if "password" not in request.args:
      abort(403, 'must provide a password parameter')
   return request.args["password"]

# Check if bucket exists and password is correct 
# returns bucket object if everything is correct
def getBucketAndCheckPassword(bucketId, password = None):
   if bucketId is None:
      return None
   bucket = db.getBucket(bucketId)
   if bucket is None:
      abort(404, 'unknown bucketId')
   passHash = utils.getHash(password)
   if password is not None and bucket.passwordHash != passHash:
      abort(403, 'incorrect password')
   return bucket



## HELPER METHODS FOR BUCKET_CREATE_WITH_ID
def checkBucketIdAvailable(bucketId):
   bucket = db.getBucket(bucketId)
   if bucket is not None:
      abort(403, 'bucketId already exists')

def getPasswordFromContents():
   contents = request.get_json()
   if "password" not in contents:
      abort(403, 'must provide a password field')
   return contents["password"]

def checkForDescription():
   contents = request.get_json()
   if "description" in contents:
      description = contents["description"]
   else:
      description = None
   return description


# Starts the application
if __name__ == "__main__":
   app.run()
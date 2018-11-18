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
            "link": url_for('bucket_contents', bucketId=bucket.id),
            "description": bucket.description
         }
         for bucket in buckets
      ]
   })

@app.route('/<bucketId>', methods = ['GET'])
def bucket_contents(bucketId):
   bucket = getBucketandCheckPassword(bucketId)
   return make_json_response({
      "id": bucket.id,
      "link": url_for('bucket_contents', bucketId=bucket.id),
      "description": bucket.description,
      "shortcuts": [
         {
            "linkHash": shortcut.linkHash,
            "link": url_for('shortcut_get_link', bucketId=bucket.id, hash=shortcut.linkHash),
            "description": shortcut.description
         }
         for shortcut in bucket.shortcuts
      ]
   })

@app.route('/', methods = ['POST'])
def bucket_create():
   bucketId = utils.makeId()
   return bucket_create_with_id(bucketId)

@app.route('/<bucketId>', methods = ['PUT'])
def bucket_create_with_id(bucketId):
   checkBucketIdAvailable(bucketId)
   password = getPasswordFromContents()
   passHash = utils.getHash(password)
   description = getDescriptionFromContents()
   db.addBucket(bucketId, passHash, description)
   db.commit()
   headers = { "Location": url_for('bucket_contents', bucketId=bucketId) }
   return make_json_response({ 'ok': 'bucket created' }, 201, headers)

@app.route('/<bucketId>', methods = ['DELETE'])
def bucket_delete(bucketId):
   bucket = getBucketandCheckPassword(bucketId)
   db.deleteBucket(bucket)
   db.commit()
   return make_json_response({}, 204)

@app.route('/<bucketId>/<hash>', methods = ['GET'])
def shortcut_get_link(bucketId, hash):
   shortcut = checkShortcut(bucketId, hash)
   headers = { "Location": shortcut.link }
   return make_json_response({
      "hash": hash,
      "link": shortcut.link,
      "description": shortcut.description
   }, 307, headers)

@app.route('/<bucketId>/<hash>', methods = ['PUT'])
def shortcut_create_with_hash(bucketId, hash):
   bucket = checkBucketId(bucketId)
   checkIfHashInUse(bucket, hash)
   password = getPasswordFromContents()
   passHash = utils.getHash(password)
   if password is not None and bucket.passwordHash != passHash:
      abort(403, 'incorrect password')
   description = getDescriptionFromContents()
   link = getLinkFromContents()
   db.addShortcut(hash, bucket, link, description)
   db.commit()
   headers = { "Location": url_for('shortcut_get_link', bucketId=bucketId, hash=hash) }
   return make_json_response({ 'ok': 'shortcut created' }, 201, headers)


@app.route('/<bucketId>', methods = ['POST'])
def shortcut_create(bucketId):
   hash = utils.makeId()
   return shortcut_create_with_hash(bucketId, hash)

@app.route('/<bucketId>/<hash>', methods = ['DELETE'])
def shortcut_delete(bucketId, hash):
   bucket = checkBucketId(bucketId)
   shortcut = checkShortcut(bucketId, hash)
   password = getPasswordFromQuery()
   passHash = utils.getHash(password)
   if password is not None and bucket.passwordHash != passHash:
      abort(403, 'incorrect password')
   db.deleteShortcut(shortcut)
   db.commit()
   return make_json_response({}, 204)



## HELPER METHODS

## Helper method for creating JSON responses
def make_json_response(content, response = 200, headers = {}):
   headers['Content-Type'] = 'application/json'
   return make_response(json.dumps(content), response, headers)

# Check if bucket exists, password is correct, and returns bucket object
# Returns proper error codes if any issues noticed in the request
def getBucketandCheckPassword(bucketId):
   bucket = checkBucketId(bucketId)
   password = getPasswordFromQuery()
   passHash = utils.getHash(password)
   if password is not None and bucket.passwordHash != passHash:
      abort(403, 'incorrect password')
   return bucket

# Small function that checks if the requests bucketId exists, if it doesn't, returns None or 404
def checkBucketId(bucketId):
   if bucketId is None:
      return None
   bucket = db.getBucket(bucketId)
   if bucket is None:
      abort(404, 'unknown bucketId')
   return bucket

# Checks if the bucketId is available and returns 403 if it already exists
def checkBucketIdAvailable(bucketId):
   bucket = db.getBucket(bucketId)
   if bucket is not None:
      abort(403, 'bucketId already exists')

# Check if a password was given in the request, returns 403 if no password given
def getPasswordFromQuery():
   if "password" not in request.args:
      abort(403, 'must provide a password parameter')
   return request.args["password"]

# Checks if password exists in contents, returns 403 if password isn't provided
# If password is provided, returns the password
def getPasswordFromContents():
   contents = request.get_json()
   if contents == None or "password" not in contents:
      abort(403, 'must provide a password field')
   return contents["password"]

# Checks if "description" in contents and either returns the given description
# or returns None if no description found
def getDescriptionFromContents():
   contents = request.get_json()
   if "description" in contents:
      description = contents["description"]
   else:
      description = None
   return description

# Checks if link is in given contents.
# If no link given, returns 403 stating error
def getLinkFromContents():
   contents = request.get_json()
   if "link" in contents:
      link = contents["link"]
   else:
      abort(403, 'must provide link in request')
   return link

# Checks if shortcut exists in the given bucket, returns 404 if shortcut not found
# If shortcut is found, returns the shortcut object
def checkShortcut(bucketId, hash):
   bucket = checkBucketId(bucketId)
   shortcut = db.getShortcut(hash, bucket)
   if shortcut == None:
      abort(404, 'shortcut does not exist')
   return shortcut

# Check for existing shortcut with given hash and bucket
# If one exists, return 403 indicating hash is already used
def checkIfHashInUse(bucket, hash):
   shortcut = db.getShortcut(hash, bucket)
   if shortcut != None:
      abort(403, 'hash is already used')

# Starts the application
if __name__ == "__main__":
   app.run()
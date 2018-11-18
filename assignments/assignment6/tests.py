from main import app, db
from utils import makeId, getHash
import json

session = db.session

BUCKET_ID = makeId()
BUCKET_PASSWORD = "myPassword"
PASSWORD_HASH = getHash(BUCKET_PASSWORD)
SHORTCUT_HASH = "mountains"
LINK = "https://en.wikipedia.org/wiki/List_of_mountains_by_elevation"
DESCR = "List of mountains by elevation"

print("################    DB TESTS   ###################")
# Provided DB tests
## No buckets to begin with
assert(len(db.getBuckets()) == 0)
## Adding a bucket
db.addBucket(id=BUCKET_ID, passwordHash = PASSWORD_HASH)
assert(len(db.getBuckets()) == 1)
bucket = db.getBucket(BUCKET_ID)
assert(bucket is not None)
assert(bucket.id == BUCKET_ID)
assert(bucket.passwordHash == PASSWORD_HASH)
assert(db.getBucket(BUCKET_ID + "bah") is None)
assert(db.getBuckets()[0] is bucket)
db.commit()
## Deleting the bucket
db.deleteBucket(bucket)
bucket = db.getBucket(BUCKET_ID)
assert(bucket is None)
db.commit()
## Re-adding the bucket to use in further tests
bucket = db.addBucket(id=BUCKET_ID, passwordHash = PASSWORD_HASH)
## Adding a shortcut
shortcut = db.addShortcut(SHORTCUT_HASH, bucket, LINK, DESCR)
assert(shortcut is not None)
assert(shortcut.linkHash == SHORTCUT_HASH)
assert(shortcut.bucket is bucket)
assert(shortcut.link == LINK)
assert(shortcut.description == DESCR)
assert(len(bucket.shortcuts) == 1)
assert(bucket.shortcuts[0] is shortcut)
assert(shortcut.bucket is bucket)
## Testing shortcut get
assert(db.getShortcut(SHORTCUT_HASH, bucket) is shortcut)
assert(db.getShortcut("Boo", bucket) is None)
db.commit()
## Testing shortcut delete
db.deleteShortcut(shortcut)
assert(db.getShortcut(SHORTCUT_HASH, bucket) is None)
shortcut = db.addShortcut(SHORTCUT_HASH, bucket, LINK, DESCR)
db.commit()
# ADD YOUR DB TESTS HERE
# OR USE THESE LINES TO JUST ADD MORE BUCKETS AND/OR SHORTCUTS TO THE DATABASE


print("################ DB TESTS DONE ###################")
# Provided API tests
print("################   API TESTS   ###################")

# ADD YOUR API TESTS HERE
client = app.test_client()
def get_json(r):
   return json.loads(r.get_data().decode("utf-8"))

# Testing existing bucket
r = client.get('/')
assert(r.status_code == 200)
contents = get_json(r)
assert("buckets" in contents)
assert(len(contents["buckets"]) == 1)
assert(BUCKET_ID in contents["buckets"][0]["link"])
bucket_link = contents["buckets"][0]["link"]
r = client.get(bucket_link + "bah")
assert(r.status_code == 404)
r = client.get(bucket_link)
assert(r.status_code == 403)
r = client.get(bucket_link, query_string={ "password": BUCKET_PASSWORD + "boo" })
assert(r.status_code == 403)
r = client.get(bucket_link, query_string={ "password": BUCKET_PASSWORD })
assert(r.status_code == 200)
contents = get_json(r)
for field in ["id", "link", "description", "shortcuts"]:
   assert(field in contents)
assert(contents["id"] == BUCKET_ID)
assert(BUCKET_ID in contents["link"])
shortcutList = contents["shortcuts"]
assert(len(shortcutList) == 1)
shortcutJSON = shortcutList[0]
for field in ["linkHash", "link", "description"]:
   assert(field in shortcutJSON)
assert(SHORTCUT_HASH == shortcutJSON["linkHash"])
assert(SHORTCUT_HASH in shortcutJSON["link"])
assert(DESCR == shortcutJSON["description"])
link = shortcutJSON["link"]

# Creating a new bucket via a put
r = client.put('/' + BUCKET_ID)
assert(r.status_code == 403)
r = client.put('/myBucket')
assert(r.status_code == 403)
r = client.put('/myBucket', data=json.dumps({ "description": "woohoo" }), content_type='application/json')
assert(r.status_code == 403)
r = client.put('/myBucket', data=json.dumps({ "password": "foo", "description": "woohoo" }), content_type='application/json')
assert(r.status_code == 201)
assert("Location" in r.headers)
assert("myBucket" in r.headers["Location"])
# Second time must fail
r = client.put('/myBucket', data=json.dumps({ "password": "foo", "description": "woohoo" }), content_type='application/json')
assert(r.status_code == 403)

# Creating new buckets via post
r = client.post('/', data=json.dumps({ "password": "foobar", "description": "yo" }), content_type='application/json')
assert(r.status_code == 201)
assert("Location" in r.headers)
newBucketLocation = r.headers["Location"]
r = client.get(newBucketLocation, query_string={ "password": "foobar" })
assert(r.status_code == 200)

# Second time will just create a new bucket
r = client.post('/', data=json.dumps({ "password": "fizz", "description": "yo" }), content_type='application/json')
assert(r.status_code == 201)
assert("Location" in r.headers)
newBucketLocation2 = r.headers["Location"]
assert(newBucketLocation != newBucketLocation2)

# Deleting the two extra buckets
r = client.delete(newBucketLocation + "yo")
assert(r.status_code == 404)
r = client.delete(newBucketLocation)
assert(r.status_code == 403)
r = client.delete(newBucketLocation, query_string={ "password": "foobar" })
assert(r.status_code == 204)
# Deleting the same bucket twice fails
r = client.delete(newBucketLocation, query_string={ "password": "foobar" })
assert(r.status_code == 404)

# Getting a shortcut link
r = client.get('/' + BUCKET_ID + '/false' + shortcut.linkHash)
assert(r.status_code == 404)
r = client.get('/' + BUCKET_ID + '/' + shortcut.linkHash)
assert(r.status_code == 307)
assert("Location" in r.headers)
assert(shortcut.link == r.headers["Location"])
contents = get_json(r)
for field in ["hash", "link", "description"]:
   assert(field in contents)
assert(contents["hash"] == SHORTCUT_HASH)
assert(contents["link"] == LINK)
assert(contents["description"] == DESCR)

# Putting a new link in, link required
r = client.put('/' + BUCKET_ID + '/wiki', data=json.dumps({
       "description": "The wikipedia home page",
       "password": BUCKET_PASSWORD
   }), content_type='application/json')
assert(r.status_code == 403)

# Expecting bucket password
r = client.put('/' + BUCKET_ID + '/wiki', data=json.dumps({
      "link": "https://www.wikipedia.org", "description": "The wikipedia home page"
   }), content_type='application/json')
assert(r.status_code == 403)

# This one works
r = client.put('/' + BUCKET_ID + '/wiki', data=json.dumps({
      "link": "https://www.wikipedia.org",
      "description": "The wikipedia home page",
      "password": BUCKET_PASSWORD
   }), content_type='application/json')
assert(r.status_code == 201)
assert("Location" in r.headers)
r = client.get(r.headers["Location"])
assert(r.status_code == 307)
assert("Location" in r.headers)
assert("https://www.wikipedia.org" == r.headers["Location"])
# This one works
r = client.post('/' + BUCKET_ID, data=json.dumps({
      "link": "https://www.wikipedia.org",
      "description": "The wikipedia home page",
      "password": BUCKET_PASSWORD
   }), content_type='application/json')
assert(r.status_code == 201)
assert("Location" in r.headers)
shortcutLocation = r.headers["Location"]
r = client.get(shortcutLocation)
assert(r.status_code == 307)
assert("Location" in r.headers)
assert("https://www.wikipedia.org" == r.headers["Location"])

# Deleting
r = client.delete(shortcutLocation)
assert(r.status_code == 403)
r = client.delete(shortcutLocation, query_string={ "password": BUCKET_PASSWORD+"NOT" })
assert(r.status_code == 403)
r = client.delete(shortcutLocation, query_string={ "password": BUCKET_PASSWORD })
assert(r.status_code == 204)
r = client.delete(shortcutLocation, query_string={ "password": BUCKET_PASSWORD })
assert(r.status_code == 404)

print("################ API TESTS DONE ##################")
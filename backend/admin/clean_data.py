import firebase_admin
import firebase_admin.auth
import firebase_admin.db
import firebase_admin.storage

'''
Check list:
[X] Delete all created users 
[X] Delete all data in database except for jobs data
[X] Delete all files in storage
'''

cred = firebase_admin.credentials.Certificate("../config/firebase-credential.json")
firebase_admin.initialize_app(cred, {
  'databaseURL': 'https://ds307-jobrecommendation.asia-southeast1.firebasedatabase.app',
  # 'databaseAuthVariableOverride': {
  #   'uid': "5e28547a-c340-4b0d-bd90-896554f8d580"
  # }
})

# Delete all created users
auth = firebase_admin.auth
users = auth.list_users()
for user in users.users:
  print("Deleting user:", user.uid, user.email)
  auth.delete_user(user.uid)
print("Deleted all users")

# Delete all data in database except for jobs data
COLLECTIOINS_TO_CLEAR = ["cv", "cv_data", "cv_file_info", "recommendations", "sessions", "users"]
for collection in COLLECTIOINS_TO_CLEAR:
  ref = firebase_admin.db.reference(collection)
  print("Deleting all data in:", collection)
  ref.delete()
print("Deleted all data except jobs data in database")

# Delete all files in storage
BUCKETS_TO_CLEAR = ["users", "cv"]
storage = firebase_admin.storage
bucket = storage.bucket("ds307-jobrecommendation.firebasestorage.app")
blobs = bucket.list_blobs()
for blob in blobs:
  print("Deleting file:", blob.name)
  blob.delete()
print("Deleted all files in storage")

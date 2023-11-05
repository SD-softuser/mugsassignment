import uvicorn
import firebase_admin
import pyrebase
import json
 
from firebase_admin import credentials, auth
from firebase_admin import firestore
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

cred = credentials.Certificate('user-management-system_service_account_keys.json')
firebase = firebase_admin.initialize_app(cred)
db = firestore.client()
pb = pyrebase.initialize_app(json.load(open('firebase_config.json')))
app = FastAPI()
allow_all = ['*']
app.add_middleware(
   CORSMiddleware,
   allow_origins=allow_all,
   allow_credentials=True,
   allow_methods=allow_all,
   allow_headers=allow_all
)
 
# signup endpoint
@app.post("/signup", include_in_schema=False)
async def signup(request: Request):
   req = await request.json()
   email = req['email']
   password = req['password']
   username = req['username'] 
   fullname = req['fullname']  
   data = {'username': username, 'fullname': fullname, 'email':email, 'createdDtm':firestore.SERVER_TIMESTAMP} 
   if email is None or password is None:
       return HTTPException(detail={'message': 'Error! Missing Email or Password'}, status_code=400)
   try:
       user = auth.create_user(
           email=email,
           password=password
       )
       db.collection("users").document(user.uid).set(data)
       return JSONResponse(content={'message': f'Successfully created user {user.uid}'}, status_code=200)    
   except:
       return HTTPException(detail={'message': 'Error Creating User'}, status_code=400)

# login endpoint
@app.post("/login", include_in_schema=False)
async def login(request: Request):
   req_json = await request.json()
   email = req_json['email']
   password = req_json['password']
   try:
       user = pb.auth().sign_in_with_email_and_password(email, password)
       jwt = user['idToken']
       return JSONResponse(content={'token': jwt}, status_code=200)
   except:
       return HTTPException(detail={'message': 'There was an error logging in'}, status_code=400)

# update endpoint
@app.put("/update", include_in_schema=False)
async def update(request: Request):
    req_json = await request.json()
    jwt = req_json.get('token')  # Get the JWT token from the request
    new_email = req_json.get('new_email')
    new_username = req_json.get('new_username')
    new_fullname = req_json.get('new_fullname')
    
    try:
        user = auth.verify_id_token(jwt)
        uid = user['uid']


        if new_email:
            auth.update_user(uid, email=new_email)
            db.collection("users").document(uid).update({'email':new_email})


        if new_username:
            db.collection("users").document(uid).update({'username':new_username})

        if new_fullname:
            db.collection("users").document(uid).update({'fullname':new_fullname})

        return JSONResponse(content={'message': 'User updated successfully'}, status_code=200)
    except Exception as e:
        error_message = str(e)
        if 'USER_NOT_FOUND' in error_message:
            return HTTPException(detail={'message': 'User not found'}, status_code=404)
        elif 'INVALID_PASSWORD' in error_message:
            return HTTPException(detail={'message': 'Invalid password'}, status_code=401)
        else:
            print(error_message)
            return HTTPException(detail={'message': 'Error updating user'}, status_code=400)

# ping endpoint
@app.post("/ping", include_in_schema=False)
async def validate(request: Request):
   headers = request.headers
   jwt = headers.get('authorization')
   print(f"jwt:{jwt}")
   user = auth.verify_id_token(jwt)
   return user["uid"]
 
if __name__ == "__main__":
   uvicorn.run("main:app")
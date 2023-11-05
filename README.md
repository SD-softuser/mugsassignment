# mugsassignment - User management system using firebase authentication and firestore database
##### This repository contains basic user management system where you can: 
- register (create user)
- login (retrive user)
- update (update user)
- delete (delete user)

----------------------------------------------------------------

### Setup:

##### first create firebase project : 

1. go to firebase console click on "Add Project"
2. give project name as "user-management-system" and then click on continue
3. Enable google analytics and click on continue and then select "Default Account for firebase". 
4. Click on "Create Project" now you are done with firebase project creation. 

##### Set up firebase authentication : 
1. Click on the Authentication tab that is present on the screen. 
2. Click on get started in sign-in method for now just select Email/Password from Native provider section. 
3. Enable the Email/Password and click on save.  

##### Add Firebase to your web app :
1. go side bar on the top beside project overview their is one gear button click on that and select project settings. 
2. in project settings scroll down and select web (html tag) icon. 
3. give any nickname name to your project and click on register app and then it will ask for the npm or script tag ignore for now and just click on continue to console.

##### Setting up project on local machine with some installation :
1. To run an app built on FastAPI locally, we will also need an asynchronous server gateway interface (ASGI), and we’ll use uvicorn as suggested in the docs. To get the packages you’ll need to build a basic FastAPI app, run pip install fastapi uvicorn in your terminal.

```
pip install fastapi uvicorn
```

2. To install the Google Firebase SDK and the Python wrapper to work with it, run pip install pyrebase4 firebase-admin. It is very important that you install pyrebase4 and not pyrebase which will install pyrebase 3. You will get a SyntaxError in the RSA.py file if you use pyrebase 3.

```
pip install pyrebase4 firebase-admin
```
##### creating firebase-config.json and [project name]_service_account_keys.json :
1. go to project settings and scroll down. You should now see an image like the one below. Copy the config below and save it as firebase_config.json. You will also need to add a line that says ”databaseURL”: “” because the Python SDK looks for it.
2. Once you have this file saved locally, scroll back up the page and go to the “Service accounts” tab. Choose Python to see the example code to load your credentials. Click “Generate new private key” to get your admin keys. Save this file locally as [project name]_service_account_keys.json and move it into your project root directory.

##### now clone this project to your local directory where you have stored previous two json files.  

```
git clone https://github.com/SD-softuser/mugsassignment.git
```

##### in terminal inside project directory run project using following command.  

```
uvicorn main:app --reload
```
this will start your app on http://127.0.0.1:8000 

##### now before we test our api endpoints lets create a firestore database to store our user data.
1. go firebase project overview and beside authentication tab you will see cloud store or you can go to build tab present on the side bar and click on Firestore database both are same. 
2. click on the create database button then click on next then select the start in test mode and click on enable button.

now we are good to go for api testing. 

##### to test our api endpoints ensure that our project is running. 
1. open Postman create new request past our home url and add our signup route and set the method to POST. 
```
http://127.0.0.1:8000/signup
```
2. now go to body tag and select raw and from dropdown select JSON 
3. in content field place this json object and click on send button
```
{
  "email": "test@gmail.com",
  "password":"12345pass", 
  "username":"testusername", 
  "fullname":"test fullname"
}
```
4. this will create our user in firestore as well as the in authentication. and you will get a response successfully created user with user id from firebase auth. 
5. you can also go to firebase console and check that user is created successfully in authentication as well as firestore database. 
6. now change the route to 
```
http://127.0.0.1:8000/login
```
and change the json object to get the jwt token form firebase for user authentication. 
```
{
  "email": "test@gmail.com",
  "password":"12345pass"
}
```
this will return the jwt token as response on successful login. 
7. Lets check our update endpoint similarly create new request and set the request method to PUT this time, and change the route to 
```
http://127.0.0.1:8000/update
```
and change the json object to (remember to update the token as per the instructions)
```
{
  "token": "copy the token from the login route where you got the token as response",
 "new_username":"testupdateusername",
 "new_email":"testupdate@gmail.com"
}
```
this will give you response message "user updated successfully" on successful execution and you will be able to see the updated user information in the database. 
8. Now let's check our delete endpoint to delete the user from the database set the request method to DELETE and then change route to 
```
http://127.0.0.1:8000/delete
```
in headers choose header as Authentication and value as jwt token and then simply click  on the send button on success full deletion it will give the response as "user deleted successfully". 

In this way we have simply implemented the user management using firebase authentication and firestore database. 

if you face any issues fill free to connect with me on 
linkedIn : https://www.linkedin.com/in/sanyog-mahajan-8288a7204/
email : sayogdmahajan@gmail.com

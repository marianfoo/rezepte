import secrets
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from BasicAuth import BasicAuth
import json
from dbClass import DBClass
from instagram import instagram
from googleAPI import GoogleAPI
from generateSite import GenerateSite
#Fast API
app = FastAPI()
security = HTTPBasic()
basicAuth = BasicAuth()
#Custom Classes
db = DBClass()
insta = instagram()
googleAPI = GoogleAPI()
generateSite = GenerateSite()

@app.get("/")
async def root(auth: BasicAuth = Depends(basicAuth) ):
    return {"message": "Hello World"}


@app.get("/post/{permalink}")
async def read_post(permalink: str = Depends(basicAuth)):
    return db.getPost(permalink)

@app.get("/triggerBuild")
async def triggerBuild(auth: BasicAuth = Depends(basicAuth) ):
    instagram_data = insta.load_instagram_data()
    metadata = googleAPI.get_google_sheets_data()
    generateSite.generate_posts(instagram_data, metadata)


import secrets
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from BasicAuth import BasicAuth
import json
from dbClass import DBClass
from instagram import instagram
from googleAPI import GoogleAPI
from generatesite import GenerateSite
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

@app.get("/posts")
async def read_post(permalink: str = Depends(basicAuth)):
    return db.tablePosts.all()

@app.get("/triggerBuild")
async def triggerBuild(auth: BasicAuth = Depends(basicAuth) ):
    instagram_data = db.tablePosts.all()
    metadata = googleAPI.get_google_sheets_data()
    generateSite.generate_posts(instagram_data,metadata)

@app.get("/readInstagramPosts")
async def readInstagramPosts(auth: BasicAuth = Depends(basicAuth) ):
    metadata = googleAPI.get_google_sheets_data()
    insta.load_instagram_data(db, db.tablePosts, metadata)
    return {"message": "Instagram Posts loaded"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
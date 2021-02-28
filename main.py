import secrets
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from basic_auth import BasicAuth
import json
from dbclass import DBClass
from instagram import instagram
from google_api import GoogleAPI
from generatesite import GenerateSite
from parse_recipe import RecipeParser
#Fast API
app = FastAPI()
security = HTTPBasic()
basicAuth = BasicAuth()
#Custom Classes
db = DBClass()
insta = instagram()
googleAPI = GoogleAPI()
generateSite = GenerateSite()
recipeparser = RecipeParser()

@app.get("/")
async def root(auth: BasicAuth = Depends(basicAuth) ):
    return {"message": "Hello World"}


@app.get("/post/{permalink}")
async def read_post(permalink, auth: str = Depends(basicAuth)):
    post_permalink = db.getPostByPermalink(permalink)
    if post_permalink is not None:
        return post_permalink
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Instagram Post not found"})

@app.get("/posts")
async def read_post(permalink: str = Depends(basicAuth)):
    return db.tablePosts.all()

@app.get("/recipes")
async def read_post(permalink: str = Depends(basicAuth)):
    return db.recipes.all()

@app.get("/recipe/{permalink}")
async def read_post(permalink, auth: str = Depends(basicAuth)):
    recipe = db.getRecipeByPermalink(permalink)
    if recipe is not None:
        return recipe
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Recipe not found"})

@app.get("/post/{permalink}/recipes")
async def read_recipes_from_posts(permalink, auth: str = Depends(basicAuth)):
    recipes = db.getAllRecipesByPost(permalink)
    return recipes

@app.get("/triggerBuild")
async def triggerBuild(auth: BasicAuth = Depends(basicAuth) ):
    instagram_data = db.tablePosts.all()
    generateSite.generate_posts(instagram_data, db)
    return {"message": "Post generated"}

@app.get("/readInstagramPosts")
async def readInstagramPosts(auth: BasicAuth = Depends(basicAuth) ):
    metadata = googleAPI.get_google_sheets_data()
    insta.load_instagram_data(db, db.tablePosts, metadata)
    return {"message": "Instagram Posts loaded"}

@app.get("/parseRecipe")
async def parseRecipe(auth: BasicAuth = Depends(basicAuth) ):
    recipeparser.parse_recipe()
    return {"message": "Instagram Posts loaded"}

@app.get("/generateRecipes")
async def generateRecipes(auth: BasicAuth = Depends(basicAuth) ):
    recipeparser.generate_recipes()
    return {"message": "Recipes generated"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
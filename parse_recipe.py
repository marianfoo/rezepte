from bs4 import BeautifulSoup
from google_api import GoogleAPI
from dbclass import DBClass
import requests
import os
import glob
import codecs
class RecipeParser:
    def __init__(self):
        self.googleAPI = GoogleAPI()
        self.db = DBClass()
    def parse_recipe(self, force_full_reload):
        if force_full_reload:
            self.db.recipes.truncate()
        recipes_links = self.googleAPI.get_recipes()
        for link in recipes_links:
            recipe_db = self.db.getRecipeByLink(link)
            if recipe_db is None:
                # with open("recipes.html") as fp:
                #     soup = BeautifulSoup(fp, "html.parser")
                r = requests.get(link["link"])
                soup = BeautifulSoup(r.text.encode("utf-8"), "html.parser")
                recipe_object = {}
                recipe_object["permalink"] = link["permalink"]
                try:
                    recipe_object["name"] = soup.find("h2",{"itemprop": "name"}).text
                except:
                    None
                try:
                    recipe_object["category"] = soup.find("meta",{"itemprop": "recipeCourse"}).attrs["content"]
                except:
                    None
                try:
                    recipe_object["tag"] = soup.find("meta", {"itemprop": "recipeCategory"}).attrs["content"]
                except:
                    None
                try:
                    recipe_object["source"] = soup.find("span",{"itemprop": "recipeSource"}).a["href"]
                except:
                    None

                recipe_ingredients_tags = soup.find_all("li",{"itemprop": "ingredient"})
                recipe_object["ingredients"] = []
                for ingredient in recipe_ingredients_tags:
                    recipe_object["ingredients"].append(ingredient.text)

                try:
                    recipe_instructions_ul = soup.find("ul", {"itemprop": "recipeInstructions"}).find_all('li')
                    recipe_object["instructions"] = []
                    for li in recipe_instructions_ul:
                        if li.text != '':
                            recipe_object["instructions"].append(li.text)
                except:
                    None
                recipe_photos = soup.find_all("img", {"class": "recipe-photos"})
                recipe_object["images"] = []
                for i in range(len(recipe_photos)):
                    image_object = {}
                    photo = recipe_photos[i]
                    source_url = "https://recipekeeperonline.com" + photo["src"]
                    filename = str(i) + ".jpg"
                    image_object["source_url"] = source_url
                    image_object["filename"] = filename
                    recipe_object["images"].append(image_object)
                self._download_image_to_folder(recipe_object["images"], recipe_object["permalink"])

                self.db.recipes.insert(recipe_object)
                print(recipe_object)
        self.generate_recipes(self.db.recipes.all())
    def generate_recipes(self, recipes):
        # delete all current recipes
        files = glob.glob('docs/_recipes/*')
        for f in files:
            os.remove(f)
        for recipe in recipes:
            filename = recipe["permalink"] + ".md"
            f = codecs.open("docs/_recipes/" + filename, "w", "utf-8")
            f.write("---\n")
            f.write("title: " + recipe["name"] + " \n")
            f.write("permalink: /recipes/" + recipe["permalink"] + "\n")
            try:
                f.write("course: " + recipe["category"] + "\n")
            except:
                None
            f.write("ingredients: \n")
            for ingredient in recipe["ingredients"]:
                f.write("    - '" + ingredient + "'\n")
            f.write("instructions: \n")
            for instruction in recipe["instructions"]:
                f.write("    - '" + instruction + "'\n")
            f.write("images: \n")
            for image in recipe["images"]:
                f.write("    - '" + image["filename"] + "'\n")
            f.write("---\n")
            f.write("\n")
            f.close()

    def _download_image_to_folder(self, recipe_images, foldername):
        # try to create folder
        try:
            os.mkdir("docs/assets/recipes/" + foldername)
        except OSError:
            error = 1
        # delete files in this folder
        files = glob.glob("docs/assets/recipes/" + foldername + "/*")
        for f in files:
            os.remove(f)
        for recipe_image in recipe_images:
            filename = r'docs/assets/recipes/' + foldername + "/" + recipe_image["filename"]
            receive = requests.get(recipe_image["source_url"] )
            with open(filename, 'wb') as f:
                f.write(receive.content)








#recipeparser = RecipeParser()
#recipeparser.parse_recipe(True)
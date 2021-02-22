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
            f.write("---\n")
            f.write("\n")
            f.close()








recipeparser = RecipeParser()
recipeparser.parse_recipe(True)
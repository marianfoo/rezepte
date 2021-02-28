import os
import glob
import codecs
class GenerateSite:
    def generate_posts(self, instagram_data, db):
        # delete all current posts
        files = glob.glob('docs/_posts/*')
        for f in files:
            os.remove(f)
        for post in instagram_data:
            try:
                filename = post["date"] + "-" + post["date"]  + "-" +  post["filename"] + ".md"
                picturefilename = post["date"] + "-" + post["filename"]
                f = codecs.open("docs/_posts/"+ filename, "w", "utf-8")
                f.write("---\n")
                f.write("title: '"+ post["title"] + "'\n")
                f.write("categories:\n")
                f.write("  - Essen\n")
        #         f.write("tags:\n")
        #         for tag in jsonMetaData["tags"]:
        #             f.write("  - " +tag + "\n")
                f.write("---\n")
                f.write("\n")
                f.write(post["caption"].split("{",1)[0])

                recipes = db.getAllRecipesByPost(post["permalink"])
                if recipes:
                    f.write("\n")
                    f.write("\n")
                    f.write("### Rezepte:\n")
                for recipe in recipes:
                    f.write(f"  - [{recipe['name']}](/recipes/{recipe['permalink']})\n")
                f.write("\n")
                f.write("\n")
                count = 1
                if "children" in post:
                    for child in post["children"]["data"]:
                        savepicture = '![](..\\..\\.\\assets\\' + picturefilename + "\\" + str(count) + ".jpg)"
                        f.write(savepicture)
                        f.write("\n")
                        f.write("\n")
                        count = count + 1
                else:
                    savepicture = '![](..\\..\\.\\assets\\' + picturefilename + "\\" + str(count) + ".jpg)"
                    f.write(savepicture)
                f.write("\n")
                f.close()
            except KeyError:
                print("Key not found on post " + post["permalink"])
        print("all posts generated")
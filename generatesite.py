import os
import glob
import codecs
class GenerateSite:
    def generate_posts(self, instagram_data, metadata):
        # delete all current posts
        files = glob.glob('docs/_posts/*')
        for f in files:
            os.remove(f)
        for post in instagram_data:
            jsonMetaData = self.get_metadata(post["permalink"], metadata)
            filename = jsonMetaData["date"] + "-" + jsonMetaData["date"]  + "-" +  jsonMetaData["filename"] + ".md"
            picturefilename = jsonMetaData["date"] + "-" + jsonMetaData["filename"]
            f = codecs.open("docs/_posts/"+ filename, "w", "utf-8")
            f.write("---\n")
            f.write("title: '"+ jsonMetaData["title"] + "'\n")
            f.write("categories:\n")
            f.write("  - Blog\n")
    #         f.write("tags:\n")
    #         for tag in jsonMetaData["tags"]:
    #             f.write("  - " +tag + "\n")
            f.write("---\n")
            f.write("\n")
            f.write(post["caption"].split("{",1)[0])
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
        print("all posts generated")
    def get_metadata(self, permalink, metadata):
        for tupel in metadata:
            if tupel["permalink"] == permalink:
                return tupel
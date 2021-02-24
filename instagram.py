import requests
import json
import os
import ast
from tinydb import Query
class instagram:
    def __init__(self):
        with open('secrets.json') as json_file:
            json_file_secrets = json.load(json_file)
            self.access_token_instagram = json_file_secrets["instagram_access_token"]
    def _load_local_instagram_data(self):
        if os.path.isdir("data") == False:
            try:
                os.mkdir("data")
            except OSError as e:
                print (e)
        if os.path.isfile("data/instagram_data.json"):
            with open('data/instagram_data.json', 'r') as fp:
                instagram_json_data = json.load(fp)
                return instagram_json_data
        else:
            return {}
    def load_instagram_data(self, db, tablePosts, metadata):
        instagram_data = self._instagram_api_request("https://graph.instagram.com/me/media?fields=caption,id,media_type,media_url,permalink,thumbnail_url,timestamp,username,children")
        for post in instagram_data["data"]:
            try:
                dbPost = db.getPostByFullPermalink(post["permalink"])
                if dbPost is None:
                    if "children" in post:
                        for child in post["children"]["data"]:
                            media_id = child["id"]
                            requestUrl = f"https://graph.instagram.com/{media_id}?fields=id,media_type,media_url,permalink,thumbnail_url,timestamp,username"
                            singlemedia_json = self._instagram_api_request(requestUrl)
                            child["media_type"] = singlemedia_json["media_type"]
                            child["media_url"] = singlemedia_json["media_url"]
                            child["permalink"] = singlemedia_json["permalink"]
                            child["timestamp"] = singlemedia_json["timestamp"]
                    tablePosts.insert(post)
                    self._get_media(post, metadata)
                else:
                    db.updatePost(post["permalink"], "caption", dbPost["caption"])
                    self._get_media(post, metadata)
                self._add_metadata_to_post_db(db, post, metadata)


            except KeyError:
                # Instagram Post not found, add post to local data
                print("post" + post["permalink"] + " not found in local data")
        return db.getPosts()
    def _get_media(self, post, metadata):
        jsonMetaData = self._get_metadata(post["permalink"], metadata)
        if jsonMetaData is None:
            print(post["permalink"] + " not found in metadata from google sheets!")
        else:
            folder_name = jsonMetaData["date"] + "-" + jsonMetaData["filename"]
            count = 1
            try:
                os.mkdir("docs/assets/" + folder_name)
            except OSError:
                error = 1
            if "children" in post:
                for child in post["children"]["data"]:
                    filename = r'docs/assets/' + folder_name + "/" + str(count) + ".jpg"
                    if os.path.isfile(filename):
                        filename = filename
                    else:
                        receive = requests.get(child["media_url"])
                        with open(filename, 'wb') as f:
                            f.write(receive.content)
                    count = count + 1
            else:
                filename = r'docs/assets/' + folder_name + "/" + str(count) + ".jpg"
                if os.path.isfile(filename):
                    filename = filename
                else:
                    receive = requests.get(post["media_url"])
                    with open(r'docs/assets/' + folder_name + "/" + str(count) + ".jpg", 'wb') as f:
                        f.write(receive.content)
    def _instagram_api_request(self, requestUrl):
        url = requestUrl + '&access_token=' + self.access_token_instagram
    #     print("Instagram API Request to " + url)
        request = requests.get(url)
        response_json = json.loads(request.text)
        return response_json
    def _add_metadata_to_post_db(self,db, post, metadata):
        metadata_post = self._get_metadata(post["permalink"], metadata)
        if metadata_post is None:
            print(post["permalink"] + " not found in metadata from google sheets!")
        else:
            for key in metadata_post:
                if key == 'tags':
                    string_list = ast.literal_eval(metadata_post[key])
                    db.updatePost(post["permalink"], key, string_list)
                else:
                    db.updatePost(post["permalink"], key, metadata_post[key])
    def _get_metadata(self, permalink, metadata):
        for tupel in metadata:
            if tupel["permalink"] == permalink:
                return tupel
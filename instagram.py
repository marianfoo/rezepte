import requests
import json
import os
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
    def load_instagram_data(self):
        instagram_local_data = self._load_local_instagram_data()
        # instagram_data = instagram_api_request("https://graph.instagram.com/me/media?fields=caption,id,media_type,media_url,permalink,thumbnail_url,timestamp,username,children")
        # for post in instagram_data["data"]:
        #     try:
        #         local_post = instagram_local_data[post["permalink"]]
        #         local_post["caption"] = post["caption"]
        #         print("post" + post["permalink"] + " found in local data")
        #     except KeyError:
        #         # Instagram Post not found, add post to local data
        #         print("post" + post["permalink"] + " not found in local data")
        #         instagram_local_data[post["permalink"]] = post
        #         local_post = instagram_local_data[post["permalink"]]
        #         ## if children media, add url info
        #         if "children" in local_post:
        #             for child in local_post["children"]["data"]:
        #                 media_id = child["id"]
        #                 requestUrl = f"https://graph.instagram.com/{media_id}?fields=id,media_type,media_url,permalink,thumbnail_url,timestamp,username"
        #                 singlemedia_json = instagram_api_request(requestUrl)
        #                 child["media_type"] = singlemedia_json["media_type"]
        #                 child["media_url"] = singlemedia_json["media_url"]
        #                 child["permalink"] = singlemedia_json["permalink"]
        #                 child["timestamp"] = singlemedia_json["timestamp"]
        #         get_insta_media(local_post)
        # with open('data/instagram_data.json', 'w') as fp:
        #     json.dump(instagram_local_data, fp)
        return instagram_local_data
    def _instagram_api_request(self, requestUrl):
        url = requestUrl + '&access_token=' + self.access_token_instagram
    #     print("Instagram API Request to " + url)
        request = requests.get(url)
        response_json = json.loads(request.text)
        return response_json
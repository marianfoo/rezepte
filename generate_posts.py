#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import codecs
import os
import glob
import httplib2
import sys
from apiclient import discovery
from google.oauth2 import service_account


# In[2]:


with open('secrets.json') as json_file:
    json_file_secrets = json.load(json_file)
    access_token_instagram = json_file_secrets["instagram_access_token"]
    spreadsheet_id = json_file_secrets["spreadsheet_id"]


# In[3]:


force_reload_bool = False
try:
    first_argument = sys.argv[1]
    if first_argument == "force_reload":
        force_reload_bool = True
        print("Forcing reloading Instagram and Google Sheets")
except:
    force_reload_bool = False


# In[4]:


# add media information to child media
# def add_mediainfo_to_child_media(d, access_token_instagram, instagram_json_data):
#     for post in d["data"]:
#         if get_post_from_data(post["permalink"], instagram_json_data) == True:
#             print("post already loaded")
#             continue
#         else:
#             if "children" in post:
#                 for child in post["children"]["data"]:
#                     media_id = child["id"]
#                     requestUrl = f"https://graph.instagram.com/{media_id}?fields=id,media_type,media_url,permalink,thumbnail_url,timestamp,username"
# #                     singlemedia = r =requests.get(requestUrl)
# #                     singlemedia_json = json.loads(singlemedia.text)
#                     singlemedia_json = instagram_api_request(requestUrl)
#                     child["media_type"] = singlemedia_json["media_type"]
#                     child["media_url"] = singlemedia_json["media_url"]
#                     child["permalink"] = singlemedia_json["permalink"]
#                     child["timestamp"] = singlemedia_json["timestamp"]
#         print("Media Information from Child Media loaded")
#         return d
    


# In[5]:


# 1. load posts
# def load_insta_posts(access_token_instagram):
    # check if data file exists
#     r =requests.get('https://graph.instagram.com/me/media?fields=caption,id,media_type,media_url,permalink,thumbnail_url,timestamp,username,children)
#     d = json.loads(r.text)
#     d = instagram_api_request("https://graph.instagram.com/me/media?fields=caption,id,media_type,media_url,permalink,thumbnail_url,timestamp,username,children")
#     print("Instagram Posts loaded")
#     instagram_json_data = None
#     # insta data exists, load and check for new data
#     if os.path.isfile("tmp/instagram_data.json") and force_reload_bool == False:
#         print ("File instagram_data exist")
#         with open('tmp/instagram_data.json', 'r') as fp:
#             instagram_json_data = json.load(fp)
#         d = add_mediainfo_to_child_media(d, access_token_instagram, instagram_json_data)
#     else:
#         print ("File instagram_data not exist")
#         d = add_mediainfo_to_child_media(d, access_token_instagram, instagram_json_data)
#         with open('tmp/instagram_data.json', 'w') as fp:
#             json.dump(d, fp)


# In[6]:


# 2. get metadata from google sheets
def get_google_sheets_data():
    try:
        scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
        secret_file = os.path.join(os.getcwd(), 'client_secret.json')
        credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=scopes)
        service = discovery.build('sheets', 'v4', credentials=credentials)

        request  = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='A1:F300')
        response = request.execute()

        metadata = []
        length = len(response["values"])
        values = response["values"]
        for data in range(1, length):
            tupel = {}
            for value in range(len(values[data])):
                tupel[response["values"][0][value]] = values[data][value]
            metadata.append(tupel)
        print("Metadata from Google Sheets loaded")
        return metadata
    except OSError as e:
        print (e)


# In[7]:


# 3. get all media and child media
def get_all_insta_media(post):
    for post in d["data"]:
        jsonMetaData = get_metadata(post["permalink"], metadata)
        folder_name = jsonMetaData["date"] + "-" + jsonMetaData["filename"]
        count = 1
        try:
            os.mkdir("docs/assets/"+ folder_name)
        except OSError:
            error = 1
        if "children" in post:
            for child in post["children"]["data"]:
                filename = r'docs/assets/'+ folder_name + "/" + str(count) +".jpg"
                if os.path.isfile(filename):
                    filename = filename
                else:
                    receive = requests.get(child["media_url"])
                    with open(filename,'wb') as f:
                        f.write(receive.content)
                count = count + 1
        else:
            filename = r'docs/assets/'+ folder_name + "/" + str(count) +".jpg"
            if os.path.isfile(filename):
                filename = filename
            else:
                with open(r'docs/assets/'+ folder_name + "/" + str(count) + ".jpg",'wb') as f:
                    f.write(receive.content)
    print("downloaded Instagram Media")
# 3. get media and child media from post
def get_insta_media(post):
    jsonMetaData = get_metadata(post["permalink"], metadata)
    folder_name = jsonMetaData["date"] + "-" + jsonMetaData["filename"]
    count = 1
    try:
        os.mkdir("docs/assets/"+ folder_name)
    except OSError as e:
        print(e)
    if "children" in post:
        for child in post["children"]["data"]:
            filename = r'docs/assets/'+ folder_name + "/" + str(count) +".jpg"
            if os.path.isfile(filename):
                filename = filename
            else:
                receive = requests.get(child["media_url"])
                with open(filename,'wb') as f:
                    f.write(receive.content)
            count = count + 1
    else:
        receive = requests.get(post["media_url"])
        filename = r'docs/assets/'+ folder_name + "/" + str(count) +".jpg"
        if os.path.isfile(filename):
            filename = filename
        else:
            with open(r'docs/assets/'+ folder_name + "/" + str(count) + ".jpg",'wb') as f:
                f.write(receive.content)


# In[8]:


# 4. write posts
def generate_posts(instagram_data, metadata):
    # delete all current posts
    files = glob.glob('docs/_posts/*')
    for f in files:
        os.remove(f)
    for postkey in instagram_data:
        print(postkey)
        post = instagram_data[postkey]
        jsonMetaData = get_metadata(post["permalink"], metadata)
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


# In[9]:


def get_metadata(permalink, metadata):
    for tupel in metadata:
        if tupel["permalink"] == permalink:
            return tupel


# In[10]:


# def get_post_from_data(permalink, instagram_json_data):
#     for post in instagram_json_data["data"]:
#         if post["permalink"] == permalink:
#             return True


# In[11]:


def instagram_api_request(requestUrl):
    url = requestUrl + '&access_token=' + access_token_instagram
#     print("Instagram API Request to " + url)
    request = requests.get(url)
    response_json = json.loads(request.text)
    return response_json


# In[12]:


def load_local_instagram_data():
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
                


# In[13]:


def load_instagram_data():
    instagram_local_data = load_local_instagram_data()
    instagram_data = instagram_api_request("https://graph.instagram.com/me/media?fields=caption,id,media_type,media_url,permalink,thumbnail_url,timestamp,username,children")
    for post in instagram_data["data"]:
        try:
            local_post = instagram_local_data[post["permalink"]]
            local_post["caption"] = post["caption"]
            print("post" + post["permalink"] + " found in local data")
        except KeyError:
            # Instagram Post not found, add post to local data
            print("post" + post["permalink"] + " not found in local data")
            instagram_local_data[post["permalink"]] = post
            local_post = instagram_local_data[post["permalink"]]
            ## if children media, add url info
            if "children" in local_post:
                for child in local_post["children"]["data"]:
                    media_id = child["id"]
                    requestUrl = f"https://graph.instagram.com/{media_id}?fields=id,media_type,media_url,permalink,thumbnail_url,timestamp,username"
                    singlemedia_json = instagram_api_request(requestUrl)
                    child["media_type"] = singlemedia_json["media_type"]
                    child["media_url"] = singlemedia_json["media_url"]
                    child["permalink"] = singlemedia_json["permalink"]
                    child["timestamp"] = singlemedia_json["timestamp"]
            get_insta_media(local_post)
    with open('data/instagram_data.json', 'w') as fp:
        json.dump(instagram_local_data, fp)
    return instagram_local_data

# In[14]:


metadata = get_google_sheets_data()
instagram_local_data = load_instagram_data()
generate_posts(instagram_local_data, metadata)


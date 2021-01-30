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


# In[ ]:


force_reload_bool = False
try:
    first_argument = sys.argv[1]
    if first_argument == "force_reload":
        force_reload_bool = True
        print("Forcing reloading Instagram and Google Sheets")
except:
    force_reload_bool = False


# In[3]:


# add media information to child media
def add_mediainfo_to_child_media(d, access_token_instagram):
    for post in d["data"]:
        if "children" in post:
            for child in post["children"]["data"]:
                media_id = child["id"]
                requestUrl = f"https://graph.instagram.com/{media_id}?fields=id,media_type,media_url,permalink,thumbnail_url,timestamp,username&access_token={access_token_instagram}"
                singlemedia = r =requests.get(requestUrl)
                singlemedia_json = json.loads(singlemedia.text)
                child["media_type"] = singlemedia_json["media_type"]
                child["media_url"] = singlemedia_json["media_url"]
                child["permalink"] = singlemedia_json["permalink"]
                child["timestamp"] = singlemedia_json["timestamp"]
    print("Media Information from Child Media loaded")
    


# In[4]:


# 1. load posts
def load_insta_posts(access_token_instagram):
    # check if data file exists
    if os.path.isfile("tmp/instagram_data.json") and force_reload_bool == False:
        print ("File instagram_data exist")
        with open('tmp/instagram_data.json', 'r') as fp:
            d = json.load(fp)
            return d
    else:
        print ("File instagram_data not exist")
        r =requests.get('https://graph.instagram.com/me/media?fields=caption,id,media_type,media_url,permalink,thumbnail_url,timestamp,username,children&access_token=' + access_token_instagram)
        d = json.loads(r.text)
        print("Instagram Posts loaded")
        d = add_mediainfo_to_child_media(d, access_token_instagram)
        with open('tmp/instagram_data.json', 'w') as fp:
            json.dump(d, fp)
        return d


# In[5]:


# 2. get metadata from google sheets
def get_google_sheets_data():
    if os.path.isfile("tmp/google_sheets_data.json") and force_reload_bool == False:
        with open('tmp/google_sheets_data.json', 'r') as fp:
            metadata = json.load(fp)
            return metadata
    else:
        try:
            scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
            secret_file = os.path.join(os.getcwd(), 'client_secret.json')
            #range_name = 'Sheet1!A1:D2'

            credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=scopes)
            service = discovery.build('sheets', 'v4', credentials=credentials)

            request  = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='A1:F30')
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
            with open('tmp/google_sheets_data.json', 'w') as fp:
                json.dump(metadata, fp)
            return metadata


        except OSError as e:
            print (e)


# In[10]:


# 3. get all media and child media
def get_all_insta_media(d, metadata):
    for post in d["data"]:
        #jsonString = "{" + post["caption"].split("{",1)[1]
        #jsonMetaData = json.loads(jsonString.replace('\n',''))
        jsonMetaData = get_metadata(post["permalink"], metadata)
        folder_name = jsonMetaData["date"] + "-" + jsonMetaData["filename"]
#         receive = requests.get(post["media_url"])
        count = 1
        try:
            os.mkdir("docs/assets/"+ folder_name)
        except OSError:
            error = 1
#             print ("Creation of the directory %s failed")
        else:
            error = 1
#             print ("Successfully created the directory %s ")
        if "children" in post:
            for child in post["children"]["data"]:
                filename = r'docs/assets/'+ folder_name + "/" + str(count) +".jpg"
                if os.path.isfile(filename):
                    filename = filename
                else:
                    #print ("File not exist")
                    receive = requests.get(child["media_url"])
                    with open(filename,'wb') as f:
                        f.write(receive.content)
                count = count + 1
        else:
            filename = r'docs/assets/'+ folder_name + "/" + str(count) +".jpg"
            if os.path.isfile(filename):
                filename = filename
            else:
                #print ("File not exist")
                with open(r'docs/assets/'+ folder_name + "/" + str(count) + ".jpg",'wb') as f:
                    f.write(receive.content)
    print("downloaded Instagram Media")


# In[7]:


# 4. write posts
def generate_posts(d, metadata):
    # delete all current posts
    files = glob.glob('docs/_posts/*')
    for f in files:
        os.remove(f)
    for post in d["data"]:
    #     jsonString = "{" + post["caption"].split("{",1)[1]
    #     jsonMetaData = json.loads(jsonString.replace('\n',''))
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


# In[8]:


def get_metadata(permalink, metadata):
    for tupel in metadata:
        if tupel["permalink"] == permalink:
            return tupel


# In[11]:


try:
    os.mkdir("tmp")
except OSError as e:
    print (e)
d = load_insta_posts(access_token_instagram)
metadata = get_google_sheets_data()
get_all_insta_media(d, metadata)
generate_posts(d, metadata)


# In[ ]:





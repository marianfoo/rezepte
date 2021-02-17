import json
from tinydb import TinyDB, Query
class DBClass:
    def __init__(self):
        self.db = TinyDB('db.json')
        self.tablePosts = self.db.table('Posts')
    def getPostByPermalink(self, permalink):
        User = Query()
        full_permalink = 'https://www.instagram.com/p/' + permalink + '/'
        return self.tablePosts.search(User.permalink == full_permalink)
    def getPostByFullPermalink(self, full_permalink):
        User = Query()
        return self.tablePosts.search(User.permalink == full_permalink)
    def getPosts(self):
        return self.tablePosts.all()

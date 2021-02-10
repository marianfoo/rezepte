import json
from tinydb import TinyDB, Query
class DBClass:
    def __init__(self):
        self.db = TinyDB('db.json')
        self.tablePosts = self.db.table('Posts')
    def getPost(self, permalink):
        User = Query()
        permalink = 'CKuA2s3BkYf'
        full_permalink = 'https://www.instagram.com/p/' + permalink + '/'
        return self.tablePosts.search(User.permalink == full_permalink)

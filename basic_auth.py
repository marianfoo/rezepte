import secrets
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import json
security = HTTPBasic()
class BasicAuth():
    def __init__(self):
        self.security = HTTPBasic()
        with open('secrets.json') as json_file:
            json_file_secrets = json.load(json_file)
            self.username = json_file_secrets["username"]
            self.pwd = json_file_secrets["pwd"]
    async def __call__(self, credentials: HTTPBasicCredentials = Depends(security)):
        correct_username = secrets.compare_digest(credentials.username, self.username)
        correct_password = secrets.compare_digest(credentials.password, self.pwd)
        if not (correct_username and correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Basic"},
            )
        return credentials.username
import hashlib
import os
from dotenv import load_dotenv #type: ignore
from blurple import ui #type: ignore

load_dotenv(".env")
envvar = os.getenv("Account")

class server:
    def __init__ (self):
        print("Initialized Server")

class User:
    def __init__ (self):    
        if envvar == "False":
            print("No acount logged in")
            # Add login code
        else:
            #add blruple success code
            print("Loaded")

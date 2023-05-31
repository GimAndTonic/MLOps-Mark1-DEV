import pandas as pd
import json

def read_token(path='../../secrets/splunk.json') :
    f = open(path)
    k = json.load(f)

    HOST  = k['HOST']
    PORT  = k['PORT']
    TOKEN = k['TOKEN']

    return HOST, PORT, TOKEN
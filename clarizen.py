import os
import json
import requests
from settings import CLARIZEN_DATA_QUERY_URL, CLARIZEN_LOGIN_URL

def cl_login():
    """Function to check login to clarizen
    When logging in for the first time, the session info is stored into a file
    which is loaded during futher logging in. To reset the cache, delete the
    file login_cache.txt from the run folder."""

    cache_file = 'login_cache.txt'
    if os.path.isfile(cache_file):
        with open("login_cache.txt", "r") as f:
            login_data = json.loads(f.read())
            return(login_data)

    username = input("Enter Clarizen Username: ")
    password = input("Enter Clarizen password: ")
    r = requests.post(CLARIZEN_LOGIN_URL,
            data = {'userName':username, 'password':password})

    with open("login_cache.txt", "w") as f:
        f.write(r.text)
    
    login_data = json.loads(r.text)
    return login_data

def cl_auth():
    return {
        'Authorization': 'Session {}'.format(cl_login()['sessionId'])
    }

def get_subprojects(parent_proj_id):
    login_data = cl_login()
    url = CLARIZEN_DATA_QUERY_URL
    querystring = {"q":"""SELECT @Name, TrackStatus.Name, ProjectManager.Name,
            PercentCompleted FROM Project WHERE
            ParentProject='{}'""".format(parent_proj_id)}
    headers = cl_auth()
    response = requests.request("GET", url, headers=headers, params=querystring)
    return json.loads(response.text)
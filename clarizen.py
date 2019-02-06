import os
import json
import requests
from settings import (CLARIZEN_DATA_QUERY_URL, 
                      CLARIZEN_LOGIN_URL,
                      CLARIZEN_RELATIONS_QUERY_URL)

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
    url = CLARIZEN_DATA_QUERY_URL
    querystring = {"q":"""SELECT @Name, TrackStatus.Name, ProjectManager.Name,
            PercentCompleted FROM Project WHERE
            ParentProject='{}'""".format(parent_proj_id)}
    headers = cl_auth()
    response = requests.request("GET", url, headers=headers, params=querystring)
    return json.loads(response.text)

def get_subtasks(parent_id):
    url = CLARIZEN_DATA_QUERY_URL
    querystring = {"q":"""SELECT @Name, TrackStatus.Name, ProjectManager.Name,
            PercentCompleted FROM WorkItem WHERE
            Parent='{}'""".format(parent_id)}
    headers = cl_auth()
    response = requests.request("GET", url, headers=headers, params=querystring)
    return json.loads(response.text)

def work_items_by_topic(topic):
    """Function to find workitems by topic"""
    headers = cl_auth()
    # Finding the id for the topic
    querystring = {"q":"SELECT @Name FROM Topic WHERE Name='{}'".format(topic)}
    response = requests.request("GET", CLARIZEN_DATA_QUERY_URL, headers=headers, params=querystring)
    topicid = json.loads(response.text)['entities'][0]['id']
    req_data = {
        "entityId":topicid,
        "relationName":"WorkItems",
        "fields": [
            "Name", "TrackStatus.Name", 
            "ProjectManager.Name", 
            "PercentCompleted",
            "InternalStatus"
        ]
    }
    response = requests.request("POST",
                                CLARIZEN_RELATIONS_QUERY_URL,
                                headers=headers,
                                data=str(req_data))
    return json.loads(response.text)

def strategy_tip_list(topic):
    tips = work_items_by_topic(topic)
    for domain in tips['entities']:
        domain['subprojects'] = get_subprojects(domain['id'])['entities']
        for tip in domain['subprojects']:
            tasks = get_subtasks(tip['id'])['entities']
            for task in tasks:
                if task['Name'].lower() == 'deliverables':
                    tip['Deliverables'] = get_subtasks(task['id'])['entities']
    return tips
import os
import datetime
from dateutil import parser
import json
import requests
import getpass
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
    password = getpass.getpass(prompt="Enter Clarizen password: ")
    r = requests.post(CLARIZEN_LOGIN_URL,
            data = {'userName':username, 'password':password})

    login_data = json.loads(r.text)
    # Checking if login was successful
    if 'sessionId' in login_data:
        # Write the login_cache file
        with open("login_cache.txt", "w") as f:
            f.write(r.text)
        return login_data
    else:
        raise Exception("Login Failed!")

    

def cl_auth():
    """Function to return the request header with login information"""
    return {
        'Authorization': 'Session {}'.format(cl_login()['sessionId'])
    }

def get_subprojects(parent_proj_id):
    """Get all the subprojects under a given project id"""
    url = CLARIZEN_DATA_QUERY_URL
    querystring = {"q":"""SELECT @Name, TrackStatus.Name, ProjectManager.Name,
            PercentCompleted FROM Project WHERE
            ParentProject='{}'""".format(parent_proj_id)}
    headers = cl_auth()
    response = requests.request("GET", url, headers=headers, params=querystring)
    return json.loads(response.text)

def get_subtasks(parent_id):
    """Get all subtasks for a given task/project id"""
    url = CLARIZEN_DATA_QUERY_URL
    querystring = {"q":"""SELECT @Name, TrackStatus.Name, State.Name, DueDate
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

def tip_count(tips):
    count = 0
    for domain in tips['entities']:
        count += len(domain['subprojects'])
    return count

def delivery_count(tips):
    dtotal, dcompleted = 0, 0
    for domain in tips['entities']:
        for tip in domain['subprojects']:
            try:
                for deliverable in tip['Deliverables']:
                    dtotal +=1
                    if deliverable['State']['Name'] == 'Completed':
                        dcompleted +=1
            except KeyError:
                pass
    return (dtotal, dcompleted)

def prio_tips(tips):
    """ Function to return the priority tips for the next 30 days """
    priotips = []
    for domain in tips['entities']:
        for tip in domain['subprojects']:
            try:
                for deliverable in tip['Deliverables']:
                    delta = parser.parse(deliverable['DueDate']) - datetime.datetime.now()
                    if delta.days < 30:
                        priotips.append({
                            'TipName':tip['Name'],
                            'ProjectManager': tip['ProjectManager']['Name'],
                            'DeliverableName': deliverable['Name'],
                            'DueDate': deliverable['DueDate'],
                        })
            except KeyError:
                pass
    return tips
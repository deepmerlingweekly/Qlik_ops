import requests
import json
from dotenv import load_dotenv
import os
import logging
from logging import getLogger
import time
import sqlite3

#load_dotenv('/mnt/.env')

logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Backend avviato")
# try:
#     # qui la tua logica Streamlit o backend
# except Exception as e:
#     logging.exception("Errore nel backend")
#     sys.exit(1)


def get_apikey(env):
    con = sqlite3.connect("qlik_ops.db")
    cur = con.cursor()
    res = cur.execute('select apikey from settings where environment="{}"'.format(env))
    apikey=res.fetchall()[0][0]
    return apikey

def get_tenant(env):
    con = sqlite3.connect("qlik_ops.db")
    cur = con.cursor()
    res = cur.execute('select tenant from settings where environment="{}"'.format(env))
    tenant=res.fetchall()[0][0]
    return tenant

def get_assigneeId_tenant_admin(env):
    con = sqlite3.connect("qlik_ops.db")
    cur = con.cursor()
    res = cur.execute('select assigneeId_tenant_admin from settings where environment="{}"'.format(env))
    assigneeId_tenant_admin=res.fetchall()[0][0]
    return assigneeId_tenant_admin

def show_current_settings():
    con = sqlite3.connect("qlik_ops.db")
    cur = con.cursor()
    res = cur.execute('select * from settings')
    currents_settings=res.fetchall()
    return currents_settings


def create_qlik_space(environment,space):
    #app_logger.info(space)
    api_key=get_apikey(environment)
    tenant=get_tenant(environment)
    # if environment=='prod':
    #     tenant=os.getenv('prod_tenant')
    #     api_key=os.getenv('prod_api_key')
    # if environment=='test':
    #     tenant=os.getenv('test_tenant')
    #     api_key=os.getenv('test_api_key')
        
    endpoint="{}/api/v1/spaces".format(tenant)
    headers={
        "Authorization": "Bearer {}".format(api_key),
        "Content-Type": "application/json"
    }

    payload=space
    try:
        r = requests.post(endpoint,headers=headers,json=payload)
        id=json.loads(r.text)['id']
        tenant_default_assignment(environment,id)
        return json.loads(r.text)
    except Exception as e:
        logging.exception(e)
        print('error')
        print(e)

def tenant_default_assignment(environment,spaceid):
    api_key=get_apikey(environment)
    tenant=get_tenant(environment)
    assigneeId_tenant_admin=get_assigneeId_tenant_admin(environment)
    headers={
        "Authorization": "Bearer {}".format(api_key),
        "Content-Type": "application/json"
    }
    endpoint="{}/api/v1/spaces".format(tenant)
    assignment_endpoint="{}/{}/assignments".format(endpoint,spaceid)
    assignment_payload={"type":"group","roles":["consumer","facilitator"],"assigneeId":assigneeId_tenant_admin}
    print(assignment_payload)
    try:
        r = requests.post(assignment_endpoint,headers=headers,json=assignment_payload)
        print(json.loads(r.text))
        #return json.loads(r.text)
    except Exception as e:
        logging.exception(e)
        print(e)


def default_group_creation(environment,domain,category):
    print("#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+")
    print("start default group creation")
    api_key=get_apikey(environment)
    tenant=get_tenant(environment)
        
    headers={
        "Authorization": "Bearer {}".format(api_key),
        "Content-Type": "application/json"
    }
    endpoint="{}/api/v1/groups".format(tenant)

    payload=''
    payload_consumers={"payload":{"name":domain+" - Consumers","status":"active","assignedRoles":[],"providerType":"custom"},"category":"consumers"}
    payload_testers={"payload":{"name":domain+" - Testers","status":"active","assignedRoles":[],"providerType":"custom"},"category":"testers"}
    payload_developers={"payload":{"name":domain+" - Developers","status":"active","assignedRoles":[],"providerType":"custom"},"category":"developers"}
    if category=='Consumers':
        payload=payload_consumers['payload']
    if category=='Tester':
        payload=payload_testers['payload']
    if category=='Developer':
        payload=payload_developers['payload']

    try:
        r = requests.post(endpoint,headers=headers,json=payload)
        
        group_id=json.loads(r.text)['id']
        group_name=json.loads(r.text)['name']
        print(group_name)
        assign_group(environment,domain,group_name,group_id)
        return json.loads(r.text)
    except Exception as e:
        print(e)


def assign_group(environment,domain,group_name,group_id):
    print("{},{},{},{}".format(environment,domain,group_name,group_id))
    
    api_key=get_apikey(environment)
    tenant=get_tenant(environment)
        
    headers={
        "Authorization": "Bearer {}".format(api_key),
        "Content-Type": "application/json"
    }
    endpoint="{}/api/v1/spaces?name={}".format(tenant,domain)
    # MANAGED PROD - consumers: ['consumer','contributor']
    managed_prod_consumers={"type":"group","roles":["consumer","contributor"],"assigneeId":group_id}
    # MANAGED PROD - testers: ['consumer','contributor']
    managed_prod_testers={"type":"group","roles":["consumer","contributor"],"assigneeId":group_id}
    # MANAGED PROD - developers: ['publisher']
    managed_prod_developers={"type":"group","roles":["publisher"],"assigneeId":group_id}
    # MANAGED PROD - BACKEND - developers: ['publisher']
    managed_prod_developers_backend={"type":"group","roles":["publisher"],"assigneeId":group_id}

    # MANAGED TEST - testers: ['consumer','contributor']
    managed_test_testers={"type":"group","roles":["consumer","contributor"],"assigneeId":group_id}
    # MANAGED TEST - developers: ['publisher']
    managed_test_developers={"type":"group","roles":["publisher"],"assigneeId":group_id}
    # MANAGED TEST - BACKEND - developers: ['publisher']
    managed_test_developers_backend={"type":"group","roles":["publisher"],"assigneeId":group_id}

    # SHARED DEV - developers: ["codeveloper","dataconsumer","producer"]
    shared_dev_developers={"type":"group","roles":["codeveloper","dataconsumer","producer"],"assigneeId":group_id}
    # SHARED DEV BACKEND - developers
    shared_dev_developers_backend={"type":"group","roles":["codeveloper","dataconsumer","producer"],"assigneeId":group_id}
    # SHARED DEV BACKEND SHARED DATA - developers
    shared_dev_developers_shared={"type":"group","roles":["codeveloper","dataconsumer","producer"],"assigneeId":group_id}

    r = requests.get(endpoint,headers=headers)
    for space in json.loads(r.text)['data']:
        endpoint="{}/api/v1/spaces".format(tenant)
        assignment_endpoint="{}/{}/assignments".format(endpoint,space['id'])
        if space['name']==domain:
            if group_name==domain+" - Consumers":
                print("Space {}, Consumer Assignment: {}, assignment url {}".format(space['name'],managed_prod_consumers,assignment_endpoint))
                try:
                    assignment_request=requests.post(assignment_endpoint,headers=headers,json=managed_prod_consumers)
                    print(json.loads(assignment_request.text))
                except Exception as e:
                    print(e)
            if group_name==domain+" - Testers":
                print("Space {}, Tester Assignment: {}, assignment url {}".format(space['name'],managed_prod_testers,assignment_endpoint))
                try:
                    assignment_request=requests.post(assignment_endpoint,headers=headers,json=managed_prod_testers)
                    print(json.loads(assignment_request.text))
                except Exception as e:
                    print(e)
            if group_name==domain+" - Developers":
                print("Space {}, Developer Assignment: {}, assignment url {}".format(space['name'],managed_prod_developers,assignment_endpoint))
                try:
                    assignment_request=requests.post(assignment_endpoint,headers=headers,json=managed_prod_developers)
                    print(json.loads(assignment_request.text))
                except Exception as e:
                    print(e)
        if space['name']==domain+" - BACKEND":
            if group_name==domain+" - Developers":
                print("Space {}, Developer Assignment: {}, assignment url {}".format(space['name'],managed_prod_developers_backend,assignment_endpoint))
                try:
                    assignment_request=requests.post(assignment_endpoint,headers=headers,json=managed_prod_developers_backend)
                    print(json.loads(assignment_request.text))
                except Exception as e:
                    print(e)
        if space['name']==domain+" - TEST":
            if group_name==domain+" - Testers":
                print("Space {}, Tester Assignment: {}, assignment url {}".format(space['name'],managed_test_testers,assignment_endpoint))
                try:
                    assignment_request=requests.post(assignment_endpoint,headers=headers,json=managed_test_testers)
                    print(json.loads(assignment_request.text))
                except Exception as e:
                    print(e)
            if group_name==domain+" - Developers":
                print("Space {}, Developer Assignment: {}, assignment url {}".format(space['name'],managed_test_developers,assignment_endpoint))
                try:
                    assignment_request=requests.post(assignment_endpoint,headers=headers,json=managed_test_developers)
                    print(json.loads(assignment_request.text))
                except Exception as e:
                    print(e)
        if space['name']==domain+" - TEST - BACKEND":
            if group_name==domain+" - Developers":
                print("Space {}, Developer Assignment: {}, assignment url {}".format(space['name'],managed_test_developers_backend,assignment_endpoint))
                try:
                    assignment_request=requests.post(assignment_endpoint,headers=headers,json=managed_test_developers_backend)
                    print(json.loads(assignment_request.text))
                except Exception as e:
                    print(e)
        if space['name']==domain+" - DEV":
            if group_name==domain+" - Developers":
                print("Space {}, Developer Assignment: {}, assignment url {}".format(space['name'],shared_dev_developers,assignment_endpoint))
                try:
                    assignment_request=requests.post(assignment_endpoint,headers=headers,json=shared_dev_developers)
                    print(json.loads(assignment_request.text))
                except Exception as e:
                    print(e)
        if space['name']==domain+" - DEV - BACKEND":
            if group_name==domain+" - Developers":
                print("Space {}, Developer Assignment: {}, assignment url {}".format(space['name'],shared_dev_developers_backend,assignment_endpoint))
                try:
                    assignment_request=requests.post(assignment_endpoint,headers=headers,json=shared_dev_developers_backend)
                    print(json.loads(assignment_request.text))
                except Exception as e:
                    print(e)
        if space['name']==domain+" - DEV - SHARED DATA":
            if group_name==domain+" - Developers":
                print("Space {}, Developer Assignment: {}, assignment url {}".format(space['name'],shared_dev_developers_shared,assignment_endpoint))
                try:
                    assignment_request=requests.post(assignment_endpoint,headers=headers,json=shared_dev_developers_shared)
                    print(json.loads(assignment_request.text))
                except Exception as e:
                    print(e)
        




def list_spaces(environment):
    print("----------------------------------------")
    api_key=get_apikey(environment)
    tenant=get_tenant(environment)
    headers={
        "Authorization": "Bearer {}".format(api_key),
        "Content-Type": "application/json"
    }
    endpoint="{}/api/v1/spaces".format(tenant)
    all_spaces=[]
    try:
        while endpoint:
            time.sleep(0.3)
            r = requests.get(endpoint,headers=headers)
            all_spaces.extend(json.loads(r.text)['data'])
            print(json.loads(r.text))
            if 'next' in json.loads(r.text)['links'].keys():
                endpoint=json.loads(r.text)['links']['next']['href']
            else:
                endpoint=None
        sorted_data = sorted(all_spaces, key=lambda x: x["name"])
        return sorted_data
    except Exception as e:
        print(e)





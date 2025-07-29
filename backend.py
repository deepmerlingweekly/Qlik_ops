import requests
import json
from dotenv import load_dotenv
import os
import logging
from logging import getLogger
import time

load_dotenv()

def create_qlik_space(environment,space):
    #app_logger.info(space)
    if environment=='prod':
        tenant=os.getenv('prod_tenant')
        api_key=os.getenv('prod_api_key')
    if environment=='test':
        tenant=os.getenv('test_tenant')
        api_key=os.getenv('test_api_key')
        
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
        print('error')
        print(e)

def tenant_default_assignment(environment,spaceid):
    if environment=='prod':
        tenant=os.getenv('prod_tenant')
        api_key=os.getenv('prod_api_key')
        assigneeId_tenant_admin=os.getenv('prod_assigneeId_tenant_admin')
    if environment=='test':
        tenant=os.getenv('test_tenant')
        api_key=os.getenv('test_api_key')
        assigneeId_tenant_admin=os.getenv('test_assigneeId_tenant_admin')
    headers={
        "Authorization": "Bearer {}".format(api_key),
        "Content-Type": "application/json"
    }
    endpoint="{}/api/v1/spaces".format(tenant)
    assignment_endpoint="{}/{}/assignments".format(endpoint,spaceid)
    print(assigneeId_tenant_admin)
    print(tenant)
    print(os.getenv('test_assigneeId_tenant_admin'))
    print(assignment_endpoint)
    assignment_payload={"type":"group","roles":["consumer","facilitator"],"assigneeId":assigneeId_tenant_admin}
    print(assignment_payload)
    try:
        r = requests.post(assignment_endpoint,headers=headers,json=assignment_payload)
        print(json.loads(r.text))
        #return json.loads(r.text)
    except Exception as e:
        print(e)


def list_spaces(environment):
    print("----------------------------------------")
    if environment=='prod':
        tenant=os.getenv('prod_tenant')
        api_key=os.getenv('prod_api_key')
    if environment=='test':
        tenant=os.getenv('test_tenant')
        api_key=os.getenv('test_api_key')
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





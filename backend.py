import requests
import json
from dotenv import load_dotenv
import os
import logging
from logging import getLogger

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
        print(json.loads(r.text))
        return json.loads(r.text)
    except Exception as e:
        print(e)

def tenant_default_assignment(environment,spaceid):
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
    assignment_endpoint="{}/{}/assignments".format(endpoint,spaceid)
    assignment_payload={"type":"group","roles":["consumer","facilitator"],"assigneeId":os.getenv("assigneeId_tenant_admin_prod")}
    try:
        r = requests.post(assignment_endpoint,headers=headers,json=assignment_payload)
        print(json.loads(r.text))
        return json.loads(r.text)
    except Exception as e:
        print(e)


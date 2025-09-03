import streamlit as st
#import pandas as pd
import backend
import json

import logging
from logging import getLogger

app_logger = getLogger()
app_logger.setLevel(logging.INFO)


st.title("Qlik-Ops Space Manager")
col1, col2 = st.columns(2)

with col2:
     container = st.container(border=True,height=650)

if 'environment' not in st.session_state:
    st.session_state.environment = 'test'
if 'space_list' not in st.session_state:
    st.session_state.space_list = []
if 'ambiente' not in st.session_state:
    st.session_state.dominio = ""
if 'dominio' not in st.session_state:
    st.session_state.dominio = ""
# if 'api_key' not in st.session_state:
#     st.session_state.api_key = ""
if 'space_dev' not in st.session_state:
    st.session_state.space_dev = {}
if 'space_dev_backend' not in st.session_state:
    st.session_state.space_dev_backend = {}
if 'space_dev_shared' not in st.session_state:
    st.session_state.space_dev_shared = {}
if 'space_test' not in st.session_state:
    st.session_state.space_test = {}
if 'space_test_backend' not in st.session_state:
    st.session_state.space_test_backend = {}
if 'space_test_shared' not in st.session_state:
    st.session_state.space_test_shared = {}
if 'space_prod' not in st.session_state:
    st.session_state.space_prod = {}
if 'space_prod_backend' not in st.session_state:
    st.session_state.space_prod_backend = {}
if 'space_prod_shared' not in st.session_state:
    st.session_state.space_prod_shared = {}


def print_creating_space():
    st.session_state.space_list=[]
    if st.session_state.dominio != "":
        container.write("saranno creati i seguenti spazi in ambiente "+st.session_state.environment)
        for i in st.session_state.keys():
            if i.startswith('space_'):
                    if 'name' in st.session_state[i]:
                        if st.session_state[i]['name'] != '':
                            
                            container.write(st.session_state[i])
                            st.session_state.space_list.append(st.session_state[i])              
    else:
        st.warning('Attenzione, il dominio deve essere valorizzato', icon="⚠️")

def create_space_from_list(space_list):
    #app_logger.info(space_list)
    for space in space_list:
        print(space)
        try:
            res=backend.create_qlik_space(st.session_state.environment,space,st.session_state.dominio)
            col2.write("spazio {} creato".format(res['name']))
        except Exception as e:
             print(e)
             st.error(e)
    print("---------------------------------------")

environment = col1.toggle("PROD",help="Indica in quale Tenant (Prod/Test) eseguire la creazione. Default è test")
dominio = col1.text_area("Dominio",st.session_state.dominio,help="con 'dominio applicativo' si intende un gruppo di app Qlik Sense che nel loro insieme costituiscono un dominio di analisi (dati comuni, use case comune, stesso 'dominio progettuale', stesso team business di riferimento")
if dominio:
    st.session_state.dominio = dominio
dev = col1.toggle("DEV (shared)")
dev_backend = col1.toggle("DEV BACKEND (shared)")
dev_shared = col1.toggle("DEV SHARED (shared)")
test = col1.toggle("TEST (managed)")
test_backend = col1.toggle("TEST BACKEND (managed)")
test_shared = col1.toggle("TEST SHARED (managed)")
prod = col1.toggle("PROD (managed)")
prod_backend = col1.toggle("PROD BACKEND (managed)")
prod_shared = col1.toggle("PROD SHARED (managed)")
if col1.button("Visualizza Spazi da creare",type="primary"):
     print_creating_space()
if col1.button("Crea space", type="primary"):
     create_space_from_list(st.session_state.space_list)


if environment:
    st.session_state.environment = 'prod'
else:
    st.session_state.environment = 'test'

if dev:
    if st.session_state.dominio != "":
            st.session_state.space_dev={"name":"{} - DEV".format(st.session_state.dominio),"type":"shared","description":""}
    else:
        st.warning('Attenzione, l\' dominio deve essere valorizzato', icon="⚠️")
if not dev:
    st.session_state.space_dev={}

if dev_backend:
    if st.session_state.dominio != "":
            st.session_state.space_dev_backend={"name":"{} - DEV - BACKEND".format(st.session_state.dominio),"type":"shared","description":""}
    else:
        st.warning('Attenzione, l\' dominio deve essere valorizzato', icon="⚠️")
if not dev_backend:
    st.session_state.space_dev_backend={}

if dev_shared:
    if st.session_state.dominio != "":
            st.session_state.space_dev_shared={"name":"{} - DEV - SHARED DATA".format(st.session_state.dominio),"type":"shared","description":""}
    else:
        st.warning('Attenzione, l\' dominio deve essere valorizzato', icon="⚠️")
if not dev_shared:
    st.session_state.space_dev_shared={}

#TEST
if test:
    if st.session_state.dominio != "":
            st.session_state.space_test={"name":"{} - TEST".format(st.session_state.dominio),"type":"managed","description":""}
    else:
        st.warning('Attenzione, l\' dominio deve essere valorizzato', icon="⚠️")
if not test:
    st.session_state.space_test={}

if test_backend:
    if st.session_state.dominio != "":
            st.session_state.space_test_backend={"name":"{} - TEST - BACKEND".format(st.session_state.dominio),"type":"managed","description":""}
    else:
        st.warning('Attenzione, l\' dominio deve essere valorizzato', icon="⚠️")
if not test_backend:
    st.session_state.space_test_backend={}

if test_shared:
    if st.session_state.dominio != "":
            st.session_state.space_test_shared={"name":"{} - TEST - SHARED DATA".format(st.session_state.dominio),"type":"managed","description":""}
    else:
        st.warning('Attenzione, l\' dominio deve essere valorizzato', icon="⚠️")
if not test_shared:
    st.session_state.space_test_shared={}

#PROD
if prod:
    if st.session_state.dominio != "":
            st.session_state.space_prod={"name":"{}".format(st.session_state.dominio),"type":"managed","description":""}
    else:
        st.warning('Attenzione, l\' dominio deve essere valorizzato', icon="⚠️")
if not prod:
    st.session_state.space_prod={}

if prod_backend:
    if st.session_state.dominio != "":
            st.session_state.space_prod_backend={"name":"{} - BACKEND".format(st.session_state.dominio),"type":"managed","description":""}
    else:
        st.warning('Attenzione, l\' dominio deve essere valorizzato', icon="⚠️")
if not prod_backend:
    st.session_state.space_prod_backend={}

if prod_shared:
    if st.session_state.dominio != "":
            st.session_state.space_prod_shared={"name":"{} - SHARED DATA".format(st.session_state.dominio),"type":"managed","description":""}
    else:
        st.warning('Attenzione, l\' dominio deve essere valorizzato', icon="⚠️")
if not prod_shared:
    st.session_state.space_prod_shared={}





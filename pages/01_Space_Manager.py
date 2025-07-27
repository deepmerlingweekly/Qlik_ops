import streamlit as st
import pandas as pd
import requests
import json
import boto3
import os
import time

st.title("Qlik-Ops Space Manager")
col1, col2 = st.columns(2)

# if 'thespace_list' not in st.session_state:
#     st.session_state.thespace_list = []
if 'ambito' not in st.session_state:
    st.session_state.ambito = ""
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
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


#container = st.container(border=True)
#col1, col2 = st.columns(2)

#container.write(st.session_state.space_list)
#st.session_state.space_list = list(filter(lambda d: d.get('name') != "{} - DEV".format(st.session_state.ambito), st.session_state.space_list))

def print_creating_space():
    if st.session_state.ambito != "":
        for i in st.session_state.keys():
            if i.startswith('space_'):
                    if 'name' in st.session_state[i]:
                        col2.write(st.session_state[i]['name']+","+st.session_state[i]['type'])
        col2.button("Crea space", type="primary",on_click=create_space)                
    else:
        st.warning('Attenzione, l\' Ambito deve essere valorizzato', icon="⚠️")

def clear_space():
    st.session_state.space_list = []

def create_space():
    if st.session_state.ambito != "":
        for i in st.session_state.keys():
            if i.startswith('space_'):
                    if 'name' in st.session_state[i]:
                        col2.write(st.session_state[i]['name']+","+st.session_state[i]['type']+" Creato!")
    else:
        st.warning('Attenzione, l\' Ambito deve essere valorizzato', icon="⚠️")

api_key = col1.text_area("ApiKey: ",st.session_state.api_key,help="Inserire qui una API Key di un utente con permessi di creazione Spazi e Gruppi")
ambito = col1.text_area("Dominio",st.session_state.api_key,help="con 'dominio applicativo' si intende un gruppo di app Qlik Sense che nel loro insieme costituiscono un dominio di analisi (dati comuni, use case comune, stesso 'ambito progettuale', stesso team business di riferimento")
if ambito:
    st.session_state.ambito = ambito
dev = col1.toggle("DEV (shared)")
dev_backend = col1.toggle("DEV BACKEND (shared)")
dev_shared = col1.toggle("DEV SHARED (shared)")
test = col1.toggle("TEST (managed)")
test_backend = col1.toggle("TEST BACKEND (managed)")
test_shared = col1.toggle("TEST SHARED (managed)")
prod = st.toggle("PROD (managed)")
prod_backend = col1.toggle("PROD BACKEND (managed)")
prod_shared = col1.toggle("PROD SHARED (managed)")
st.button("Visualizza Spazi da creare",type="secondary", on_click=print_creating_space)




if dev:
    if st.session_state.ambito != "":
            st.session_state.space_dev={"name":"{} - DEV".format(st.session_state.ambito),"type":"shared","description":""}
    else:
        st.warning('Attenzione, l\' Ambito deve essere valorizzato', icon="⚠️")
if not dev:
    st.session_state.space_dev={}

if dev_backend:
    if st.session_state.ambito != "":
            st.session_state.space_dev_backend={"name":"{} - DEV BACKEND".format(st.session_state.ambito),"type":"shared","description":""}
    else:
        st.warning('Attenzione, l\' Ambito deve essere valorizzato', icon="⚠️")
if not dev_backend:
    st.session_state.space_dev_backend={}

if dev_shared:
    if st.session_state.ambito != "":
            st.session_state.space_dev_shared={"name":"{} - DEV SHARED".format(st.session_state.ambito),"type":"shared","description":""}
    else:
        st.warning('Attenzione, l\' Ambito deve essere valorizzato', icon="⚠️")
if not dev_shared:
    st.session_state.space_dev_shared={}

#TEST
if test:
    if st.session_state.ambito != "":
            st.session_state.space_test={"name":"{} - TEST".format(st.session_state.ambito),"type":"managed","description":""}
    else:
        st.warning('Attenzione, l\' Ambito deve essere valorizzato', icon="⚠️")
if not test:
    st.session_state.space_test={}

if test_backend:
    if st.session_state.ambito != "":
            st.session_state.space_test_backend={"name":"{} - TEST BACKEND".format(st.session_state.ambito),"type":"managed","description":""}
    else:
        st.warning('Attenzione, l\' Ambito deve essere valorizzato', icon="⚠️")
if not test_backend:
    st.session_state.space_test_backend={}

if test_shared:
    if st.session_state.ambito != "":
            st.session_state.space_test_shared={"name":"{} - TEST SHARED".format(st.session_state.ambito),"type":"managed","description":""}
    else:
        st.warning('Attenzione, l\' Ambito deve essere valorizzato', icon="⚠️")
if not test_shared:
    st.session_state.space_test_shared={}

#PROD
if prod:
    if st.session_state.ambito != "":
            st.session_state.space_prod={"name":"{}".format(st.session_state.ambito),"type":"managed","description":""}
    else:
        st.warning('Attenzione, l\' Ambito deve essere valorizzato', icon="⚠️")
if not prod:
    st.session_state.space_prod={}

if prod_backend:
    if st.session_state.ambito != "":
            st.session_state.space_prod_backend={"name":"{} - BACKEND".format(st.session_state.ambito),"type":"managed","description":""}
    else:
        st.warning('Attenzione, l\' Ambito deve essere valorizzato', icon="⚠️")
if not prod_backend:
    st.session_state.space_prod_backend={}

if prod_shared:
    if st.session_state.ambito != "":
            st.session_state.space_prod_shared={"name":"{} - SHARED".format(st.session_state.ambito),"type":"managed","description":""}
    else:
        st.warning('Attenzione, l\' Ambito deve essere valorizzato', icon="⚠️")
if not prod_shared:
    st.session_state.space_prod_shared={}


# assigneeId_tenant_admin_prod="681a1bde0c8be1507615d804"





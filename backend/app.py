import streamlit as st
import os
from dotenv import load_dotenv
import sqlite3
import backend

#load_dotenv('/mnt/.env')

def main():
    print("Qlik-ops utility")

    st.title("Qlil-Ops Utility")
    st.write("This utility is designed to help manage Qlik-Ops operations.")
    st.write("Use the sidebar to navigate through different functionalities.")
    st.sidebar.title("Navigation")
    st.sidebar.write("Select a page to manage spaces, groups")  
    st.sidebar.write("Currently, the utility supports space management, group management")
    st.image("resources\\backend\\space_everywhere.png")
    container = st.container(border=True)
    con = sqlite3.connect("qlik_ops.db")
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS settings (id TEXT NOT NULL PRIMARY KEY, tenant TEXT, environment TEXT, apikey TEXT,assigneeId_tenant_admin TEXT);')
    res = cur.execute('select count(*) as tot from settings')
    con.commit()
    if res.fetchall()[0][0]==0:
        st.write("Salverò il DB in:", os.path.abspath("qlik_ops.db"))
        cur.execute('INSERT INTO settings(id, tenant, environment, apikey, assigneeId_tenant_admin) VALUES ("01","https://mediaset.eu.qlikcloud.com","prod","","681a1bde0c8be1507615d804")')
        cur.execute('INSERT INTO settings(id, tenant, environment, apikey,assigneeId_tenant_admin) VALUES ("02","https://mediaset-test.eu.qlikcloud.com","test","","67e289759be3e7c7be680e45")')
        con.commit()
    con.close()
    if 'prod_api_key' not in st.session_state:
        st.session_state.prod_api_key = ""
    if 'test_api_key' not in st.session_state:
        st.session_state.test_api_key = ""
    
    with st.form("Configura API KEY PROD"):
        prod_apikey_input = st.text_area("prod_api_key",st.session_state.prod_api_key)
        if prod_apikey_input:
            st.session_state.prod_api_key = prod_apikey_input
        submitted1 = st.form_submit_button("Salva API KEY PROD")
        if submitted1:
            con = sqlite3.connect("qlik_ops.db")
            cur = con.cursor()
            update_query = '''
                UPDATE settings
                SET apikey = ?
                WHERE id = ?
                '''
            cur.execute(update_query, (st.session_state.prod_api_key,"01"))
            con.commit()
            container.write(cur.execute('select * from settings'))
            con.close()
    with st.form("Configura API KEY TEST"):
        test_api_key_input = st.text_area("test_api_key",st.session_state.test_api_key)
        if test_api_key_input:
            st.session_state.test_api_key = test_api_key_input
        submitted2 = st.form_submit_button("Salva API KEY TEST")
        if submitted2:
            con = sqlite3.connect("qlik_ops.db")
            cur = con.cursor()
            update_query = '''
                UPDATE settings
                SET apikey = ?
                WHERE id = ?
                '''
            cur.execute(update_query, (st.session_state.test_api_key,"02"))
            con.commit()
            container.write()
            con.close()
    if st.button("Visualizza configurazione attuale",type="primary"):
        st.write(backend.show_current_settings())
        
if __name__ == "__main__":
    main()

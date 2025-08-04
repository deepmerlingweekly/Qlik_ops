import streamlit as st
import os
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy import insert
load_dotenv('/mnt/.env')

def main():
    print("Qlik-ops utility")

    st.title("Qlil-Ops Utility")
    st.write("This utility is designed to help manage Qlik-Ops operations.")
    st.write("Use the sidebar to navigate through different functionalities.")
    st.sidebar.title("Navigation")
    st.sidebar.write("Select a page to manage spaces, groups")  
    st.sidebar.write("Currently, the utility supports space management, group management")
    st.image("space_everywhere.png")    
    st.sidebar.write(os.getenv('prod_tenant'))
    st.sidebar.write(os.getenv('test_tenant'))
    st.sidebar.write(os.getenv('test_api_key'))
    st.sidebar.write(os.getenv('prod_api_key'))

    # Create the SQL connection to pets_db as specified in your secrets file.
    conn = st.connection('qlik_ops_db', type='sql')

    # Insert some data with conn.session.
    
    with conn.session as s:
        s.execute(text('CREATE TABLE IF NOT EXISTS settings (id TEXT, tenant TEXT, environment TEXT, apikey TEXT);'))
        s.execute(text('''INSERT INTO settings(id, tenant, environment, apikey) VALUES (:id, :tenant, :environment, :apikey)'''),
                    {
                        'id': '01',
                        'tenant': 'mediaset.eu.qlikcloud.com',
                        'environment': 'prod',
                        'apikey': ""
                        }
                )
        
        s.execute(text('''INSERT INTO settings(id, tenant, environment, apikey) VALUES (:id, :tenant, :environment, :apikey)'''),
                    {
                        'id': '02',
                        'tenant': 'mediaset.eu.qlikcloud.com',
                        'environment': 'test',
                        'apikey': ""
                        }
                )
        s.commit()
        s.close()
    if 'prod_api_key' not in st.session_state:
        st.session_state.prod_api_key = ""
    if 'test_api_key' not in st.session_state:
        st.session_state.test_api_key = ""
    
    with st.form("set_prod_api_key"):
        prod_apikey_input = st.text_area("prod_api_key",st.session_state.prod_api_key)
        if prod_apikey_input:
            st.session_state.prod_api_key = prod_apikey_input
        submitted1 = st.form_submit_button("Salva API KEY PROD")
        if submitted1:
            with conn.session as s:
                s.execute(text("""
                    UPDATE settings
                    SET apikey = :new_apikey
                    WHERE id = :id_value
                """), {
                    "new_apikey": st.session_state.prod_api_key,
                    "id_value": "01"
                })
                s.commit()
                
                settings_conn=conn.query('select * from settings')
                st.dataframe(settings_conn)
                s.close()
    with st.form("set_test_api_key"):
        test_api_key_input = st.text_area("test_api_key",st.session_state.test_api_key)
        if test_api_key_input:
            st.session_state.test_api_key = test_api_key_input
        submitted2 = st.form_submit_button("Salva API KEY TEST")
        if submitted2:
            with conn.session as s:
                s.execute(text("""
                    UPDATE settings
                    SET apikey = :new_apikey
                    WHERE id = :id_value
                """), {
                    "new_apikey": st.session_state.test_api_key,
                    "id_value": "02"
                })
                s.commit()
                settings_conn=conn.query('select * from settings')
                st.dataframe(settings_conn)
                s.close()
if __name__ == "__main__":
    main()

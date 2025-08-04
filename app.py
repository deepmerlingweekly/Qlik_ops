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
        s.execute("""INSERT INTO settings(id,tenant,environment,apikey) VALUES (?,?)""", ("01", "mediaset.eu.qlikcloud.com","apikey"))
        s.execute("""INSERT INTO settings(id,tenant,environment,apikey) VALUES (?,?)""", ("02", "mediaset-test.eu.qlikcloud.com","apikey"))
        s.commit()

    # Query and display the data you inserted
    settings_conn=conn.query('select * from settings')
    st.dataframe(settings_conn)
if __name__ == "__main__":
    main()

import streamlit as st
import os
from dotenv import load_dotenv
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

if __name__ == "__main__":
    main()

import streamlit as st
def main():
    print("Qlil-ops utility")

    st.title("Qlil-Ops Utility")
    st.write("This utility is designed to help manage Qlik-Ops operations.")
    st.write("Use the sidebar to navigate through different functionalities.")
    st.sidebar.title("Navigation")
    st.sidebar.write("Select a page to manage spaces, groups")  
    st.sidebar.write("Currently, the utility supports space management, group management")


if __name__ == "__main__":
    main()

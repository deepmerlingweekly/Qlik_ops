import streamlit as st
import backend
st.title("Qlik-Ops Group Manager")

#st.session_state

if 'environment_group' not in st.session_state:
    st.session_state.environment_group = 'test'

col1, col2 = st.columns(2)

with col2:
     container = st.container(border=True,height=650)

environment_group = col1.toggle("PROD")
if environment_group:
    st.session_state.environment_group = 'prod'
else:
    st.session_state.environment_group = 'test'

if col1.button("Visualizza Spazi",type="primary"):
    current_space=backend.list_spaces(st.session_state.environment_group)
    for space in current_space:
        container.checkbox(space['name'])
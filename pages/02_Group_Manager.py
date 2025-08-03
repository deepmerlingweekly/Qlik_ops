import streamlit as st
import backend
st.title("Qlik-Ops Group Manager")

#st.session_state

if 'environment_group' not in st.session_state:
    st.session_state.environment_group = 'test'
if 'dominio_group' not in st.session_state:
    st.session_state.dominio_group = ""
if 'group_cat' not in st.session_state:
    st.session_state.group_cat = []

# col1, col2 = st.columns(2)

# with col2:
#      container = st.container(border=True,height=650)

environment_group = st.toggle("PROD",help="Indica in quale Tenant (Prod/Test) eseguire la creazione. Default è test")
if environment_group:
    st.session_state.environment_group = 'prod'
else:
    st.session_state.environment_group = 'test'

# if col1.button("Visualizza Spazi",type="primary"):
#     current_space=backend.list_spaces(st.session_state.environment_group)
#     for space in current_space:
#         container.checkbox(space['name'])


with st.form("my_form"):
    dominio_group = st.text_area("Dominio",st.session_state.dominio_group,help="con 'dominio applicativo' si intende un gruppo di app Qlik Sense che nel loro insieme costituiscono un dominio di analisi (dati comuni, use case comune, stesso 'dominio progettuale', stesso team business di riferimento")
    if dominio_group:
        st.session_state.dominio_group = dominio_group
    checkbox_consumer = st.checkbox("consumer")
    checkbox_tester = st.checkbox("tester")
    checkbox_developer = st.checkbox("developer")
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.session_state.group_cat = []
        if checkbox_consumer:
            st.session_state.group_cat.append('Consumers')
        if checkbox_tester:
            st.session_state.group_cat.append('Tester')
        if checkbox_developer:
            st.session_state.group_cat.append('Developer')
        st.write("saranno creati i seguenti gruppi:")
        print(st.session_state.group_cat)
        for category in st.session_state.group_cat:
            st.write(st.session_state.dominio_group+" - "+category)
            backend.default_group_creation(st.session_state.environment_group,st.session_state.dominio_group,category)

import streamlit as st
from src.api.subjects import create_subject



@st.dialog("Create New Subject")
def create_subject_dialog():
    st.write("Enter the details of new subject")
    sub_id = st.text_input("Subject Code", placeholder="CS101")
    sub_name = st.text_input("Subject Name", placeholder="Introduction to Computer Science")
    sub_section = st.text_input("Section", placeholder="A")


    if st.button("Create Subject Now", type='primary', width='stretch'):
        if sub_id and sub_name and sub_section:
            token = st.session_state.access_token
            try:
                create_subject(token,sub_id, sub_name, sub_section)
                st.toast("Subject Created Succesfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please fill all the fields")
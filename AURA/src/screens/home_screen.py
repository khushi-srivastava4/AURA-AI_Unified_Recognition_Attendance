import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout ,  style_background_home
from src.core.session import switch_role

def home_screen():

    header_home()

    style_base_layout()
    style_background_home()

    with st.container(key="role_cards"):
        col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("I'm Teacher")
        st.image("assets/teacher.jpg", width=135)
        if st.button('Teacher Portal', icon=':material/arrow_outward:' , icon_position='right'):
            switch_role("teacher")
            st.rerun()
    with col2:
        st.header("I'm Student")
        st.image("assets/student.jpg", width=135)
        if st.button('Student Portal', icon=':material/arrow_outward:' , icon_position='right'):
            switch_role("student")
            st.rerun()
    footer_home()



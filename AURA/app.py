
import streamlit as st

from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen

from src.components.dialog_auto_enroll import auto_enroll_dialog
from src.core.session import switch_role

def main():
    logo_path="assets/aura_logo.png"
    st.set_page_config(
        page_title='AURA - AI Unified Recognition Attendance',
        page_icon= logo_path
    )
    if 'login_type' not in st.session_state:
        st.session_state['login_type']=None

    join_code = st.query_params.get("join-code")

    if join_code and st.session_state["login_type"] != "student":
        switch_role("student")
        st.rerun()


    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()
        case 'student':
            student_screen()
        case None:
            home_screen()

    if (
        join_code
        and st.session_state.get("is_logged_in")
        and st.session_state.get("user_role") == "student"
    ):
        auto_enroll_dialog(join_code)
    
main()
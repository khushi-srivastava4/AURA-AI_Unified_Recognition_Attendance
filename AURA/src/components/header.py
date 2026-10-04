import streamlit as st
from src.core.session import clear_auth_session

def header_home():
    logo_path="assets/aura_logo.png"

    img_col1, img_col2, img_col3 = st.columns([2, 1, 2])
    with img_col2:
        st.image(logo_path, width=150)

    st.markdown(f"""
    <div class="aura-title" style='display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:30px; margin-top:30px;'>
        <h1 style='text-align:center; color:#ECE7D1'>AURA</h1>
    </div>
        
    """, unsafe_allow_html=True)

def header_dashboard(current_role=None):
    logo_path="assets/aura_logo.png"

    col1, col2, col3 = st.columns([1,2,1])

    with col1:
        st.image(logo_path, width=100)

    with col2:
        st.markdown("""
            <div class="dashboard-aura">
                <h2>AURA</h2>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        if st.button("Go back to Home",key="back_home",shortcut="escape",width="stretch"):
            clear_auth_session()           
            st.session_state['login_type'] = None
            st.rerun()

        # Show Logout ONLY if the user is logged into
        # the role whose screen is currently being displayed
        if current_role == "teacher" and "teacher_data" in st.session_state:

            if st.button(
                "Logout",
                key="teacher_logout",
                shortcut="control+backspace",
                width="stretch"
            ):
                clear_auth_session()
                st.session_state["login_type"] = None
                st.rerun()

        elif current_role == "student" and "student_data" in st.session_state:

            if st.button(
                "Logout",
                key="student_logout",
                shortcut="control+backspace",
                width="stretch"
            ):
                clear_auth_session()
                st.session_state["login_type"] = None
                st.rerun()
        




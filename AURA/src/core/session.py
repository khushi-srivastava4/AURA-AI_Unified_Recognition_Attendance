import streamlit as st


def clear_auth_session():
    """Clear all authentication-related session state."""

    keys_to_remove = [
        "access_token",
        "teacher_data",
        "student_data",
        "user_role",
        "is_logged_in",
        "teacher_login_type",
    ]

    for key in keys_to_remove:
        st.session_state.pop(key, None)


def switch_role(role):
    """Clear current authentication and switch to a new portal."""

    clear_auth_session()

    st.session_state["login_type"] = role
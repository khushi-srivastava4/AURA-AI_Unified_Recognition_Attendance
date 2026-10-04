import streamlit as st
from src.api.enrollments import enroll_subject
import time


@st.dialog("Enroll in Subject")
def enroll_dialog():

    st.write(
        "Enter the subject code provided by your teacher to enroll"
    )

    subject_code = st.text_input(
        "Subject Code",
        placeholder="Eg. CS101"
    )

    if st.button(
        "Enroll now",
        type="primary",
        width="stretch"
    ):

        if not subject_code:
            st.warning("Please enter a subject code")
            return

        try:
            token = st.session_state.access_token

            enroll_subject(
                token,
                subject_code
            )

            st.success("Successfully enrolled!")

            time.sleep(1)
            st.rerun()

        except Exception as e:
            st.error(f"Enrollment failed: {str(e)}")
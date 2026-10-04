import streamlit as st
from src.api.enrollments import enroll_subject

import time


@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):

    st.write(
        f"Would you like to enroll in subject **{subject_code}**?"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("No thanks", width="stretch"):
            st.query_params.clear()
            st.rerun()

    with col2:
        if st.button(
            "Yes enroll now!",
            type="primary",
            width="stretch"
        ):
            try:
                token = st.session_state.access_token

                enroll_subject(
                    token,
                    subject_code
                )

                st.success("Joined successfully!")
                st.query_params.clear()

                time.sleep(1)
                st.rerun()

            except Exception as e:
                error = str(e)

                if "409" in error:
                    st.info("You are already enrolled!")

                elif "404" in error:
                    st.error("Subject Code not found!")

                else:
                    st.error(f"Enrollment failed: {error}")
import streamlit as st

from src.api.attendance import create_attendance


def show_attendance_result(df, logs):
    st.write("Please review attendance before confirming.")
    st.dataframe(df, hide_index=True, width="stretch")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Discard", width="stretch"):
            st.session_state.attendance_images = []
            st.session_state.pop("voice_attendance_results", None)
            st.rerun()

    with col2:
        if st.button(
            "Confirm & Save",
            width="stretch",
            type="primary"
        ):
            try:
                token = st.session_state.access_token

                for log in logs:
                    create_attendance(
                        token=token,
                        subject_id=log["subject_id"],
                        student_id=log["student_id"],
                        is_present=log["is_present"],
                        timestamp=log["timestamp"]
                    )

                st.toast("Attendance taken successfully!")

                st.session_state.attendance_images = []
                st.session_state.pop("voice_attendance_results", None)

                st.rerun()

            except Exception as e:
                st.error(f"Sync failed! {e}")


@st.dialog("Attendance Reports")
def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs)
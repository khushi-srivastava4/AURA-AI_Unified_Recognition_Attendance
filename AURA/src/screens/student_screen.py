import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.api.students import create_student
from src.api.attendance import get_student_attendance
from src.api.enrollments import get_my_subjects, unenroll_subject
from src.api.student_auth import student_face_login
import time

from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card

def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    header_dashboard(current_role="student")
    st.subheader(f"""Welcome, {student_data['name']} """)

    st.space()

    c1, c2 =st.columns(2)
    with c1:
        st.header('Your Enrolled Subjects')
    with c2:
        if st.button('Enroll in Subject', type='primary', width='stretch'):
            enroll_dialog()


    st.divider()


    with st.spinner('Loading your enrolled subjects..'):
        token = st.session_state.access_token
        subjects = get_my_subjects(token)
        logs = get_student_attendance(token)
    if not subjects:
        st.info("You haven't enrolled in any subjects yet. Please enroll in a subject to start tracking your attendance.")
        footer_dashboard()
        return
    stats_map = {}

    for log in logs:
        sid = log['subject_id']

        if sid not in stats_map:
            stats_map[sid] = {"total":0, "attended": 0}

        stats_map[sid]['total'] +=1

        if log.get('is_present'):
            stats_map[sid]['attended'] += 1


    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']

        stats = stats_map.get(sid,{"total":0, "attended": 0} )

        def unenroll_button(subject_id=sid, subject_name=sub['name']):
            if st.button("Unenroll from this course", key=f"unenroll_{student_id}_{subject_id}", type='tertiary', width='stretch', icon=':material/delete_forever:'):
                token = st.session_state.access_token
                unenroll_subject(token, subject_id)
                st.toast(f'Unenrolled from {subject_name} successfully!')
                st.rerun()

        with cols[i % 2]:

            subject_card(
                name = sub['name'],
                code =sub['subject_code'],
                section = sub['section'],
                stats = [
                    ('📅', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended']),
                ],
                footer_callback=unenroll_button
            )
    footer_dashboard()


def student_screen():

    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    header_dashboard(current_role=None)

    st.header("Login using FaceID", text_alignment="center")

    show_registration=False
   
    st.markdown(
        '<div class="face-camera-label">Position your face in the center</div>',
        unsafe_allow_html=True
    )

    photo_source = st.camera_input(
        "Camera",
        label_visibility="collapsed"
    )

    if photo_source:
        img= np.array(Image.open(photo_source))
        with st.spinner("AI is scanning..."):
            encodings = get_face_embeddings(img)

            if len(encodings) == 0:
                st.warning("Face not found!")
            elif len(encodings) > 1:
                st.warning("Multiple faces found!")
            else:
                try:
                    face_embedding = encodings[0].tolist()

                    login_response = student_face_login(
                        face_embedding
                    )

                    student = login_response["student"]

                    st.session_state.access_token = login_response["access_token"]
                    st.session_state.is_logged_in = True
                    st.session_state.user_role = "student"
                    st.session_state.student_data = student

                    st.toast(
                        f"Welcome Back, {student['name']}!"
                    )

                    time.sleep(1)
                    st.rerun()

                except Exception as e:
                    if "401" in str(e):
                        st.error("Face not recognized. Please try again.")
                    else:
                        st.error(f"Face login failed: {e}")
    if show_registration:
        with st.container(border=True):
            st.header("Register new profile")
            new_name=st.text_input("Enter your name", placeholder="E.g. Isha Raut")

            st.header("Optional : Voice Enrollment")
            st.markdown(
                '<div class="voice-enrollment-text">Enroll yourself for voice only attendance</div>',
                unsafe_allow_html=True
            )
            audio_data=None

            try:
                st.markdown(
                    '<div class="voice-record-label">Record a short phrase like I am present, My name is Isha.</div>',
                    unsafe_allow_html=True
                )
                audio_data = st.audio_input("")
            except Exception:
                st.error("Audio Data failed!")

            if st.button("Create Account", type="primary"):
                if new_name:
                    with st.spinner("Creating profile.."):
                        img=np.array(Image.open(photo_source))
                        encodings=get_face_embeddings(img)
                        if encodings:
                            face_emb=encodings[0].tolist()

                            voice_emb=None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())

                            response_data=create_student(new_name,face_embedding=face_emb, voice_embedding=voice_emb)

                            if response_data:
                                train_classifier(st.session_state.access_token)
                                st.session_state.is_logged_in=True
                                st.session_state.user_role="student"
                                st.session_state.student_data=response_data
                                st.toast(f"Profile created! Hi {new_name}!")
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error("Couldnt capture your facial features for registration")
                                
                else:
                    st.warning("Please enter your name.")



    footer_dashboard()
import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.api.auth import teacher_login, teacher_register
from src.api.subjects import get_teacher_subjects
from src.api.subjects import get_subject_students
from src.api.attendance import get_teacher_attendance
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog

from datetime import datetime
from zoneinfo import ZoneInfo

from src.pipelines.face_pipeline import predict_attendance
from src.components.dialog_attendance_results import attendance_result_dialog
import numpy as np

from datetime import datetime

import pandas as pd


from src.components.dialog_voice_attendance import voice_attendance_dialog


def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif "teacher_login_type" not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type=="register":
        teacher_screen_register()   

def teacher_dashboard():
    teacher_data = st.session_state.teacher_data

    header_dashboard(current_role="teacher")

    st.subheader(f"""Welcome, {teacher_data['name']} """)

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'
    tab1, tab2, tab3 = st.columns(3)


    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('Take Attendance',type=type1, width='stretch', icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"
        if st.button('Manage Subjects', type=type2, width='stretch', icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "tertiary"
        if st.button('Attendance Records',type=type3, width='stretch', icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()


    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    


    footer_dashboard()


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('Take AI Attendance')


    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(
        st.session_state.access_token
    )

    if not subjects:
        st.markdown("""
        <div class="no-subjects-message" style="
            background-color: #85877D;
            padding: 20px 16px;">
            You have not created any subjects yet! Please create one to begin!
        </div>""", unsafe_allow_html=True)
        return
    
    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3,1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:', width='stretch'):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header('Added Photos')
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4 ]:
                st.image(img, width='stretch', caption=f'Photo {idx+1}')
    has_photos = bool(st.session_state.attendance_images)

    warning_placeholder = st.empty()

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button('Clear all photos', width='stretch', type='tertiary', icon=':material/delete:', disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()


    with c2:
        
        if st.button('Run Face Analysis', width='stretch', type='secondary', icon=':material/analytics:', disabled=not has_photos):
            with st.spinner('Deep scanning classroom photos...'):
                all_detected_ids = {}

                token = st.session_state.access_token
                
                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(img_np,token)


                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)

                            all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")

                token = st.session_state.access_token

                enrolled_students = get_subject_students(
                    token,
                    selected_subject_id
                )

                if not enrolled_students:
                    warning_placeholder.warning('No students enrolled in this course')
                else:

                    results, attendance_to_log  = [], []

                    current_timestamp = datetime.now(ZoneInfo("Asia/Kolkata")).isoformat()


                    for node in enrolled_students:
                        student = node['students']
                        sources = all_detected_ids.get(int(student['student_id']), [])
                        is_present= len(sources) > 0

                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Source": ", ".join(sources) if is_present else "-",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })

                    attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with c3:
        if st.button('Use Voice Attendance', type='primary', width='stretch', icon=':material/mic:'):
            voice_attendance_dialog(selected_subject_id)





def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2)
    with col1:
        st.header('Manage Subjects', width='stretch')

    with col2:
        if st.button('Create New Subject', width='stretch'):
            create_subject_dialog()


    # LIST all SUBJECTS
    subjects = get_teacher_subjects(
        st.session_state.access_token
    )
    if subjects:
        for sub in subjects:

            stats = [
                ("🫂", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats
            )

            if st.button(
                f"Share Code: {sub['name']}",
                key=f"share_{sub['subject_code']}",
                icon=":material/share:"
            ):
                share_subject_dialog(
                    sub['name'],
                    sub['subject_code']
                )
    else:
        st.markdown("""
        <div class="no-subjects-message" style="
            background-color: #85877D;
            padding: 20px 16px;">
            NO SUBJECTS FOUND. CREATE ONE ABOVE
        </div>""", unsafe_allow_html=True) 



def teacher_tab_attendance_records():
    st.header('Attendance Records')

    token = st.session_state.access_token

    records = get_teacher_attendance(token)

    if not records:
        st.markdown("""
        <div class="no-subjects-message" style="
            background-color: #85877D;
            padding: 20px 16px;">
            No records.
        </div>""", unsafe_allow_html=True)
        return
    
    data = []

    for r in records:
        ts = r.get('timestamp')

        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": (
                datetime.fromisoformat(ts)
                .astimezone(ZoneInfo("Asia/Kolkata"))
                .strftime("%Y-%m-%d %H:%M")
                if ts else "N'A"
            ),
            "Subject": r['subjects']['name'],
            "Subject Code":r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })


    df = pd.DataFrame(data)



    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count = ('is_present', 'sum'),
            Total_Count =('is_present', 'count')
        ).reset_index()

    )

    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + " /"
        + summary['Total_Count'].astype(str) + ' Students'
    )

    display_df = ( summary.sort_values(by='ts_group' ,ascending=False)
                  [['Time', 'Subject', 'Subject Code', 'Attendance Stats']]
                  )
    
    st.dataframe(display_df, width='stretch', hide_index=True)




def login_teacher(username,password):
    if not username or not password:
        return False
    
    try:
        response = teacher_login(username, password)

        st.session_state.user_role = "teacher"
        st.session_state.teacher_data = response["teacher"]
        st.session_state.access_token = response["access_token"]
        st.session_state.is_logged_in = True

        return True

    except Exception:
        return False

def teacher_screen_login():

    header_dashboard(current_role=None)

    st.header("Login using password", text_alignment="left")

    teacher_username=st.text_input("Enter username", placeholder="ishara")
    teacher_pass=st.text_input("Enter password", type="password", placeholder="Enter password")

    st.space()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button("Login" , icon=":material/passkey:", shortcut="control+enter", width="stretch"):
            if login_teacher(teacher_username,teacher_pass):
                st.toast(f"Welcome Back, {st.session_state.teacher_data['name']}!")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username and password")

    with btnc2:
        if st.button("Register Instead",type="primary" , icon=":material/passkey:", width="stretch"):
            st.session_state.teacher_login_type="register"
    
    footer_dashboard()





def register_teacher(
    teacher_username,
    teacher_name,
    teacher_pass,
    teacher_pass_confirm
):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All Fields are required!"

    if teacher_pass != teacher_pass_confirm:
        return False, "Password doesn't match"

    try:
        teacher_register(
            teacher_username,
            teacher_name,
            teacher_pass
        )

        return True, "Successfully created, Login now!"

    except Exception as e:
        error = str(e)

        if "409" in error:
            return False, "Username already taken"

        return False, "Unexpected Error!"

    
def teacher_screen_register():
    header_dashboard(current_role=None)
    
    st.header("Register your Teacher Profile", text_alignment="left")

    teacher_username=st.text_input("Enter username", placeholder="ishara")
    teacher_name=st.text_input("Enter name", placeholder="Isha Raut")
    teacher_pass=st.text_input("Enter password", type="password", placeholder="Enter password")
    teacher_pass_confirm=st.text_input("Confirm password", type="password", placeholder="Re-enter password")

    st.space()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button("Register now",type="primary" , icon=":material/passkey:", width="stretch"):
            success, message=register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type="login"
                st.rerun()
            else:
                st.error(message)

    with btnc2:
        if st.button("Login Instead" , icon=":material/passkey:", shortcut="control+enter", width="stretch"):
            st.session_state.teacher_login_type="login"
    
    footer_dashboard()



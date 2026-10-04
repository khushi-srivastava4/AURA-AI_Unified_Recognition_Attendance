import streamlit as st

def style_background_home():
    st.markdown(""" 
        <style>
                .stApp{
                    background: #8A7650 !important;
                }     

                .st-key-role_cards {
                    margin-top: -40px !important;
                }

                .st-key-role_cards div[data-testid="stColumn"]{
                    background-color:#ECE7D1 !important;
                    padding:2.5rem !important;
                    border-radius: 5rem !important;
                }                   
        </style>
                """, unsafe_allow_html=True)
    
def style_background_dashboard():
    st.markdown(""" 
        <style>
                .stApp{
                    background: #ECE7D1 !important;
                }     

                .dashboard-footer {   
                    color: #8E977D !important;
                }

                .dashboard-aura {
                    display: flex !important;
                    align-items: center !important;
                    justify-content: center !important;
                    height: 100% !important;
                    margin-top: 5px !important;
                    transform: translateX(-130px) !important;   
                }

                .dashboard-aura h2 {
                    font-family: 'Jersey 15', sans-serif !important;
                    font-size: 5rem !important;
                    color: #8E977D !important;
                    margin: 0 !important;
                    line-height: 1 !important;
                }
   

                .st-key-back_home button,
.st-key-teacher_logout button, .st-key-student_logout button{
    width: 200px !important;
    min-width: 200px !important;
    max-width: 200px !important;
    box-sizing: border-box !important;
    white-space: nowrap !important;
    padding: 10px 20px !important;
}

                /* Text input labels */
                div[data-testid="stTextInput"] label,
                div[data-testid="stTextInput"] label p {
                    color: #8A7650 !important;
                    font-weight:bold !important;
                }

                /* Input box */
                div[data-testid="stTextInput"] div[data-baseweb="input"] {
                    background-color: #DBCEA5 !important;
                    border-radius: 8px !important;
                    box-shadow: none !important;
                }

                /* Text typed inside input */
                div[data-testid="stTextInput"] input {
                    background-color: #DBCEA5 !important;
                    color: #000000 !important;
                    caret-color: #000000 !important;
                }      
                
                /* Placeholder text */
                div[data-testid="stTextInput"] input::placeholder {
                    color: #333333 !important;
                    font-family: 'Bitcount Prop Single', sans serif !important;
                    opacity: 0.5 !important;
                }   


/* Deep scanning spinner text */
div[data-testid="stSpinner"] p {
    white-space: nowrap !important;
    color:#8E977D !important;
}

/* Warning message */
div[data-testid="stAlert"] {
    background-color: #8A7650 !important;
    width: 100% !important;
    box-sizing: border-box !important;
}

div[data-testid="stAlert"] p {
    color: #FFFFFF !important;
}

/* Selectbox label */
div[data-testid="stSelectbox"] label,
div[data-testid="stSelectbox"] label p {
    color: #8A7650 !important;
    font-weight:bold !important;
}                       

.face-camera-label {
    color: #8A7650 !important;
    font-family: 'Bitcount Prop Single', sans-serif !important;
    font-size: 1.1rem !important;
    margin-bottom: 3px !important;
    font-weight:bold !important;
}

.face-not-recognized {
    color: #8A7650 !important;
    font-family: 'Bitcount Prop Single', sans-serif !important;
    font-size: 1.5rem !important;
    font-weight:bold !important;
}

.voice-enrollment-text {
    color: #8A7650 !important;
    font-family: 'Bitcount Prop Single', sans-serif !important;
    font-size: 1rem !important;
    font-weight:bold !important;
}

.voice-record-label {
    color: #8A7650 !important;
    font-family: 'Bitcount Prop Single', sans-serif !important;
    font-size: 1rem !important;
    margin-bottom: 5px !important;
    font-weight:bold !important;
}

.no-subjects-message {
    font-family: 'Bitcount Prop Single', sans-serif !important;
    color: white !important;
    font-size: 1rem !important;
}

        </style>
                """, unsafe_allow_html=True)

def style_base_layout():
    st.markdown(""" 
        <style>
                @import url('https://fonts.googleapis.com/css2?family=Bitcount+Prop+Single:wght@100..900&display=swap');
                @import url('https://fonts.googleapis.com/css2?family=Jersey+15&display=swap');

                /*Hide Top Bar of streamlit*/

                #MainMenu,footer,header{ 
                    visibility:hidden;
                }               

                .block-container{
                    padding-top:1.5rem  !important;
                    padding-bottom: 0rem !important;
                }

                

                h1{
                    font-family: 'Jersey 15', sans serif !important;
                    font-size: 6rem !important;
                    line-height: 1 !important;
                    margin-bottom: 0rem !important;
                    color : #ECE7D1 !important;
                    text-align: center !important;
                    
                    margin-top: -10px !important;
                    margin-bottom: 30px !important;
                }

                h2{
                    font-family: 'Bitcount Prop Single', sans serif !important;
                    font-size: 2rem !important;
                    line-height: 1.1 !important;
                    margin-bottom: 0rem !important;
                    color : #8E977D !important;
                }

                h3{
                    font-family: 'Bitcount Prop Single', sans serif !important;
                    color: #8A7650 !important;
                }

                h4, p{
                    font-family: 'Bitcount Prop Single', sans serif !important;
                }

                button{
                    border-radius : 1.5rem !important;
                    background-color : #8A7650 !important;
                    color: white !important;
                    padding: 10px 20px !important;
                    border: none !important;
                    transition: transform 0.25s ease-in-out !important;
                }

                button[kind="secondary"]{
                    border-radius : 1.5rem !important;
                    background-color : #8E977D !important;
                    color: white !important;
                    padding: 10px 20px !important;
                    border: none !important;
                    transition: transform 0.25s ease-in-out !important;
                }

                button[kind="tertiary"]{
                    border-radius : 1.5rem !important;
                    background-color : #8E977D !important;
                    color: white !important;
                    padding: 10px 20px !important;
                    border: none !important;
                    transition: transform 0.25s ease-in-out !important;
                }

                button:hover{
                    transform:scale(1.05)
                }



        </style>
                """, unsafe_allow_html=True)
    

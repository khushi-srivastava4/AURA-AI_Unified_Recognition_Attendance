import streamlit as st

def footer_home():

    st.markdown(f"""
    <div style='display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:2rem; margin-top:2rem;'>
        <p style='text-align:center; color:#ECE7D1;font-weight:bold !important;'>Created by Isha Raut</p>
    </div>
        
    """, unsafe_allow_html=True)

def footer_dashboard():

    st.markdown(f"""
    <div class="dashboard-footer" style='display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:2rem; margin-top:2rem;'>
        <p style='text-align:center; color:#8E977D !important; font-weight:bold !important;'>Created by Isha Raut</p>
    </div>
        
    """, unsafe_allow_html=True)

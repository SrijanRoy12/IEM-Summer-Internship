import streamlit as st
import time

st.set_page_config(page_title="Login | Smart City Simulation", layout="centered")
st.title("🔐 User Login")

# Hardcoded creator credentials
CREATOR_USERNAME = "srijan"
CREATOR_PASSWORD = "srijan2004@"

if 'user' not in st.session_state:
    st.session_state['user'] = None

if st.session_state['user'] is None:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == CREATOR_USERNAME and password == CREATOR_PASSWORD:
            st.session_state['user'] = username
            st.success(f"Welcome, {username}! Redirecting to dashboard...")
            time.sleep(1)
            st.markdown("<meta http-equiv='refresh' content='0; url=dashboard.py'>", unsafe_allow_html=True)
            st.stop()
        else:
            st.error("Invalid username or password.")
else:
    st.success(f"Already logged in as {st.session_state['user']}.")
    st.markdown("<meta http-equiv='refresh' content='0; url=dashboard.py'>", unsafe_allow_html=True)

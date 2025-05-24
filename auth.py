import streamlit as st
from crypto_utils import hash_text
from data_handler import save_data

def register():
    st.subheader("📝 Register")
    new_user = st.text_input("New Username :")
    new_pass = st.text_input("New Password :", type="password")
    if st.button("Register"):
        if new_user in st.session_state.users:
            st.error("Username already exists!")
        elif new_user and new_pass:
            st.session_state.users[new_user] = {"password": hash_text(new_pass)}
            st.success("✔️ Registration successful! Please login.")
        else:
            st.warning("⚠️ Please fill all fields.")

def login():
    st.subheader("🔐 Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if user in st.session_state.users and st.session_state.users[user]["password"] == hash_text(pwd):
            st.session_state.logged_in_user = user
            if user not in st.session_state.stored_data:
                st.session_state.stored_data[user] = {
                    "encrypted": "", 
                    "passkey": "", 
                    "attempts": 0, 
                    "locked_until": None
                }
            save_data()  # Save data after login
            st.success("✔️ Logged in!")
            st.rerun()
        else:
            st.error("❌ Invalid credentials!")

def logout():
    st.session_state.logged_in_user = None
    save_data()
    st.success("👋 Logged out!")
    st.rerun()

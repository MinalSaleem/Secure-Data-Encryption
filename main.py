import streamlit as st
from auth import login, register, logout
from crypto_utils import store_data, retrieve_data
from data_handler import load_data

# Streamlit config
st.set_page_config(page_title="Secure Data Vault", page_icon="🔐", layout="centered")

# Session setup
if "users" not in st.session_state:
    st.session_state.users = {}
if "stored_data" not in st.session_state:
    st.session_state.stored_data = load_data()
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

# Sidebar menu
st.sidebar.title("🔐 Secure App Menu")

if st.session_state.logged_in_user:
    st.sidebar.success(f"👋 Welcome, **{st.session_state.logged_in_user}**!")
    option = st.sidebar.radio("Navigate", ["Home", "📂 Store Data", "🔍 Retrieve Data", "🚪 Logout"])

    if option == "🏠 Home":
        st.markdown(f"## 👋 Welcome, {st.session_state.logged_in_user}!\nSecure Data Vault with encryption 🔐")
    elif option == "📂 Store Data":
        store_data()
    elif option == "🔍 Retrieve Data":
        retrieve_data()
    elif option == "🚪 Logout":
        logout()
else:
    st.sidebar.info("Please login or register to continue.")
    option = st.sidebar.radio("Select", ["🔐 Login", "📝 Register"])
    if option == "🔐 Login":
        login()
    elif option == "📝 Register":
        register()

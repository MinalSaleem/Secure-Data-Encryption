import hashlib
from datetime import datetime, timedelta
from cryptography.fernet import Fernet, InvalidToken
import streamlit as st
from data_handler import save_data

# One-time Fernet key
if "fernet_key" not in st.session_state:
    st.session_state.fernet_key = Fernet.generate_key()
cipher = Fernet(st.session_state.fernet_key)

def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()

def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(username, passkey):
    data = st.session_state.stored_data[username]
    now = datetime.now()

    # currently locked
    if "locked_until" in data and data["locked_until"]:
        locked_until = datetime.strptime(data["locked_until"], "%Y-%m-%d %I:%M:%S %p")
        if now < locked_until:
            return "locked"

    if hash_text(passkey) == data["passkey"]:
        try:
            decrypted = cipher.decrypt(data["encrypted"].encode()).decode()
            data["attempts"] = 0
            data["locked_until"] = None  # Clear lockout
            save_data()
            return decrypted
        except InvalidToken:
            data["attempts"] += 1
    else:
        data["attempts"] += 1

# Apply lock if too many failed attempts
    if data["attempts"] >= 3:
        data["locked_until"] = (now + timedelta(minutes=1)).strftime("%Y-%m-%d %I:%M:%S %p")

    save_data()
    return None

def store_data():
    st.subheader("📂 Store Data")
    data = st.text_area("Enter secret data:")
    passkey = st.text_input("Set passkey:", type="password")
    if st.button("Encrypt & Save"):
        if data and passkey:
            encrypted = encrypt_data(data)
            st.session_state.stored_data[st.session_state.logged_in_user] = {
                "encrypted": encrypted,
                "passkey": hash_text(passkey),
                "attempts": 0
            }
            save_data() # Save data to JSON file
            st.success("✔️ Encrypted and stored!")
            st.code(encrypted)
        else:
            st.warning("⚠️ Please enter all fields!")

def retrieve_data():
    st.subheader("🔍 Retrieve Data")
    passkey = st.text_input("Enter passkey to decrypt", type="password")
    if st.button("Decrypt"):
        user = st.session_state.logged_in_user
        result = decrypt_data(user, passkey)
        if result == "locked":
            unlock_time = st.session_state.stored_data[user]["locked_until"]
            st.warning(f"🔒 Locked! Try again at: {unlock_time}")
            return
        elif result:
            st.success("✔️ Decryption successful")
            st.code(result)
        else:
            attempts_left = 3 - st.session_state.stored_data[user]["attempts"]
            st.error(f"❌ Wrong passkey! {attempts_left} attempts left.")

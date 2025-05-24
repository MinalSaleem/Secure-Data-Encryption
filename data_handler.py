import json
import streamlit as st

# Load and save data of JSON file
def load_data():
    try:
        with open('stored_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data():
    with open('stored_data.json', 'w') as f:
        json.dump(st.session_state.stored_data, f)

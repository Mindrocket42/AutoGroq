# main.py

import streamlit as st
import os
import toml

# Load secrets from secrets.toml and set as environment variables if not already set
secrets_path = os.path.join(os.path.dirname(__file__), "secrets.toml")
if os.path.exists(secrets_path):
    secrets = toml.load(secrets_path)
    for key, value in secrets.items():
        if key not in os.environ or not os.environ[key]:
            os.environ[key] = value

from agent_management import display_agents
from utils.api_utils import fetch_available_models, get_api_key
from utils.auth_utils import display_api_key_input
from utils.error_handling import setup_logging
from utils.session_utils import initialize_session_variables
from utils.tool_utils import load_tool_functions
from utils.ui_utils import (
    display_reset_and_upload_buttons, 
    display_user_request_input, handle_user_request, 
    select_model, select_provider, set_css, 
    set_temperature, show_interfaces
)


from utils.ui_utils import project_management_ui

def main():
    project_management_ui()
    if "current_project" not in st.session_state or not st.session_state["current_project"]:
        st.stop()
    setup_logging()
    if 'warning_placeholder' not in st.session_state:
        st.session_state.warning_placeholder = st.empty()
    st.title("AutoGroq™")

    set_css()
    initialize_session_variables()
    fetch_available_models()
    load_tool_functions()

    if st.session_state.get("need_rerun", False):
        st.session_state.need_rerun = False
        st.rerun()    

    display_api_key_input()
    get_api_key() 
    
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        select_provider()
    
    with col2:
        select_model()

    with col3:
        set_temperature()

    if st.session_state.show_request_input:
        with st.container():
            if st.session_state.get("rephrased_request", "") == "":
                user_request = st.text_input("Enter your request:", key="user_request", value=st.session_state.get("user_request", ""), on_change=handle_user_request, args=(st.session_state,))
                display_user_request_input()
            if "agents" in st.session_state and st.session_state.agents:
                show_interfaces()
                display_reset_and_upload_buttons()
        
    with st.sidebar:
        display_agents()
         

if __name__ == "__main__":
    main()
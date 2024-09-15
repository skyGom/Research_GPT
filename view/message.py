import streamlit as st

import view.constants as const

def paint_message(message, role, is_save=True):
    with st.chat_message(role):
        st.markdown(message)
        
    if is_save:
        st.session_state[const.MESSAGES].append({"message": message, "role": role})
        
def paint_message_history():
    for message in st.session_state[const.MESSAGES]:
        paint_message(message["message"], message["role"], is_save=False)
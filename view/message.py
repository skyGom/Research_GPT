import streamlit as st

import view.constants as const

from datetime import datetime

def paint_message(message, role, is_downloadable=False, is_save=True):
    with st.chat_message(role):
        st.markdown(message)
        if is_downloadable:
            text_file = create_text_file(message)
            st.download_button(
                label="Download Message",
                data=text_file,
                file_name="chat_message.txt",
                mime="text/plain"
            )
        
    if is_save:
        st.session_state[const.MESSAGES].append({"message": message, "role": role})
        
def paint_message_history():
    for message in st.session_state[const.MESSAGES]:
        paint_message(message["message"], message["role"], is_save=False)
        
def create_text_file(content):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(f"{now}.txt", "w") as file:
        file.write(content)
    return f"{now}.txt"
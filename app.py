import time

import streamlit as st

from gpt.assistants_Manager import AssistantManager, is_valid_openai_key

import view.constants as const
from view.message import paint_message, paint_message_history

if const.MESSAGES not in st.session_state:
    st.session_state[const.MESSAGES] = []

st.set_page_config(page_title="Research GPT App", page_icon="💡",)

st.title("Research GPT App")

st.markdown(
    """
    This app is a research assistant that helps you search for information, extract content from websites, and save your findings to a text file.
    
    Fisrt step, write down your OpenAI API key in the sidebar.
"""
)

if const.API_KEY not in st.session_state:
    st.session_state[const.API_KEY] = None

with st.sidebar:
    if st.session_state[const.API_KEY] is None:
        api_key = st.text_input("First write down OpenAI API key.", type="password")
        
        if api_key:
            with st.spinner("Checking API Key..."):
                if is_valid_openai_key(api_key):
                    st.session_state.api_key = api_key
                else:
                    st.warning("API key is not valid. Try again.")
                    
if st.session_state[const.API_KEY]:
    if const.ASSISTANTS not in st.session_state:
        assistants = AssistantManager(st.session_state[const.API_KEY])
        st.session_state[const.ASSISTANTS] = assistants
    else:
        assistants = st.session_state[const.ASSISTANTS]
    
    if len(st.session_state[const.MESSAGES]) <= 0:
        paint_message("Assistant is ready!", const.AI, False)
    else:
        paint_message_history()
    
    if input_topic := st.text_input("Ask about any topic!", placeholder="What is the XL Backdoor?"):
        paint_message(input_topic, const.USER)
        assistants.research_topic(input_topic)
        while assistants._run.status != 'completed':
            if assistants._run.required_action.type == "submit_tool_outputs":
                assistants.submit_tool_outputs()
            else:
                assistants.runs_poll()
                
            if assistants._run.status == "complete":
                paint_message(assistants.get_messages(), const.AI)
                break
            # match assistants._run.status:
            #     case "requires_action":
            #         assistants.submit_tool_outputs()
            #     case "complete":
            #         paint_message(assistants.get_messages(), "ai")
            #         break
            #     case "expired" | "cancelled" | "failed":
            #         st.error("AI failed to complete the request.")
            #         break
            #     case _:
            #         pass
            # time.sleep(0.5)
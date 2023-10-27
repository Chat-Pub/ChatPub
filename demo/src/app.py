import streamlit as st
from streamlit.components.v1 import html
import os
from dotenv import load_dotenv
from functions import *
from streamlit_chat import message
import time
import openai
from prompts import *
import json

st.set_page_config(page_title="Chat-pub")

import streamlit.components.v1 as components

html_temp = """
                <div style="background-color:{};padding:1px">
                </div>
                """

tabs_font_css = """
<style>
strong{
    font-size: 20px;
}
</style>
"""

st.write(tabs_font_css, unsafe_allow_html=True)

# 안내 문구
text = 'Chat-pub Chatbot Demo'
st.info(text, icon='🤖')

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_KEY")
openai.api_key = os.getenv("OPENAI_KEY")

# config
MODEL_NAME = 'gpt-3.5-turbo'
k = 2
data_path = 'data/data.json'

# load data
with open(data_path, "r") as st_json:
     data_list = json.load(st_json)
index = set_index(data_list)

# Initialize chat history
if "assistant" not in st.session_state:
    st.session_state["assistant"] = []

if "user" not in st.session_state:
    st.session_state["user"] = []

response_container = st.container()

if st.session_state["assistant"] and st.session_state["user"]:
    with response_container:
        # Display chat messages from history on app rerun
        for response, query in zip(st.session_state['assistant'], st.session_state['user']):
            if query != "":
                with st.chat_message('user'):
                    st.markdown(query)
            if response != "":
                with st.chat_message('assistant'):
                    st.markdown(response)

query = st.text_input("input", placeholder ="문의 사항을 입력하세요!", label_visibility="hidden")

# Accept user input
if query:
    with response_container:
         # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(query)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            full_context = ""

        context, title_url_lists = get_context(index=index, query=query, k=k, data_list=data_list)

        for response in openai.ChatCompletion.create(
                model=MODEL_NAME,
                messages=[{"role":"system", "content":chat_system_prompt},
                        {"role":"user", "content":chat_user_prompt_template.format(context=context, query=query)}],
                stream=True,
                temperature = 0
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)


        # get the only referenced context
        referenced_context = get_valid_references(response = full_response,
                                                  title_url_lists=title_url_lists)

        if referenced_context != '':
            # referecned document 
            with st.chat_message("assistant"):
                message_placeholder = st.empty()

                for c in referenced_context:
                    if c == '\t':
                        c = "　"
                    if c == '\n':
                        c = "  \n"
                    full_context += c
                    message_placeholder.markdown(full_context + "▌")
                    message_placeholder.markdown(full_context)
                    time.sleep(0.005)

    # Add user query and assistant response to chat history
    if full_context == "":
        st.session_state['user'].append(query)
        st.session_state['assistant'].append(full_response)
    else:
        st.session_state['user'].append(query)
        st.session_state['user'].append("")
        st.session_state['assistant'].append(full_response)
        st.session_state['assistant'].append(full_context)
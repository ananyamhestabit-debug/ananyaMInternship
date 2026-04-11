import streamlit as st
import requests
import time

st.set_page_config(page_title="LLM Chat", layout="wide")

st.title(" Local LLM Interface (GGUF)")

#  Mode selector
mode = st.radio("Select Mode:", ["Generate", "Chat"])

# API URLs
GEN_URL = "http://127.0.0.1:8000/generate"
CHAT_URL = "http://127.0.0.1:8000/chat"

user_input = st.text_area("Enter your prompt:")

if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please enter something")
    else:
        with st.spinner("Thinking..."):
            start = time.time()

            try:
                if mode == "Generate":
                    response = requests.post(
                        GEN_URL,
                        json={"prompt": user_input}
                    )
                else:
                    response = requests.post(
                        CHAT_URL,
                        json={"message": user_input}
                    )

                result = response.json()
                end = time.time()

                st.markdown("###  You:")
                st.write(user_input)

                st.markdown("###  AI:")
                st.write(result.get("response", "No response"))

                st.caption(f"⏱ {round(end-start,2)} sec")

            except Exception as e:
                st.error(f"Error: {e}")
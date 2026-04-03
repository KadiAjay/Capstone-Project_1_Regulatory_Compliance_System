import streamlit as st
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

st.set_page_config(page_title="Regulatory Compliance Assistant", layout="wide")


is_admin = st.sidebar.toggle("Admin Mode")

if is_admin:
    st.sidebar.header("Upload Document")

    uploaded_file = st.sidebar.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

    if st.sidebar.button("Upload"):
        if uploaded_file is not None:

            files = {
                "file": (uploaded_file.name, uploaded_file.getvalue())
            }

            data = {
                "regulation_type": None
            }

            response = requests.post(
                f"{BASE_URL}/admin/upload",
                files=files,
                data=data
            )

            if response.status_code == 200:
                st.sidebar.success("File uploaded and processed successfully!")
                st.sidebar.json(response.json())
            else:
                st.sidebar.error("Upload failed")
                st.sidebar.text(response.text)

        else:
            st.sidebar.warning("Please upload a file")


if st.sidebar.button(" Clear Chat"):
    st.session_state.messages = []


st.title("Regulatory Compliance Intelligence System")



if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

        if msg["role"] == "assistant" and "raw_output" in msg:
            if msg["raw_output"]:
                with st.expander("View Agent Raw Output"):
                    st.json(msg["raw_output"], expanded=False)


user_input = st.chat_input("Ask your question...")

if user_input:
  
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    payload = {
        "query": user_input,
        "regulation_type": None,
    }

    with st.spinner("Processing your query..."):
        response = requests.post(
            f"{BASE_URL}/query",
            json=payload
        )

    if response.status_code == 200:
        data = response.json()

       
        answer = data.get("answer", "No answer returned.")
        raw_output = data.get("raw_output", {})

     
        if isinstance(raw_output, str):
            try:
                raw_output = json.loads(raw_output)
            except:
                raw_output = {"raw_text": raw_output}

       
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "raw_output": raw_output
        })

        with st.chat_message("assistant"):
            st.write(answer)

            if raw_output:
                with st.expander("View Agent Output"):
                    st.json(raw_output, expanded=False)

    else:
        error_msg = "Query failed"

        st.session_state.messages.append({
            "role": "assistant",
            "content": error_msg
        })

        with st.chat_message("assistant"):
            st.error(error_msg)
            st.text(response.text)
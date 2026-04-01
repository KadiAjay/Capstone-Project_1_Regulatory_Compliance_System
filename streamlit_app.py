import streamlit as st
import requests

BASE_URL = "http://localhost:8000/api/v1"



st.set_page_config(page_title="Regulatory Compliance Assistant", layout="wide")


st.sidebar.header("📤 Upload Document")

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
            st.sidebar.success(" File uploaded and processed successfully!")
            st.sidebar.json(response.json())
        else:
            st.sidebar.error(" Upload failed")
            st.sidebar.text(response.text)

    else:
        st.sidebar.warning("Please upload a file")


st.title("Regulatory Compliance Intelligence System")

st.header("Ask a Question")

query = st.text_area("Enter your question here", height=120)

if st.button("Submit Query"):
    if query:

        payload = {
            "query": query,
            "regulation_type": None,
        }

        response = requests.post(
            f"{BASE_URL}/query",
            json=payload
        )

        if response.status_code == 200:
            data = response.json()

            st.subheader(" Answer")
            st.write(data.get("answer", "No answer returned."))

        else:
            st.error(" Query failed")
            st.text(response.text)
    else:
        st.warning("Please enter a question")
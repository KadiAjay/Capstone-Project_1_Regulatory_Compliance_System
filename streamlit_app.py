import streamlit as st
import requests

BASE_URL = "http://localhost:8000/api/v1"

st.set_page_config(page_title="Regulatory Compliance Assistant")

st.title("📊 Regulatory Compliance Intelligence System")

# =======================
# 📤 Upload Section
# =======================
st.header("Upload Document")

uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

regulation_type = st.selectbox(
    "Select Regulation Type",
    ["RBI", "SEBI", "Basel", "Internal"]
)

if st.button("Upload"):
    if uploaded_file is not None:

        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue())
        }

        data = {
            "regulation_type": regulation_type
        }

        response = requests.post(
            f"{BASE_URL}/admin/upload",
            files=files,
            data=data
        )

        if response.status_code == 200:
            st.success("✅ File uploaded and processed successfully!")
            st.json(response.json())
        else:
            st.error("❌ Upload failed")
            st.text(response.text)

    else:
        st.warning("Please upload a file")

# =======================
# 🔍 Query Section
# =======================
st.header("Ask a Question")

query = st.text_input("Enter your question")

filter_regulation = st.selectbox(
    "Filter by Regulation (optional)",
    ["None", "RBI", "SEBI", "Basel", "Internal"]
)



if st.button("Submit Query"):
    if query:

        payload = {
            "query": query,
            "regulation_type": None if filter_regulation == "None" else filter_regulation,
           
        }

        response = requests.post(
            f"{BASE_URL}/query",
            json=payload
        )

        if response.status_code == 200:
            data = response.json()

            st.subheader("📌 Answer")
            st.write(data["answer"])

            st.subheader("📊 Rule Summary")
            st.write(data["rule_summary"])

            st.subheader("📈 Confidence Score")
            st.write(data["confidence_score"])

            st.subheader("📚 Citations")
            for c in data["citations"]:
                st.write(f"- {c['content'][:200]}...")

            st.warning(data["disclaimer"])

        else:
            st.error("❌ Query failed")
            st.text(response.text)

    else:
        st.warning("Please enter a question")
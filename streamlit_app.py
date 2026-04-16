import streamlit as st
import requests

API_URL = "http://localhost:8000/api"

st.set_page_config(page_title="AI Support Assistant", page_icon="💡", layout="wide")

st.title("💡 AI Support Assistant")
st.markdown("Retrieval-Augmented Generation (RAG) powered customer support hub. Ask anything based on your uploaded documents!")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you today? Please upload documents to the left to give me context."}]

# Sidebar for uploading files
with st.sidebar:
    st.header("Document Ingestion")
    st.write("Upload knowledge base files to build vector embeddings locally via HuggingFace.")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt"])
    
    if st.button("Upload & Index"):
        if uploaded_file is not None:
            with st.spinner("Extracting, segmenting, and embedding..."):
                files = {"file": (uploaded_file.name, uploaded_file, "application/octet-stream")}
                try:
                    response = requests.post(f"{API_URL}/upload", files=files)
                    if response.status_code == 200:
                        res_data = response.json()
                        st.success(f"Success! Processed into {res_data.get('chunks_created')} semantic chunks.")
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
                except Exception as e:
                    st.error(f"Connection error: Is FastAPI running locally? {str(e)}")
        else:
            st.warning("Please drag & drop a file first.")

# Main Chat Interface
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sources" in msg and msg["sources"] and msg["sources"][0] != "Unknown":
            with st.expander("Cited Sources"):
                st.caption(", ".join(msg["sources"]))

# Chat input
if prompt := st.chat_input("Ask a question conceptually contained in your documents..."):
    
    # Render user query
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Render Assistant reasoning & inference
    with st.chat_message("assistant"):
        with st.spinner("Retrieving vector context and generating inference..."):
            try:
                response = requests.post(f"{API_URL}/chat", json={"query": prompt})
                if response.status_code == 200:
                    data = response.json()
                    bot_reply = data.get("response", "")
                    sources = data.get("context_sources", [])
                    
                    st.markdown(bot_reply)
                    
                    # Store to UI context
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply, "sources": sources})
                    
                    if sources and sources[0] != "Unknown":
                        with st.expander("Cited Sources"):
                            st.caption(", ".join(sources))
                else:
                    err_msg = f"API Error {response.status_code}: {response.text}"
                    st.error(err_msg)
                    st.session_state.messages.append({"role": "assistant", "content": err_msg})
            except Exception as e:
                err_msg = "Critical error: Cannot connect to FastAPI backend. Ensure uvicorn is running."
                st.error(err_msg)
                st.session_state.messages.append({"role": "assistant", "content": err_msg})

import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure API URL with fallback
API_URL = os.getenv("API_URL", "http://localhost:8000/api")
BASE_URL = API_URL.replace("/api", "")

st.set_page_config(page_title="AI Support Assistant", page_icon="💡", layout="wide")

# Check API connection status
def check_api_connection():
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        return response.status_code == 200
    except:
        return False

api_connected = check_api_connection()

st.title("💡 AI Support Assistant")

# Connection status indicator
col1, col2 = st.columns([1, 4])
with col1:
    if api_connected:
        st.success("🟢 API Connected")
    else:
        st.error("🔴 API Disconnected")
with col2:
    st.markdown("Retrieval-Augmented Generation (RAG) powered customer support hub. Ask anything based on your uploaded documents!")

if not api_connected:
    st.warning("⚠️ **FastAPI backend is not running.** Please start it with: `python -m uvicorn app.main:app --port 8000`")
    st.info("Or configure API URL in environment variable: `API_URL=http://your-server:8000/api`")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you today? Please upload documents to the left to give me context."}]

# Sidebar for uploading files
with st.sidebar:
    st.header("Document Ingestion")
    st.write("Upload knowledge base files to build vector embeddings locally via HuggingFace.")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt"])
    
    if st.button("Upload & Index", disabled=not api_connected):
        if uploaded_file is not None:
            if api_connected:
                with st.spinner("Extracting, segmenting, and embedding..."):
                    files = {"file": (uploaded_file.name, uploaded_file, "application/octet-stream")}
                    try:
                        response = requests.post(f"{API_URL}/upload", files=files, timeout=30)
                        if response.status_code == 200:
                            res_data = response.json()
                            st.success(f"Success! Processed into {res_data.get('chunks_created', 0)} semantic chunks.")
                        else:
                            st.error(f"Error {response.status_code}: {response.text}")
                    except requests.exceptions.Timeout:
                        st.error("Upload timed out. Please try with a smaller file.")
                    except requests.exceptions.ConnectionError:
                        st.error("Connection lost. Please check if the API is still running.")
                    except Exception as e:
                        st.error(f"Unexpected error: {str(e)}")
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
if prompt := st.chat_input("Ask a question conceptually contained in your documents...", disabled=not api_connected):
    
    # Render user query
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Render Assistant reasoning & inference
    with st.chat_message("assistant"):
        if api_connected:
            with st.spinner("Retrieving vector context and generating inference..."):
                try:
                    response = requests.post(f"{API_URL}/chat", json={"query": prompt}, timeout=30)
                    if response.status_code == 200:
                        data = response.json()
                        bot_reply = data.get("response", "I apologize, but I couldn't generate a response.")
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
                except requests.exceptions.Timeout:
                    err_msg = "Request timed out. Please try again."
                    st.error(err_msg)
                    st.session_state.messages.append({"role": "assistant", "content": err_msg})
                except requests.exceptions.ConnectionError:
                    err_msg = "Lost connection to API. Please check if the backend is still running."
                    st.error(err_msg)
                    st.session_state.messages.append({"role": "assistant", "content": err_msg})
                except Exception as e:
                    err_msg = f"Unexpected error: {str(e)}"
                    st.error(err_msg)
                    st.session_state.messages.append({"role": "assistant", "content": err_msg})
        else:
            err_msg = "Cannot process request: FastAPI backend is not connected. Please start the backend service first."
            st.error(err_msg)
            st.session_state.messages.append({"role": "assistant", "content": err_msg})

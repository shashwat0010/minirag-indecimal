import streamlit as st
import os
import asyncio
from rag_engine import RAGEngine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Mini RAG System", page_icon="🏗️", layout="wide")

# Initialize RAG Engine
@st.cache_resource
def get_rag_engine():
    engine = RAGEngine()
    engine.initialize()
    return engine

def main():
    st.title("🏗️ Mini RAG System – Construction Knowledge Assistant")
    st.markdown("---")

    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        st.info("Ensure your documents are in the `data` folder.")
        if st.button("Refresh Index"):
            st.cache_resource.clear()
            st.success("Index refreshed!")

    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your Indecimal RAG Assistant. How can I help you today?"}
        ]

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "chunks" in message and message["chunks"]:
                with st.expander("View Source Chunks"):
                    for i, chunk in enumerate(message["chunks"]):
                        st.markdown(f"**Source {i+1}:** {chunk.get('metadata', {}).get('source', 'Unknown')}")
                        st.text(chunk["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about construction policies..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Retrieving context and generating answer..."):
                engine = get_rag_engine()
                # Run the async method in a synchronous-like manner for Streamlit
                result = asyncio.run(engine.answer_question(prompt))
                
                response = result["response"]
                chunks = result["chunks"]
                
                st.markdown(response)
                if chunks:
                    with st.expander("View Source Chunks"):
                        for i, chunk in enumerate(chunks):
                            st.markdown(f"**Source {i+1}:** {chunk.get('metadata', {}).get('source', 'Unknown')}")
                            st.text(chunk["content"])
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response,
                    "chunks": chunks
                })

if __name__ == "__main__":
    main()

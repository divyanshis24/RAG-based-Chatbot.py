import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceHub
from dotenv import load_dotenv
import os

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
 # Replace with your Hugging Face API token
DB_FAISS_PATH = "vectorstore/db_faiss"
HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"

# Load vectorstore
@st.cache_resource
def get_vectorstore():
    embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
    return db

# Load LLM
@st.cache_resource
def load_llm():
    return HuggingFaceHub(
        repo_id=HUGGINGFACE_REPO_ID,
        model_kwargs={"temperature": 0.5, "max_length": 512},
        huggingfacehub_api_token=HF_TOKEN
    )

# Initialize the QA chain
@st.cache_resource
def create_qa_chain():
    vectorstore = get_vectorstore()
    llm = load_llm()
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={'k': 7}),
        return_source_documents=False
    )

# App title
st.title("🍽️ Zomato Chatbot")
st.markdown("Ask anything about restaurants, dishes, or pricing!")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input loop
qa_chain = create_qa_chain()

for i, entry in enumerate(st.session_state.chat_history):
    st.markdown(f"**You:** {entry['question']}")
    st.markdown(f"**Bot:** {entry['answer']}")

# New input box (always at the bottom)
user_input = st.text_input("Ask a new question:", key=f"input_{len(st.session_state.chat_history)}")

if user_input:
    with st.spinner("Thinking..."):
        response = qa_chain.invoke({"query": user_input})
        answer = response["result"]
        
        if "Helpful Answer:" in answer:
            answer = answer.split("Helpful Answer:")[-1].strip()

        st.session_state.chat_history.append({
            "question": user_input,
            "answer": answer
        })

        st.rerun()

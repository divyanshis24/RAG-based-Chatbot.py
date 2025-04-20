# 🍽️ Zomato Kanpur Chatbot

An AI-powered chatbot that answers questions about restaurants, dishes, and pricing in Kanpur. Built using LangChain, FAISS, Hugging Face LLM, and Streamlit.

---

## Features

- Chat with restaurant data using natural language
- Uses `sentence-transformers` for embeddings
- Powered by `mistralai/Mistral-7B-Instruct-v0.3` via Hugging Face
- Fast retrieval with FAISS vector store
- Clean Streamlit interface for ease of use

---

## Setup and Running Instructions

### 1. Clone Repository

```bash
git clone <your_repo_url>
cd <your_repo_dir>
```

### 2. Install Dependencies 

```bash
pip install -r requirements.txt
```

### 3. Scrap the data

```bash 
python scrape_data.py
``` 

### 4. Build FAISS Vectorstore

```bash
python kb.py
```
### 5. Run your bot

```bash 
python -m streamlit run bot.py
```

---

### Note: Please put your own API key from Hugging face as HF_TOKEN = <YOUR_API_KEY>, it is free for limited queries. 
Enjoy talking to the bot and make one on your personal datasets


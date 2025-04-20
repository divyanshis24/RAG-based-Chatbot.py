
import os
import json
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

DATA_PATH = "data"                # Folder with your restaurant JSON files
DB_FAISS_PATH = "vectorstore/db_faiss"

def load_json_files(data_path):
    all_data = []
    for filename in os.listdir(data_path):
        if filename.endswith(".json"):
            with open(os.path.join(data_path, filename), "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    all_data.append(data)
                elif isinstance(data, list):
                    all_data.extend(data)
    return all_data

def format_entries(data):
    entries = []
    for r in data:
        name = r.get("Name", "").strip()
        # metadata
        entries.append(f"Restaurant: {name} | Address: {r.get('Address','')}")
        entries.append(f"Restaurant: {name} | Contact: {r.get('Contact Number','')}")
        entries.append(f"Restaurant: {name} | Cuisines: {r.get('Cuisines','')}")
        entries.append(f"Restaurant: {name} | Facilities: {r.get('Facilities','')}")
        entries.append(f"Restaurant: {name} | Remarks: {r.get('Remarks','')}")
        entries.append(f"Restaurant: {name} | Delivery Rating: {r.get('Delivery Rating','')}")
        # top dishes if any
        if td := r.get("Top_dishes"):
            entries.append(f"Restaurant: {name} | Top Dishes: {td}")
        # opening hours
        oh = r.get("Opening Hours")
        if isinstance(oh, dict):
            for day, hrs in oh.items():
                entries.append(f"Restaurant: {name} | Opening hours on {day.capitalize()}: {hrs}")
        else:
            entries.append(f"Restaurant: {name} | Opening hours not available.")
        # dishes
        for dish in r.get("Dishes", []):
            entries.append(
                f"Restaurant: {name} | Dish: {dish.get('Dish','')}. "
                f"Description: {dish.get('Description','')}. "
                f"Price: {dish.get('Price','')}."
            )
    return entries

def main():
    print("Loading JSON data…")
    data = load_json_files(DATA_PATH)

    print("Formatting entries…")
    entries = format_entries(data)

    print(f"Wrapping {len(entries)} entries into Documents…")
    docs = [Document(page_content=txt) for txt in entries]

    print("Creating embeddings & FAISS index…")
    embed = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(docs, embed)
    db.save_local(DB_FAISS_PATH)

    print(f"✅ FAISS index written to: {DB_FAISS_PATH}")

if __name__ == "__main__":
    main()
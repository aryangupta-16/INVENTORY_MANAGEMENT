# app/repositories/ai_vector_db.py
import faiss # @unresolvedImport
import numpy as np
import pickle
import os

VECTOR_DIM = 384
INDEX_PATH = "faiss_index.index"
META_PATH = "metadata_store.pkl"

# Initialize or load FAISS index
if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH)
else:
    index = faiss.IndexIDMap(faiss.IndexFlatL2(VECTOR_DIM))

# Load metadata
if os.path.exists(META_PATH):
    with open(META_PATH, "rb") as f:
        metadata_store = pickle.load(f)
else:
    metadata_store = {}

def save_index():
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(metadata_store, f)

def upsert_vector(entry_id: int, vector: list, metadata: dict):
    vec = np.array([vector], dtype='float32')
    ids = np.array([entry_id], dtype='int64')
    if entry_id in metadata_store:
        index.remove_ids(np.array([entry_id], dtype='int64'))
    index.add_with_ids(vec, ids)
    metadata_store[entry_id] = metadata
    save_index()

def delete_vector(entry_id: int):
    if entry_id in metadata_store:
        index.remove_ids(np.array([entry_id], dtype='int64'))
        metadata_store.pop(entry_id)
        save_index()

def query_vectors(vector: list, top_k: int = 5):
    vec = np.array([vector], dtype='float32')
    distances, ids = index.search(vec, top_k)
    results = []
    for i, entry_id in enumerate(ids[0]):
        if entry_id in metadata_store:
            results.append(metadata_store[entry_id])
    return results

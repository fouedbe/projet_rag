import faiss
import numpy as np
import pickle

def create_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return index

def save_index(index, chunks, index_file='index.faiss', data_file='chunks.pkl'):
    faiss.write_index(index, index_file)
    with open(data_file, 'wb') as f:
        pickle.dump(chunks, f)

def load_index(index_file='index.faiss', data_file='chunks.pkl'):
    index = faiss.read_index(index_file)
    with open(data_file, 'rb') as f:
        chunks = pickle.load(f)
    return index, chunks

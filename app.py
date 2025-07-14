import streamlit as st
from pdf_utils import extract_text_from_pdf, extract_text_from_image
from embed_utils import chunk_text, embed_chunks
from vector_store import create_faiss_index, save_index, load_index
from rag_pipeline import generate_answer
import numpy as np
from sentence_transformers import SentenceTransformer
import requests

# Initialisation de l'historique et des chunks dans la session
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'chunks' not in st.session_state:
    st.session_state['chunks'] = []
if 'file_name' not in st.session_state:
    st.session_state['file_name'] = None

st.set_page_config(page_title="Assistant RAG", page_icon="🧠", layout="wide")

with st.sidebar:
    st.markdown("## 📚 Historique des questions")
    for i, (q, a) in enumerate(st.session_state['history']):
        st.markdown(f"**Q{i+1}:** {q}")
        st.markdown(f"<span style='color: #4F8BF9;'>Réponse:</span> {a}", unsafe_allow_html=True)
        st.markdown("---")
    st.markdown("## 📄 Fichier chargé")
    if st.session_state['file_name']:
        st.info(f"**{st.session_state['file_name']}**")
    st.markdown("## 🧩 Chunks générés")
    if st.session_state['chunks']:
        for i, chunk in enumerate(st.session_state['chunks']):
            st.markdown(f"**Chunk {i+1}:** {chunk[:80]}{'...' if len(chunk)>80 else ''}")
            if i > 4:
                st.markdown(f"...et {len(st.session_state['chunks'])-5} autres chunks")
                break

st.markdown("""
    <style>
    .main {background-color: #F5F7FB;}
    .stButton>button {background-color: #4F8BF9; color: white;}
    .stTextInput>div>input {background-color: #EAF0FB;}
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 Assistant RAG - PDF & Image")
st.markdown("""
Bienvenue sur votre assistant RAG !
- Uploadez un PDF ou une image, posez vos questions, et retrouvez l'historique dans la barre latérale.
""")

uploaded_file = st.file_uploader("📄 Choisissez un fichier PDF ou une image", type=["pdf", "jpg", "jpeg", "png"])
question = st.text_input("❓ Posez votre question")

if uploaded_file:
    file_type = uploaded_file.type
    file_name = uploaded_file.name
    with open(file_name, "wb") as f:
        f.write(uploaded_file.read())
    st.session_state['file_name'] = file_name

    if file_type == "application/pdf":
        text = extract_text_from_pdf(file_name)
    elif file_type in ["image/jpeg", "image/png", "image/jpg"]:
        text = extract_text_from_image(file_name)
    else:
        st.error("Type de fichier non supporté.")
        st.stop()

    chunks = chunk_text(text)
    st.session_state['chunks'] = chunks
    embeddings, chunks = embed_chunks(chunks)
    index = create_faiss_index(embeddings)
    save_index(index, chunks)
    st.success("✅ Fichier traité et indexé")

pdf_url = st.text_input("🌐 Ou collez un lien vers un PDF")

if pdf_url:
    try:
        response = requests.get(pdf_url)
        if response.status_code == 200 and 'application/pdf' in response.headers.get('Content-Type', ''):
            file_name = pdf_url.split('/')[-1] or 'document.pdf'
            with open(file_name, 'wb') as f:
                f.write(response.content)
            st.session_state['file_name'] = file_name
            text = extract_text_from_pdf(file_name)
            chunks = chunk_text(text)
            st.session_state['chunks'] = chunks
            embeddings, chunks = embed_chunks(chunks)
            index = create_faiss_index(embeddings)
            save_index(index, chunks)
            st.success("✅ PDF téléchargé, traité et indexé")
        else:
            st.error("Lien invalide ou le fichier n'est pas un PDF.")
    except Exception as e:
        st.error(f"Erreur lors du téléchargement : {e}")

if question and st.session_state['chunks']:
    index, chunks = load_index()
    model = SentenceTransformer("all-MiniLM-L6-v2")
    question_embedding = model.encode([question])
    D, I = index.search(np.array(question_embedding), k=3)
    relevant_chunks = [chunks[i] for i in I[0]]
    answer = generate_answer(question, relevant_chunks)
    st.markdown("### 📝 Réponse")
    st.write(answer)
    st.session_state['history'].append((question, answer))

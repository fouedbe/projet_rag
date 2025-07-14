# 🧠 Assistant RAG - PDF & Image

Assistant RAG (Retrieval-Augmented Generation) interactif pour PDF et images, avec interface Streamlit moderne, support multilingue (français, anglais, arabe), OCR, et historique des questions/réponses.

## Fonctionnalités principales
- **Upload de PDF ou d'image** (JPG, PNG)
- **Coller un lien URL vers un PDF** (téléchargement et traitement automatique)
- **Extraction de texte** :
  - PDF : extraction classique
  - Image : OCR multilingue (français, anglais, arabe)
- **Chunking** automatique du texte
- **Indexation vectorielle** (FAISS)
- **Question/réponse** sur le contenu (RAG)
- **Historique** des questions/réponses et des chunks générés
- **Interface multilingue** (français, anglais, arabe)
- **Design moderne** (sidebar, couleurs, sections)

## Installation

1. **Cloner le repo**
2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```
3. **Installer Tesseract OCR** (pour l'OCR sur images) :
   - [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) doit être installé sur votre système
   - Installer les packs de langues nécessaires (fra, eng, ara)

## Utilisation

```bash
streamlit run app.py
```

- Ouvrez l'interface dans votre navigateur
- Uploadez un PDF ou une image **ou** collez un lien PDF
- Choisissez la langue de l'interface et de l'OCR (français, anglais, arabe)
- Posez vos questions sur le contenu
- Consultez l'historique et les chunks dans la sidebar

## Dépendances principales
- streamlit
- PyPDF2
- faiss-cpu
- sentence-transformers
- transformers
- numpy
- pytesseract
- Pillow
- requests

## Remarques
- Pour l'OCR arabe ou français, installez les packs de langue Tesseract correspondants (`tesseract-ocr-fra`, `tesseract-ocr-ara`)
- L'historique est conservé tant que la session Streamlit reste ouverte

## Auteur
- Projet généré avec l'aide de l'IA 
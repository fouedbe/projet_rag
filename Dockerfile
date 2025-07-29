# Utilise une image officielle Python légère
FROM python:3.10-slim

# Crée le dossier de travail dans le conteneur
WORKDIR /app

# Copie le fichier requirements.txt
COPY requirements.txt ./

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le contenu du projet dans le conteneur
COPY . .

# Expose le port Streamlit (8501 par défaut)
EXPOSE 8501

# Commande pour lancer l'app Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# 1. Image de base : Python léger (variante "slim" = plus petite)
FROM python:3.12-slim

# 2. Dossier de travail dans l'image
WORKDIR /code

# 3. Les dépendances D'ABORD (couche rare → protégée du cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Le code ENSUITE (couche fréquente → en bas)
COPY ./app ./app

# 5. Documente le port sur lequel l'appli écoute
EXPOSE 8000

# 6. Commande de démarrage du conteneur
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
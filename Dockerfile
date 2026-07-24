FROM python:3.12-slim

WORKDIR /code

# Les dépendances d'abord (cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Le code ensuite
COPY ./app ./app

# Création d'un utilisateur non privilégié
RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /code

# On bascule dessus : tout ce qui suit tourne sans privilèges
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
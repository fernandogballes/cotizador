# docker/backend/Dockerfile
FROM python:3.11.5

WORKDIR /app

COPY docker/backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY . .

COPY docker/backend/entrypoint.sh /entrypoint.sh
COPY KDD/Algoritmos/trained_models KDD/Algoritmos/trained_models

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "Sistema/backend/manage.py", "runserver", "0.0.0.0:8000"]
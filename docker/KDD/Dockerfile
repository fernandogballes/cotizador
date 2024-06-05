# docker/kdd/Dockerfile
FROM python:3.11.5

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todos los scripts necesarios
COPY KDD/ KDD/
COPY paths.py /app/
COPY KDD/data KDD/data
COPY KDD/Algoritmos/cluster_data KDD/Algoritmos/cluster_data
COPY KDD/Algoritmos/trained_models KDD/Algoritmos/trained_models

# Establecer el PYTHONPATH
ENV PYTHONPATH=/app/KDD/Algoritmos:/app

ENTRYPOINT ["python", "KDD/Algoritmos/KDDMain.py"]

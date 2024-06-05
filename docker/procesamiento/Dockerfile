# docker/procesamiento/Dockerfile
FROM python:3.11.5

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todos los scripts necesarios
COPY KDD/ KDD/
COPY paths.py /app/
COPY KDD/data KDD/data

# Establecer el PYTHONPATH
ENV PYTHONPATH=/app/KDD/Procesamiento:/app

ENTRYPOINT ["python", "KDD/Procesamiento/ProcesamientoMain.py"]

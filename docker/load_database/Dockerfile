FROM python:3.11.5

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todos los scripts y archivos necesarios
COPY KDD/ KDD/
COPY Sistema/bbdd/code/ Sistema/bbdd/code/
COPY Sistema/bbdd/tool_querys/ Sistema/bbdd/tool_querys/
COPY Sistema/bbdd/data/ Sistema/bbdd/data/
COPY paths.py /app/
COPY wait-for-it.sh /app/

# Establecer el PYTHONPATH
ENV PYTHONPATH=/app/Sistema/bbdd/code:/app/KDD

# Dar permisos de ejecución a wait-for-it.sh
RUN chmod +x wait-for-it.sh

ENTRYPOINT ["./wait-for-it.sh", "db:5432", "--", "python", "Sistema/bbdd/code/LoadDatabase.py"]

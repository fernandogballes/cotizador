FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY KDD/ KDD/
COPY LoadDatabase.py LoadDatabase.py

ENTRYPOINT ["python", "LoadDatabase.py"]

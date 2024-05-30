FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY KDD/ KDD/
COPY KKDMain.py KKDMain.py

ENTRYPOINT ["python", "KKDMain.py"]

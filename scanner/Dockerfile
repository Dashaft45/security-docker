FROM cr.yandex/mirror/python:3.11-slim

WORKDIR /scanner

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scan.py .

CMD ["python", "scan.py"]

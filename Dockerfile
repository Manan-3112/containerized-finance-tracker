cat > app/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY wait-for-db.py .

EXPOSE 5000

CMD ["sh", "-c", "python wait-for-db.py && python app.py"]
EOF

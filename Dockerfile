FROM python:3-slim
WORKDIR /goldongo
COPY requirements.txt .
RUN pip install --no-cache-dir -r libs.txt

COPY api /app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

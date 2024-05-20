FROM python:3-slim
WORKDIR /goldongo
COPY libs.txt .
RUN pip install --no-cache-dir -r libs.txt

COPY . /app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

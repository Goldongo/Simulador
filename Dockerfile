FROM python:3-slim
WORKDIR /goldongo/simulador
COPY req.txt .
RUN pip3 install --no-input -r req.txt
COPY . api/
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
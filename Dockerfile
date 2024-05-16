FROM python:3-slim
WORKDIR /goldongo
RUN pip3 install --no-input -r libs.txt

COPY . .
CMD ["uvicorn", "api.main:app"]
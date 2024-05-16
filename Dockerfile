FROM python:3-slim
WORKDIR /goldongo
RUN pip3 install --no-input -r libs.txt

COPY . .
CMD ["python3", "sim_api.py"]
FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN export HNSWLIB_NO_NATIVE=1  
COPY . .

CMD ["python3", "main.py"]
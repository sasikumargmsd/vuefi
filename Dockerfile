FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install langchain
RUN pip3 install flask
COPY . .

CMD ["python3", "main.py"]
FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install langchain
RUN pip3 install flask
RUN pip3 install pypdf
COPY . .

CMD ["flask", "--app=main", "run" , "--host=0.0.0.0", "--port=80"]
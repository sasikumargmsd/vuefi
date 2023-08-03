FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

# RUN apt install python3-dev
RUN apt-get update && apt-get install build-essential -y

RUN pip3 install langchain
RUN pip3 install flask
RUN pip3 install pypdf
RUN pip3 install openai
RUN export HNSWLIB_NO_NATIVE=1 
# RUN pip3 install sqlite3
RUN pip3 install chromadb==0.3.29
RUN pip3 install tiktoken
COPY . .

CMD ["flask", "--app=app", "run" , "--host=0.0.0.0", "--port=80"]
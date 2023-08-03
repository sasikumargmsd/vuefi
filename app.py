import os 
os.environ["OPENAI_API_KEY"] = ""

import json
import uuid
import sqlite3
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain


from flask import Flask, jsonify, request
app = Flask(__name__)

def create_table():
    conn = sqlite3.connect('test.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS VECTOR_MAPPINGS
            (ID INT PRIMARY KEY     NOT NULL,
            PATH           TEXT    NOT NULL);''')
    conn.commit()
    conn.close()

@app.route('/upload_file', methods=['POST'])
def parse_file():
    record = json.loads(request.data)
    print(record)
    mapping_id = str(uuid.uuid4())
    file_name = record['url']

    conn = sqlite3.connect('test.db')
    query = "INSERT INTO VECTOR_MAPPINGS (ID,PATH) \
        VALUES ('{}', '{}')".format(mapping_id, file_name)
    print(query)
    conn.execute(query)
    conn.commit()
    conn.close()
    return jsonify({
		"index": mapping_id
	})
	

@app.route('/query', methods=['POST'])
def query():
    payload = json.loads(request.data)
    query = payload['query']
    index = payload['index']
    path = get_file_path(index)

    loader = PyPDFLoader(path)
    documents = loader.load()
    print(documents)
    vector_index = VectorstoreIndexCreator().from_loaders([loader])
    response = vector_index.query(query)
    return jsonify({
		"response": response
	})

def get_file_path(index):
    conn = sqlite3.connect('test.db')
    print ("Opened database successfully")

    cursor = conn.execute("SELECT ID,PATH from VECTOR_MAPPINGS where ID='{}'".format(index))
    path = ''
    for row in cursor:
        path = row[1]
    conn.close()
    return path

if __name__ == '__main__': 
    create_table()
    app.run(host='0.0.0.0', port=80)
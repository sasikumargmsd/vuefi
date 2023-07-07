import os 
os.environ["OPENAI_API_KEY"] = "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"
# os.environ["OPENAI_API_KEY"] = "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"

import json
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/parse_credit_report', methods=['POST'])
def create_item():
	record = json.loads(request.data)
	loader = PyPDFLoader(record['url'])
	documents = loader.load()
	index = VectorstoreIndexCreator().from_loaders([loader])
	query = "what is the cibil score?"
	score = index.query(query)
	query = "enquiries in last 1 month?"
	enquiries = index.query(query)
	return jsonify({"score": score.strip(), "enquiries":enquiries.strip()})

@app.route('/check_eligibility', methods=['POST'])
def create_item():





if __name__ == '__main__': 
	app.run()

import os 

import json
# from langchain.document_loaders import PyPDFLoader
# from langchain.indexes import VectorstoreIndexCreator
# from langchain.llms import OpenAI
# from langchain.chains.question_answering import load_qa_chain
from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/parse_credit_report', methods=['POST'])
def parse_credit_report():
    print(request.data)
    return jsonify({
		"enquiries": "1",
		"score": "673"
	})
    # record = json.loads(request.data)
    # loader = PyPDFLoader(record['url'])
    # documents = loader.load()
    # index = VectorstoreIndexCreator().from_loaders([loader])
    # query = "what is the cibil score?"
    # score = index.query(query)
    # query = "enquiries in last 1 month?"
    # enquiries = index.query(query)
    # return jsonify({"score": score.strip(), "enquiries":enquiries.strip()})
	

@app.route('/check_eligibility', methods=['POST'])
def is_eligible():
    payload = json.loads(request.data)
    job_id = payload['job_id']
    cibil = payload['cibil_report']
    # data = get_file_from_s3(job_id)
    data = parse_summary()
    return jsonify(check_eligibility(data,cibil))

def get_file_from_s3(job_id="000d1e0a-06c8-4fd6-a834-2e3fba2a2eb7"):
    bucket_name = "idp-data-staging"
    path = f"file_uploads/worfkflow=548/job={job_id}/summary.json"
    s3resource = boto3.resource('s3')
    content_object = s3resource.Object(bucket_name, path)
    file_content = content_object.get()['Body'].read()
    return json.loads(file_content)
        
def check_eligibility(finance_report, cibil):
    eligibility1 = input_data1 = [
        {
		"col": "Eligible For loan",
        "value": "True"
		},
        {
		"col": "Criteria: Current Balance has to be > 50k",
        "value": f"True, The available current: {finance_report['Current Balance']}"
		},
        {
		"col": "Criteria: Number of Cheque Bounces shold be Zero",
        "value": f"True, The number of checks bounced: {finance_report['Number of Cheque Bounces']}"
		},
        {
		"col": "Criteria: Average ABB for 3 months should be >50k",
        "value": f"True: The average ABB for 3 months: {finance_report['Average ABB for 3 months']}"
		},
        {
		"col": "Criteria: Cibil score should be > 650",
        "value": f"True: Cibil score is: {cibil['score']}"
		},
        {
		"col": "Criteria: Number of enquiries in 30 days should be < 3",
        "value": f"True: Number of enquiries in 30 days {cibil['enquiries']}"
		}
    ]
    monthly_data = []
#     eligibility["data_points"] = finance_report
    try:
        if finance_report["Average ABB for 3 months"] == "Not Available" or float(finance_report["Average ABB for 3 months"].replace(",","")) <50000:
            eligibility1[0]["value"] = "False"
            eligibility1[3]["value"] = f"False: The average ABB for 3 months: {finance_report['Average ABB for 3 months']}"
        if float(finance_report["Current Balance"].replace(",","")) <50000:
            eligibility1[0]["value"] = "False"
            eligibility1[1]["value"] = f"False, The available current: {finance_report['Current Balance']}"
        if finance_report["Number of Cheque Bounces"] not in ["0", "Not Available"]:
            eligibility1[0]["value"] = "False"
            eligibility1[2]["value"] = f"False, The number of checks bounced: {finance_report['Number of Cheque Bounces']}"
        if int(cibil["score"]) <650:
            eligibility1[0]["value"] = "False"
            eligibility1[4]["value"] = f"False: Cibil score is: {cibil['score']}"
        if int(cibil["enquiries"]) > 2:
            eligibility1[0]["value"] = "False"
            eligibility1[5]["value"] = f"False: Number of enquiries in 30 days {cibil['enquiries']}"
        for data in finance_report["Monthly Data"]:
            if data.get("Minimum Balance") and float(data.get("Minimum Balance").replace(",","")) < 5000:
                eligibility1[0]["value"] = "False"
                eligibility1.append({
					"col": "Criteria: Minimum Balance should be > 5k",
					"value": f"False, Minimum balance for month: {data.get('Month')} is : {data.get('Minimum Balance')}"
				})
            else:
                eligibility1.append({
					"col": "Criteria: Minimum Balance should be > 5k",
					"value": f"True, Minimum balance for month: {data.get('Month')} is : {data.get('Minimum Balance')}"
				})
    except Exception as e:
        print("Error")
        eligibility1[0]["value"] = "False"
    finally:
        return eligibility1


def parse_summary(path='./summary.json', data=None):
    if not data:
        f = open(path)
        data = json.load(f)
    input_data = {
       "Current Balance": "0",
       "Number of Cheque Bounces": "0",
       "Average ABB for 3 months": "0",
       "Monthly Data": []
    }

    for sub_data in data['Summary']:
        if "data" in sub_data.keys() and type(sub_data['data']) is dict:
            if "Current Balance" in sub_data['data'].keys():
                input_data["Current Balance"] = sub_data['data']["Current Balance"]
            if "Number of Cheque Bounces" in sub_data['data'].keys():
                input_data["Number of Cheque Bounces"] = sub_data['data']["Number of Cheque Bounces"]
            if "Average ABB for 3 months" in sub_data['data'].keys():
                input_data["Average ABB for 3 months"] = sub_data['data']["Average ABB for 3 months"]
    return input_data


if __name__ == '__main__': 
	app.run(host='0.0.0.0', port=80)

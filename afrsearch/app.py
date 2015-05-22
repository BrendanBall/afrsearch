import json
import os
import requests
from flask import Flask, send_from_directory, render_template, request

app = Flask(__name__)

solr_url = "http://localhost:8983/solr/af-search/select"
solr_opt = {"wt": "json"}
documentDb = "db/"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", title="Search")

@app.route("/search", methods=["GET"])
def search():
	solr_opt["q"] = request.args["query"]
	response = requests.get(solr_url, params=solr_opt).json()
	results = response["response"]["docs"]

	for result in results:
		result["name"] = os.path.basename(result["id"])
	return render_template("index.html", title="Results", results=results)

@app.route("/doc", methods=["GET"])
def document():
	filename = request.args["filename"]
	path = os.path.join(documentDb, filename)
	with open(path, "rb") as f:
		file_contents = f.read().decode("utf-8")	
	return render_template("result.html", title="Results", document=file_contents)

@app.route("/static/<path:path>", methods=["GET"])
def staticfiles(path):
    return send_from_directory("static", path)

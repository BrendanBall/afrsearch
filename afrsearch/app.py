import json
import requests
from flask import Flask, send_from_directory, render_template, request

app = Flask(__name__)

solr_url = "http://localhost:8983/solr/af-search/select"
solr_opt = {"wt": "json"}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", title="Search")

@app.route("/search", methods=["GET"])
def search():
	solr_opt["q"] = request.args["query"]
	response = requests.get(solr_url, params=solr_opt)
	results = response.json()
	top_result_id = results["response"]["docs"][0]["id"]

	with open(top_result_id, "rb") as f:
		file_contents = f.read().decode("utf-8")

	return render_template("result.html", title="Results", top_result=file_contents)

@app.route("/static/<path:path>", methods=["GET"])
def staticfiles(path):
    return send_from_directory("static", path)

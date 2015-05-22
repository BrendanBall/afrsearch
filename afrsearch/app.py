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
	results = json.loads(response.content)
	return response.content
	# return render_template("index.html", title="Search", query=request.args["query"])

@app.route("/static/<path:path>", methods=["GET"])
def staticfiles(path):
    return send_from_directory("static", path)

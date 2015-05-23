import json
import os
import math
import requests
from flask import Flask, send_from_directory, render_template, request

app = Flask(__name__)

solr_url = "http://localhost:8983/solr/af-search/select"
solr_opt = {"wt": "json"}
documentDb = "db/"
results_per_page = 10

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", title="Search")

@app.route("/search", methods=["GET"])
def search():
	page = 0
	if "page" in request.args:
		page = eval(request.args["page"])
	results = solar_request(request.args["query"], page)
	return render_template("index.html", title="Results", results=results, query=request.args["query"])


def solar_request(search_query, page):
	solr_opt["q"] = search_query
	solr_opt["start"] = page * results_per_page
	response = requests.get(solr_url, params=solr_opt).json()
	results = response["response"]["docs"]
	filenames = []
	numResults = response["response"]["numFound"]

	for result in results:
		filenames.append(os.path.basename(result["id"]))
	pages = int(math.ceil(numResults / float(results_per_page)))

	return {"numResults": numResults, "results": filenames, "pages": pages}
	 

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

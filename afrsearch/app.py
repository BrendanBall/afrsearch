import json
import os
import math
import requests
from flask import Flask, send_from_directory, render_template, request

app = Flask(__name__)

results_per_page = 15
solr_url = "http://localhost:8983/solr/af-search/select"
solr_opt = {"wt": "json", "rows": results_per_page}
documentDb = "db/"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", title="Search")

@app.route("/search", methods=["GET"])
def search():
	page = 0
	if "page" in request.args:
		page = eval(request.args["page"])
	results = solar_request(stem(request.args["query"]), page)
	return render_template("index.html", title="Results", results=results, query=request.args["query"], page=page)

def stem(query):
	new_query = query
	with open("stem.txt", "rb") as f:
		raw = f.read().decode("utf-8")
	lines = raw.split("\n")
	for line in lines:
		for word in line.split(","):
			if query == word.strip():
				line.replace(query, "")
				new_query +=" %s" % line
	
	#if not query == new_query:
	#	print "Stemmed '%s' to '%s'" % (query, new_query)
	return new_query


def document_summary(filename):
	path = os.path.join(documentDb, filename)
	with open(path, "rb") as f:
		file_contents = f.read(100).decode("utf-8")	
	return file_contents + "..."
	

def solar_request(search_query, page):
	solr_opt["q"] = search_query
	solr_opt["start"] = page * results_per_page
	response = requests.get(solr_url, params=solr_opt).json()
	results = response["response"]["docs"]
	documents = []
	numResults = response["response"]["numFound"]

	for result in results:
		filename = os.path.basename(result["id"])
		# summary = document_summary(filename)
		summary = ""
		documents.append({"filename": filename, "summary": summary})
	pages = int(math.ceil(numResults / float(results_per_page)))

	return {"numResults": numResults, "documents": documents, "pages": pages, "start": solr_opt["start"] + 1}
	 

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

import json
import os
import re
import math
import requests
from flask import Flask, send_from_directory, render_template, request

app = Flask(__name__)

results_per_page = 10
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
	stemmed = ""
	stopwords = get_stopwords()
	for w in request.args["query"].lower().split(" "):
		if w in stopwords:
			continue
		stemmed += stem(w)+" "
	results = solar_request(stemmed, page)
	return render_template("index.html", title="Results", results=results, stemmed=stemmed, query=request.args["query"].lower(), page=page)

def stem(query):
	new_query = ""
	with open("stem.txt", "rb") as f:
		raw = f.read().decode("utf-8")
	lines = raw.split("\n")
	for line in lines:
		for word in line.split(","):
			if query == word.strip():
				line.replace(query, "")
				new_query +=" %s" % line
	
	new_query = new_query.replace(",", "")
	new_query = query + re.sub(r"\b%s\b" % query , "", new_query)
	return new_query

def get_stopwords():
	with open("stopwords.txt", "rb") as f:
		lines = f.read().decode("utf-8").splitlines()
	return lines

def document_summary(filename):
	path = os.path.join(documentDb, filename)
	with open(path, "rb") as f:
		file_contents = f.read().decode("utf-8")	
	return file_contents[0:100] + "..."
	

def solar_request(search_query, page):
	solr_opt["q"] = search_query
	solr_opt["start"] = page * results_per_page
	response = requests.get(solr_url, params=solr_opt).json()
	results = response["response"]["docs"]
	documents = []
	numResults = response["response"]["numFound"]

	for result in results:
		filename = os.path.basename(result["id"])
		summary = document_summary(filename)
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

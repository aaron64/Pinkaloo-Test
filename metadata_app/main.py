from flask import Flask, request, jsonify
from flask import render_template
from flaskext.markdown import Markdown
import requests
import json
import sys

app = Flask(__name__)

## /
# Index page
@app.route("/")
def index():
	site = 	render_template("header.html")
	site += render_template("index.html")
	site += render_template("footer.html")
	return site

## /metadata/<_id>
# Metadata page, isplays metadata
#
# Params:
#	- _id: ID of the metadata (24 byte hex string)
@app.route("/metadata/<_id>")
def metadata(_id):
	payload = {'_id': _id}
	response = requests.get(url = "http://metadata-api:5000/api/metadata", json = payload) 

	site = render_template("header.html")
	if response.json() and response.status_code == 200:
		site += render_template("metadata.html", metadata=response.json()[0])
	else:
		site += render_template("404.html")
	site += render_template("footer.html")
	return site

## /search/<title> -- GET
# Retreives metadata from the database
#
# Params:
#	- title: regex of the titles to search for
#
# Example data:
#	{"title": "pplication"} (returns all metadata that contains "pplication")
#
# Returns:
#	- 200: Successfully returned a search
#	- 400: Bad data
@app.route("/search/<title>")
def search(title):
	payload = {"title": title}
	response = requests.get(url = "http://metadata-api:5000/api/metadata/search", json = payload) 
	return json.dumps(response.json())

# /add -- POST
# Adds metadata json into the database
#
# Params:
#	- request: request data to get json, must contain all
#		required fields and no extra
#
# Example data:
#	{
#		"title": "Application 2",
#		"version": "0.2.1",
#		"maintainers": [
#			{
#				"name": "firstmaintainer app1",
#				"email": "secondmaintainer@gmail.com"
#				
#			}
#		],
#		"company": "Random Inc.",
#		"website": "https://website.com",
#		"source": "https://github.com/random/repo",
#		"license": "Apache-2.0",
#		"description": "### Interesting Title"
#	}
#
# Returns:
#	- 201: Data successfully stored
#	- 400: Bad data
@app.route('/add', methods=['POST'])
def addMetadata():
	payload = request.json
	response = requests.post(url = "http://metadata-api:5000/api/metadata", json = payload) 
	return json.dumps(response.json()), response.status_code

@app.errorhandler(404) 
def not_found(e): 
	site = render_template("header.html")
	site += render_template("404.html")
	site += render_template("footer.html")
	return site

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=80)
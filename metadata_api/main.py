from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import re
import os
import sys


app = Flask(__name__)

client = MongoClient(os.environ.get("DB")) 
db = client.app_metadata

fields = ["title", "version", "maintainers", "company", "website", "source", "license", "description"];
maintainer_fields = ["name", "email"]


## /api/metadata endpoint -- POST, GET, PUT, DELETE
# Routes CRUD requests to appropriate function
@app.route("/api/metadata", methods = ["POST", "GET", "PUT", "DELETE"])
def metadata_endpoint():
	if not request.data:
		return message("No request data found", 400)
	if not request.is_json:
		return message("Requst data must be in JSON format", 400)

	if request.method 	== 	"GET":
		return get_metadata(request)
	elif request.method == 	"POST":
		return post_metadata(request)
	elif request.method == 	"PUT":
		return put_metadata(request)
	elif request.method == 	"DELETE":
		return delete_metadata(request)
	return message("Invalid HTTP method", 401)


## /api/metadata -- GET
# Retreives metadata from the database
#
# Params:
#	- request: request data to get json query
#
# Example data:
#	{"title": "Application 1"} (returns all metadata with the title "Application 1")
#
# Returns:
#	- 200: Data successfully retreived
#	- 400: Bad data
def get_metadata(request):
	query = request.json

	if "_id" in query:
		if not is_valid_id(query["_id"]):
			return message("Invalid id: " + query["_id"], 400)
		query["_id"] = ObjectId(query["_id"])

	return dumps(db.metadata.find(query))
	#, {"_id": 0}))


# /api/metadata -- POST
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
def post_metadata(request):
	data = request.json

	valid_error = check_validation(data)
	if valid_error:
		return message(valid_error, 400)

	db.metadata.insert_one(data)
	return message("Success", 201)


# /api/metadata -- PUT
# Updates metadata
#
# Params:
#	- request: request data to get json query / update
#
# Example data:
#	{"query": {"version": "0.2"}, "data": {"title": "New Application name"}}
#	(updates all metadata with version 0.2 to a new title "New Application name")
#
# Returns:
#	- 200: Data successfully updated
#	- 400: Bad data
def put_metadata(request):
	if not "query" in request.json:
		return message("Missing query", 400)
	if not "data" in request.json:
		return message("Missing data", 400)

	query = request.json["query"]
	data = request.json["data"]
	db.metadata.update(query, { "$set": data })
	return message("Success", 200)


# /api/metadata -- DELETE
# Updates metadata
#
# Params:
#	- request: request data to get json query
# 		query can not be empty for delete
#
# Example data:
#	{"title": "Application 1"} (removes all metadata with the title "Application 1")
#
# Returns:
#	- 200: Data successfully removed
#	- 400: Bad data
def delete_metadata(request):
	query = request.json
	if len(query) < 1:
		return message("Query parameters needed", 400)

	db.metadata.delete_many(query)
	return message("Success", 200)


# /api/metadata/search -- GET
# Searches database for metadata that
# satisfies the given regex
#
# Params:
#	- request: request data to get json query
# 		query should only contain "title"
#
# Example data:
#	{"title": "pplication"} (returns all metadata with a title containing "pplication")
#
# Returns:
#	- 200: Successfully returned a search
#	- 400: Bad data
@app.route("/api/metadata/search", methods = ["GET"])
def metadata_search():
	title = request.json["title"]
	return dumps(db.metadata.find({"title" :{"$regex":title}}))


## check_validation
# Checks if metadata json is valid
#
# Params
# 	- data: json data being tested
#
# Returns: string describing the error, 
#	empty if there is no error
def check_validation(data):

	# Check for missing fields
	for field in fields:
		if not field in data:
			return "Missing field: " + field

	# Check for extra fields
	for field in data:
		if not field in fields:
			return "Extra field: " + field

	# Check for empty fields
	for field in fields:
		if field != "maintainers" and is_empty_string(data[field]):
			return "Field is empty: " + field

	for maintainer in data["maintainers"]:

		# Check for missing maintainer fields
		for field in maintainer_fields:
			if not field in maintainer:
				return "Maintainer missing field: " + field

		# Check for extra maintainer fields
		for field in maintainer:
			if not field in maintainer_fields:
				return "Maintainer extra field: " + field

		# Check for empty maintainer fields
		for field in maintainer_fields:
			if is_empty_string(maintainer[field]):
				return "Field is empty: " + field

		# Check email validation
		email = maintainer["email"]
		if not is_valid_email(email):
				return "Maintainer email: " + email + " is not valid"

	# Check website validation
	if not is_valid_website(data["website"]):
		return "Website: " + data["website"] + " is not valid"

	return ""


## is_valid_email
# Checks whether a given email is valid
#
# Params:
# 	- email (string): String of the email
#
# Returns: boolean
def is_valid_email(email):
	pattern = re.compile("^([\w\.\-]+)@([\w]+)(\.(\w){2,3})$")
	return pattern.match(email)


## is_valid_website
# Checks whether a given web address is valid
#
# Params:
# 	- website (string): String of the website
#
# Returns: boolean
def is_valid_website(website):
	pattern = re.compile("^(http)(s?):\/\/(\w+)\.(\w){2,3}$")
	return pattern.match(website)

## is_valid_id
# Checks whether a given mongo id is valid
# Mongo ids are 24 digit hex strings, a-f 0-9
#
# Params:
# 	- _id (string): String of the id
#
# Returns: boolean
def is_valid_id(_id):
	pattern = re.compile("^[a-f0-9]{24}$")
	return pattern.match(_id)

## is_empty_string
# Checks whether a given string only whitespace
#
# Params:
# 	- string (string): String to check for whitespace
#
# Returns: boolean
def is_empty_string(string):
	pattern = re.compile("^\s*$")
	return pattern.match(string)

## message
# Creates a json message to respond
#
# Params:
# 	- resp (string): Message
#	- code (integer): HTTP status code
#
# Returns: json object
def message(resp, code):
	return jsonify({"message": resp}), code


if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=5000)
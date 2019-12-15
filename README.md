# Metadata API

## 1. Running
To run the api and web server, simply go to the root directory of the project and run docker-compose
```
sudo docker-compose up --build
```
To run test cases first ensure the server is running, go to the metadata_api then run
```
python3 test_api.py
```
(or python if you only have 3+ installed)
It is recommended that the entire database gets deleted before running tests 

## 2. Endpoints
The front-end site can be reached at http://localhost (port 80)
The database API can be reached at http://localhost:5000

## 3. API
### /api/metadata -- GET
Retreives metadata from the database
Params:
* request: request data to get json query

Returns:
* 200: Data successfully 
* 400: Bad data

Example data:
```
{"title": "Application 1"} 
(returns all metadata with the title "Application 1")
```
---
### /api/metadata -- POST
Adds metadata json into the database
Params:
* request: request data to get json, must contain all
required fields and no extra

Returns:
* 201: Data successfully stored
* 400: Bad data

 Example data:
 ```
{
	"title": "Application 2",
	"version": "0.2.1",
	"maintainers": [
		{
			"name": "firstmaintainer app1",
			"email": "firstmaintainer@gmail.com"
		},
		{
			"name": "secondmaintainer app1",
			"email": "secondmaintainer@gmail.com"
		}
	],
	"company": "Random Inc.",
	"website": "https://website.com",
	"source": "https://github.com/random/repo",
	"license": "Apache-2.0",
	"description": "### Interesting Title"
}
```
---
### /api/metadata -- PUT
Updates metadata
Params:
* request: request data to get json query / update

Returns:
* 200: Data successfully updated
* 400: Bad data

Example data:
```
{"query": {"version": "0.2"}, "data": {"title": "New Application name"}}
(updates all metadata with version 0.2 to a new title "New Application name")
```
---
### /api/metadata -- DELETE
Updates metadata
Params:
* request: request data to get json query
		query can not be empty for delete

Returns:
* 200: Data successfully removed
* 400: Bad data

Example data:
```
{"title": "Application 1"} (removes all metadata with the title "Application 1")
```
---
### /api/metadata/search -- GET
Searches database for metadata that satisfies the given regex
Params:
* request: request data to get json query
 query should only contain "title"

Returns:
* 200: Successfully returned a search
* 400: Bad data

 Example data:
 ```
{"title": "pplication"} (returns all metadata with a title containing "pplication")
```


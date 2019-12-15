import unittest
import requests
import json

class TestApi(unittest.TestCase):

	def test_post(self):
		str = """{
		"title": "Valid App 2",
		"version": "0.0.1",
		"maintainers": [
		{
		"name": "firstmaintainer app1",
		"email": "secondmaintainer@gmail.com"
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
		}"""
		payload = json.loads(str)
		response = requests.post(url = "http://localhost:5000/api/metadata", json = payload) 

		assert response.json()["message"] 	== "Success"
		assert response.status_code 		== 201

	def test_invalid_post(self):
		str = """{
		"title": "Valid App 2",
		"version": "0.0.1",
		"maintainers": [
		{
		"name": "firstmaintainer app1",
		"email": "secondmaintainer@gmail.com"
		},
		{
		"name": "secondmaintainer app1",
		"email": "secondmaintainer@gmail.com"
		}
		],
		"company": "Random Inc.",
		"source": "https://github.com/random/repo",
		"license": "Apache-2.0",
		"description": "### Interesting Title"
		}"""
		payload = json.loads(str)
		response = requests.post(url = "http://localhost:5000/api/metadata", json = payload) 

		assert response.json()["message"] 	== "Missing field: website"
		assert response.status_code 		== 400

	def test_get(self):
		str = """{
		"title": "Valid App 2",
		"version": "0.0.1",
		"maintainers": [
		{
		"name": "firstmaintainer app1",
		"email": "secondmaintainer@gmail.com"
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
		}"""
		payload = json.loads(str)
		requests.post(url = "http://localhost:5000/api/metadata", json = payload) 

		str = '{"title": "Valid App 2"}'
		payload = json.loads(str)
		response = requests.get(url = "http://localhost:5000/api/metadata", json = payload) 

		assert response.json()[0]["title"] 	== "Valid App 2"
		assert response.status_code 		== 200

	def test_empty_get(self):
		str = '{"title": "Valid App 3"}'
		payload = json.loads(str)
		response = requests.get(url = "http://localhost:5000/api/metadata", json = payload) 

		assert len(response.json()) == 0
		assert response.status_code == 200

	def test_update(self):
		str = '{"query": {"version": "0.0.1"}, "data": {"title": "New title"} }'
		payload = json.loads(str)
		response = requests.put(url = "http://localhost:5000/api/metadata", json = payload) 

		str = '{"title": "Valid App 3"}'
		payload = json.loads(str)
		getResponse = requests.get(url = "http://localhost:5000/api/metadata", json = payload) 

		str = '{"title": "New title"}'
		payload = json.loads(str)
		getResponse2 = requests.get(url = "http://localhost:5000/api/metadata", json = payload) 

		assert len(getResponse.json()) 			== 0
		assert getResponse2.json()[0]["title"] 	== "New title"
		assert response.status_code 			== 200

	def test_delete(self):
		str = """{
		"title": "Delete me",
		"version": "0.0.1",
		"maintainers": [
		{
		"name": "firstmaintainer app1",
		"email": "secondmaintainer@gmail.com"
		},
		{
		"name": "secondmaintainer app1",
		"email": "secondmaintainer@gmail.com"
		}
		],
		"company": "Random Inc.",
		"source": "https://github.com/random/repo",
		"license": "Apache-2.0",
		"description": "### Interesting Title"
		}"""
		payload = json.loads(str)
		requests.post(url = "http://localhost:5000/api/metadata", json = payload) 

		str = '{"title": "Delete me"}'
		payload = json.loads(str)
		response = requests.delete(url = "http://localhost:5000/api/metadata", json = payload)

		str = '{"title": "Delete me"}'
		payload = json.loads(str)
		getResponse = requests.get(url = "http://localhost:5000/api/metadata", json = payload) 

		assert len(getResponse.json()) 		== 0
		assert response.json()["message"] 	== "Success"
		assert response.status_code 		== 200

	def test_invalid_delete(self):
		str = '{}'
		payload = json.loads(str)
		response = requests.delete(url = "http://localhost:5000/api/metadata", json = payload) 

		assert response.json()["message"] 	== "Query parameters needed"
		assert response.status_code 		== 400

	def test_search(self):
		str = """{
		"title": "abcdefghijklmnopqrstuvwxyz",
		"version": "0.0.1",
		"maintainers": [
		{
		"name": "firstmaintainer app1",
		"email": "secondmaintainer@gmail.com"
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
		}"""
		payload = json.loads(str)
		requests.post(url = "http://localhost:5000/api/metadata", json = payload)

		str = '{"title": "ef"}'
		payload = json.loads(str)
		response = requests.get(url = "http://localhost:5000/api/metadata/search", json = payload) 

		assert len(response.json()) 	>= 1
		assert response.status_code 	== 200

if __name__ == '__main__':
	unittest.main()
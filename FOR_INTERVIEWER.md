# For the interviewer

Hello, thank you for taking the time to look at this test
I would like to use this page to explain some of the technical and design choises I made

## 1. Tech Used
The framework I used was Flask, which is written in python. I used flask because it is used at Pinkaloo and because I am quite comfterable with it. In addition python and Flask are great for getting projects started quickly.

The entire server runs using docker-compose. Docker-compose is great at quickly orchestrating different services, for this project I use it to run 2 instances of Flask for serving the front-end site and one for the database-api. I also spin up a mongodb container for the database.

I chose to use mongo over SQL because I find mongo is easier to set up (no need to specify tables and what not), and since the data I'm working on is in JSON, mongo is perfecct since it uses JSON as its interface.

## 2. Design Choices
### Architecture
The entire project is made of 3 microservcies, this approach gives loose coupling between the front-end server and the api-database, and allows additional components to be easily placed.

### Endpoints
I chose to have 5 endpoints for the project, 4 for simple CRUD, and a fifth one for searching. The difference between get api/metadata and get api/metadata/search is that get api/metadata searches explicitely on the key and value pairs specified, where as get api/metadata/search uses regex only on the title. 

### Validation
Validation is done in the database-api and returns descriptive error messages. The main things that are validated are:
* On post, all fields must be included, fields can not be whitespace only, and no extra fields are allowed
* Emails and websites must be in correct format
* If on get metadata the id is passed, it must be a 24 character hex string
* On delete, some query must be specified (to not delete entire database)
    * Empty quieries are allowed for find, which will return all metadata
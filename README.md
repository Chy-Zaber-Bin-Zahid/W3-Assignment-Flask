# W3-Assignment-Flask

- ```git clone https://github.com/Chy-Zaber-Bin-Zahid/W3-Assignment-Flask.git```
- cd W3-Assignment-Flask

## Create an environment and activate it

- ```python3.12 -m venv env```
- ```source env/bin/activate```
- ```pip install -r requirements.txt```

## Create a `.env` file and copy paste below code
```
JWT_SECRET_KEY=your_jwt_secret_key_here
PORT_AUTHENTICATION=5000
PORT_DESTINATION=5001
PORT_USER=5002
```

## Running and Testing setup

- To run server go to each service folder and run ```python main.py```
- To test go to each service folder and run ```pytest --cov```

# Swagger API

The server must be running in terminal in order to see swagger api

- `http://127.0.0.1:5000/apidocs/` Authentication Service
- `http://127.0.0.1:5001/apidocs/` Destination Service
- `http://127.0.0.1:5002/apidocs/` User Service

# Postman Collection

To help you get started quickly, I have provided a Postman collection that includes all our API endpoints with example requests.

### Importing the Collection

1. Download our Postman Collection: [W3 Flask Assignment.json](/Postman/W3_Flask_postman_collection.json)

2. Open Postman and click on "Import" in the top left corner

3. Drag and drop the downloaded JSON file or click "Upload Files" to select it

4. The collection will be imported with all available endpoints

### Available Endpoints in Collection

The collection includes the following endpoints:

**Destination Service**
- GET /destinations: Retrieve a list of all travel destinations.
- DELETE /destinations/<id>: Delete a specific travel destination (Admin-only).


**User Service**
- POST /register: Register a new user.
- POST /login: Authenticate a user and provide an access token.
- GET /profile: View profile information (user-specific).


**Authentication Service**
- GET /role-check: Verify user role is admin or not.
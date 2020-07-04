# This is an AUTH service that uses: JWT and BCrypt

A simple authentication service built with:
    - FastAPI (Python)
    - JSON Web Token authentication
    - BCrypt for hashing and salting passwords
    - PostgreSQL database


### The API and the DataBase both have their own docker image

To run the project use the following commands:
(you need to have DOCKER installed - https://www.docker.com/products/docker-desktop)

    - docker-compose build
    - docker-compose up


### Features / Routes

    - '/register' : Register a new user account
    - '/login' : Login with username and password (this returns an access_token which you'll need to pass in the 'Authorization' header with value: 'Bearer <your-access-token-here>' to be able to use the other routes)
    - '/status' : Only returns a json object -> {"status": "ok"} if you have a valid token
    - '/users/me/items' : Returns the current user and a list of items that belongs to it /the list is only a placeholder for now/


### To see the interactive docs visit: http://localhost:8001/docs

Here you will get SWAGGER UI and can interact with the API
Authorization doesn't work from this UI - for that you need to use Postman or similar to pass in the access_token as the Authorization header's value


### To generate your own SECRET_KEY for your passwords

    - Open a terminal window
    - Run command: $ openssl rand -hex 32
    - And paste your key as the value for the SECRET_KEY variable in utils.py
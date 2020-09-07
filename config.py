import os
from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo
from flask_restful_swagger import swagger

app = Flask(__name__)

api = swagger.docs(
    Api(app),
    apiVersion="0.1",
    basePath="http://0.0.0.0:5012",
    resourcePath="/",
    produces=["application/json"],
    api_spec_url="/api/spec",
    description="User Management service api documentation",
)

app.config['MONGO_DBNAME'] = os.environ["AZURE_SERVICE_DBNAME"]
app.config['MONGO_URI'] = "mongodb://" + os.environ["MONGODB_HOSTNAME"] + ":27017/" + os.environ["AZURE_SERVICE_DBNAME"]


@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', "*")
    response.headers.add('Access-Control-Allow-Methods', 'DELETE')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Authorization, X-Access-Token, data')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Content-Type', 'applictaion/json')
    return response


mongo = PyMongo(app)

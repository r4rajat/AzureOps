from flask_restful import Resource
from flask import make_response, request
import http
import json
import constant
from config import mongo


class ApplicationConfiguration(Resource):
    def options(self):
        return make_response(json.dumps({}), http.HTTPStatus.OK)

    def get(self):
        try:
            app_config = get_app_config()
            return make_response(json.dumps({
                constant.DATA: app_config,
                constant.STATUS: http.HTTPStatus.OK
            }), http.HTTPStatus.OK)
        except Exception as e:
            return make_response(json.dumps({
                constant.ERROR_MESSAGE: {constant.MESSAGE: str(e)},
                constant.STATUS: http.HTTPStatus.BAD_REQUEST
            }), http.HTTPStatus.BAD_REQUEST)

    def post(self):
        try:
            data = json.loads(request.data.decode())
            AZURE_SUBSCRIPTION_ID = data[constant.AZURE_SUBSCRIPTION_ID]
            AZURE_CLIENT_ID = data[constant.AZURE_CLIENT_ID]
            AZURE_CLIENT_SECRET = data[constant.AZURE_CLIENT_SECRET]
            AZURE_TENANT_ID = data[constant.AZURE_TENANT_ID]
            set_app_config(subscription_id=AZURE_SUBSCRIPTION_ID, client_id=AZURE_CLIENT_ID, client_secret=AZURE_CLIENT_SECRET, tenent_id=AZURE_TENANT_ID)
            return make_response(json.dumps({
                constant.DATA: "Configuration Done",
                constant.STATUS: http.HTTPStatus.OK
            }), http.HTTPStatus.OK)
        except Exception as e:
            return make_response(json.dumps({
                constant.ERROR_MESSAGE: {constant.MESSAGE: str(e)},
                constant.STATUS: http.HTTPStatus.BAD_REQUEST
            }), http.HTTPStatus.BAD_REQUEST)

    def put(self):
        pass


def get_app_config():
    try:
        app_config = mongo.db.app_config.find()
        config = []
        for i in app_config:
            config.append(i)
        config = config[0]
        return config['azure_config']

    except Exception as e:
        raise e


def set_app_config(subscription_id=None, client_id=None, client_secret=None, tenent_id=None):
    try:
        _config = {
            constant.AZURE_SUBSCRIPTION_ID: subscription_id,
            constant.AZURE_CLIENT_ID: client_id,
            constant.AZURE_CLIENT_SECRET: client_secret,
            constant.AZURE_TENANT_ID: tenent_id
        }
        mongo.db.app_config.update({}, {"$set": {"azure_config": _config}}, upsert=True)
    except Exception as e:
        raise e

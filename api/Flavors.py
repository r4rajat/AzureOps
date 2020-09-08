from flask_restful import Resource
from flask import make_response, request
import http
import json
import constant


from azure.mgmt.compute import ComputeManagementClient


from service import get_credentials


class Flavors(Resource):
    def options(self):
        return make_response(json.dumps({}), http.HTTPStatus.OK)

    def get(self):
        try:
            flavors = get_azure_flavors()
            return make_response(json.dumps({
                constant.DATA: flavors,
                constant.STATUS: http.HTTPStatus.OK
            }), http.HTTPStatus.OK)

        except Exception as e:
            return make_response(json.dumps({
                constant.ERROR_MESSAGE: {constant.MESSAGE: str(e)},
                constant.STATUS: http.HTTPStatus.BAD_REQUEST
            }), http.HTTPStatus.BAD_REQUEST)


def get_azure_flavors():
    try:
        credentials, subscription_id = get_credentials()
        compute_client = ComputeManagementClient(credentials=credentials, subscription_id=subscription_id)
        flavors = compute_client.virtual_machine_sizes.list()
        print(flavors)
    except Exception as e:
        raise e
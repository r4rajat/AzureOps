from flask_restful import Resource
from flask import make_response, request
import http
import json
from bson import json_util
import constant
from config import mongo


from azure.mgmt.compute import ComputeManagementClient


from service import get_credentials


class Flavors(Resource):
    def options(self):
        return make_response(json.dumps({}), http.HTTPStatus.OK)

    def get(self):
        try:
            flavors = get_azure_flavors()
            return make_response(json_util.dumps({
                constant.DATA: flavors,
                constant.STATUS: http.HTTPStatus.OK
            }), http.HTTPStatus.OK)

        except Exception as e:
            return make_response(json.dumps({
                constant.ERROR_MESSAGE: {constant.MESSAGE: str(e)},
                constant.STATUS: http.HTTPStatus.BAD_REQUEST
            }), http.HTTPStatus.BAD_REQUEST)


def get_azure_flavors():
    flavour_list = []
    flavours = mongo.db.azure_flavors.find()
    for flavor in flavours:
        flavour_list.append(flavor)

    return flavour_list


def fetch_azure_flavors():
    try:
        credentials, subscription_id = get_credentials()
        compute_client = ComputeManagementClient(credentials=credentials, subscription_id=subscription_id)
        flavors = compute_client.virtual_machine_sizes.list(location='westus')
        for flavor in flavors:
            mongo.db.azure_flavors.update({constant.NAME: flavor.name}, {"$set": {
                                                        constant.NUMBER_OF_CORES: flavor.number_of_cores,
                                                        constant.OS_DISK_SIZE_IN_MB: flavor.os_disk_size_in_mb,
                                                        constant.RESOURCE_DISK_SIZE_IN_MB: flavor.resource_disk_size_in_mb,
                                                        constant.MEMORY_IN_MB: flavor.memory_in_mb,
                                                        constant.MAX_DATA_DISK_COUNT: flavor.max_data_disk_count
                                                        }}, upsert=True)
    except Exception as e:
        raise e
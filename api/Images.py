import http
import json

from flask import make_response
from flask_restful import Resource

import constant
from service import get_credentials
from azure.mgmt.compute import ComputeManagementClient


class Images(Resource):
    def options(self):
        return make_response(json.dumps({}), http.HTTPStatus.OK)

    def get(self):
        try:
            images = get_azure_images()
            return make_response(json.dumps({
                constant.DATA: images,
                constant.STATUS: http.HTTPStatus.OK
            }), http.HTTPStatus.OK)

        except Exception as e:
            return make_response(json.dumps({
                constant.ERROR_MESSAGE: {constant.MESSAGE: str(e)},
                constant.STATUS: http.HTTPStatus.BAD_REQUEST
            }), http.HTTPStatus.BAD_REQUEST)


def get_azure_images():
    region = 'westus'
    credentials, subscription_id = get_credentials()
    compute_client = ComputeManagementClient(credentials=credentials, subscription_id=subscription_id)

    region = 'eastus'

    result_list_pub = compute_client.virtual_machine_images.list_publishers(
        region,
    )

    for publisher in result_list_pub:
        result_list_offers = compute_client.virtual_machine_images.list_offers(
            region,
            publisher.name,
        )

        for offer in result_list_offers:
            result_list_skus = compute_client.virtual_machine_images.list_skus(
                region,
                publisher.name,
                offer.name,
            )

            for sku in result_list_skus:
                result_list = compute_client.virtual_machine_images.list(
                    region,
                    publisher.name,
                    offer.name,
                    sku.name,
                )

                for version in result_list:
                    result_get = compute_client.virtual_machine_images.get(
                        region,
                        publisher.name,
                        offer.name,
                        sku.name,
                        version.name,
                    )

                    print('PUBLISHER: {0}, OFFER: {1}, SKU: {2}, VERSION: {3}'.format(
                        publisher.name,
                        offer.name,
                        sku.name,
                        version.name,
                    ))



import http
import json

from flask import make_response
from flask_restful import Resource

import constant
from service import get_credentials
from azure.mgmt.compute import ComputeManagementClient
from config import mongo


class Images(Resource):
    def options(self):
        return make_response(json.dumps({}), http.HTTPStatus.OK)

    def get(self):
        try:
            images = fetch_azure_images()
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
    pass


def fetch_azure_images():
    credentials, subscription_id = get_credentials()
    compute_client = ComputeManagementClient(credentials=credentials, subscription_id=subscription_id)

    region = 'westus'

    # result_list_pub = compute_client.virtual_machine_images.list_publishers(
    #     region,
    # )
    images_list = []
    result_list_pub = ['Canonical', 'RedHat']
    for publisher in result_list_pub:
        result_list_offers = compute_client.virtual_machine_images.list_offers(
            region,
            publisher,
        )
        images = {publisher: []}
        for offer in result_list_offers:
            result_list_skus = compute_client.virtual_machine_images.list_skus(
                region,
                publisher,
                offer.name,
            )

            for sku in result_list_skus:
                result_list = compute_client.virtual_machine_images.list(
                    region,
                    publisher,
                    offer.name,
                    sku.name
                    # "latest"
                )
                _images = {offer.name: sku.name}
                if _images not in images[publisher]:
                    images[publisher].append(_images)
                    print('PUBLISHER: {0}, OFFER: {1}, SKU: {2}'.format(
                        publisher,
                        offer.name,
                        sku.name,
                    ))
        images_list.append(images)
    a = 2+2
    print(a)
                # mongo.db.azure_images.insert_one({
                #     constant.PUBLISHER: publisher,
                #     constant.OFFER: offer.name,
                #     constant.SKU: sku.name,
                #     constant.VERSION: "latest"
                # })


from api.AppConfig import get_app_config
from azure.common.credentials import ServicePrincipalCredentials
import constant


def get_credentials():
    app_config = get_app_config()
    subscription_id = app_config[constant.AZURE_SUBSCRIPTION_ID]
    credentials = ServicePrincipalCredentials(
        client_id=app_config[constant.AZURE_CLIENT_ID],
        secret=app_config[constant.AZURE_CLIENT_SECRET],
        tenant=app_config[constant.AZURE_TENANT_ID]
    )
    return credentials, subscription_id
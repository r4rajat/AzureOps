from config import api, app
import constant
import os
from api.AppConfig import ApplicationConfiguration
from api.Images import Images
from api.Flavors import Flavors


api.add_resource(ApplicationConfiguration, '/api/azure/application-configuration')
api.add_resource(Images, '/api/azure/images')
api.add_resource(Flavors, '/api/azure/flavors')



if __name__ == '__main__':
    ENVIRONMENT_DEBUG = os.environ.get(constant.APP_DEBUG, True)
    ENVIRONMENT_HOST = os.environ.get(constant.APP_HOST, '0.0.0.0')
    ENVIRONMENT_PORT = os.environ.get(constant.APP_PORT, '5012')
    app.run(debug=ENVIRONMENT_DEBUG, host=ENVIRONMENT_HOST, port=ENVIRONMENT_PORT)
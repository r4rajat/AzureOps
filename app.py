from config import api, app
import constant
import os
from api.AppConfig import ApplicationConfiguration

api.add_resource(ApplicationConfiguration, '/api/azure/application-configuration')



if __name__ == '__main__':
    ENVIRONMENT_DEBUG = os.environ.get(constant.APP_DEBUG, True)
    ENVIRONMENT_HOST = os.environ.get(constant.APP_HOST, '0.0.0.0')
    ENVIRONMENT_PORT = os.environ.get(constant.APP_PORT, '5012')
    app.run(debug=ENVIRONMENT_DEBUG, host=ENVIRONMENT_HOST, port=ENVIRONMENT_PORT)
"""Application factory and configuration for azure_lightning_flask applications"""

from logging import getLogger, StreamHandler
from warnings import warn
from flask import Flask
from flask_env import MetaFlaskEnv
from azure_lightning_flask.application_blueprint import application_blueprint

class Configuration(object): # pylint: disable=too-few-public-methods
    """Config merging environment variables into flask config using flask-env"""
    __metaclass__ = MetaFlaskEnv

    # Default values for configuration taken from ember-cli-deploy-azure
    AZURE_STORAGE_TABLE = 'emberdeploy'
    AZURE_STORAGE_TABLE_PARTITION_KEY = 'manifest'
    REVISION_PARAMETER = 'index_key'

def create_app(config=Configuration):
    """Return azure_lightning_flask application using given configuration"""
    app = Flask(__name__)

    app.config.from_object(config)

    required_environment_variables = [
        'AZURE_STORAGE_ACCOUNT',
        'AZURE_STORAGE_KEY',
        'APP_NAME',
    ]

    for required_environment_variable in required_environment_variables:
        if not app.config.get(required_environment_variable):
            warning = "Environment variable {0} must be set!".format(required_environment_variable)
            warn(warning)

    # Setup logging for Azure network requests
    azure_logger = getLogger('azure.storage.common.storageclient')
    azure_logger_handler = StreamHandler()
    azure_logger_handler.setLevel(app.logger.getEffectiveLevel())
    azure_logger.addHandler(azure_logger_handler)

    app.register_blueprint(application_blueprint)

    return app

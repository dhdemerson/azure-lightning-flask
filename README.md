# azure_lightning_flask
A [Flask](http://flask.pocoo.org/) server to serve single-page applications deployed using the [lightning strategy](http://ember-cli-deploy.com/docs/v1.0.x/the-lightning-strategy/) on [Azure Table Storage](https://azure.microsoft.com/en-us/services/storage/tables/). Designed to work with [Ember-cli-deploy-azure](https://github.com/duizendnegen/ember-cli-deploy-azure), but should be compatible with any lightning strategy demployment on Azure Table Storage via configuration. Developed with Python 2.7

## Installation
```
pip install -r requirements.txt
```
## Application Configuration
Configure the application by setting environment variables. **All application configuration variables without a default must be set.**

This application serves content from [Azure Storage Table](https://azure.microsoft.com/en-us/services/storage/tables/) requiring an Azure account and a storage table to be setup for some of the required configuration.

|Environment Variable | Usage | Default
|---|---|---|
|AZURE_STORAGE_ACCOUNT|The name of the Azure Storage account to be used|None (Must be set)
|AZURE_STORAGE_KEY|The key for the given Azure Storage account| None (Must be set)
|AZURE_STORAGE_TABLE|The name of the table where revisions are stored|`emberdeploy`
|AZURE_STORAGE_TABLE_PARTITION_KEY|The partition key to search under|`manifest`
|APP_NAME|The name of the application being served|None (Must be set)
|REVISION_PARAMETER|The query parameter used to request specific revisions|`index_key`

## Running
```
export FLASK_APP=runserver.py
flask run
```

## Flask configuration
[Flask configuration values](http://flask.pocoo.org/docs/0.12/config/#builtin-configuration-values) can also be set via environment variables as the environment is merged into the flask configuration via [flask-env](https://github.com/brettlangdon/flask-env).

## Running tests
Run tests with [Nose](http://nose.readthedocs.io/en/latest/). After installing run `nosetests` in the root directory of the project.
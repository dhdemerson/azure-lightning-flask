azure_lightning_flask
=====================

A `Flask`_ server to serve single-page applications deployed using the
`lightning strategy`_ on `Azure Table Storage`_. Designed to work with
`Ember-cli-deploy-azure`_, but should be compatible with any lightning
strategy deployment on Azure Table Storage via configuration. Developed
with Python 2.7

Installation
------------
It is recommended that you install and run azure_lightning_flask inside of a ``virtualenv``
::

    virtualenv venv
    . venv/bin/activate

Via pip
~~~~~~~
::

    pip install azure_lightning_flask

Manual
~~~~~~

Download the application files and in the root directory run

::

    pip install -r requirements.txt
    python setup.py install

Application Configuration
-------------------------

Configure the application by setting environment variables. **All
application configuration variables without a default must be set.**

This application serves content from `Azure Storage Table`_ requiring an
Azure account and a storage table to be setup for some of the required
configuration.

+-----------------------+-----------------------+-----------------------+
| Environment Variable  | Usage                 | Default               |
+=======================+=======================+=======================+
| AZURE_STORAGE_ACCOUNT | The name of the Azure | None (Must be set)    |
|                       | Storage account to be |                       |
|                       | used                  |                       |
+-----------------------+-----------------------+-----------------------+
| AZURE_STORAGE_KEY     | The key for the given | None (Must be set)    |
|                       | Azure Storage account |                       |
+-----------------------+-----------------------+-----------------------+
| AZURE_STORAGE_TABLE   | The name of the table | ``emberdeploy``       |
|                       | where revisions are   |                       |
|                       | stored                |                       |
+-----------------------+-----------------------+-----------------------+
| AZURE_STORAGE_TABLE_P | The partition key to  | ``manifest``          |
| ARTITION_KEY          | search under          |                       |
+-----------------------+-----------------------+-----------------------+
| APP_NAME              | The name of the       | None (Must be set)    |
|                       | application being     |                       |
|                       | served                |                       |
+-----------------------+-----------------------+-----------------------+
| REVISION_PARAMETER    | The query parameter   | ``index_key``         |
|                       | used to request       |                       |
|                       | specific revisions    |                       |
+-----------------------+-----------------------+-----------------------+

Running
-------

After it is configured, run the application with

::

    azure_lightning_flask

Flask configuration
-------------------

`Flask configuration values`_ can also be set via environment variables
as the environment is merged into the flask configuration via
`flask-env`_.

Running tests
-------------

::

    python setup.py nosetests

.. _Flask: http://flask.pocoo.org/
.. _lightning strategy: http://ember-cli-deploy.com/docs/v1.0.x/the-lightning-strategy/
.. _Azure Table Storage: https://azure.microsoft.com/en-us/services/storage/tables/
.. _Ember-cli-deploy-azure: https://github.com/duizendnegen/ember-cli-deploy-azure
.. _Azure Storage Table: https://azure.microsoft.com/en-us/services/storage/tables/
.. _Flask configuration values: http://flask.pocoo.org/docs/0.12/config/#builtin-configuration-values
.. _flask-env: https://github.com/brettlangdon/flask-env
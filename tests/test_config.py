"""The configuration class used for testing using no default values"""

class TestConfig(object): # pylint: disable=too-few-public-methods
    """The configuration class used for testing using no default values"""
    AZURE_STORAGE_ACCOUNT = 'TestApplicationAccount'
    AZURE_STORAGE_KEY = 'TestApplicationKey'
    AZURE_STORAGE_TABLE = 'TestApplicationTable'
    AZURE_STORAGE_TABLE_PARTITION_KEY = 'TestApplicationPartitionKey'
    APP_NAME = 'TestApplicationRowKeyAppName'
    REVISION_PARAMETER = 'TestApplicationRevisionParameter'

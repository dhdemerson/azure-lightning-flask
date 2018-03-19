"""Helpers for the application"""

from azure.cosmosdb.table import TableService
from flask import g, current_app as app

def format_row_key(revision):
    """Return a formatted row key for a given revision."""
    return '{app}:{revision}'.format(
        app=app.config['APP_NAME'],
        revision=revision)

def get_table_service():
    """Return the TableService instance for this request initializing it if it doesn't exist."""
    table_service = getattr(g, 'table_service', None)
    if table_service is None:
        table_service = g.table_service = TableService(
            account_name=app.config['AZURE_STORAGE_ACCOUNT'],
            account_key=app.config['AZURE_STORAGE_KEY'])
    return table_service

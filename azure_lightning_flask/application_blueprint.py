"""The blueprint for the azure_lightning_flask application"""

from flask import Blueprint, request, abort, current_app as app
from azure.common import AzureMissingResourceHttpError
from azure_lightning_flask.helpers import format_row_key, get_table_service

application_blueprint = Blueprint('application', __name__) # pylint: disable=C0103

ACTIVE_REVISION = 'current'

# Respond to all requests regardless of path letting the served application handle routing
@application_blueprint.route('/', defaults={'path': ''})
@application_blueprint.route('/<path:path>')
def index(path):
    # pylint: disable=unused-argument
    # Flask will crash with a 500 error if path is not included
    """Return the active revision of the application, or the revision requested if specified"""

    revision = request.args.get(app.config['REVISION_PARAMETER'])

    if revision:
        response = content_for_revision(revision)
    else:
        response = content_for_active_revision()
    return response

def content_for_active_revision():
    """Return the active revision of the application"""
    active_row_key = format_row_key(ACTIVE_REVISION)
    row_key = fetch_row_content(active_row_key)
    return fetch_row_content(row_key)

def content_for_revision(revision):
    """Return the requested revision of the application"""
    row_key = format_row_key(revision)
    try:
        content = fetch_row_content(row_key)
    except AzureMissingResourceHttpError as error:
        if error.status_code == 404:
            content = abort(404)
        else:
            raise
    return content

def fetch_row_content(row_key):
    """Return the content for the row with the given row_key"""
    table_service = get_table_service()
    return table_service.get_entity(
        app.config['AZURE_STORAGE_TABLE'],
        app.config['AZURE_STORAGE_TABLE_PARTITION_KEY'],
        row_key).content

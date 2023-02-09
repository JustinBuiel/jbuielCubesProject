"""
Gather entry data from the form's backend
"""

import sys
from secrets import wufoo_key  # type: ignore reportShadowedImport
import requests
from requests.auth import HTTPBasicAuth


def get_json_data() -> dict:
    """Accesses the JSON data from the form using httpbasicauth and the API key"""
    url = "https://justinb.wufoo.com/api/v3/forms/cubes-project-proposal-submission/entries/json"
    response = requests.get(url, auth=HTTPBasicAuth(wufoo_key, 'pass'))

    # No data retrieved, terminate program execution
    if response.status_code != 200:
        print(
            f'Failed to get data, response from website: {response.status_code} with error: {response.reason}')
        sys.exit(-1)

    json_object = response.json()
    print('Data gathered from api')
    return json_object

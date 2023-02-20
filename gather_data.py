"""
Gather entry data from the form's backend
"""

import sys
from secrets import wufoo_key  # type: ignore reportShadowedImport
import requests
from requests.auth import HTTPBasicAuth

WUFOO_KEY: str = wufoo_key
URL = "https://justinb.wufoo.com/api/v3/forms/cubes-project-proposal-submission/entries/json"


def get_json_data() -> dict[str, list[dict[str, str]]]:
    """Accesses the JSON data from the form using httpbasicauth and the API key"""
    response = requests.get(URL, auth=HTTPBasicAuth(WUFOO_KEY, 'pass'))

    # No data retrieved, terminate program execution
    if response.status_code != 200:
        print(
            f'Failed to get data, response from website: {response.status_code} with error: {response.reason}')
        sys.exit(-1)

    json_object: dict = response.json()
    print('Data gathered from api')
    return json_object

import requests
from secrets import wufoo_key
import sys
from requests.auth import HTTPBasicAuth


def get_json_data() -> dict:
    url = "https://justinb.wufoo.com/api/v3/forms/cubes-project-proposal-submission/entries/json"
    response = requests.get(url, auth=HTTPBasicAuth(wufoo_key, 'pass'))

    if response.status_code != 200:
        print(
            f'Failed to get data, response from website: {response.status_code} with error: {response.reason}')
        sys.exit(-1)

    json_object = response.json()
    return json_object

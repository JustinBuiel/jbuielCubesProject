import requests
import sys
from secret import wufoo_key
from requests.auth import HTTPBasicAuth


def main():
    url = "https://justinb.wufoo.com/api/v3/forms/cubes-project-proposal-submission/entries/json"
    response = requests.get(url, auth=HTTPBasicAuth(wufoo_key, 'pass'))

    if response.status_code != 200:
        print(
            f'Failed to get data, response from website: {response.status_code} with error: {response.reason}')
        sys.exit(-1)

    json_object = response.json()
    print(json_object)


if __name__ == "__main__":
    main()

from gather_data import get_json_data


def test_data_amount():
    json_test: dict = get_json_data()
    lst_test = json_test['Entries']
    assert len(lst_test) == 2

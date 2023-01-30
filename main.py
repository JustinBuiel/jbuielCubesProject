from gather_data import get_json_data
from process_data import process


def main():
    json_object = get_json_data()
    process(json_object)


if __name__ == "__main__":
    main()

from datetime import datetime


def process(json_object: dict):  # noqa: C901
    global time
    time = datetime.now().strftime('%Y%m%d-%H%M%S')

    lst = json_object['Entries']
    entries = len(lst)
    count = 0
    try:
        for entry in lst:
            count += 1
            write_data_to_file(f"Entry: {entry['EntryId']}")
            write_data_to_file('_'*24)
            write_data_to_file(
                f"Name: {entry['Field1']} {entry['Field2']} {entry['Field3']}")
            write_data_to_file(f"Title: {entry['Field4']}")
            write_data_to_file(f"Organization: {entry['Field5']}")
            write_data_to_file(f"Email: {entry['Field6']}")
            if entry['Field7'] != '':
                write_data_to_file(f"Website: {entry['Field7']}")
            if entry['Field9'] != '':
                phone_number: str = entry['Field9'][:3] + '-' + \
                    entry['Field9'][3:6] + '-' + entry['Field9'][6:]
                write_data_to_file(f"Phone: {phone_number}")

            write_data_to_file('\nOpportunities Interested in:')
            write_data_to_file(f"{entry['Field11']}")
            write_data_to_file(f"{entry['Field12']}")
            write_data_to_file(f"{entry['Field13']}")
            write_data_to_file(f"{entry['Field14']}")
            write_data_to_file(f"{entry['Field15']}")
            write_data_to_file(f"{entry['Field16']}")
            write_data_to_file(f"{entry['Field17']}")

            write_data_to_file('\nTime Period:')
            write_data_to_file(f"{entry['Field111']}")
            write_data_to_file(f"{entry['Field112']}")
            write_data_to_file(f"{entry['Field113']}")
            write_data_to_file(f"{entry['Field114']}")
            write_data_to_file(f"{entry['Field115']}")

            write_data_to_file(f"\nName Permission: {entry['Field211']}")

            if entries != count:
                write_data_to_file('\n\n')
    except KeyError as exception:
        print(f'KeyError:{exception}, using universal method')
        universal_processing(lst)


def write_data_to_file(str):
    if str == '':
        return
    file_name = f"form_entries_{time}.txt"
    with open(file_name, 'a') as fileIO:
        fileIO.write(str + '\n')


def universal_processing(lst):
    entries = len(lst)
    count = 0

    file_name = f"form_entries_{time}.txt"
    with open(file_name, 'w') as fileIO:
        fileIO

    for entry in lst:
        count += 1
        for k, v in entry.items():
            write_data_to_file(f"{k}: {v}")
        if entries != count:
            write_data_to_file('\n\n')

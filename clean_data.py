import csv
import os
import re

MALE_NAMES_FILE = 'data/male_names.csv'
FEMALE_NAMES_FILE = 'data/female_names.csv'

male_names, female_names = None, None

capture_year = re.compile(r'[12][0-9]{3}')


def load_names():
    global male_names, female_names

    with open(MALE_NAMES_FILE) as f:
        male_names = set(row[0] for row in csv.reader(f))
    with open(FEMALE_NAMES_FILE) as f:
        female_names = set(row[0] for row in csv.reader(f))


def guess_gender(name):
    if name is None:
        return None

    name = name.title()

    if name in male_names:
        return 'M'
    if name in female_names:
        return 'F'


def parse_name(name_str):
    try:
        name, *_, surname = name_str.strip().split()
    except:
        name, surname = None, None
    return name, surname


def parse_dates(date_str):
    years = capture_year.findall(date_str)
    
    if years is not None and len(years) == 2:
        born, died = map(int, years)

        if born <= died:
            return born, died

    return None, None


def clean_data(input_dir, output_dir, output_filename):
    out_file = os.path.join(output_dir, output_filename)
    
    if os.path.exists(out_file):
        os.remove(out_file)   
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        print(f'Cleaning data from {filename}')        
        data = []

        with open(os.path.join(input_dir, filename)) as f:
            reader = csv.reader(f)
            reader.__next__()  # skip header

            for person in reader:
                name_str, date_str = person

                name, surname = parse_name(name_str)
                born_year, died_year = parse_dates(date_str)
                gender = guess_gender(name)

                data.append(
                    (name, surname, gender, born_year, died_year)
                )

        with open(out_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerows(data)
    
    print(f'Done. All data written to {out_file}.')


if __name__ == '__main__':
    load_names()
    clean_data('data/raw', 'data/cleaned', 'data.csv')
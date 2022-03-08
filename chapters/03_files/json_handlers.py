from faker import Faker
import json
import pandas as pd


def write_json():
    output = open('data/data.json', 'w')
    fake = Faker()

    all_data = {}
    all_data['records'] = []

    for x in range(1000):
        data = { "name" :   fake.name(),
                 "age" :    fake.random_int(min=18, max=80, step=1),
                 "street" : fake.street_address(),
                 "city" :   fake.city(),
                 "state" :  fake.state(),
                 "zip" :    fake.zipcode(),
                 "lng" :    float(fake.longitude()),
                 "lat" :    float(fake.latitude()) }
        all_data['records'].append(data)

    json.dump(all_data, output)

def read_json():
    with open('data/data.json', 'r') as f:
        data = json.load(f)
        first_record = data['records'][0]
        print(first_record)

def read_json_pandas():
        f = open('data/data.json', 'r')
        data = pd.io.json.loads(f.read())
        df = pd.json_normalize(data, record_path='records')

        # Gets the first 2 rows, grouped by attribute
        by_attr = df.head(2).to_json()
        print(by_attr)

        # Gets the first 2 rows, grouped by row
        by_row = df.head(2).to_json(orient='records')
        print(by_row)


if __name__ == '__main__':
    # write_json()
    # read_json()
    read_json_pandas()

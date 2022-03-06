import csv
import pandas as pd

from faker import Faker


def read_csv():
    with open('data/data.csv') as f:
        myreader = csv.DictReader(f)
        headers = next(myreader)

        for row in myreader:
            print(row['name'])

def write_csv():
    output = open('data/data.csv','w')
    fake = Faker()

    header = ['name','age','street','city','state','zip','lng','lat']
    mywriter = csv.writer(output)
    mywriter.writerow(header)

    for r in range(1000):
        mywriter.writerow([fake.name(),
                           fake.random_int(min=18, max=80, step=1), 
                           fake.street_address(), 
                           fake.city(),
                           fake.state(),
                           fake.zipcode(),
                           fake.longitude(),
                           fake.latitude()])

    output.close()

def read_csv_pandas():
    df = pd.read_csv('data/data.csv')
    print(df.head(10))

def write_csv_pandas():
    data = {'Name': ['Paul','Bob','Susan','Yolanda'], 'Age': [23,45,18,21]}
    df = pd.DataFrame(data)
    df.to_csv('data/fromdf.csv',index=False)


if __name__ == '__main__':
    # read_csv()
    # write_csv()
    # read_csv_pandas()
    # write_csv_pandas()

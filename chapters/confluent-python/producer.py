from confluent_kafka import Producer
from faker import Faker
import json
import time

fake=Faker()

p = Producer({'bootstrap.servers':'localhost:9092'})

# Create a callback to use for receiving message acknowledgments
def receipt(err,msg):
    if err is not None:
        print('Error: {}'.format(err))
    else:
        print('%s : Message on topic %s on partition %s with value of %s' % \
                  (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(msg.timestamp()[1]/1000)), 
                   msg.topic(), 
                   msg.partition(),
                   msg.value().decode('utf-8')))

# Create the producer loop
def produce_messages():
    for i in range(10):
        data = {'name': fake.name(),
                'age': fake.random_int(min=18, max=80, step=1),
                'street': fake.street_address(),
                'city': fake.city(),
                'state': fake.state(),
                'zip': fake.zipcode()}

        m = json.dumps(data)

        # Get any acknowledgments for previous messages, which will be sent to callback
        p.poll(0)

        # Pass data and the function to send acknowledgments to
        p.produce('users', m.encode('utf-8'), callback=receipt)

        # Flush the producer to get any existing acknowledgments
        p.flush()


if __name__ == '__main__':
    produce_messages()

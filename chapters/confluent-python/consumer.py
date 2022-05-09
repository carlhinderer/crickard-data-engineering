from confluent_kafka import Consumer


c = Consumer({'bootstrap.servers': 'localhost:9092',
              'group.id': 'python-consumer',
              'auto.offset.reset': 'earliest'})

# Subscribe to topic
c.subscribe(['users'])

while True:
    msg = c.poll(1.0) # Timeout

    if msg is None:
        continue

    if msg.error():
        print('Error: {}'.format(msg.error()))
        continue

    data = msg.value().decode('utf-8')
    print(data)


# Close connection
c.close()
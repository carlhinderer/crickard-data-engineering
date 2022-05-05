import random
import time

from kafka import KafkaProducer


def produce_random_data():
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    while True:
        key = f"{random.randrange(999)}"
        value = "{'URL': 'URL%s'}" % random.randrange(999)

        producer.send(
            topic='pageview',
            key=key.encode(),
            value=value.encode()
        )

        time.sleep(1)


if __name__ == '__main__':
    produce_random_data()

from kafka import KafkaConsumer


def consume_messages():
    consumer = KafkaConsumer('pageview',
                             auto_offset_reset='earliest',
                             group_id='pageview-group1',
                             bootstrap_servers='localhost:9092')
                             
    for message in consumer:
        print(f"""
            topic     => {message.topic}
            partition => {message.partition}
            offset    => {message.offset}
            key={message.key} value={message.value}
        """)


if __name__ == '__main__':
    consume_messages()

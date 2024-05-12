from confluent_kafka import Producer
from time import sleep

print('STARTING..........')

conf = {
        'bootstrap.servers': 'localhost:9092'
        ,'auto.offset.reset': 'earliest'
        }

my_producer = Producer(conf)

my_producer.poll(0)

try:
    for n in range(5):  
        my_data = str({'num' : n}).encode()  
        my_producer.produce(topic='quickstart', value=my_data)  
        sleep(5)  
    my_producer.flush()
except Exception as e:
    print("ERROR: ", e)            
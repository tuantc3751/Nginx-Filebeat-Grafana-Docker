from confluent_kafka import Consumer, KafkaError
import json

from elasticsearch import Elasticsearch
from production import predict_single_url
import re

print("vong1")
conf = {
    'bootstrap.servers': 'kafka:9092',  # Kết nối tới Kafka bằng tên service 'kafka' trong Docker Compose
    'group.id': 'consumer',
    'auto.offset.reset': 'latest'
}

print("vong2")
consumer = Consumer(conf)
print("vong3")
consumer.subscribe(['nginx123'])  # Thay bằng tên topic Kafka
print("vong4")

es = Elasticsearch(hosts='http://elasticsearch:9200', headers={"Content-Type": "application/json"})
def process_data(message):

    print(message)

    pattern = r'(?P<ip>[\d.]+) - - \[(?P<timestamp>[^\]]+)\] "(?P<request>[^"]+)" (?P<status>\d+) (?P<response_size>\d+) "(?P<referrer>[^"]+)" "(?P<user_agent>[^"]+)"'
    log_entry = message['message']
    match = re.match(pattern, log_entry)
    print(match)
    # if match:
    #     # Print all groups
    #     print("Matched groups:", match.groups())  # Prints a tuple of all matched groups
        
    #     # Print individual group values
    #     for i, group in enumerate(match.groups(), start=1):
    #         print(f"Group {i}: {group}")
    if match:
        type_attack = "none"
        ip = match.group('ip')
        request = match.group('request')
        status = match.group('status')
        response_size = match.group('response_size')
        data_predict = request.split(' ')
        if(len(data_predict) == 3):
           type_attack = predict_single_url(data_predict[1])
        data = {
            "request": request,
            "status": status,
            "@timestamp": message['@timestamp'],
            # "type": message['event']['dataset'],
            "response_size": response_size,
            "ip": ip,
            "attack" : type_attack
        }

        print("Đây là data đẩy vào:",data)
        
        return data
    else:
        return None
    
def push_es(message):
    data = process_data(message)
    if data != None:
        # try:
        #     res = es.index(index='nginx-log-new1', document=data)
        #     print("Data đã được đẩy vào Elasticsearch:", res)
        # except Exception as e:
        #     print("Lỗi khi đẩy vào Elasticsearch:", e)
        res = es.index(index='nginx-log', document=data)

def get_message():
    print("okokok")

    while True:
        print("okokokok")
        # try:
        msg = consumer.poll(1.0)  # Adjust the timeout as needed
        print(msg)
        if msg is None:
            continue
        message_json = json.loads(msg.value().decode('utf-8'))
        print(message_json)
        push_es(message_json)
        # except Exception as e:
        #     print("loi roi ngu lam")
        #     print(e)
        
print("okok")
get_message()

# try:
#     while True:
#         msg = consumer.poll(timeout=1.0)

#         if msg is None:
#             continue
#         if msg.error():
#             if msg.error().code() == KafkaError._PARTITION_EOF:
#                 print('End of partition reached {0}/{1}'
#                       .format(msg.topic(), msg.partition()))
#             elif msg.error():
#                 raise KafkaException(msg.error())
#         else:
#             print('Received message: {}'.format(msg.value().decode('utf-8')))

# except KeyboardInterrupt:
#     pass
# finally:
#     consumer.close()
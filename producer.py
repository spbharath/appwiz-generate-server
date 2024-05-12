import pika
import json


connection_parameter = pika.ConnectionParameters("64.227.172.61")

connection = pika.BlockingConnection(connection_parameter)

channel = connection.channel()

channel.queue_declare(queue="generateApps")


data = {
    "username": "Valli456",
    "template_path": "/home/valli/testing/Templates/Education/template_2",
    "app_name": "ValliApp2345",
    "client_email": "vallivn18@gmail.com",
}

message_body = json.dumps(data)


channel.basic_publish(exchange="", routing_key="generateApps", body=message_body)

print(f"Sent Message : {data}")

connection.close()

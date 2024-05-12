import pika
import json
from generateapp_linux import generateApps
import os


def on_message_received(ch, method, properties, body):

    message_data = json.loads(body)
    username = message_data.get("username")
    template_path = message_data.get("template_path")
    client_email = message_data.get("client_email")
    app_name = message_data.get("app_name")
    app_image = message_data.get("app_image")

    if (
        username != None
        and template_path != None
        and client_email != None
        and app_name != None
        and app_image != None
    ):

        print(f"Received new Message, will take some time to process")

        JAVA_HOME = "/usr/lib/jvm/java-21-openjdk-amd64"
        ANDROID_HOME = "/home/valli/Android/Sdk"
        os.environ["ANDROID_HOME"] = ANDROID_HOME
        os.environ["JAVA_HOME"] = JAVA_HOME
        generateApps(
            username=username,
            template_path=template_path,
            app_name=app_name,
            client_email=client_email,
            app_image=app_image,
        )
    else:
        print("Message recieved with empty body cannot process......")

    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Finished processing the message")


connection_parameter = pika.ConnectionParameters("64.227.172.61")

connection = pika.BlockingConnection(connection_parameter)

channel = connection.channel()

channel.queue_declare(queue="generateApps")

channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue="generateApps", on_message_callback=on_message_received)

print("Starting Consuming")

channel.start_consuming()

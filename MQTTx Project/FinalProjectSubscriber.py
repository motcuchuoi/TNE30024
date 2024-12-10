import paho.mqtt.client as mqtt
import time
import ssl

broker_address = 'rule172.caia.swin.edu.au'
broker_port = 8883 # TLS port

client_information = dict ( # declare a dictionary with these following keywords and values
    client_identity = "Subscriber", 
    username = "103532674", # login info
    password = "nguyen" # login info
)

topics = [("103532674/private_topic", 0), ("public/#",0)]

client = mqtt.Client(client_id = client_information["client_identity"])
client.username_pw_set(client_information["username"], client_information["password"])

# SSL/TLS context setup
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.minimum_version = ssl.TLSVersion.TLSv1_3
context.load_verify_locations(cafile = r"C:\Users\Dell\OneDrive - Swinburne University\Desktop\TNE30024\MQTTX\final.crt")
client.tls_set_context(context)
client.tls_insecure_set(False)

def connect_mqtt(): 
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker!: {}".format(rc))
            for topic, qos in topics:
                client.subscribe(topic,qos)
        else:
            print("Failed to connect with code: "+str(rc))
    
    client.on_connect = on_connect
    client.connect(broker_address, broker_port)
    return client     

# reference: https://www.emqx.com/en/blog/how-to-use-mqtt-in-python 
   
def subscribe(client: mqtt.Client):
    def on_message(client, userdata, msg):
        print(f"Received '{msg.payload.decode()}' from topic {msg.topic}")
    
    client.on_message = on_message

def main():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    main()

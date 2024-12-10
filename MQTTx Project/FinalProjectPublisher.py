import paho.mqtt.client as mqtt
import time
import ssl

broker_address = 'rule172.caia.swin.edu.au' 
broker_port = 8883 # ssl/tls

# publisher information
client_information = dict (
    client_identity = "Publisher", 
    username = "103532674", 
    password = "nguyen",
    messages = ["help", "need", "what"]
)

topic = "103532674/private_topic"

def connect_mqtt() -> mqtt.Client:
    # global broker_address, client_information

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker!: " +str(rc))
        else:
            print("Failed to connect with code: "+str(rc))
    
    client = mqtt.Client(client_id = client_information["client_identity"])
    client.username_pw_set(client_information["username"], client_information["password"])
    client.on_connect = on_connect
    
    # TLS
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    # self signed cert file path
    context.load_verify_locations(cafile = r"C:\Users\Dell\OneDrive - Swinburne University\Desktop\TNE30024\MQTTX\final.crt")
    client.tls_set_context(context)
    client.tls_insecure_set(False)

    client.connect(broker_address, broker_port)
    
    return client

def publish(client: mqtt.Client):
    print("Type 'exit' to stop publishing messages.")
    
    while True:
        msg = input("Enter a message to publish: ")
        if msg.lower() == "exit":
            break

        result = client.publish(topic, msg, qos=1)
        
        # Check if the message was successfully published
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Sent '{msg}' to topic '{topic}'")
        else:
            print(f"Failed to send message to '{topic}'")
    
    disconnect_mqtt(client)

def disconnect_mqtt(client: mqtt.Client):
    def on_disconnect(client, userdata, rc):
        print(f"Disconnected with result code: {str(rc)}")
    
    client.on_disconnect = on_disconnect
    client.disconnect()

def main():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()

if __name__ == '__main__':
    main()
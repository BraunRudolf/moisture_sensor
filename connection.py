import network
import utime
from umqttsimple import MQTTClient
import machine

def connect_wlan(ssid:str, password:str)->None:
    """"""
    # Initialise wlan class
    wlan = network.WLAN(network.STA_IF)
    # Activate wlan interface
    wlan.active(True)
    # connect to wlan
    wlan.connect(ssid=ssid, key=password)
    # wait for connection 
    utime.sleep(5)
    return True

def reset_after_failed_connect():
    """
    Function that restarts pico after failed connection attempt
    """
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    utime.sleep(5)
    machine.reset()
    return True

def mqtt_connect(client_id:str, user:str, password:str, server:str, port:int):
    """
    Function to connect to MQTT Broker
    """
    try:
        client = MQTTClient(client_id=client_id,
                            user=user,
                            password=password,
                            server=server,
                            port=port,
                            keepalive=360)
        utime.sleep(1)
        client.connect()
        print(f'Connected to {server} MQTT Broker')
        return client
    #client = mqtt_connect()
    except OSError as os_exception:
        print(os_exception)
        reset_after_failed_connect()
        return None

def mqtt_publish(client:MQTTClient, topic_pub:str, msg:str):
    """
    Function to publish mqtt msg to given client/topic
    """
    topic_msg = str(msg)
    client.publish(topic_pub, topic_msg, retain=True)
    return True

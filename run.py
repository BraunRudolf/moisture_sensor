import config, config_secrets
import utime
import min_max_values
import connection
import flash
import read_ads115

def read_transform_value(min_moisture:list[int], max_moisture:list[int]):
    """
    Function to transform values into percent
    """
    value_list = read_ads115.all_channel_read() 
    transform_values = [0, 0, 0, 0]
    for i in range(0,4):
        try:
            transform_values[i] = (max_moisture[i]-value_list[i])/(max_moisture[i]-min_moisture[i])
            if transform_values[i] < 0:
                transform_values[i] = 0
            elif transform_values[i]>100:
                transform_values[i] = 100
        except TypeError:
            transform_values[i] = None

    return transform_values


# Initialise varibals  
# Wlan 
ssid= config_secrets.SSID
password =config_secrets.PASSWORD

# Mqtt broker
brokr_ip = config_secrets.BROKER_IP
brokr_port = config_secrets.BROKR_PORT
broker_password = config_secrets.MQTT_PW
user = config_secrets.MQTT_USR
client_id = config.CLIENT_ID
topic_pub = config.TOPIC_PUB 


wlan_status = connection.connect_wlan(ssid=ssid, password=password)
if wlan_status != True:
    print('Wlan connection failed')
else:
    print('Wlan connected')

client = connection.mqtt_connect(client_id=client_id, user=user, password=broker_password, server=brokr_ip, port=brokr_port)

min_moisture, max_moisture = min_max_values.read_min_max_values()


while True:
    value_list = read_transform_value(min_moisture=min_moisture, max_moisture=max_moisture)
    # print(f'min_moisture: {min_moisture}, max_moisture: {max_moisture}, values: {value_list}')
    connection.mqtt_publish(client=client, topic_pub=topic_pub, msg=value_list)
    utime.sleep(60)

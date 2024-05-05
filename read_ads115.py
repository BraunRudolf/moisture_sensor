import utime
from machine import I2C , Pin

dev = I2C(1, freq=40000, scl=Pin(15), sda=Pin(14))

devices = dev.scan()

for device in devices:
    print(device)
address = 72

def readConfig():
    dev.writeto(address, bytearray([1]))
    result = dev.readfrom(address,2)

    return result[0]<<8 | result[0]


def readValue():
    dev.writeto(address, bytearray([0]))
    result = dev.readfrom(address,2)
    
    config = readConfig()
    config &= ~(7<<12)& ~(7<<9)
    config |= (4<<12) | (1<<9) | (1<<15)
    
    config = [ int(config>>i & 0xff) for i in (8,0)]
    
    dev.writeto(address, bytearray([1] + config))
    
    return result[0]<<8 | result[1]
    
def readValueFrom(channel):
    config = readConfig()
    
    config &= ~(7<<12) # clear MUX bits?
    config &= ~(7<<9) # clear PGA
    
    config |= (7 & (4 + channel))<<12
    config |= (1<<15) # trigger next conversion.
    config |= (1<<9) # gain 4.096 volts
    
    config = [ int(config>>i & 0xff) for i in (8,0)]
    
    dev.writeto(address, bytearray([1] + config))
    
    config = readConfig()
    while(config & 0x8000) == 0:
        config = readConfig()
        
    dev.writeto(address, bytearray([0]))
    result = dev.readfrom(address, 2)
    
    return result[0]<<8 | result[0]

def all_channel_read()->list:
    """
    Function to read all values of all channels

    Return val: List of all values from all channels
    """
    # Initialise value list
    val = [0, 0, 0, 0]

    val[0] = readValueFrom(0)
    val[1] = readValueFrom(1)
    val[2] = readValueFrom(2)
    val[3] = readValueFrom(3)  

    return val
#
# value_array=[]
# action_time=5
# time_passed =0
# while time_passed < action_time:
#         value_list = read_ads1115.all_channel_read()
#         value_array.append(value_list)    
#         flash.blink_per_sec(1)
#         time_passed+=1
# print(value_array)
# max_moisture = [0, 0, 0, 0]
# i = 0
#
# print(len(value_array), len(value_array[1]))
#
# while i < 4:
#     max_value = 0
#     print(len(value_array[i]))
#     for col in range(0,len(value_array)):
#         if max_value < value_array[col][i]:
#             max_value = value_array[col][i]
#     max_moisture[i] = max_value
#     i+=1
# print(max_moisture)
#
# time_passed = 0
#
# time_passed =0
# while time_passed < action_time:
#         value_list = read_ads1115.all_channel_read()
#         value_array.append(value_list)    
#         flash.blink_per_sec(1)
#         time_passed+=1
# print(value_array)
# max_moisture = [0, 0, 0, 0]
# i = 0
#
# print(len(value_array), len(value_array[1]))
#
# while i < 4:
#     max_value = 0
#     print(len(value_array[i]))
#     for col in range(0,len(value_array)):
#         if max_value < value_array[col][i]:
#             max_value = value_array[col][i]
#     max_moisture[i] = max_value
#     i+=1
# print(max_moisture)

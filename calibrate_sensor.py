import read_ads115
import min_max_values
import flash

def calibrate_sensor(action_time:int)->list[int]:
    """
    Function to calibrate moisture sensors
    :pram action_time: Time the user has to execute required manual 
    actions, defined in the readme
    """
    # Initialise value_array for max values
    value_array_max = []

    print('Keep the sensor dry, on open air and separated from each other') 
    flash.shine_till_end(time=action_time)
    
    # Read values and write to matrix 
    time_passed = 0
    while time_passed < action_time:
        value_list = read_ads115.all_channel_read()
        value_array_max.append(value_list)    
        flash.blink_per_sec(1)
        time_passed+=1

    max_moisture = [0, 0, 0, 0]
    i = 0
    while i < 4:
        max_value = 0 
        for col in range(0,len(value_array_max)):
            if max_value < value_array_max[col][i]:
                max_value = value_array_max[col][i]
        max_moisture[i] = max_value
        i+=1

    print('Submerge sensors into water up to the white line')
    flash.shine_till_end(time=action_time)

    # Initialise value array for min values
    value_array_min = []
    # Read values and write to matrix
    time_passed = 0
    while time_passed < action_time:
        value_list = read_ads115.all_channel_read()
        value_array_min.append(value_list)
        flash.blink_per_sec(1)
        time_passed +=1

    min_moisture = [0, 0, 0, 0]
    i = 0
    while i < 4:
        min_value = 0
        for col in range(0,len(value_array_min)):
            if min_value < value_array_min[col][i]:
                min_value = value_array_min[col][i]
        min_moisture[i] = min_value
        i +=1
    for i in range(0,4):
        if (round(max_moisture[i]/10000)-round(min_moisture[i]/10000)) == 0:
            max_moisture[i] = None
            min_moisture[i] = None

    return min_moisture, max_moisture

min_moisture, max_moisture = calibrate_sensor(action_time=10)
min_max_values.write_min_max_values(min_moisture, max_moisture)



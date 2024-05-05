import json

def write_min_max_values(min_values:list, max_values:list, json_name:str='min_max_values.json'):
    min_max_value_dic = {'min_values':min_values,
                         'max_values':max_values
                         }
    with open(json_name, 'w') as json_file:
        json.dump(min_max_value_dic, json_file)

def read_min_max_values(json_name:str='min_max_values.json'):
    with open(json_name, 'b') as json_file:
        min_max_values = json.load(json_file)
    return min_max_values['min_values'], min_max_values['max_values']

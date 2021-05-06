import yaml2 as yaml

with open('nat-rule.yaml', 'r') as file:
        parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

# for i in parsed_yaml_file:
    # print('*'*24)
print(parsed_yaml_file[0]['Name'])
print(parsed_yaml_file[0]['source-translation']['dynamic-ip-and-port']['translated-address']['member'][0])
print(parsed_yaml_file[0]['source']['member'][0])
print(parsed_yaml_file[0]['destination']['member'][0])
print(parsed_yaml_file[0]['service'])
print(parsed_yaml_file[0]['destination-translation']['translated-address'])
print(parsed_yaml_file[0])
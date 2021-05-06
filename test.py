import yaml2 as yaml

with open('sec-rule.yaml', 'r') as file:
        parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

for rule in parsed_yaml_file:
    print(rule['Name'])
    print(rule['source']['member'][0])
    print(rule['destination']['member'][0])
    app_string = "| "
    for app in rule['application']['member']:
        app_string += app + ' | '
    print(app_string)
    print(rule['service']['member'][0])
    print(rule['action'])
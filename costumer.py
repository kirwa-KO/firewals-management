import yaml2 as yaml
from flask import Flask, render_template

# with open('customers.yml', 'r') as file:
#     parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

# for i in parsed_yaml_file:
#     print(i['Name'])
#     try:
#         pass
#         # for value in i['Netops']['Fw']:
#         #     print('    => ' + value)
#     except KeyError:
#         pass
        

fw_app = Flask(__name__)

@fw_app.route('/')
def home_page():
    with open('customers.yml', 'r') as file:
        parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)
    names = []
    for line in parsed_yaml_file:
        names.append({'href' : line['Name'], 'link_name' : line['Name']})
    return render_template('index.html', names=names)

@fw_app.route('/<name>')
def name_page(name):
    with open('customers.yml', 'r') as file:
        parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)
    for line in parsed_yaml_file:
        if line['Name'] == name:
            fws = []
            try:
                for value in line['Netops']['Fw']:
                    fws.append({'href': name + '/' + value, 'link_name': value})
                return render_template('index.html', names=fws)
            except:
                return ('Name Have NO Firewell')
    return ('Name Have NO Firewell')

@fw_app.route('/<name>/<fw>')
def fw_page(name, fw):
    with open('nat-rule.yaml', 'r') as file:
        parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)
    nut_rule = []
    nut_rule.append(parsed_yaml_file[0]['Name'])
    nut_rule.append(parsed_yaml_file[0]['source-translation']['dynamic-ip-and-port']['translated-address']['member'][0])
    nut_rule.append(parsed_yaml_file[0]['source']['member'][0])
    nut_rule.append(parsed_yaml_file[0]['destination']['member'][0])
    nut_rule.append(parsed_yaml_file[0]['service'])
    nut_rule.append(parsed_yaml_file[0]['destination-translation']['translated-address'])
    nut_rule.append(parsed_yaml_file[0])

    return render_template('firewell_info.html', nut_rule=nut_rule)

if __name__ == "__main__":
    fw_app.run(debug=True)

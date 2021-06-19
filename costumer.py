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
    return render_template('index.html', names=names, custom_css="index")

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
                # return render_template('firewall_list.html', names=fws, custom_css="firewall_list")
                return render_template('firewall_list.html', names=fws, custom_css="index")
            except:
                return render_template('no_firewall_found.html', names=fws, custom_css="no_firewall_found")
    return render_template('no_firewall_found.html', custom_css="no_firewall_found")

@fw_app.route('/<name>/<fw>')
def fw_page(name, fw):
    with open('nat-rule.yaml', 'r') as file:
        parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)
    nat_rules = []
    
    for rule in parsed_yaml_file:
        nested_rule = []
        try:
            nested_rule.append(rule['Name'])
        except:
            nested_rule.append('')
        try:
            nested_rule.append(rule['source-translation']['dynamic-ip-and-port']['translated-address']['member'][0])
        except:
            nested_rule.append('')
        try:
            nested_rule.append(rule['source']['member'][0])
        except:
            nested_rule.append('')
        try:
            nested_rule.append(rule['destination']['member'][0])
        except:
            nested_rule.append('')
        try:
            nested_rule.append(rule['service'])
        except:
            nested_rule.append('')
        try:
            nested_rule.append(rule['destination-translation']['translated-address'])
        except:
            nested_rule.append('')
        nat_rules.append(nested_rule)



    with open('sec-rule.yaml', 'r') as file:
        parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)
    sec_rules = []
    
    for rule in parsed_yaml_file:
        nested_rule = []
        try:
            nested_rule.append(rule['Name'])
        except:
            nested_rule.append('')
        try:
            nested_rule.append(rule['source']['member'][0])
        except:
            nested_rule.append('')
        try:
            nested_rule.append(rule['destination']['member'][0])
        except:
            nested_rule.append('')
        try:
            app_string = "| "
            for app in rule['application']['member']:
                app_string += app + ' | '
            nested_rule.append(app_string)
        except:
            nested_rule.append('')
        try:
            nested_rule.append(rule['service']['member'][0])
        except:
            nested_rule.append('')
        try:
            nested_rule.append(rule['action'])
        except:
            nested_rule.append('')
        sec_rules.append(nested_rule)

    return render_template('firewell_info.html', nat_rules=nat_rules, sec_rules=sec_rules, custom_css="firewall_info")

if __name__ == "__main__":
    fw_app.run(debug=True)

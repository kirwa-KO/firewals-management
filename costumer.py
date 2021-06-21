import yaml2 as yaml
from flask import Flask, render_template, request, redirect

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
		
def remove_spacing_string_and_empty(the_list):
	# remove empty strings
	while '' in the_list:
		the_list.remove('')
	# remove strings that contains just a space
	while ' ' in the_list:
		the_list.remove(' ')
	return the_list

def append_set_rules_data_with_filter(nested_rule, rule, client_name, apply_filter):

	if apply_filter == True and client_name not in rule['Name'].lower():
		print(rule['Name'])
		return
	try:
		nested_rule.append(rule['Name'])
	except:
		nested_rule.append('')
	try:
		source_string = ''
		for source in rule['source']['member']:
			source_string += source + ', '
		# nested_rule.append(rule['source']['member'][0])
		nested_rule.append(source_string)
	except:
		nested_rule.append('')
	try:
		destination_string = ''
		for destination in rule['destination']['member']:
			destination_string += destination + ', '
		# nested_rule.append(rule['destination']['member'][0])
		nested_rule.append(destination_string)
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


	filtered_firewals = ["orfw01"]

	with open('sec-rule.yaml', 'r') as file:
		parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)
	sec_rules = []
	
	for rule in parsed_yaml_file:
		nested_rule = []
		if fw in filtered_firewals:
			append_set_rules_data_with_filter(nested_rule, rule, name, True)
		else:
			append_set_rules_data_with_filter(nested_rule, rule, name, False)

		# check if the table is empty to dont append an empty list
		if len(nested_rule) > 0:
			sec_rules.append(nested_rule)

	return render_template('firewell_info.html',
							nat_rules=nat_rules,
							sec_rules=sec_rules,
							custom_css="firewall_info",
							edit_link='/' + name + '/' + fw + '/edit')

@fw_app.route('/<name>/<fw>/edit', methods=['POST', 'GET'])
def fw_edit_page(name, fw):
	if request.method == 'GET':
		return render_template('edit_firewall_sec_rule.html',
								name=request.args.get("name"),
								source=request.args.get("source"),
								destination=request.args.get("destination"),
								application=request.args.get("application"),
								service=request.args.get("service"),
								action=request.args.get("action"),
								post_link='/' + name + '/' + fw + '/edit'
								)

	elif request.method == 'POST':
		old_name = request.form['old_name']
		new_name = request.form['name']

		new_source = request.form['source'].replace(' ', '').split(',')
		new_source = remove_spacing_string_and_empty(new_source)
		
		new_destination = request.form['destination'].replace(' ', '').split(',')
		new_destination = remove_spacing_string_and_empty(new_destination)

		new_application = request.form['application'].replace(' ', '').split('|')
		new_application = remove_spacing_string_and_empty(new_application)

		new_service = request.form['service']
		new_action = request.form['action']

		with open('sec-rule.yaml', 'r') as file:
			parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

		for rule in parsed_yaml_file:
			if old_name == rule['Name']:
				rule['Name'] = new_name
				rule['source']['member']= new_source
				rule['destination']['member'] = new_destination
				rule['application']['member'] = new_application
				rule['service']['member'][0] = new_service
				rule['action'] = new_action
				with open('sec-rule.yaml', 'w') as file:
					yaml.dump(parsed_yaml_file, file)
				break

		return redirect('/' + name + '/' + fw, code=302)

if __name__ == "__main__":
	fw_app.run(debug=True)

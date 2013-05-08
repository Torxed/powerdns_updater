from sys import version_info, argv
from backend import SQL

__version__ = '0.1-alpha'
__authors__ = 'anton@hvornum.se'
__verified__ = ('3.3')

if version_info.major < 3:
	_input = raw_input
elif version_info.major > 2:
	_input = input

def reconstrunct_record_values(values={}):
	if not 'type' in values:
		values['type'] = 'A'
	if not 'name' in values:
		values['name'] = '3net.se'
	if not 'ip' in values:
		values['ip'] = '166.78.238.96'
	if not 'domain' in values:
		values['domain'] = None
	if not 'prio' in values:
		values['prio'] = 'NULL'
	return values

if len(argv) > 1:
	database = '\ '.join(argv[1:])
	backend = SQL(database)
else:
	backend = SQL()

print('v' + __version__)
print('Tested on Python versions:' + ' '.join(__verified__))
print('\tValid options are:')
print('\tadd [domain|record] - create a record or domain')
print('\tmodify - modify a record')
print('\treplace - Replace IP on records\n')

while 1:
	inp = _input('\n> ')
	low_inp = inp.lower()

	if low_inp in ('quit', 'exit', 'break', 'die'):
		break

	if low_inp[:3] == 'add':
		if not 'domain' in low_inp or 'record' in low_inp:
			low_inp += ' ' + _input('\nRecord or domain?> ')
		
		values = {}
		print('Enter: "key=value" to commit to the database.')
		print('When done, write "done" to commit (if any values were submitted)\n')

		if 'domain' in low_inp:
			inp_string = 'domain-values'
			print('Valid options are:')
			print('\tname=<domain name>')
		elif 'record' in low_inp:
			inp_string = 'record-values'
			print('Valid options are:')
			print('\tname=<record name>')
			print('\tip=<ip|hostname> (IP for ex A record, hostname for MX records etc)')
			print('\ttype<record type> (A|MX|CNAME... etc)')
			print('\tdomain=<domain that the record belongs to>')
			print('\tprio=<prio for MX record if that\'s the type> (optional)\n')

		while 1:
			value = _input('\n' + inp_string + '> ')
			if value.lower() == 'done':
				break
			elif '=' in value:
				key, value = value.split('=',1)
				values[key] = value
		
		if len(values) <= 0: continue

		if 'record' in low_inp:
			values = reconstrunct_record_values(values)
			backend.add_record(_type=values['type'],
								name=values['name'],
								ip=values['ip'],
								domain=values['domain'],
								prio=values['prio'])
		elif 'domain' in low_inp:
			if not 'name' in values:
				print(' [!] At least a name for the domain must be given!\n')
			else:
				backend.add_domain(name=values['name'])
	elif low_inp[:3] == 'mod' or low_inp[:6] == 'modify':
		values = {}
		print('Enter: "key=value" to commit to the database.')
		print('When done, write "done" to commit (if any values were submitted)\n')

		print('Valid options are:')
		print('\tname=<record name>')
		print('\tip=<ip|hostname> (IP for ex A record, hostname for MX records etc)')
		print('\trecord=<record type> (A|MX|CNAME... etc)\n')

		while 1:
			value = _input('\nModifications> ')
			if value.lower() == 'done':
				break
			elif '=' in value:
				key, value = value.split('=',1)
				values[key] = value
		
		if len(values) <= 0: continue

		values = reconstrunct_record_values(values)
		backend.modify_record(name=values['name'], ip=values['ip'], record=values['record'])
	elif low_inp[:7] == 'replace':
		values = {}
		print('Enter: "key=value" to commit to the database.')
		print('When done, write "done" to commit (if any values were submitted)')

		print('Valid options are:')
		print('\told=<old IP address>')
		print('\nnew=<new ip>')
		print('\trecord=<record name> (example.com, www.example.com etc)\n')

		while 1:
			value = _input('\nReplacement values> ')
			if value.lower() == 'done':
				break
			elif '=' in value:
				key, value = value.split('=',1)
				values[key] = value

		if not 'old' in values or 'new' in values:
			print ' [!] At least specify a old and new IP to match in database!\n'
		else:
			backend.replace_all_ip(values['old'], values['new'])
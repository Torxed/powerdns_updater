from os.path import isfile
from os import remove
import sqlite3

class SQL():
	def __init__(self, path='/var/empty/database.sqlite'):
		self.database = path
		self.conHandle = None
		if not isfile(path):
			self.create_clean_db()

	def connect(self):
		self.conHandle = sqlite3.connect(self.database)

	def disconnect(self):
		self.conHandle.close()
		self.conHandle = None

	def close(self):
		self.disconnect()

	def query(self, q):
		if not self.conHandle:
			self.connect()

		cursor = self.conHandle.cursor()

		execHandle = cursor.execute(q)
		results = execHandle.fetchall()

		self.conHandle.commit()
		cursor.close()
		self.disconnect()

		return results

	def create_clean_db(self):
		if isfile(self.database): remove(self.database)

		template = './sql_createdb.py-sqlite'
		with open(template, 'rb') as fh:
			querydata = fh.read()
		for query in querydata.split('%%'):
			if len(query) <= 0: continue
			self.query(query)

	def get_id_from_domainname(self, domain):
		result = self.query("SELECT id FROM domains WHERE name='" + domain + "';")
		if len(result) <= 0:
			return None
		else:
			return result[0][0]

	def add_record(self, _type='A', name='3net.se', ip='166.78.238.96', domain=None):
		"""
		Some examples:

		Adding a NS record: add_record('NS', 'example.com', 'ns1.example.com')
		 - Note: ip is not actually an IP since NS records is defined as pointer
		         to an A record.
		Adding a A record: add_record('A', 'www.example.com', '127.0.0.1')
		Adding a MX record: add_record('MX', 'example.com', 'mail.example.com')
		"""

		if not domain:
			domain=name
		domain_id = self.get_id_from_domainname(domain)
		if not domain_id:
			return None

		query = ""
		query += "INSERT INTO records (domain_id, name, content, type,ttl,prio)"
		query += " VALUES (" + str(domain_id) + ",'" + name + "','" + ip + "','" + _type + "',60,NULL);"
		self.query(query)

	def add_domain(self, name='3net.se'):
		## this query will return [(1,)] because query reunts all results
		## in a list, and each result is a tuple of all the columns fetched
		## even if we only request one column that will be a tuple.
		##
		## And in any case, the first result and the first column is the coun we need.
		new_domainID = self.query("SELECT MAX(id) FROM domains;")

		if not new_domainID:
			new_domainID = 0
		else:
			new_domainID = new_domainID[0][0]
			if not new_domainID:
				new_domainID=1
			else:
				new_domainID = int(new_domainID)
				new_domainID+=1

		self.query("INSERT INTO domains (name, type) values ('" + name + "', 'NATIVE');")

		query = "INSERT INTO records (domain_id, name, content, type,ttl,prio)"
		query += " VALUES(" + str(new_domainID) + ",'" + name + "','ns1." + name + " root@" + name + " 1','SOA',60,NULL);"
		self.query(query)

	def modify_record(self, name='3net.se', ip='166.78.238.96', domain=None, record='A'):
		if domain:
			pass
			## This would be where we build a add-in to the UPDATE row
			## to only affect a certain ID, in case there happens to be similar names
			## on the records (shouldn't happen?) and we only want to affect a certain ID
		self.query("UPDATE records SET content='" + ip + "' WHERE name='" + name + "' and type='" + record + "';")

	def replace_all_ip(self, ip, newip):
		self.query("UPDATE records SET content='" + newip + "' WHERE content='" + ip + "';")		

test = SQL('./database.sqlite')
test.add_domain()
test.add_record()
test.modify_record('3net.se', '127.0.0.1')
test.replace_all_ip('127.0.0.1', '192.168.0.1')

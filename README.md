PowerDNS Updater
================
This is a toolkit for creating, updating and maintaining PowerDNS 3.2+


local_tool
----------

The local tool is a small CLI that interacts with the backend.<br>
It consists of a few short "commands" that executes backend functions.<br>
And these are the following commands:<br>

 * add [domain|record]
 * modify
 * replace

With these short commands you'll the the options to add a record or domain,<br>
modify a existing record via name specification or replace old ip's with new ones.


backend
-------

The backend is mainly a wrapper for traditional SQL statements.<br>
This will be a shared module that any script or tool can import<br>
and execute simple tasks on the PowerDNS SQL database structure,<br>
such as:<br>

 * Creating a brand new database
 * Adding domains
 * Adding record
 * Modifying records based on type and name
 * Renew all IP records with a new IP (`replace(old_ip, new_ip)`)

More "features" will come, mainly for DNSSEC but for now these are<br>
the tasks that are simplified by having taken the manual tasks and<br>
replaced them with functions within the `SQL()` class.<br>

The Backend also relies on `sql_createdb.py-sqlite` for syntax.<br>
Since sqlite3 in Python doesn't handle multiple queries well enough<br>
in one execution the SQL statements are divided by `%%` between each<br>
statement and within the backend.py it just takes `data.split('%%')`<br>
and executes one query at a time.<br>

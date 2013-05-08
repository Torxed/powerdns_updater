PowerDNS Updater
================
This is a toolkit for creating, updating and maintaining PowerDNS 3.2+


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

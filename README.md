PowerDNS Updater
================
This is a toolkit for creating, updating and maintaining PowerDNS 3.2+


backend
-------

The backend is mainly a wrapper for traditional SQL statements.
This will be a shared module that any script or tool can import
and execute simple tasks on the PowerDNS SQL database structure,
such as:

 * Creating a brand new database
 * Adding domains
 * Adding record
 * Modifying records based on type and name
 * Renew all IP records with a new IP (`replace(old_ip, new_ip)`)

More "features" will come, mainly for DNSSEC but for now these are
the tasks that are simplified by having taken the manual tasks and
replaced them with functions within the `SQL()` class.

The Backend also relies on `sql_createdb.py-sqlite` for syntax.
Since sqlite3 in Python doesn't handle multiple queries well enough
in one execution the SQL statements are divided by `%%` between each
statement and within the backend.py it just takes `data.split('%%')`
and executes one query at a time.

Institute Mess Management System 
				-- by D-Minions


Instructions 
-------------
sudo apt-get update
sudo apt-get install python-pip
sudo pip install virtualenv
git clone http://github.com/vishwesh96/mess-management_system
cd mess-management_system
source newenv/bin/activate
sudo pip install django --upgrade


LDAP Authentication Dependenices 

* python-dev
* libldap2-dev
* libsasl2-dev
* python-ldap

sudo apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev
sudo apt-get install python-ldap


To install postgresql
---------------------
sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib
sudo pip install psycopg2


To connect to postgresql remotely on server
-------------------------------------------
listen_address = '*' in postgresql.conf
add host    <dbname> 	all 	0.0.0.0/0 	trust    in pg_hba.conf
CREATE ROLE <name>;
GRANT ALL PRIVILEGES ON DATABASE <dbname> TO <role>;
alter role <role> with login;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO <role>;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO <role>;

Version
-------
Using django version 1.10.2
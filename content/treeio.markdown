Title: Install Tree.io
Date: 2013-11-19 22:47 
Category: Python 
Tags: python
Slug: installing-tree-io
Author: Nick Bennett
Summary: Notes on installing Tree.io collaborative suite.

## Installing Tree.io 
[Original Instructions](https://github.com/treeio/treeio)

### Add EPEL repository 
````
CT-111-bash-4.1# cd /opt
CT-111-bash-4.1# wget http://fedora-epel.mirror.lstn.net/6/i386/epel-release-6-8.noarch.rpm
CT-111-bash-4.1# rpm -Uvh epel-release-6-8.noarch.rpm
CT-111-bash-4.1# rm epel-release-6-8.noarch.rpm -f
````

### Install prerequisites
````
CT-111-bash-4.1# yum install python python-devel python-imaging python-lxml python-pip python-virtualenv mysql-devel mod_wsgi
````

### Configure Apache
Create treeio config file:
````
CT-111-bash-4.1# vim /etc/httpd/conf.d/treeio.conf
````

#### treeio.conf:
````
<VirtualHost 0.0.0.0:9200>
    ServerName 0.0.0.0

    DocumentRoot /usr/share/treeio

    <Directory /usr/share/treeio>
      Order allow,deny
      Allow from all
    </Directory>

    WSGIDaemonProcess treeio.djangoserver processes=2 threads=15 display-name=%{GROUP} python-path=/usr/share/treeio:/usr/share/treeio/.ve/lib/python2.6/site-packages
    WSGIProcessGroup treeio.djangoserver

    WSGIScriptAlias / /usr/share/treeio/wsgi.py

    <Location />
      AuthType Basic
      AuthName "Gerrit"
      Require valid-user
      AuthUserFile /etc/httpd/htpasswds/gerrit
    </Location>
</VirtualHost>
````

Change WSGI socket location:
````
CT-111-bash-4.1# vim /etc/httpd/conf/httpd.conf
````

Add to the end of ````httpd.conf````:
````
WSGISocketPrefix /var/run/wsgi
````

### Create MySQL Database 
````
CT-111-bash-4.1# mysql -u root -p
````

````sql
mysql> create database treeio;
mysql> grant all privileges on treeio.* to treeio@localhost identified by 'numberswords';
mysql> \q
````

### Clone Tree.io 
````
CT-111-bash-4.1# cd /usr/share
CT-111-bash-4.1# git clone https://github.com/treeio/treeio.git
CT-111-bash-4.1# cd treeio
````

### Initialize Django app 
#### Create Virtual Environment and install requirements 
````
CT-111-bash-4.1# pwd
/usr/share/treeio
CT-111-bash-4.1# virtualenv .ve
New python executable in .ve/bin/python
Installing setuptools............done.
Installing pip...............done.
CT-111-bash-4.1# source .ve/bin/activate
(.ve)CT-111-bash-4.1# pip install -r requirements.pip
````

#### Install mysql-python
````
(.ve)CT-111-bash-4.1# pip install mysql-python
````

#### Apply Patch 
````
(.ve)CT-111-bash-4.1# python related_fields_patch.py
````

#### Install Databases 
````
(.ve)CT-111-bash-4.1# python manage.py installdb
Enter database engine <mysql,postgresql,oracle,sqlite3> (defaults to sqlite3): mysql
Enter database name (defaults to treeio.db): treeio
Database user (defaults to treeio): 
Database password: numberswords
````

#### Load Initial Data 
````
(.ve)CT-111-bash-4.1# mysql -u treeio -p treeio < sql/mysql-treeio-current.sql
````

#### Create wsgi.py 
````
(.ve)CT-111-bash-4.1# vim /usr/share/treeio/wsgi.py
````

##### wsgi.py:
````python
import os
import sys

import django.core.handlers.wsgi

sys.path = ['/usr/share/treeio/.ve/lib/python2.6/site-packages/'] + sys.path
sys.path.append('/usr/share/')
sys.path.append('/usr/share/treeio/')
    
os.environ['DJANGO_SETTINGS_MODULE'] = 'treeio.settings'
    
application = django.core.handlers.wsgi.WSGIHandler()
````

#### Add Mail Sending Config to settings.py 
To enable things like invitation by email, an SMTP server needs to be configured. Edit ````settings.py```` to include the following information (get the password from Joe or someone else with access to the mail server):
````python
#
# Email settings
#

EMAIL_SERVER = 'mail.sneakysnakes.com'
IMAP_SERVER = 'mail.sneakysnakes.com'
EMAIL_USERNAME = 'appmailer+sneakysnakes.com'
EMAIL_PASSWORD = 
EMAIL_FROM = 'appmailer@sneakysnakes.com'
DEFAULT_SIGNATURE = """
Brought you by Tree.io.
            """
````

#### Fix projects_task DB table
The ````projects_task```` database table is missing a column ````depends_id```` with INTEGER type. This prevents the Calendar from working. This has been [previously reported](http://tree.io/en/community/questions/230/unable-to-work-with-projects) by other users, and the fastest way to fix it is to simply add the missing column to the table.
````
(.ve)CT-111-bash-4.1# mysql -u treeio -p treeio -e "ALTER TABLE projects_task ADD depends_id int(11);"
````

### Restart Apache 
````
(.ve)CT-111-bash-4.1# /etc/init.d/httpd restart
````

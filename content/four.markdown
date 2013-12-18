Title: notes from work
Date: 2013-11-19 21:56  
Category: Python 
Tags: python
Slug: notes-from-beginning-developer
Author: Nick Bennett
Summary: personal notes I used while getting started at my programming job.

Below is a set of notes I created at work for what I learned and needed to know from the first 4 months of my job. It's all ingrained in my head by now so I rarely look at the page anymore. Perhaps someone out there in Web Land could use it.

### ~/.screenrc

````
term "screen-256color"
startup_message off
caption string "%?%F%{= Bk}%? %C%A %D %d-%m-%Y %{= kB} %t%= %?%F%{= Bk}%:%{= wk}%? %n "
hardstatus alwayslastline
hardstatus string '%{= kG}[ %{G}%H %{g}][%= %{= kw}%?%-Lw%?%{r}(%{W}%n*%f%t%?(%u)%?%{r})%{w}%?%+Lw%?%?%= %{g}][%{B} %d/%m %{W}%c %{g}]'
````

### ~/.bashrc 

````
# .bashrc

# Function for randomized password
randpw(){ < /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c${1:-16};echo;}

# Source global definitions
if [ -f /etc/bashrc ]; then
        . /etc/bashrc
fi
alias spotify='~/bin/my-spotify 2> /dev/null &'

export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
source /usr/bin/virtualenvwrapper.sh

export PS1="\[\a\]\[\e[0;31m\]\u@\h {\[\e[1;32m\]\w\[\e[0;31m\]}\n\[\e[0;31m\]$\[\033[0m\]"

export PATH=~/bin:$PATH
````

## vim 

### Remapping Caps-Lock key to CTRL
In Gnome in Fedora 18, the Caps-Lock key cannot be remapped to CTRL through the GUI keyboard settings. The remapping is done thusly:
````bash
$ gsettings set org.gnome.desktop.input-sources xkb-options "['ctrl:nocaps']"
````
reference: http://simonbaird.blogspot.com/2013/01/fixing-caps-lock-key-in-gnome-in-fedora.html

### Shortcuts
My vim config: https://github.com/tothebeat/.vim

Add a space after all commas that don't already have a space after them:
````vim
:%s/,\([^ ]\)/, \1/g
````

Remove trailing whitespace on all lines:
````vim
:%s/\s\+$//g
````

Move opening curly braces that appear on their own line to instead appear at the end of the statement on the previous line:
````vim
:%s/\n^\s*{/ {/g
````

Remap the arrow keys to nothing to make myself use hjkl:
````vim
noremap <Up> <Nop>
noremap <Down> <Nop>
noremap <Left> <Nop>
noremap <Right> <Nop>
````
reference: http://codingfearlessly.com/2012/08/21/vim-putting-arrows-to-use/

## screen

* ````screen -S floop```` : start a new screen session and name it "floop"
* ````screen -R floop```` : reconnect to the screen session named "floop"
* ````screen -ls```` : list current screen sessions
* ````screen -dRR```` : goddamnit I just want to connect to a screen session
* ````CTRL-a d```` : detach from the current screen session
* ````CTRL-a c```` : create a new window with a shell and switch to that window
* ````CTRL-a A```` : rename the current window
* ````CTRL-a CTRL-a```` : toggle to the last used screen window (hold in CTRL and tap 'a' twice)
* ````CTRL-a CTRL-n```` :  switch to the next window
* ````CTRL-a CTRL-p```` : switch to the previous window


## MySQL

* To list tables in database: ````SHOW TABLES;````
* To list columns in a table: ````DESCRIBE table_name;````
* To show the storage engine being used by a specific table: ````SELECT ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'database_name' AND TABLE_NAME = 'table_name';````
* To alter a table by adding a column: ````ALTER TABLE table_name ADD column_name datatype````
* To alter a table by dropping a column: ````ALTER TABLE table_name DROP COLUMN column_name````
* To alter a table by changing the type of an existing column: ````ALTER TABLE table_name MODIFY column_name datatype````
* To add a user: ````CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';````
* To grant permissions to a user:````GRANT ALL PRIVILEGES ON databasename.* TO 'newuser'@'localhost'; FLUSH PRIVILEGES;````

## Django

* To show SQL that would be generated for an app:````python manage.py sqlall app_name````
* To open a shell to the database being used by the project:````python manage.py dbshell````
* To open a shell in the context of the project:````python manage.py shell````
* To create a models.py describing the tables already existing in a database:````python manage.py inspectdb --database=database_name_in_settings_py > models.py````
* The database name used is not necessarily the same as that in the database itself. This is the key used in the DATABASES dictionary in settings.py.

## git

* Show a log of previous commits, one per line, showing only the commit hash and the message:````git log --pretty=oneline````
* Throw out all local changes and revert the local repository to a previous commit specified by hash:````git reset --hard sha1_hash_here````
* Make a commit of all local changes with a message on the command line (as opposed to the default of spawning an editor):````git commit -a -m "Added stuff."````
* Update local repository with all changes since last update from remote:````git pull````
* Update remote repository with local changes:````git push````
* Show all branches with current branch indicated by an asterisk:````git branch````
* Switch to another branch:````git checkout branch_name````
* Merge all changes from another branch into the current branch:````git merge other_branch_name````
* Create a new branch and check out code to it immediately:````git checkout -b new_branch_name````
* List files changed in a single commit: ````git show --name-only commit-hash````
* List files changed between two commits:````git diff commit-hash-1 commit-hash-2 --name-only````
* Stash your changes before you're ready for a commit but need to pull or otherwise merge changes:````git stash````
* Apply your changes again from the stash:````git stash apply````

### git-rebase

* Run git log ````git log --pretty=oneline````
* Copy hash of commit just before the ones you want to merge. Use it in: ````git rebase -i hash````
* Change the more recent commit from 'pick' to 'f', save file
* (optional) If you need to amend your change on Gerrit, ````git push -f origin HEAD:refs/for/master````

### Helpful References
* http://cheat.errtheblog.com/s/git
* http://rogerdudler.github.io/git-guide/
* http://pcottle.github.io/learnGitBranching/
* https://wiki.openstack.org/wiki/GitCommitMessages

### password-less ssh login
* Generate an SSH key pair on your client machine if you have not already done so. ````ssh-keygen -t rsa````
* Register this key with the SSH agent.  ````ssh-add````
* Copy the id_rsa.pub to the remote host. ````ssh-copy-id <host>````

### Mounting locally using SSHFS 
* Install SSHFS.  ````sudo yum install fuse-sshfs````
* Create a mount point.   ````mkdir -p ~/Documents/Code/xylem-redux/````
* Mount.  ````sshfs nbennett@xylem-redux: ~/Documents/Code/xylem-redux/````

### Tunnelling MySQL through SSH
Forward the MySQL 3306 port on xylem-redux to port 3307 on localhost to use MySQL Workbench more easily. 
````ssh -L 3307:localhost:3306 nbennett@xylem-redux````

### Activating Virtual Environment
This sets the PATH so that you can use python and pip without having to provide the full path. 
````source pythonenv/bin/activate````

## PHP

### Debugging
To aid debugging in the PHP, throw this at the top of your settings.php file:
````php
//ini_set('display_errors', 'On');
````
Then just uncomment it when you want to see errors.

### Setting Up on dev server 

#### Setting Up Apache VirtualHost

Apache VirtualHost config files are located in /etc/httpd/vhosts.d/. You should already have a VirtualHost configured for 443/SSL. Add the highlighted lines to your <VirtualHost *:443> section:
````
<VirtualHost *:443>
    ServerName nbennett.xylem-redux.wiredtree.com:443
    DocumentRoot "/home/nbennett/www/"
    ServerAdmin nbennett@wiredtree.com
    ErrorLog logs/nbennett-ssl_error_log
    LogLevel warn
    SSLEngine on
    SSLCipherSuite ALL:!ADH:!EXPORT56:RC4+RSA:+HIGH:+MEDIUM:+LOW:+SSLv2:+EXP
    SSLCertificateFile /etc/httpd/conf/ssl/server.crt
    SSLCertificateKeyFile /etc/httpd/conf/ssl/server.key
    Alias /inventory /home/nbennett/src/wt/inventory/htdocs
    WSGIScriptAlias /arbor /home/nbennett/src/wt/arbor/arbor/wsgi.py
    WSGIScriptAlias /creeper /home/nbennett/src/wt/creeper/creeper/wsgi.py
    WSGIPassAuthorization On
#     <Location />
#         Order Deny,Allow
#         AuthType Basic
#         AuthName "nbennett.xylem-redux.wiredtree.com"
#         AuthUserFile /var/www/auth/xylemusers
#         Require valid-user
#         SSLRequireSSL
#     </Location>
</VirtualHost>
````

#### Clone the repository from Gerrit

````bash
cd ~/src/wt/
git clone ssh://nbennett@gerrit.wiredtree.com:29418/api/creeper.git
````

#### Create a virtualenv

````bash
cd ~/src/wt/creeper/
virtualenv pythonenv
source pythonenv/bin/activate
pip install -r requirements.txt
````

## SAE pack for Pidgin 
Since sae.tweek.us is no more, you can't get your SAE pack on... unless you get the download here!

https://github.com/tothebeat/saemoticons/raw/master/SA-Emoticons-Pidgin.tar.gz

Need a reference on the smilies? 

[http://forums.somethingawful.com/misc.php?action=showsmilies Go to the source]

[https://github.com/tothebeat/saemoticons Work with the image URLs and emoticon shortcuts scraped from the source]

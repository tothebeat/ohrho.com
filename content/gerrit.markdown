Title: Install Gerrit Code Review
Date: 2013-11-19 22:21 
Category: Python 
Tags: python
Slug: installing-gerrit-code-review
Author: Nick Bennett
Summary: Notes on installing and configuring Gerrit Code Review and gitweb.

For the uninitiated, [Gerrit Code Review](https://code.google.com/p/gerrit/) is a [code review system](http://en.wikipedia.org/wiki/Software_code_review) used by some major projects like [cyanogenmod](http://review.cyanogenmod.org), [android](https://android-review.googlesource.com), and [openstack](https://review.openstack.org). It can be integrated nicely with [gitweb](http://git-scm.com/book/ch4-6.html), a simple but reliable web interface for browsing your git repositories. 

Gerrit Code Review has documentation, but I found that it was difficult to understand if I wanted to do anything that wasn't default. Below are the notes I took while installing and configuring it at work. I hope that this can be of some use to others.

### Installing Gerrit
[Installation Docs](http://gerrit-documentation.googlecode.com/svn/Documentation/2.6/install-quick.html)

#### Check Java
````bash
CT-111-bash-4.1# java -version
java version "1.7.0_21"
Java(TM) SE Runtime Environment (build 1.7.0_21-b11)
Java HotSpot(TM) 64-Bit Server VM (build 23.21-b01, mixed mode)
````

#### Create user and login 
````bash
adduser gerrit2
sudo su gerrit2
cd ~
````

#### Get Gerrit 
````bash
wget http://gerrit-releases.storage.googleapis.com/gerrit-2.6.war
````

#### Initialize & Start Gerrit Site
````bash
java -jar gerrit-2.6.war init --batch -d ~/gerrit_sneakysnakes
````

#### Add Gerrit Daemon to Startup
Make a symlink of the script in rc3.d:
````bash
CT-111-bash-4.1# sudo ln -snf /home/gerrit2/gerrit_sneakysnakes/bin/gerrit.sh /etc/init.d/gerrit
CT-111-bash-4.1# sudo ln -snf /etc/init.d/gerrit /etc/rc3.d/S90gerrit
````

Set the GERRIT_SITE environment variable in ````/etc/default/gerritcodereview````:
````
GERRIT_SITE=/home/gerrit2/gerrit_sneakysnakes
````

#### Configure Gerrit to run through reverse proxy
Edit ````/home/gerrit2/gerrit_sneakysnakes/etc/gerrit.config````, change:
````
canonicalWebUrl = http://gerrit.sneakysnakes.com:8080/
````
to:
````
canonicalWebUrl = http://gerrit.sneakysnakes.com/
````
and change:
````
listenUrl = http://*:8080/
````
to:
````
listenUrl = proxy-http://127.0.0.1:8080/
````

Edit ````/etc/httpd/conf.d/gerrit.conf```` and confirm it contains the following:
````
<VirtualHost 173.199.152.62:80>
  ServerName 173.199.152.62

  ProxyRequests Off
  ProxyVia Off
  ProxyPreserveHost On

  <Proxy *>
    Order deny,allow
    Allow from all
  </Proxy>

  <Location />
    AuthType Basic
    AuthName "Gerrit Code Review"
    Require valid-user
    AuthUserFile /etc/httpd/htpasswds/gerrit
  </Location>

  AllowEncodedSlashes On
  ProxyPass / http://127.0.0.1:8080/ nocanon
</VirtualHost>
````
(according to [setup instructions](https://gerrit-review.googlesource.com/Documentation/config-reverseproxy.html), the two options ````AllowEncodedSlashes On```` and ````ProxyPass .. nocanon```` are required since Gerrit 2.6.)

#### Add HTTP auth
Generate HTTP auth accounts for everyone:
````bash
CT-111-bash-4.1# htpasswd /etc/httpd/htpasswds/gerrit admin
CT-111-bash-4.1# htpasswd /etc/httpd/htpasswds/gerrit nbennett
````

Enable HTTP auth pass-through for Gerrit:
````bash
CT-111-bash-4.1# git config --file /home/gerrit2/gerrit_sneakysnakes/etc/gerrit.config auth.type HTTP
CT-111-bash-4.1# git config --file /home/gerrit2/gerrit_sneakysnakes/etc/gerrit.config --unset auth.httpHeader
CT-111-bash-4.1# git config --file /home/gerrit2/gerrit_sneakysnakes/etc/gerrit.config auth.emailFormat '{0}@sneakysnakes.com'
````

#### Apply Changes
Restart Gerrit:
````bash
CT-111-bash-4.1# /home/gerrit2/gerrit_sneakysnakes/bin/gerrit.sh restart
````

Restart Apache:
````bash
CT-111-bash-4.1# /etc/init.d/httpd restart
````

#### Installing and Configuring Firewall

Modify ````/etc/csf/csf.conf```` to add port 29418 (Gerrit) to the TCP_IN list:
````
# Allow incoming TCP ports
TCP_IN = "20,21,22,25,26,53,80,110,143,443,465,587,993,995,2077,2078,2082,2083,2086,2087,2095,2096,9100,9200,29418,30000:35000"
````

Restart CSF:
````bash
CT-111-bash-4.1# service csf restart
````

#### Create Admin
The first user to log in to a new installation will automatically be set as the admin. Log in to http://gerrit.sneakysnakes.com/ for the first time with the admin account created earlier. Subsequent logins will create ordinary Registered User accounts. 

To switch users once logged in as admin, prepend ````logout@```` to the url, i.e. go to http://logout@gerrit.sneakysnakes.com/.

#### Set Permissions
Access Control is configured through the All-Projects settings. Log in to http://gerrit.sneakysnakes.com/ as admin. Go to Projects->List in the upper left corner, and click on All-Projects. Click the ````Edit```` button to make changes. (refs: [Access Control](http://gerrit.sneakysnakes.com/Documentation/access-control.html) [Config Labels](http://gerrit.sneakysnakes.com/Documentation/config-labels.html))

##### Push Existing Repos without Code Review
In order to push an existing project into Gerrit without requiring every existing commit to be reviewed, a few flags need to  be set on the project. The easiest way to do this is to change the All-Projects template, set these flags for the Administrators group, and then simply add yourself to the Administrators group if you're going to be pushing an existing project. 

Under the section marked by ````Reference: refs/heads/*````, you will find the previously mentioned flags. The Administrators group should already have these flags enabled.

To bypass review, push to refs/heads/master instead of refs/for/master (see [this](http://gerrit.sneakysnakes.com/Documentation/user-upload.html#bypass_review)).

#### Set default Code-Review range to (-2,+2
Under the section marked by ````Reference: refs/heads/*````, look for ````Label Code-Review````. By default, just the groups ````Administrators```` and ````Project Owners```` can use -2 and +2 ratings, and the ````Registered Users```` group is limited to -1, 0, and +1. Change the min and max ratings usable by ````Registered Users```` to -2 and +2.

##### Allow gitweb Read Access

In the All-Projects settings, under the "'''Reference:''' refs/meta/config" section, with respect to the ''Read'' permission, add the '''Registered Users''' group.

### Using Gerrit
#### Set your account password
Log in to the Gerrit server via the node, spacecadet. You can find the container ID for gerrit.sneakysnakes.com:
````
root@spacecadet [1681 11:23:52 ~]$ vzlist
      CTID      NPROC STATUS       IP_ADDR         HOSTNAME

       111         11 running      123.123.123.123  gerrit.sneakysnakes.com
````
Enter the server with:
````bash
root@spacecadet [1682 11:24:08 ~]$ vzctl enter 111
````
Your HTTP auth username should be the name stub of your sneakysnakes email address. My email address is nbennett@sneakysnakes.com, so my username will be ````nbennett````. Set your htpasswd this way:
````bash
CT-111-bash-4.1# htpasswd /etc/httpd/htpasswds/gerrit nbennett
````

#### Add RSA public key to your Gerrit account
Add the contents of your ~/.ssh/id_rsa.pub file to the SSH public keys options in your user account settings on the Gerrit site. Click on your name in the upper-right corner of the page, click on Settings, and then click on SSH Public Keys. 

#### Add Gerrit commit hook script to automatically add Change-Id to commit messages
In the root of the repo from which you will be making commits, retrieve the Gerrit script that will automatically add a Change-Id to all future commits (change nbennett to your username) ([ref](http://stackoverflow.com/questions/8845658/gerrit-error-when-change-id-in-commit-messages-are-missing)):
````bash
scp -p -P 29418 nbennett@gerrit.sneakysnakes.com:hooks/commit-msg .git/hooks/
````

#### Adding git remote for Gerrit
Instead of laboriously typing in the full path every time to Gerrit and having to remember the arcane port number, you can add a git remote alias for gerrit:
````bash
git remote add gerrit ssh://nbennett@gerrit.sneakysnakes.com:29418/arbor/arbor
````
This adds the following text to the .git/config file in your repository:
````
[remote "gerrit"]
        url = ssh://nbennett@gerrit.sneakysnakes.com:29418/arbor/arbor
        fetch = +refs/heads/*:refs/remotes/gerrit/*
````
You can then push changes simply with:
````bash
git push gerrit HEAD:refs/for/master
````

#### Add existing git repo to Gerrit 
1. Add yourself to the Administrators group. 
    1. Log in to http://gerrit.sneakysnakes.com/ as admin (you may need to log out first with http://logout@gerrit.sneakysnakes.com/). 
    2. Click on People in the upper left, then click on List Groups. Click on the Administrators group.
    3. Type your username in the Members text field and click Add. NOTE: You must have logged in at least once before to have the account created and available for adding.
    4. Log out of gerrit and log back in as yourself.
2. Create a new project on Gerrit
    1. From the command line:````ssh -p 29418 nbennett@gerrit.sneakysnakes.com gerrit create-project --name arbor/arbor````
    2. Go to http://gerrit.sneakysnakes.com/ and click on Projects in the upper left corner, and then on List. Click on the new project you just created. Then click on Access, to the right of the Projects->List option. 
    3. Click the Edit button, and then click the Add Reference link. Leave the default Reference as "refs/heads/*". From the drop-down menu, pick "Create Reference". For the group name, type "Administrators" and then click the Add button to the right. Repeat this, choosing "Forge Committer Identity" and "Forge Author Identity" from the drop-down menu and adding Administrators for each one. When finished, click the "Save Changes" button at the bottom. ([ref](http://stackoverflow.com/questions/8353988/how-to-upload-a-git-repo-to-gerrit))
3. Push your repo
    1. In the command line, in the root of your repo, run ([ref](http://en.wikibooks.org/wiki/Git/Gerrit_Code_Review#Importing_project_into_Gerrit)): ````git push ssh://nbennett@gerrit.sneakysnakes.com:29418/arbor/arbor HEAD:refs/heads/master````
4. Remove yourself from the Administrators group
    1. Log out of Gerrit with http://logout@gerrit.sneakysnakes.com/, log in as admin.
    2. Following the steps you used previously to add yourself to the Administrators group, get to the point where you would have typed in your username to the Members text field. Your name is listed below. Check the box next to your name and click the Delete button. 
5. Log out of Gerrit and log back in as yourself.

#### Pushing changes to be reviewed
With your commits created with the Gerrit Change-Id hook script already installed, you're ready to push to Gerrit to have your changes reviewed:
````
git push ssh://nbennett@gerrit.sneakysnakes.com:29418/arbor/arbor HEAD:refs/for/master
````

#### To give a project the Verified label

See: http://gerrit-documentation.googlecode.com/svn/Documentation/2.6/config-labels.html#label_Verified

* Clone the project repository
* ````git fetch origin refs/meta/config````
* ````git checkout FETCH_HEAD````
* ````vi project.config````  
 Add:
````
 [label "Verified"]
     function = MaxWithBlock
     value = -1 Fails
     value =  0 No score
     value = +1 Verified
````
* ````git add --all````
* ````git commit -m "Add Verified label."````
* ````git push origin HEAD:refs/meta/config````
* Make sure the project gives Non-Interactive Users (aka, buildbot) the ability to use the Verify label.
* Make sure the user that will use Verify has the permissions.
* (May have to restart the gerrit server?)

Note: The buildbot source code has been slightly modified in pythonenv/lib/python2.6/site-packages/buildbot/status/status_gerrit.py to support this new --label syntax as the current stable version (0.8.7p1) doesn't support it:

````
 -command.extend(["--verified %d" % int(verified)])
 +command.extend(["--label Verified=%d" % int(verified)])
````
#### Further Help 
* [Quick Introduction](http://gerrit.sneakysnakes.com/Documentation/intro-quick.html)
* [Gerrit Workflow for OpenStack](https://wiki.openstack.org/wiki/Gerrit_Workflow)

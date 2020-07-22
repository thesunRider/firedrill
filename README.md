# Firedrill (bypass firewall)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://www.youtube.com/channel/UCvbFfGomoaEKufdWCQ44KWA)

firedrill can bypass all firewalls by tunneling from your attacker machine to your target by tunneling traffic through an intermediate php file running on the server.

**PLEASE DO NOT REPORT THE FILE TO VIRUSTOTAL!**

# When to use ?
 - After compromising a website had troubled with converting your webshell to a reverse tcp connection because the firewall doesnt allow tcp connections ?
 - Unable to access ports in the compromised system through your webshell?
 - Unable to execute ```fsock fopen ``` commands on compromised machine through php
 - Don't have a VPS to act as a jumphost to redirect tcp to your attacker machine?
 - SSL impersonation in meterpreter didnt work?

# How to setup ?
Put the ```target.py``` and the ```firedrill.php``` in the compromised target.Place firedrill.php in a place where you can execute it through your browser.

# Requirements
plain old Python 2.7 only!
TESTED IN python 2.4.3,2.7

This program does not need any external libraries to install whatsoever...
Providing you with maximum portability.
The compromised **Website** should be able to run php files.

# Usage

Edit the `attacker.py` and set the port to listen to make changes in this section only!.
```php
#target where php resides
target = 'http://<location to your website>/firedrill.php' #change it to the compromised host addres
channelmine = "chnl1" #channelwhich this console recieves read(LEAVE THIS AS DEFAULT)
channelother = "chnl0"  #channelwhich this console writes to. (LEAVE THIS AS DEFAULT)
cookies =  'A111A135818' #default session id (LEAVE IT AS DEFAULT)
host = ''        # Symbolic name meaning all available interfaces (LEAVE IT AS DEFAULT)
port = 1234     # Port to listen to for attacker service
buffrlngth = 1024 * 4 #the default buffer lenght to read
speed = 0.05 #adjust speed of requests
key = "12345" #password used to encrypt the data before sending
```
Likewise edit the ```target.py``` but for ```target.py``` set target as 
```php
target = 'http://127.0.0.1/<location to tunnel>/firedrill.php' #here loopback address is used instead of original site's name.
```
for the ```firedrill.php``` set the number of channels to create 
>NOTE!: For communication with one port in the target machine you need 2 channels.

Put the ```firedrill.php``` in the target at a place where you can run the php file from your machine.And fire up your listners.

>NOTE!: On the attacker machine fire up your listner ***before*** your reverse_shell

# Features!

  - Bypass firewall rules.
  - Much more Stealth!
  - No need of any external hosting to redirect traffic to attacker machine.
  
You can also:
  - Connect with any port on the compromised machine.
  - Use as proxy to tunnel data through http/https. 
  - Communicate with multiple ports using single php.

# How it works

 The listner on the attacker machine sents the data to the php file on the server which is passed on to the listner on the server , which is passed on to the target port.
 
```sh
 [target port] <====> listner <======> Php intermediate <=====> listner <====> [attacker port] 
 ```
 This method is more effective since to the point of the firewall the attacker is just plainly visiting a page in the website and furthermore this method uses the same certificate as used by the web app.
 All the data is sent as password protected so the waf cannot inspect the http/https packets

### Development

Want to contribute? Great!
Do stuff with my code but be sure to attribute me before distributing it.

### Todos

 - Aspx intermediate file
 - Use asyncio for faster speeds
 - Improve code security.
 - Post video Explaing how it works..
 - Add an option to change user-agent strings.

License
----

MIT

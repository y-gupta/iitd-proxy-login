from getpass import getpass
from datetime import datetime
import urllib2,urllib,sys,threading,webbrowser

class Proxy:
    proxy_set={'btech':22,'dual':62,'diit':21,'faculty':82,'integrated':21,'mtech':62,'phd':61,'retfaculty':82,'staff':21,'irdstaff':21,'mba':21,'mdes':21,'msc':21,'msr':21,'pgdip':21}
	google = 'http://www.google.com'
	def __init__(self, username, password, proxy_cat):
		self.username = username
		self.password = password
		self.proxy_cat = proxy_cat
		self.auto_proxy = "http://www.cc.iitd.ernet.in/cgi-bin/proxy."+proxy_cat
		self.urlopener = urllib2.build_opener(urllib2.ProxyHandler({'auto_proxy':self.auto_proxy}))
		self.proxy_page_address = 'https://proxy'+str(Proxy.proxy_set[proxy_cat])+'.iitd.ernet.in/cgi-bin/proxy.cgi'
		self.new_session_id()
		self.details()
		

	def is_connected(self):
		proxies = {'http': 'http://proxy'+str(Proxy.proxy_set[self.proxy_cat])+'.iitd.ernet.in:3128'}
		try:
			response = urllib.urlopen(Proxy.google, proxies=proxies).read()
		except Exception, e:
			return "Not Connected"
		if "<title>IIT Delhi Proxy Login</title>" in response:
			return "Login Page"
		elif "<title>Google</title>" in response:
			return "Google"
		else:
			return "Not Connected"

	def get_session_id(self):
		try:
			response = self.open_page(self.proxy_page_address)
		except Exception, e:
			print "hello"
			return None
		check_token='sessionid" type="hidden" value="'
		token_index=response.index(check_token) + len(check_token)
		sessionid=""
		for i in range(16):
		    sessionid+=response[token_index+i]
		return sessionid

	def new_session_id(self):
		self.sessionid = self.get_session_id()
		self.loginform={'sessionid':self.sessionid, 'action':'Validate', 'userid':self.username, 'pass':self.password}
		self.logout_form={'sessionid':self.sessionid, 'action':'logout', 'logout':'Log out'}
		self.loggedin_form={'sessionid':self.sessionid, 'action':'Refresh'}

	def login(self):
		self.new_session_id()
		response = self.submitform(self.loginform)
		if "Either your userid and/or password does'not match." in response:
			return "Incorrect", response
		elif "You are logged in successfully as "+self.username in response:
			def ref():
				res = user.refresh()
				if res=='Success':
					self.top_label.config(text=user.username)
					threading.Timer(100.0,ref).start()
				elif res=='Session Expired':
					print "Session Expired Run Script again"
				else:
					threading.Timer(10.0,self.ref).start()
				print "Refresh",res,datetime.now()
			threading.Timer(60.0,ref).start()
			return "Success", response
		elif "already logged in" in response:
			return "Already", response
		elif "Session Expired" in response:
			return "Expired", response
		else:
			return "Not Connected", response

	def logout(self):
		response = self.submitform(self.logout_form)
		if "you have logged out from the IIT Delhi Proxy Service" in response:
			return "Success", response
		elif "Session Expired" in response:
			return "Expired", response
		else:
			return "Failed", response
	    
	def refresh(self):
		response = self.submitform(self.loggedin_form)
		if "You are logged in successfully" in response:
			if "You are logged in successfully as "+self.username in response:
				return "Success", response
			else:
				return "Not Logged In"
		elif "Session Expired" in response:
			return "Expired", response
		else:
			return "Not Connected", response

	def details(self):
		for property, value in vars(self).iteritems():
			print property, ": ", value

	def submitform(self, form):
		return self.urlopener.open(urllib2.Request(self.proxy_page_address,urllib.urlencode(form))).read()

	def open_page(self, address):
		return self.urlopener.open(address).read()

user = Proxy(username='cs5110272', password='yourPasswordHere', proxy_cat='dual')
print user.login()[0] #for logging in


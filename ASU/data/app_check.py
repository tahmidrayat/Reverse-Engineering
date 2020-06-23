import os
import re
import sys
import bs4
import json
import requests
import interpreter
from data.color import *
from multiprocessing.pool import ThreadPool

def kintl():
	if os.path.exists("out"):
		if os.path.exists("out/app.txt"):
			if os.path.getsize("out/app.txt") !=0:
				print("%s[!]%s path exists: out/app.txt"%(R,N))
				s=raw_input("%s[?]%s replace? y/n: "%(R,N))
				if s.lower() =="y":
					open("out/app.txt","w").close()
		else:
			open("out/app.txt","w").close()
	else:
		os.mkdir("out")
		open("out/app.txt","w").close()

class app(object):
	def __init__(self):
		self.i="https://mbasic.facebook.com/{}"
		self.fa=0
		self.o=0
		self.file()
	
	def back(self):
		raw_input("press enter to menu...")
		interpreter.ASU()
		
	def file(self):
		try:
			self.a=open(raw_input("%s[?]%s Account List: "%(
				G,N))).read().splitlines()
		except Exception as e:
			print("%s[!]%s %s"%(R,N,e))
			self.file()
		print("%s[*]%s total account: %s"%(G,N,len(self.a)))
		self.q()
	
	def q(self):
		self.qw=raw_input("%s[?]%s App Query: "%(G,N)).lower()
		if self.qw =="":
			self.q()
		self.file2()
		
	def file2(self):
		if os.path.exists("out"):
			try:
				self.f=raw_input("%s[?]%s filename: "%(G,N))
				if self.f =="":
					self.file2()
				open("out/%s"%(self.f),"w").close()
			except Exception as f:
				print("%s[!]%s %s"%(R,N,f))
				self.file2()
		else:
			os.mkdir("out")
			self.file2()
		self.thread()
		
	def thread(self):
		try:
			self.t=ThreadPool(input("%s[?]%s Thread: "%(G,N)))
		except Exception as e:
			print("%s[!]%s %s"%(R,N,e))
			self.thread()
		self.t.map(self.login,self.a)
		if len(open("out/%s"%(self.f)).read().splitlines()) ==0:
			print("\n[*] all done,no app found writed with query: %s"%(self.qw))
			self.back()
		else:
			print("\n[*] all done, %s app writted saved to: out/%s"%(
				len(open("out/%s"%(self.f)).read().splitlines()),self.f))
			self.back()
		
	def login(self,a):
		s=requests.Session()
		o=s.post(self.i.format("login"),
		data={
			"email":a.split("|")[-0],
			"pass":a.split("|")[-1]
		}).url
		if "save-device" in o or "m_sess" in o:
			self.cek(s,
				self.i.format("settings/apps/tabbed/?tab=active"),a)
		else:
			self.fa+=1
		print("\r[*] Searching app: %s/%s Found-:%s Login fail-:%s   "%(self.o,
			len(self.a),len(open("out/%s"%(self.f)).read().splitlines()),self.fa)),;sys.stdout.flush()
			
	def cek(self,s,url,a):
		o=bs4.BeautifulSoup(s.get(url).text,"html.parser")
		for x in o.find_all("span",class_="cx"):
			if self.qw in x.text.lower():
				open("out/%s"%(self.f),"a").write("[%s]: %s\n"%(a,x.text))
		self.o+=1
		
class unf:
	def __init__(self,email,pasw):
		self.pasw=pasw
		self.email=email
		self.req=requests.Session()
		self.i="https://mbasic.facebook.com/{}"
		self.login()
		
	def login(self):
		s=self.req.post(self.i.format("login"),
		data=
			{
				"email":self.email,
				"pass":self.pasw
			}
		).url
		if "save-device" in s or "m_sess" in s:
			print("%s[*]%s login success: %s|%s"%(G,N,self.email,self.pasw))
			print("%s[*]%s Checking application found ..."%(G,N))
			self.cek()
		else:
			print("%s[!]%s login failed: %s|%s"%(R,N,self.email,self.pasw))
			
	def cek(self):
		bz=bs4.BeautifulSoup(
		self.req.get(self.i.format(
			"settings/apps/tabbed/?tab=active")).text,
		features="html.parser")
		pepek=[]
		for x in bz.find_all("span",class_="cx"):
			pepek.append(x.renderContents())
			print("%s[%s]%s %s"%(G,len(pepek),N,x.renderContents()))
		if len(pepek) !=0:
			print("%s[!]%s %s application found!"%(G,N,len(pepek)))
			open("out/app.txt","a").write("\n[account] %s|%s\n"%(
			self.email,self.pasw))
			for x in pepek:
				open("out/app.txt","a").write("[+] %s\n"%(x))
			open("out/app.txt","a").write("-"*50)
			print("-"*50+"\n")
			self.req.cookies.clear()
		else:
			print("%s[!]%s no application found."%(R,N))
			print("-"*50+"\n")
			self.req.cookies.clear()

class check:
	def __init__(self):
		kintl()
		self.file()
		
	def file(self):
		try:
			print("%s[!]%s sparate: |"%(R,N))
			self.f=open(
				raw_input(
					"%s[?]%s Account List: "%(
			G,N))).read().splitlines()
		except Exception as __errors__:
			print("%s[!]%s %s"%(R,N,__errors__))
			return self.file()
		print "%s[*]%s output: out/app.txt"%(G,N)
		for x in self.f:
			p=x.split("|")
			try:
				unf(p[0],p[-1])
			except:continue
			
class ina(object):
	def __init__(self):
		self.i="https://mbasic.facebook.com/{}"
		self.fa=0
		self.o=0
		self.file()
	
	def back(self):
		raw_input("press enter to menu...")
		interpreter.ASU()
		
	def file(self):
		try:
			self.a=open(raw_input("%s[?]%s Account List: "%(
				G,N))).read().splitlines()
		except Exception as e:
			print("%s[!]%s %s"%(R,N,e))
			self.file()
		print("%s[*]%s total account: %s"%(G,N,len(self.a)))
		self.q()
	
	def q(self):
		self.qw=raw_input("%s[?]%s App Query: "%(G,N)).lower()
		if self.qw =="":
			self.q()
		self.file2()
		
	def file2(self):
		if os.path.exists("out"):
			try:
				self.f=raw_input("%s[?]%s filename: "%(G,N))
				if self.f =="":
					self.file2()
				open("out/%s"%(self.f),"w").close()
			except Exception as f:
				print("%s[!]%s %s"%(R,N,f))
				self.file2()
		else:
			os.mkdir("out")
			self.file2()
		self.thread()
		
	def thread(self):
		try:
			self.t=ThreadPool(input("%s[?]%s Thread: "%(G,N)))
		except Exception as e:
			print("%s[!]%s %s"%(R,N,e))
			self.thread()
		self.t.map(self.login,self.a)
		if len(open("out/%s"%(self.f)).read().splitlines()) ==0:
			print("\n[*] all done,no app found writed with query: %s"%(self.qw))
			self.back()
		else:
			print("\n[*] all done, %s app writted saved to: out/%s"%(
				len(open("out/%s"%(self.f)).read().splitlines()),self.f))
			self.back()
		
	def login(self,a):
		s=requests.Session()
		o=s.post(self.i.format("login"),
		data={
			"email":a.split("|")[-0],
			"pass":a.split("|")[-1]
		}).url
		if "save-device" in o or "m_sess" in o:
			self.cek(s,
				self.i.format("settings/apps/tabbed/?tab=inactive"),a)
		else:
			self.fa+=1
		print("\r[*] Searching app: %s/%s Found-:%s Login fail-:%s   "%(self.o,
			len(self.a),len(open("out/%s"%(self.f)).read().splitlines()),self.fa)),;sys.stdout.flush()
			
	def cek(self,s,url,a):
		o=bs4.BeautifulSoup(s.get(url).text,"html.parser")
		for x in o.find_all("span",class_="cx"):
			if self.qw in x.text.lower():
				open("out/%s"%(self.f),"a").write("[%s]: %s\n"%(a,x.text))
		self.o+=1

class apps(object):
	def __init__(self):
		print "\n\t[ Select Actions ]\n"
		print "  {%s01%s} Check All App From Account List."%(G,N)
		print "  {%s02%s} Check All App By Query Account List"%(G,N)
		print "  {%s03%s} Check All Expired App By Query Account List"%(G,N)
		print "  {%s04%s} Back To Menu.\n"%(R,N)
		self.c()
	
	def c(self):
		r=raw_input("%s[%s*%s]%s Actions>> "%(G,R,G,N))
		if r =="":
			self.c()
		elif r =="1" or r =="01":
			check()
		elif r =="2" or r =="02":
			app()
		elif r =="3" or r =="03":
			ina()
		elif r =="4" or r =="04":
			raw_input("press enter to menu...")
			interpreter.ASU()
		else:
			print "%s[!]%s invalid options!"%(R,N)
			self.c()


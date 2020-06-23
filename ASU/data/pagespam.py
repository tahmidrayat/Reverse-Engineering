#-*-coding:utf-8-*-
import bs4
import sys
import json
import time
import random
import requests
from data.color import *
from multiprocessing.pool import ThreadPool

class wallpage:
	def __init__(self):
		self.wal=[]
		self.success=0
		self.failed=0
		self.req=requests.Session()
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
			self.id()
		else:exit("%s[!]%s login failed."%(R,N))
		
	def id(self):
		self.pageid=raw_input("%s[?]%s page id     : "%(G,N))
		if self.pageid =="":
			self.id()
		else:
			r=self.req.get(self.i.format(self.pageid))
			self.bs=bs4.BeautifulSoup(r.text,
					features="html.parser")
			if r.status_code ==200:
				print "%s[*]%s page name   : %s"%(
					G,N,self.bs.find("title").text)
				self.akun()
			else:
				print("%s[!]%s unknown page id: %s"%(
					R,N,self.pageid))
				print("%s[!]%s ERROR: %s"%(R,N,self.bs.find("title").text))
				self.id()
			
	def akun(self):
		try:
			self.a=open(raw_input("%s[?]%s accont list : "%(G,N))).read().splitlines()
		except Exception as __e:
			print("%s[!]%s %s"%(R,N,__e))
			self.akun()
		self.cout()
		
	def cout(self):
		try:
			self.count=input("%s[?]%s mau berapa story yg mau di spam? "%(R,N))
		except Exception as __errors__:
			print("%s[!]%s %s"%(R,N,__errors__))
			self.cout()
		print("* use coma (,) for next message.")
		self.msg()
		
	def msg(self):
		self.mes=raw_input("%s[?]%s message: "%(G,N)).split(",")
		self.gooo(self.i.format(self.pageid))
		
	def gooo(self,url):
		bs=bs4.BeautifulSoup(
			self.req.get(url).text,
		features="html.parser")
		for x in bs.find_all("a",href=True):
			if "komentar" in x.text.lower():
				if "story.php" in x["href"]:
					if len(self.wal) ==self.count:
						break
					else:
						self.wal.append(self.i.format(x["href"]))
						print("\r[+] GET %s/%s story"%(
							len(self.wal),self.count
								)),;sys.stdout.flush()
					
			if "tampilkan lainnya" in x.text.lower():
				self.gooo(self.i.format(x["href"]))
		print 
		while True:
			pk=ThreadPool(3)
			pk.map(self.lok,self.a)
		
	def lok(self,akun):
		s=requests.Session()
		j=s.post(self.i.format("login"),
			data=
		{
			"email":akun.split("|")[-0],
			"pass":akun.split("|")[-1]
		}).url
		if "save-device" in j or "m_sess" in j:
			self.send(s)
		else:
			self.failed+=1
	
	def send(self,req):
		self.ckgu=req
		map(self.mek,self.wal)
		
	def mek(self,url):
		data=[]
		r=bs4.BeautifulSoup(self.ckgu.get(url).text,
			features="html.parser")
		for x in r("form"):
			if "comment.php" in x["action"]:
				data.append(self.i.format(x["action"]))
				break
		for x in r("input"):
			try:
				if "fb_dtsg" in x["name"]:
					data.append(x["value"])
				if "jazoest" in x["name"]:
					data.append(x["value"])
					break
			except:pass
		if len(data) ==3:
			self.ckgu.post(data[0],
			data={"fb_dtsg":data[1],
						"jazoest":data[2],
						"comment_text":random.choice(self.mes),
						"submit":"Komentari"}
			)
			self.success+=1
			print "\r[+] %s message sent! ERROR-%s"%(
				self.success,self.failed),;sys.stdout.flush()
		
				
class pejSpam(object):
	def __init__(self):
		self.i="https://mbasic.facebook.com/{}"
		self.gk=""
		self.page()
	
	def page(self):
		self.id=raw_input("%s[?]%s page id     : "%(G,N))
		if self.id =="":
			return self.page()
		if requests.get(self.i.format(self.id)).status_code !=200:
			print("%s[!]%s Unknown page id."%(R,N))
		else:
			bs=bs4.BeautifulSoup(
				requests.get(self.i.format(self.id)).text,
			features="html.parser")
			print("%s[!]%s Target      : %s"%(G,N,
				bs.find("title").text))
			self.list()
		
	def list(self):
		try:
			self.l=open(
				raw_input("%s[?]%s account list: "%(
			G,N))).read().splitlines()
		except Exception as __errors__:
			print("%s[!]%s %s"%(R,N,__errors__))
			return self.list()
		self.msg()
		
	def msg(self):
		self.ms=raw_input("%s[?]%s message     : "%(G,N))
		if self.ms =="":
			return self.msg()
		while True:
			p=ThreadPool(100)
			p.map(self.send,self.l)
		
	def send(self,a):
		req=requests.Session()
		s=req.post(self.i.format("login"),
			data=
				{
					"email":a.split("|")[-0],
					"pass":a.split("|")[-1]
				}
		).url
		if "save-device" in s or "m_sess" in s:
			self.sends(a.split("|")[-0],req)
		else:
			print("%s[!]%s %s failed login."%(G,N,
				a.split("|")[-0]))
				
	def sends(self,b,a):
		datas=[]
		bs=bs4.BeautifulSoup(
			a.get(self.i.format(self.id)).text,
		features="html.parser")
		for x in bs.find_all("a",href=True):
			if "messages/thread" in x["href"]:
				datas.append(self.i.format(x["href"]))
				break
		if len(datas) !=0:
			self.priv(b,a,datas[0])
		
	def priv(self,b,req,url):
		data=[]
		bs=bs4.BeautifulSoup(
			req.get(url).text,features="html.parser")
		for x in bs('form'):
			if "send" in x["action"]:
				data.append(self.i.format(x["action"]))
		for x in bs("input"):
			try:
				if "fb_dtsg" in x["name"]:
					data.append(x["value"])
				if "jazoest" in x["name"]:
					data.append(x["value"])
				if "ids" in x["name"]:
					data.append(x["name"])
					data.append(x["value"])
				if "Send" in x["name"]:
					data.append(x["value"])
					break
			except:pass
		if len(data) !=0:
			sendss=req.post(data[0],
				data=
					{
						"fb_dtsg":data[1],
						"jazoest":data[2],
						data[3]:data[4],
						"body":self.ms,
						"Send":data[5]
					}
			).url
			if "success" in sendss:
				print("%s[*]%s %s -> send success"%(G,N,b))
			else:
				print("%s[!]%s %s -> send failed."%(R,N,b))
				
				



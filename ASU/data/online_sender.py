import bs4
import json
import random
import requests
from data import cache
from data.color import *

class buddy:
	def __init__(self):
		self.i="https://mbasic.facebook.com/{}"
		self.req=requests.Session()
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.getLogin()
		
	def send(self,*args,**kwargs):
		s=self.req.post(args[0],data=kwargs)
		bs=bs4.BeautifulSoup(
				s.text,features="html.parser")
		title=bs.find("title").renderContents()
		if "success" in s.url:
			print(" | %s%s -> %s message sent.%s"%(G,title,kwargs["body"],N))
		else:
			print(" | %s%s -> %s message not sent.%s"%(R,title,kwargs["body"],N))
		
	def getLogin(self):
		s=self.req.post(self.i.format("login"),
		data=
			{
				"email":self.config["email"],
				"pass":self.config["pass"]
			}
		).url
		if "save-device" in s or "m_sess" in s:
			print("%s[*]%s Login success ..."%(G,N))
			print("%s[*]%s Getting Friends Online ..."%(G,N))
			self.buddy()
		else:exit("%s[!]%s Login Failed."%(R,N))
		
	def buddy(self):
		bs=bs4.BeautifulSoup(
			self.req.get(self.i.format("buddylist.php")
		).text,features="html.parser")
		self.pq=[]
		for x in bs.find_all("a",class_="bm"):
			print "%s[*]%s %s"%(G,N,x.renderContents())
			if "messages/read" in x["href"]:
				self.pq.append(self.i.format(x["href"]))
		print "\n%s[+]%s Online: %s"%(G,N,len(self.pq))
		s=raw_input("%s[?]%s Start? y/n: "%(R,N))
		if s.lower() == "y":
			self.msg()
			self.spam()
		else:exit("%s[!]%s Exit."%(R,N))
		
	def msg(self):
		print("%s[+]%s Use coma (,) to random msg"%(G,N))
		self.m=raw_input("%s[+]%s Message: "%(G,N))
		if self.m == "":
			print('%s[!]%s Message empty.'%(R,N))
			return self.msg()
		
	def spam(self):
		for i in self.pq:
			self.bom(i)
	
	def bom(self,i):
		postdata=[]
		s=bs4.BeautifulSoup(
			self.req.get(i).text,features="html.parser")
		for x in s("form"):
			if "messages/send" in x["action"]:
				postdata.append(x["action"])
		for x in s("input"):
			try:
				if "fb_dtsg" in x["name"]:
					postdata.append(x["value"])
				if "jazoest" in x["name"]:
					postdata.append(x["value"])
				if "send" in x["name"]:
					postdata.append(x["value"])
				if "tids" in x["name"]:
					postdata.append(x["value"])
					break
			except:pass
		
		self.send(self.i.format(postdata[0]),
			fb_dtsg=postdata[1],
				jazoest=postdata[2],
					body=random.choice(self.m.split(",")),
				send=postdata[3],
		tids=postdata[4])
		


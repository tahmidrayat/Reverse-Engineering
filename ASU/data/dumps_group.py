#-*-coding:utf-8-*-
import re
import os
import bs4
import sys
import json
import time
import random
import requests
import interpreter
from data.color import *
from multiprocessing.pool import ThreadPool

def ngntd():
	if os.path.exists("out"):
		if os.path.exists("out/group.txt"):
			if os.path.getsize("out/group.txt") !=0:
				o=raw_input("%s[!]%s path exists: out/group.txt\n%s[?]%s replace? y/n): "%(R,N,R,N)).lower()
				if o == "y":
					open("out/group.txt","w").close()
		else:
			open("out/group.txt","w").close()
	else:
		os.mkdir("out")
		open("out/group.txt","w").close()
		
class dumps_group(object):
	def __init__(self):
		self.wal=[]
		self.req=requests.Session()
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.i="https://mbasic.facebook.com/{}"
		self.api="https://graph.facebook.com/"
		self.mbasic()
		
	def mbasic(self):
		s=self.req.post(self.i.format("login"),
			data=
				{
					"email":self.config["email"],
					"pass":self.config["pass"]
				}
		).url
		if "save-device" in s or "m_sess" in s:
			self.q()
		else:exit("%s[!]%s login failed."%(R,N))
	
	def q(self):
		self.query=raw_input("%s[?]%s Query: "%(
			G,N)).lower()
		if self.query =="":
			self.q()
		self.Dump(self.i.format("groups/?seemore"))
		
	def Dump(self,url):
		s=bs4.BeautifulSoup(self.req.get(url).text,
			features="html.parser")
		print 
		for x in s.find_all("a",href=True):
			if "/groups/" in x["href"]:
				if "category" in x["href"] or "create" in x["href"]:
					continue
				if self.query in x.text.lower():
					f=re.findall("/groups/(.*?)\?",x["href"])
					if len(f) !=0:
						self.wal.append(f[0])
						print("%s. %s"%(len(self.wal),
							x.text.lower().replace(self.query,
						"%s%s%s"%(R,self.query,N))))
						
		if len(self.wal) !=0:
			self.choice()
		else:
			print("%s[!]%s No Result.\n"%(R,N))
			self.q()
			
	def choice(self):
		try:
			self.num=input("%s[?]%s Select Number: "%(
				G,N))
		except Exception as e:
			print("%s[!]%s %s"%(R,N,e))
			self.choice()
		self.login(self.wal[self.num-1])
		
	def login(self,id):
		s=bs4.BeautifulSoup(requests.post(
			"https://m.autolikeus.me/token.get.php",
		data={
			"username":self.config["email"],
			"password":self.config["pass"]
		}).text,features="html.parser")
		for x in s.find_all("iframe"):
			try:
				self.token=requests.get(
					x["src"]).json()["access_token"]
				
			except:
				print "[!] failed when generate token"
			self.dump(id)
				
	def dump(self,id):
		ngntd()
		bs=bs4.BeautifulSoup(
			self.req.get(self.i.format("groups/"+id)).text,
		features="html.parser")
		title=bs.find("title").text
		print("%s[*]%s Group Name: %s"%(G,N,title))
		print("%s[*]%s Output    : out/group.txt"%(G,N))
		self.dumps(
		"%s%s/members?fields=id&access_token=%s"
			%(self.api,id,self.token))
	
	def dumps(self,id):
		self.j=self.req.get(id).json()
		for x in self.j["data"]:
			z=open("out/group.txt").readlines()
			print("\r[%s%s%s] Writing..."%(R,len(z),N
				)),;sys.stdout.flush()
			open("out/group.txt","a").write(x["id"]+"\n")#
		try:
			self.dumps(self.j["paging"]["next"])
		except:
			print "\n[+] finished."
			raw_input("press enter to menu...")
			interpreter.ASU()


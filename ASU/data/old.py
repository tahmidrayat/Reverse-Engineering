import re
import os
import sys
import bs4
import random
import requests
from data.color import *
from multiprocessing.pool import ThreadPool

class old_account_detector(object):
	def __init__(self,accounts):
		self.accounts=accounts.split("|")
		self.req=requests.Session()
		self.i="https://mbasic.facebook.com/{}"
		self.login()
		
	def login(self):
		s=self.req.post(self.i.format("login"),
			data=
				{
					"email":self.accounts[-0],
					"pass":self.accounts[-1]
				}
		).url
		if "save-device" in s or "m_sess" in s:
			self.set(self.i.format("settings"))
		else:
			print("%s[!]%s failed login: %s|%s"%(
				R,N,self.accounts[-0],self.accounts[-1]))
	
	def set(self,url):
		s=bs4.BeautifulSoup(self.req.get(url).text,
			features="html.parser")
		for x in s.find_all("a",href=True):
			if "allactivity" in x["href"]:
				self.detect(self.i.format(x["href"]))
				
	def detect(self,url):
		p=[]
		bs=bs4.BeautifulSoup(self.req.get(url).text,
			features="html.parser")
		for x in bs.find_all("a",href=True):
			if "year" in x["href"]:
				se=re.findall("year_(.*?)$",x["href"])
				if len(se) !=0:
					p.append(se[0])
		if len(p) !=0:
			print "%s[*]%s %s|%s -> %s"%(G,N,
				self.accounts[-0],self.accounts[-1],p.pop())

class old(object):
	def __init__(self):
		print("%s[*]%s sparator: |"%(R,N))
		self.lst()
		
	def lst(self):
		try:
			self.ak=open(
				raw_input("%s[?]%s account list: "%(G,N))
					).read().splitlines()
		except Exception as __errors__:
			print("%s[!]%s %s"%(R,N,__errors__))
			return self.lst()
		self.pool()
	
	def pool(self):
		try:
			self.p=ThreadPool(
				input("%s[?]%s Enter Threads: "%(G,N)))
		except Exception as __errors__:
			print("%s[!]%s %s"%(R,N,__errors__))
			return self.pool()
		self.p.map(old_account_detector,self.ak)
		



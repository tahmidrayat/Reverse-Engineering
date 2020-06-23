#-*-coding:utf-8-*-
import bs4
import sys
import json
import time
import random
import requests
from data.color import *
from multiprocessing.pool import ThreadPool

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
		print "* use coma (,) for next message"
		self.msg()
		
	def msg(self):
		self.ms=raw_input("%s[?]%s message     : "%(G,N)).split(",")
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
		for x in bs("form"):
			if "composer" in x["action"]:
				datas.append(self.i.format(x["action"]))
		for x in bs("input"):
			try:
				if "fb_dtsg" in x["name"]:
					datas.append(x["value"])
				if "jazoest" in x["name"]:
					datas.append(x["value"])
				if "target" in x["name"]:
					datas.append(x["value"])
				if "view_post" in x["name"]:
					datas.append(x["value"])
					break
			except:pass
		if len(datas) ==5:
			print a.post(datas[0],
				data=
					{
						"fb_dtsg":datas[1],
						"jazoest":datas[2],
						"r2a":"1",
						"xhpc_timeline":"1",
						"target":datas[3],
						"c_src":"page_self",
						"cwevent":"composer_entry",
						"referrer":"pages_feed" ,
						"ctype":"inline",
						"cver":"amber",
						"rst_icv":"",
						"xc_message":random.choice(self.ms),
						"view_post":datas[4]
					}
			).url
				
				



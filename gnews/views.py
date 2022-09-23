# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 16:30:29 2022

@author: Nisar Ahmad
"""

from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests
import json
import re

#token = 'b30aa7373234c9e250e972eaf6d5f760'
#token = '4875137a0290af43dad4b43d775ea71c'
token = 'f4d6ebc179de5d1e0dea9e7bdce29554'

def main_page(request): #main page view 
	cookie = request.COOKIES.get('auth')
	if(cookie != None):	
		return HttpResponseRedirect("/home/")
	else:
		return render(request,"main_page.html")

def login(request): #login view
	return render(request,"login.html")

def logout(request): #logout
	response = render(request,"main_page.html")
	response.delete_cookie('auth')
	return response

def home(request):
	cookie = request.COOKIES.get('auth')
	if(cookie != None):
		return render(request,"home.html")
	else:
		return HttpResponseRedirect("/login/")
	
def login_response(request):
	dict_post = dict()
	if request.method == 'POST':
		user = request.POST['user']
		pass1 = request.POST['pass']
		url = 'http://127.0.0.1:8000/auth/login/'
		
		payload = {
		   "username": user,
		   "password": pass1,
		}
		response = requests.request("POST",url,data=payload) #request login endpoint
		if(response.status_code == 200): 
			access_token = response.json()['access']
			response = render(request,"home.html")
			response.set_cookie('auth',access_token) #create session cookie
			return response
		else:
			dict_post['response'] = response.json()
			return render(request,"login_response.html",dict_post) #dump json to html in-case of error
		
def register(request):
	return render(request,"register.html")

def register_response(request):
	dict_post = dict()
	if request.method == 'POST':
		user = request.POST['user']
		first = request.POST['first']
		last = request.POST['last']
		email = request.POST['email']
		pass1 = request.POST['pass']
		pass2 = request.POST['pass2']
		 
		url = 'http://127.0.0.1:8000/auth/register/'
		
		payload = {
		   "username": user,
		   "password": pass1,
		   "password2": pass2,
		   "email": email,
		   "first_name": first,
		   "last_name": last
		}
		response = requests.request("POST",url,data=payload) #request register endpoint
		if(response.status_code == 201):
			print(response.json())
			user_name = response.json()['username']
			response1 = render(request,"home.html")
			response1.set_cookie('auth',user_name) #create session cookie
			return response1
		else:
			dict_post['response'] = response.json()
			return render(request,"register_response.html",dict_post)
	
def get_top_records(request):
	cookie = request.COOKIES.get('auth')
	if(cookie != None):
		return render(request,"get_top_records.html")
	else:
		return render(request,"main_page.html")

def top_records_response(request):
	#get data from html form
	no_records = request.POST['recnum']
	lang = request.POST['lang']
		
	cookie = request.COOKIES.get(no_records+'-'+lang)
	if(cookie == None):	
		dict_post = dict() #creating dict to pass to html
		
		#show api restriction error if user requests for records > 10
		if(int(no_records)>10):
			dict_post['max_issue'] = 'max 10 records will be displayed because of api restriction'
			
		dict_post['lang'] = lang
		dict_post['no_records'] = no_records
		url = "https://gnews.io/api/v4/top-headlines?token=" + token + "&max=" + no_records + "&lang=" + lang
		
		response = requests.request("GET",url)
		resp_j = json.dumps(response.text, ensure_ascii=False)
		response = eval(resp_j)
		response = json.loads(response)
		
		articles = list(response['articles'])
		
		dict_post['articles'] = articles
		
		response1 = render(request,"top_records_response.html",dict_post) #render html with data
		try:
			#creating caching-cookie if there is no decoding error.
			print(str(dict_post).encode('cp1252').decode('utf-8'))
			response1.set_cookie(no_records+'-'+lang,dict_post,max_age=90)
		except:
			pass
		return response1
	else:
		p = re.compile('(?<!\\\\)\'') #converting dict format to json format. replacing ' with "
		cookie = p.sub('\"', cookie)
		response = json.loads(cookie)
		return render(request,"top_records_response.html",response)

def search_records(request):
	cookie = request.COOKIES.get('auth')
	if(cookie != None):
		return render(request,"search_records.html")
	else:
		return render(request,"main_page.html")
	
def search_records_response(request):
	#get data from html form
	keyw = request.POST['keyw']
	search_type = request.POST['search_type']
	no_records = request.POST['recnum']
	lang = request.POST['lang']
	cookie = request.COOKIES.get(no_records+'-'+lang+'-'+search_type+'-'+keyw)
	if(cookie == None):	
		dict_post = dict() #creating dict to pass to html
		
		#show api restriction error if user requests for records > 10
		if(int(no_records)>10):
			dict_post['max_issue'] = 'max 10 records will be displayed because of api restriction'
			
		dict_post['keyw'] = keyw
		dict_post['search_type'] = search_type
		dict_post['no_records'] = no_records
		dict_post['lang'] = lang
		
		url = "https://gnews.io/api/v4/search?q=" + keyw + "&in=" + search_type + "&token=" + token + "&max=" + no_records + "&lang=" + lang

		response = requests.request("GET",url)
		resp_j = json.dumps(response.text, ensure_ascii=False)
		response = eval(resp_j)
		response = json.loads(response)
		
		articles = list(response['articles'])
		
		dict_post['articles'] = articles
		response1 = render(request,"search_records_response.html",dict_post) #render html with data
		try:
			#creating caching-cookie if there is no decoding error.
			print(str(dict_post).encode('cp1252').decode('utf-8'))
			response1.set_cookie(no_records+'-'+lang+'-'+search_type+'-'+keyw,dict_post,max_age=90)
		except:
			pass
		return response1
	else:
		p = re.compile('(?<!\\\\)\'') #converting dict format to json format. replacing ' with "
		cookie = p.sub('\"', cookie)
		response = json.loads(cookie)
		return render(request,"search_records_response.html",response)
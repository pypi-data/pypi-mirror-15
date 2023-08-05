#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
filters.py

Filtering utility library

Created by SWS on 2013-01-03.
Copyright (c) 2012 StoneWorkSolutions. All rights reserved.
'''

from datetime import date,datetime, timedelta
from django.utils.translation import ugettext_lazy as _ # Internacionalization
from sws_tags.sws_utils import json_encode
from math import ceil
import time
import copy
import re
from decimal import *
import types
from sws_tags.sws_utils.date import *
import django_mobile
from stoneauth.scripts.stoneauth_utils import getSystemTimezone


def connectedDevice(request):

	DEFAULT_DEVICE=(
		('iphone','mobile'),
		('ipad','mobile'),
		('android','mobile'),
		('winphone7','mobile'),
		('winmo','mobile'),
		('other','full'),
		)
	device = {}

	ua = request.META.get('HTTP_USER_AGENT', '').lower()
	
	if ua.find("iphone") > 0:
		device['iphone'] = "iphone" + re.search("iphone os (\d)", ua).groups(0)[0]
		
	if ua.find("ipad") > 0:
		device['ipad'] = "ipad"
		
	if ua.find("android") > 0:
		device['android'] = "android" + re.search("android (\d\.\d)", ua).groups(0)[0].translate(None, '.')
		
	if ua.find("blackberry") > 0:
		device['blackberry'] = "blackberry"
		
	if ua.find("windows phone os 7") > 0:
		device['winphone7'] = "winphone7"
		
	if ua.find("iemobile") > 0:
		device['winmo'] = "winmo"
		
	if not device:          # either desktop, or something we don't care about.
		device['other'] = "other"
	
	# spits out device names for CSS targeting, to be applied to <html> or <body>.
	device['classes'] = " ".join(v for (k,v) in device.items())
	
	select_default = ('other','full','full')
	for d in DEFAULT_DEVICE:
		if device['classes'].find(d[0])>=0:
			select_default = (d[0],d[1],device['classes'])

	return select_default


def InterfaceType(request):
	# select value default for first load 
	connected_device = connectedDevice(request)
	if 'interface_type' not in request.session:
		if connected_device[1] =='mobile':
			django_mobile.set_flavour('mobile',permanent=True)
		else:
			django_mobile.set_flavour('full',permanent=True)

	flavour = django_mobile.get_flavour(request)

	if flavour == "full":
		request.session['interface_type'] = 'normal'
	else:
		request.session['interface_type'] = 'simple'
		# logger.debug("Setting interface type to simple, mobile device detected")

def profileField(filters,user,interface_type):
	# if  not simple interface show all interface normal
	interface_simple = False
	list_filters=[]


	if len(filters[0])==3:
		for f in filters:
			view_type = f[2]
			if view_type[1] == 'S':
				interface_simple = True
		if interface_simple != True:
			interface_type = 'normal'

		for f in filters:
			user_view_type = f[2]
			type_user = user_view_type[0]
			type_view = user_view_type[1]

			if interface_type == 'normal':
				if user == 'admins':
					list_filters.append(f[0:2]) 
				elif user == 'superresellers' and  type_user != 'A':
					list_filters.append(f[0:2])
				elif user == 'resellers' and  (type_user == 'R' or type_user == 'C') :
					list_filters.append(f[0:2])
				elif user == 'clients' and type_user == 'C':
					list_filters.append(f[0:2])
			else:
				if type_view=='S':
					if user == 'admins':
						list_filters.append(f[0:2]) 
					elif user == 'superresellers' and  type_user != 'A':
						list_filters.append(f[0:2])
					elif user == 'resellers' and  (type_user == 'R' or type_user == 'C') :
						list_filters.append(f[0:2])
					elif user == 'clients' and type_user == 'C':
						list_filters.append(f[0:2])
		return list_filters

	elif len(filters[0])==4:
		for f in filters:
			view_type = f[3]
			if view_type[1] == 'S':
				interface_simple = True
		if interface_simple != True:
			interface_type = 'normal'

		for f in filters:
			user_view_type = f[3]
			type_user = user_view_type[0]
			type_view = user_view_type[1]

			if interface_type == 'normal':
				if user == 'admins':
					list_filters.append(f[0:3]) 
				elif user == 'superresellers' and  type_user != 'A':
					list_filters.append(f[0:3])
				elif user == 'resellers' and  (type_user == 'R' or type_user == 'C') :
					list_filters.append(f[0:3])
				elif user == 'clients' and type_user == 'C':
					list_filters.append(f[0:3])
			else:
				if type_view=='S':
					if user == 'admins':
						list_filters.append(f[0:3]) 
					elif user == 'superresellers' and  type_user != 'A':
						list_filters.append(f[0:3])
					elif user == 'resellers' and  (type_user == 'R' or type_user == 'C') :
						list_filters.append(f[0:3])
					elif user == 'clients' and type_user == 'C':
						list_filters.append(f[0:3])
		return list_filters


	else:

		for f in filters:
			view_type = f[1]
			if view_type[1] == 'S':
				interface_simple = True
		if interface_simple != True:
			interface_type = 'normal'

		for f in filters:
			user_view_type = f[1]
			type_user = user_view_type[0]
			type_view = user_view_type[1]

			if interface_type == 'normal':
				if user == 'admins':
					list_filters.append(f[0]) 
				elif user == 'superresellers' and  type_user != 'A':
					list_filters.append(f[0])
				elif user == 'resellers' and  (type_user == 'R' or type_user == 'C') :
					list_filters.append(f[0])
				elif user == 'clients' and type_user == 'C':
					list_filters.append(f[0])
			else:
				if type_view=='S':
					if user == 'admins':
						list_filters.append(f[0]) 
					elif user == 'superresellers' and  type_user != 'A':
						list_filters.append(f[0])
					elif user == 'resellers' and  (type_user == 'R' or type_user == 'C') :
						list_filters.append(f[0])
					elif user == 'clients' and type_user == 'C':
						list_filters.append(f[0])
		return list_filters


def profileFieldExclusive(filters,user,interface_type):
	# if  not simple interface show all interface normal
	interface_simple = False
	list_filters=[]


	if len(filters[0])==3:
		for f in filters:
			view_type = f[2]
			if view_type[1] == 'S':
				interface_simple = True
		if interface_simple != True:
			interface_type = 'normal'

		for f in filters:
			user_view_type = f[2]
			type_user = user_view_type[0]
			type_view = user_view_type[1]
			type_restriction = 'F'
			if len(user_view_type)==3:
				type_restriction = user_view_type[2]

			if interface_type == 'normal':
				if user == 'admins':
					if type_user == 'A':
						list_filters.append(f[0:2]) 
					elif type_restriction !='E':
						list_filters.append(f[0:2])  

				elif user == 'superresellers' and  type_user != 'A':
					if type_user == 'S':
						list_filters.append(f[0:2]) 

					elif type_restriction !='E':
						list_filters.append(f[0:2]) 


				elif user == 'resellers' and  (type_user == 'R' or type_user == 'C') :
					if type_user == 'R':
						list_filters.append(f[0:2]) 
					elif type_restriction!='E':
						list_filters.append(f[0:2]) 
						
				elif user == 'clients' and type_user == 'C':
					list_filters.append(f[0:2]) 
			else:
				if type_view=='S':
					if user == 'admins':
						if type_user == 'A':
							list_filters.append(f[0:2]) 
						elif type_restriction !='E':
							list_filters.append(f[0:2])  

					elif user == 'superresellers' and  type_user != 'A':
						if type_user == 'S':
							list_filters.append(f[0:2]) 
						elif type_restriction !='E':
							list_filters.append(f[0:2]) 

					elif user == 'resellers' and  (type_user == 'R' or type_user == 'C') :
						if type_user == 'R':
							list_filters.append(f[0:2]) 
						elif type_restriction!='E':
							list_filters.append(f[0:2]) 
							
					elif user == 'clients' and type_user == 'C':
						list_filters.append(f[0:2]) 
		return list_filters

	else:

		for f in filters:
			view_type = f[1]
			if view_type[1] == 'S':
				interface_simple = True
		if interface_simple != True:
			interface_type = 'normal'

		for f in filters:
			user_view_type = f[1]
			type_user = user_view_type[0]
			type_view = user_view_type[1]
			type_restriction = 'F'
			if len(user_view_type)==3:
				type_restriction = user_view_type[2]


			if interface_type == 'normal':
				if user == 'admins':
					if type_user == 'A':
						list_filters.append(f[0])
					elif type_restriction !='E':
						list_filters.append(f[0]) 

				elif user == 'superresellers' and  type_user != 'A':
					if type_user == 'S':
						list_filters.append(f[0])
					elif type_restriction !='E':
						list_filters.append(f[0])

				elif user == 'resellers' and  (type_user == 'R' or type_user == 'C') :
					if type_user == 'R':
						list_filters.append(f[0])
					elif type_restriction!='E':
						list_filters.append(f[0])

				elif user == 'clients' and type_user == 'C':
					list_filters.append(f[0])
			else:
				if type_view=='S':
					if user == 'admins':
						if type_user == 'A':
							list_filters.append(f[0]) 
						elif type_restriction !='E':
							list_filters.append(f[0]) 
					elif user == 'superresellers' and  type_user != 'A':
						if type_user == 'S':
							list_filters.append(f[0])
						elif type_restriction !='E':
							list_filters.append(f[0])
					elif user == 'resellers' and  (type_user == 'R' or type_user == 'C') :
						if type_user == 'R':
							list_filters.append(f[0])
						elif type_restriction!='E':
							list_filters.append(f[0])
					elif user == 'clients' and type_user == 'C':
						list_filters.append(f[0])
		return list_filters


def requestGet(name,request):
	if name in request.GET:
		return request.GET[name]
	else:
		return 'NULL'


def normalizeData(x):
	if x == '':
		return 'NULL'
	elif x == 'true':
		return True
	elif x == 'false':
		return False
	return x


#update the request_data dictionary with the values of request.GET
def reloadRequest(request_data,request,var_settins,filters=None): 

	request_data['var_settins'] = var_settins 
	
	request_data['system_timezone']=getSystemTimezone()
	
	try:
		request_data['django_timezone'] = request.session['django_timezone'] 
	except KeyError:
		request_data['django_timezone'] = request_data['system_timezone']

		
	if filters != None:
		uploadRequestFilters(request_data,filters) 

	request_data ['previous'] = -1
	for k,v in request.GET.iteritems():
		if k in map(lambda x: x[0][0], filters if filters else []):
			if ',' in request.GET[k]:
				request_data[k] = ('{0}__in'.format(k), [normalizeData(x) for x in request.GET[k].split(',')])
			else:
				request_data[k] = (k, normalizeData(request.GET[k]))
		else:
			request_data[k] = normalizeData(request.GET[k])

	if 'int_all_time' in request_data:
		if request_data['int_all_time']=='OFF':
			request_data['int_all_time'] = 0
		else:
			request_data['int_all_time'] =1

	if 'from_calldate' in request_data:
		request_data['from_Date'] = request_data['from_calldate']

	if 'to_calldate' in request_data:
		request_data['to_Date'] = request_data['to_calldate']

	if 'from_Date' in request_data:
		
		request_data['from_Date'] = strToDatetime(request_data['from_Date'])
		request_data['to_Date'] = strToDatetime(request_data['to_Date'])

		updateDateTz(request_data)

		request_data['from_Date'] = request_data['from_Date_tz']
		request_data['to_Date'] = request_data['to_Date_tz']

		if 'from_calldate' in request_data:
			request_data['from_calldate'] = request_data['from_Date']
			request_data['to_calldate'] = request_data['to_Date']


	if 'filter_selected' in request_data:
		request_data[request_data['filter_selected']] = (request_data['filter_selected'], 'NULL')

	if 'to_Date' in request_data:
		request_data['to_Date'] = request_data['to_Date'] +timedelta(microseconds=999999) 
		
	return request_data

def uploadRequestFilters(request_data,filters):       
	for f in filters:
		try:
			request_data[f[0]] = f[2]
		except:
			request_data[f[0]] = 'None'
   

def adjustTimeZone(queryset,tz_adjustement,date_fields):
	for n in queryset:
		for d in date_fields:
			if n[d]:
				n[d] = tzAdjustement(n[d],tz_adjustement)


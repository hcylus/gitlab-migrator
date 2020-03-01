# -*- coding: utf-8 -*-

import json,os,requests

class BaseApi(object):
	def __init__(self):
		super(BaseApi, self).__init__()

	def cache(self, name, data):
		cachepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'cache')
		if not os.path.exists(cachepath):
			os.makedirs(cachepath)
			
		with open(cachepath + '/%s.json' % name, 'w', encoding = 'UTF-8') as f:
			json.dump(data, f, sort_keys = False, indent = 2, ensure_ascii = False)

	def apiOperate(self, methods, api, config, **paramdata):
		if methods == 'get' or methods == 'GET':
			param = { 'per_page': config['per_page'], 'sort': 'asc' ,'order_by': 'id'}
			param.update(paramdata)
			#print(param)
			resp = requests.request( method = methods, url = api % config['address'],
				headers = config['headers'], params = param)
		elif methods == 'post' or methods == 'POST':
			resp = requests.request( method = methods, url = api % config['address'],
				headers = config['headers'], data = paramdata)
		else:
			return "method Error"	

		return resp
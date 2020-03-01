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

	def apiOperate(self, api,config,**params):
		param = { 'per_page': config['per_page'], 'sort': 'asc' ,'order_by': 'id'}
		param.update(params)
		print(param)
		resp = requests.get(api % config['address'],
			headers = config['headers'], params = param)

		return resp
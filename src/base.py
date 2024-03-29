# -*- coding: utf-8 -*-

import json,os,requests
from functools import partial

#展开列表中的列表
#参考链接：https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
#https://blog.csdn.net/weixin_40539892/article/details/79103290
from itertools import chain

class BaseApi(object):
	def __init__(self,cfg):
		#super(BaseApi, self).__init__()
		super().__init__()
		self.api = 'http://%s/api/v4'
		self.source = cfg['source']
		self.target = cfg['target']
		self.rsync=cfg['rsync']

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
		elif methods == 'delete' or methods == 'DELETE':
			param = {}
			param.update(paramdata)
			#print(param)
			print(api % config['address'])
			resp = requests.request( method = methods, url = api % config['address'],
				headers = config['headers'], params = param)
		else:
			return "method Error"	

		return resp

	#默认list source资源
	def listResInfo(self, resname, url=None, rescfg=None):
		if rescfg is None:
			rescfg =  self.source
		if url is None:
			url =  self.api
		pre_resp = self.apiOperate('get', url, rescfg, page=1)
		total = pre_resp.headers['X-Total']
		page = int(pre_resp.headers['X-Total-Pages'])
		print(' %s total %d page' % (resname, page))

		if page > 1:
			'''
			此处本考虑使用map函数处理apiOperate循环，但暂未找到循环传入关键字参数的方法，于是改为使用partial函数来处理，
			即将关键字参数格式为字典，循环dict的value，通过**dict方式传入
			resp = list(map(lambda x:x.json(), list(map( self.apiOperate,
				page*([(self.api)]),page*[(self.source)],
				[ 'page={}'.format(x) for x in range(1,page+1) ] ))))
			'''
			# 实现http翻页，处理总条目数超过单页默认显示最大值
			apiOperate = partial(self.apiOperate, 'get', url, rescfg)
			resp = list(map(lambda x:x.json(), list(apiOperate(**{'page':x}) for x in range(1,page+1))))			
			res = list(chain(*resp))
		else:
			res = pre_resp.json()

		print(' Total %s %s ' % ( total, resname))

		return res	

	def inserts(self, source):
		pass	

	def run(self):
		resname = (self.api).split('/')[-1]
		source = self.listResInfo(resname)
		if self.rsync:
			target = self.inserts(source)
		else:
			target=[]
		resp = { 'source': source, 'target': target }
		self.cache(resname, resp)
		return resp

	#默认remove target资源
	def remove(self, resname, rescfg=None):
		if rescfg is None:
			rescfg =  self.target
		url = self.api +'/%s' % resname
		source = self.listResInfo(resname, url, self.target)
		for src in source:
			durl = '%s/%s' % (url, src['id'])
			if 'username' in src:
				if src['username'] != 'root':
					self.apiOperate('delete', durl, rescfg, hard_delete=True)
					print('delete %s: ' % resname, src['username'])
			else:
				self.apiOperate('delete', durl, rescfg)
				print('delete %s: ' % resname, src['name'])
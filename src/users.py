# -*- coding: utf-8 -*-

from base import BaseApi
from functools import partial

#展开列表中的列表
#参考链接：https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
#https://blog.csdn.net/weixin_40539892/article/details/79103290
from itertools import chain

base = BaseApi()

class Users(object):
	def __init__(self, cfg):
		super(Users, self).__init__()
		self.api = 'http://%s/api/v4/users'
		self.source = cfg['source']
		self.target = cfg['target']

	def run(self):
		source = self.get()
		target = self.inserts(source)

		return { 'source': source, 'target': target }

	def get(self):
		pre_resp = base.apiOperate('get', self.api, self.source, page=1)
		total = pre_resp.headers['X-Total']
		page = int(pre_resp.headers['X-Total-Pages'])

		if page > 1:
			print('user page: '+str(page))
			'''
			此处本考虑使用map函数处理apiOperate循环，但暂未找到循环传入关键字参数的方法，于是改为使用partial函数来处理，
			即将关键字参数格式为字典，循环dict的value，通过**dict方式传入
			resp = list(map(lambda x:x.json(), list(map( Baseapi().apiOperate,
				page*([(self.api)]),page*[(self.source)],
				[ 'page={}'.format(x) for x in range(1,page+1) ] ))))
			'''
			# 实现http翻页，处理总条目数超过单页默认显示最大值
			apiOperate = partial(base.apiOperate, 'get', self.api, self.source)
			resp = list(map(lambda x:x.json(), list(apiOperate(**{'page':x}) for x in range(1,page+1))))			
			users = list(chain(*resp))
		else:
			print('user page: 1')
			users = pre_resp.json()

		print('Source total users: %s' % total)

		return users

	def inserts(self, users):
		new_users = []
		exist_users = []
		target_users = []

		for user in users:
			uname = user['username']
			tresp = base.apiOperate('get', self.api, self.target, username=uname)
			tuser = tresp.json()
			if tuser:
				target_users.append(tuser[0])
				exist_users.append(tuser[0]['username'])
			else:
				data = {
					'admin': user.get('is_admin'),
					'can_create_group': user.get('can_create_group'),
					'email': user.get('email'),
					'external': user.get('external'),
					'name': user.get('name'),
					'organization': user.get('organization'),
					'password': 'hellouser',
					'projects_limit': user.get('projects_limit'),
					'username': user.get('username'),					
					'skip_confirmation': True
				}
				resp = base.apiOperate('post', self.api, self.target, **data)
				uresp = resp.json()
				target_users.append(uresp)
				new_users.append(uresp['username'])
				if user['state'] == 'blocked':
					uid = uresp['id']
					url = self.api + '/%s/block' % uid
					base.apiOperate('post', url, self.target,)

		print('Target exist %s user: ' % len(exist_users), *exist_users)			
		print('Target create %s new user: ' % len(new_users), *new_users)
		
		return target_users

# -*- coding: utf-8 -*-

from base import BaseApi

class Users(BaseApi):
	def __init__(self, cfg):
		#super(Users, self).__init__(cfg)
		super().__init__(cfg)
		self.api = 'http://%s/api/v4/users'


	#def run(self):
	#	super().run()

	def inserts(self, source):
		new_res = []
		exist_res = []
		target_res = []

		for src in source:
			sname = src['username']
			tresp = super().apiOperate('get', self.api, self.target, username=sname)
			tinfo = [ r for r in tresp.json() if sname == r['username'] ]
			if tinfo:
				target_res.append(tinfo[0])
				exist_res.append(tinfo[0]['username'])
			else:
				data = {
					'admin': src.get('is_admin'),
					'can_create_group': src.get('can_create_group'),
					'email': src.get('email'),
					'external': src.get('external'),
					'name': src.get('name'),
					'organization': src.get('organization'),
					'password': 'hellouser',
					'projects_limit': src.get('projects_limit'),
					'username': src.get('username'),					
					'skip_confirmation': True
				}
				resp = super().apiOperate('post', self.api, self.target, **data)
				cresp = resp.json()
				target_res.append(cresp)
				new_res.append(cresp['username'])
				if src['state'] == 'blocked':
					uid = cresp['id']
					url = self.api + '/%s/block' % uid
					super().apiOperate('post', url, self.target,)

		print('Target exist %s users: ' % len(exist_res), *exist_res)			
		print('Target create %s new users: ' % len(new_res), *new_res)
		
		return target_res


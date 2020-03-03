# -*- coding: utf-8 -*-

from base import BaseApi

class Projects(BaseApi):
	def __init__(self, cfg, users, groups):
		super().__init__(cfg)
		self.api = 'http://%s/api/v4/projects'
		self.target_users = users['target']
		self.target_groups = groups['target']

	def inserts(self, source):
		new_res = []
		exist_res = []
		target_res = []

		for src in source:
			sname = src['name']
			tresp = super().apiOperate('get', self.api, self.target, search=sname)
			tinfo = [ r for r in tresp.json() if src['path_with_namespace'] == r['path_with_namespace'] ]
			if tinfo:
				target_res.append(tinfo[0])
				exist_res.append(tinfo[0]['path_with_namespace'])
			else:
				kind = src['namespace']['kind']
				if kind == 'group':
					tinfo = next((x for x in self.target_groups if x['name'] == src['namespace']['name']), '')
					if tinfo:
						data = {
							"name": src['name'],
							"path": src['path'],
							"namespace_id": tinfo['id'],
							"description": src['description'],
							"visibility": src['visibility'],
							"lfs_enabled": src['lfs_enabled']
						}
						url = self.api
				elif kind == 'user':
					tinfo = next((x for x in self.target_users if x['username'] == src['namespace']['name']), '')
					if tinfo:
						data = {
							"name": src['name'],
							"path": src['path'],
							"user_id": tinfo['id'],
							"description": src['description'],
							"visibility": src['visibility'],
							"lfs_enabled": src['lfs_enabled']
						}
						url = self.api + '/user/%s' % tinfo['id']

				resp = super().apiOperate('post', url, self.target, **data)
				cresp = resp.json()
				target_res.append(cresp)
				new_res.append(src['path_with_namespace'])
						
		print('Target exist %s projects: ' % len(exist_res), *exist_res)			
		print('Target create %s new projects: ' % len(new_res), *new_res)

		return target_res

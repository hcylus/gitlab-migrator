# -*- coding: utf-8 -*-

from base import BaseApi

class Groups(BaseApi):
	def __init__(self, cfg):
		super().__init__(cfg)
		self.api = 'http://%s/api/v4/groups'

	#def run(self):
	#	super().run()

	def inserts(self, source):
		new_res = []
		exist_res = []
		target_res = []

		for src in source:
			sname = src['name']
			tresp = super().apiOperate('get', self.api, self.target, search=sname)
			tinfo = [ r for r in tresp.json() if sname == r['name'] ]
			if tinfo:
				target_res.append(tinfo[0])
				exist_res.append(tinfo[0]['name'])
			else:
				data = {
				"name": src['name'],
				"path": src['path'],
				"description": src['description'],
				"visibility": src['visibility'],
				"lfs_enabled": src['lfs_enabled'],
				"request_access_enabled": src['request_access_enabled'],
				"parent_id": src['parent_id']
				}
				resp = super().apiOperate('post', self.api, self.target, **data)
				cresp = resp.json()
				target_res.append(cresp)
				new_res.append(cresp['name'])
				
		print('Target exist %s groups: ' % len(exist_res), *exist_res)			
		print('Target create %s new groups: ' % len(new_res), *new_res)
		
		return target_res
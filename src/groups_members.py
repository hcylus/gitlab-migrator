# -*- coding: utf-8 -*-

from base import BaseApi

class GroupsMembers(BaseApi):
	def __init__(self, cfg, users, groups):
		super().__init__(cfg)
		self.api = 'http://%s/api/v4/groups/%s/members'
		self.users = users
		self.groups = groups

	def listResInfo(self, resname):
		if resname == (self.api).split('/')[-1]:
			resname = self.groups['source']
			config = self.source
		else:
			resname = self.groups['target']
			config = self.target	
		
		resp = {}
		for res in resname:
			url = self.api % ('%s', res['id'])
			apiOperate = super().apiOperate('get', url, config)
			resp[res['name']] = apiOperate.json()
		
		return resp	
		
	def index(self):
		target_groups = self.groups['target']
		target_users = self.users['target']
		source_groups = self.groups['source']

		mem = {}
		for group in source_groups:
			tgroup = next((x for x in target_groups if x['name'] == group['name']), '')
			#group-members以source为基础，即只查询和添加source对应的target组成员
			if tgroup:
				mem[tgroup['name']] = {}
				url = self.api % ('%s', group['id'])
				resp = super().apiOperate('get', url, self.source)
				source_members = resp.json()
				for m in source_members:
					tm = next((x for x in target_users if x['username'] == m['username']), '')
					if tm:
						mem[tgroup['name']][tm['username']] = {
							'id': tgroup['id'],
							'user_id': tm['id'],
							'access_level': m['access_level']
						}

		return mem

	def inserts(self, source):
		members = self.index()
		mem = {}
		for k,v in members.items():
			mem[k] = []
			for subk,subv in v.items():
				url = (self.api +'/%s' % subv['user_id']) % ('%s', subv['id'])
				resp = super().apiOperate('get', url, self.target)
				if not resp.ok:
					mem[k].append(subk)
					url = self.api % ('%s', subv['id'])
					super().apiOperate('post', url, self.target, **subv)

		for k,v in mem.items():
			if int(len(v)) > 0:
				print('Target group %s add %s members: ' % (k,len(v)),*v)
		
		print('group members rsync done')

		tresp = self.listResInfo('target')
		return tresp
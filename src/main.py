# -*- coding: utf-8 -*-

import os, sys, config,json
from users import Users
from groups import Groups
from groups_members import GroupsMembers
from projects import Projects
from repositories import Repositories
from clean import Clean

def execute(cfg):
	#cachepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'cache')
	
	users = Users(cfg).run()
	#with open(cachepath + '/users.json','r') as f:
	#	users = json.load(f)

	groups = Groups(cfg).run()
	#with open( cachepath + '/groups.json','r') as f:
	#	groups = json.load(f)
	
	members = GroupsMembers(cfg, users, groups).run()
	
	projects = Projects(cfg, users, groups).run()
	#with open( cachepath + '/projects.json','r') as f:
	#	projects = json.load(f)

	Repositories(cfg, projects).run()

if __name__ == '__main__':

	cfg = {
		'source': os.getenv('SOURCE', config.SOURCE),
		'target': os.getenv('TARGET', config.TARGET)
	}

	#print('Migrator configuration')
	for key in cfg:
		cfg[key]['headers'] = { 'PRIVATE-TOKEN': cfg[key]['access_token'] }
		cfg[key]['per_page'] = 100
		#print('%s:' % key)
		#print(cfg[key])

	# Clean(cfg)用于清理target端user、group、project谨慎启用	
	#Clean(cfg)

	execute(cfg)

# -*- coding: utf-8 -*-

from base import BaseApi
from git import Repo
import os

#可以使用Project import/export API实现导出导入
#此处考虑使用gitpython在本地保留一份source端源代码

class Repositories(BaseApi):
	def __init__(self, cfg, projects):
		super().__init__(cfg)
		self.api = 'http://oauth2:%s@%s'
		self.source_projects = projects['source']
		self.target_projects = projects['target']
		self.rsync=cfg['rsync']
		self.repodir = os.path.join(
			os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
			(self.source['address']).split(':')[0])

	def run(self):
		isContinue=False
		for project in self.source_projects:
			# v11版本请求响应里不含有empty_repo key
			if 'empty_repo' in project:
				if not project['empty_repo']:
					isContinue=True
			else:
				isContinue=True
					
			if isContinue:
				repopath = os.path.join(self.repodir, project['path_with_namespace'])
				surl = project['http_url_to_repo']
				url = self.api % (self.source['headers']['PRIVATE-TOKEN'], surl.split('://')[1])
				print(repopath)
				#print(url)
				if not os.path.exists(repopath):
					os.makedirs(repopath)
					barepath = os.path.join(repopath, '.git')
					print('Clone:', surl)
					repo = Repo.clone_from(url = url, to_path = barepath, bare = True)
					repo.config_writer().remove_option('core','bare')
					repo = Repo(repopath)
					repo.git.reset(hard = True)
				else:
					repo = Repo(repopath)
					# for rp in repo.remotes:
					# 	repo.delete_remote(rp)
					# if 'gitlab' in repo.remotes:
					# 	repo.delete_remote('gitlab')
						
					repo.remote().set_url(url,repo.remotes.origin.url)
					# repo.create_remote('origin', url)	
					print('Pull:', surl)
					repo.git.fetch(all = True)
					repo.git.fetch(tags = True)
					repo.git.reset(hard = True)
					repo.git.pull(all = True)
					repo.git.pull(tags = True)

				if self.rsync:
					turl = self.api % (self.target['headers']['PRIVATE-TOKEN'],
										surl.replace(self.source['address'],self.target['address']).split('://')[1])
					#print(turl)
					print('Push:', surl.replace(self.source['address'],self.target['address']))
					#print(repo.remotes)
					# for rp in repo.remotes:
					# 	repo.delete_remote(rp)
					#print(repo.remotes)
					repo.remote().set_url(turl,repo.remotes.origin.url)
					repo.push(all = True)
					repo.push(tags = True)
					# gitlab = repo.create_remote('origin', turl)
					# gitlab.push(all = True)
					# gitlab.push(tags = True)



# -*- coding: utf-8 -*-

from base import BaseApi

# 清除数据
class Clean(BaseApi):
	def __init__(self, cfg):
		super().__init__(cfg)
		
		super().remove('projects')
		super().remove('groups')
		super().remove('users')
		

if __name__ == '__main__':
	Clean()
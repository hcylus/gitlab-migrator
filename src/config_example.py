# -*- coding: utf-8 -*-

SOURCE = {
	'address': '127.0.0.1',
	'access_token': 'xxxxxxxxx',
}

TARGET = {
	'address': '127.0.0.2',
	'access_token': 'xxxxxxxxxxxxxxx'
}

#True：clone到本地并导入到TARGET仓库
#False：clone到本地不导入TARGET仓库
rsync=False
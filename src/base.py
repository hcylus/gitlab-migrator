# -*- coding: utf-8 -*-

import json,os

def storage(name, data):
	cachepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'cache')
	if not os.path.exists(cachepath):
		os.makedirs(cachepath)
		
	with open(cachepath + '/%s.json' % name, 'w', encoding = 'UTF-8') as f:
		json.dump(data, f, sort_keys = False, indent = 2, ensure_ascii = False)

import os

def relative(subpath='', useCwd=False):
	import os
	basePath = os.getcwd() if useCwd else os.path.dirname(os.path.abspath(__file__))
	return os.path.normpath(os.path.join(basePath, os.path.expanduser(subpath)))

def isEmpty(path):
	return os.listdir(relative(path)) == []
import os
from distutils.dir_util import copy_tree
from isDirectoryEmpty import isEmpty

def relative(subpath='', useCwd=False):
	import os
	basePath = os.getcwd() if useCwd else os.path.dirname(os.path.abspath(__file__))
	return os.path.normpath(os.path.join(basePath, os.path.expanduser(subpath)))

def fillEmpty(path, defaultContentsPath):
	if isEmpty(path):
		copy_tree(defaultContentsPath, path, preserve_symlinks=1)
		return True
	else:
		return False
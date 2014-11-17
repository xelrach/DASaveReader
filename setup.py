from distutils.core import setup
from sys import platform

is_windows = False
if platform == "win32":
	import py2exe
	is_windows = True

info = {
	'name' : 'DASaveReader',
	'version' : 'snapshot',
	'description' : 'Dragon Age Save Reader',
	'author' : 'Charles Noneman',
	'url' : 'https://github.com/xelrach/DASaveReader',
	'options' : {
		'py2exe': {
			'compressed': 1,
			'optimize': 1,
			'bundle_files': 2,
			'typelibs' : [("{EAB22AC0-30C1-11CF-A7EB-0000C05BAE0B}", 0, 1, 1)],
		}
	},
}

if is_windows:
	info['windows'] = [{"script": "da_reader_gui.py"}]

setup(**info)

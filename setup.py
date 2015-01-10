import sys
from distutils.core import setup
from sys import platform
from glob import glob

is_windows = False
if platform == "win32":
	import py2exe
	is_windows = True

VERSION = 'beta1'

VC_LOCATION = r''
GDI_LOCATION = r''

sys.path.append(VC_LOCATION)
sys.path.append(GDI_LOCATION)

info = { \
	'name' : 'DASaveReader', \
	'version' : VERSION, \
	'description' : 'Dragon Age Save Reader', \
	'author' : 'Charles Noneman', \
	'url' : 'https://github.com/xelrach/DASaveReader', \
	'packages' : ['pygff.gff4'], \
	'options' : { \
		'py2exe': { \
			'compressed': 1, \
			'optimize': 1, \
			'bundle_files': 2, \
			'typelibs' : [("{EAB22AC0-30C1-11CF-A7EB-0000C05BAE0B}", 0, 1, 1)], \
		} \
	}, \
}

if is_windows:
	info['windows'] = [{"script": "da_reader_gui.py"}]
	info['data_files'] = [("Microsoft.VC90.CRT", glob(VC_LOCATION + r'\*.*')), \
			("gdi", glob(GDI_LOCATION))]

setup(**info)

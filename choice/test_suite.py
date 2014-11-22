# Copyright 2014 Charles Noneman
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import inspect
import os
import pkgutil
import sys
import unittest

sys.path.insert(0, os.path.abspath('.'))

import choice

def run():
	subsuite_list = []
	for importer, modname, ispkg in pkgutil.iter_modules(choice.__path__):
		if modname.startswith("test_") and modname != "test_suite":
			module = __import__(modname)
			subsuite = unittest.TestLoader().loadTestsFromModule(module)
			subsuite_list.append(subsuite)
	suite = unittest.TestSuite(subsuite_list)

	print("Testing:\n")
	unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
	run()

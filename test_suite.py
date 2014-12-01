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

"""Test suite for running the test modules"""

import importlib
import pkgutil
import unittest
import choice

def run():
	subsuite_list = []
	for _, modname, _ in pkgutil.iter_modules(choice.__path__):
		if modname.startswith("test_"):
			module = importlib.import_module('choice.' + modname)
			subsuite = unittest.TestLoader().loadTestsFromModule(module)
			subsuite_list.append(subsuite)
	suite = unittest.TestSuite(subsuite_list)

	print("Testing:\n")
	unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
	run()

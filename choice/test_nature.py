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

import unittest

from nature import nature_of_the_beast
import quest_guid

class nature_test(unittest.TestCase):
	def test_nature_of_the_beast_elves(self):
		data = {}
		flags = 2**nature_of_the_beast.ELF_FLAG
		data[quest_guid.NATURE_OF_THE_BEAST] = flags

		response = nature_of_the_beast.get_result(data)

		self.assertEquals(nature_of_the_beast.ELVES, response.result)

	def test_nature_of_the_beast_werewolves(self):
		data = {}
		flags = 2**nature_of_the_beast.WEREWOLF_FLAG
		data[quest_guid.NATURE_OF_THE_BEAST] = flags

		response = nature_of_the_beast.get_result(data)

		self.assertEquals(nature_of_the_beast.WEREWOLVES, response.result)

	def test_nature_of_the_beast_peace(self):
		data = {}
		flags = 2**nature_of_the_beast.ELF_FLAG | 2**nature_of_the_beast.ZATHRIAN_FLAG
		data[quest_guid.NATURE_OF_THE_BEAST] = flags

		response = nature_of_the_beast.get_result(data)

		self.assertEquals(nature_of_the_beast.PEACE, response.result)


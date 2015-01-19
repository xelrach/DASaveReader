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

import choice.companions as companions
import choice.plot as plot
import choice.quest_guid as quest_guid

class companions_test(unittest.TestCase):
	def test_sten_free_no(self):
		mine = [65644, 0, 0, 0]

		data = {}
		data[quest_guid.THE_QUNARI_PRISONER] = plot.plot(*mine)

		response = companions.sten_free.get_result(data)

		self.assertEquals(companions.sten_free.NOT_FREED, response.result)

	def test_morrigan_baby_no(self):
		mine = [98307, 0, 0, 0]

		data = {}
		data[quest_guid.THE_QUNARI_PRISONER] = plot.plot(*mine)

		response = companions.morrigan_baby.get_result(data)

		self.assertEquals(companions.morrigan_baby.NO, response.result)

	def test_sten_sword_returned(self):
		mine = [1581568, 0, 0, 0]

		data = {}
		data[quest_guid.STEN_SWORD] = plot.plot(*mine)

		response = companions.sten_sword.get_result(data)

		self.assertEquals(companions.sten_sword.YES, response.result)

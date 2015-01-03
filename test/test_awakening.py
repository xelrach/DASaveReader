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

from choice.awakening import felsi
import choice.plot as plot
import choice.quest_guid as quest_guid

class awakening_test(unittest.TestCase):
	def test_felsi_skip(self):
		oghren_mine = [39, 0, 0, 0]
		family_mine = [1708, 0, 0, 0]

		data = {}
		data[quest_guid.OGHREN] = plot.plot(*oghren_mine)
		data[quest_guid.FAMILY_MAN] = plot.plot(*family_mine)

		response = felsi.get_result(data)

		self.assertEquals(felsi.NOTHING, response.result)

	def test_felsi_family(self):
		oghren_mine = [47, 0, 0, 0]
		family_mine = [9964, 0, 0, 0]

		data = {}
		data[quest_guid.OGHREN] = plot.plot(*oghren_mine)
		data[quest_guid.FAMILY_MAN] = plot.plot(*family_mine)

		response = felsi.get_result(data)

		self.assertEquals(felsi.YES, response.result)

	def test_felsi_no_family(self):
		oghren_mine = [39, 0, 0, 0]
		family_mine = [9964, 0, 0, 0]

		data = {}
		data[quest_guid.OGHREN] = plot.plot(*oghren_mine)
		data[quest_guid.FAMILY_MAN] = plot.plot(*family_mine)

		response = felsi.get_result(data)

		self.assertEquals(felsi.NO, response.result)

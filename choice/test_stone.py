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

from stone import amalia_fate
import plot
import quest_guid

class stone_test(unittest.TestCase):
	def test_amalia_fate_both_alive(self):
		mine = [4044605670, 177, 0, 0]
		destaerie = [4043427022, 185, 0, 0]
		felther = [4043426022, 185, 0, 0]
		starelle = [4043427022, 177, 0, 0]

		characters = [mine, destaerie, felther, starelle]

		for flags in characters:
			data = {}
			data[quest_guid.GOLEM] = plot.plot(*flags)

			response = amalia_fate.get_result(data)

			self.assertEquals(amalia_fate.BOTH_ALIVE, response.result)


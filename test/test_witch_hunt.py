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

from choice.witch_hunt import witch_hunt
import choice.plot as plot
import choice.quest_guid as quest_guid

class witch_hunt_test(unittest.TestCase):
	def test_witch_hunt_stay(self):
		mine = [1, 0, 0, 0]

		data = {}
		data[quest_guid.MORRIGAN_ELUVIAN] = plot.plot(*mine)

		response = witch_hunt.get_result(data)

		self.assertEquals(witch_hunt.NO, response.result)

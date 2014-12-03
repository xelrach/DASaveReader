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

from choice.urn import urn
import choice.plot as plot
import choice.quest_guid as quest_guid

class urn_test(unittest.TestCase):
	def test_urn_safe(self):
		mine = [32, 0, 0, 0]

		data = {}
		data[quest_guid.THE_HIGH_DRAGONS_CHAMPION] = plot.plot(*mine)

		response = urn.get_result(data)

		self.assertEquals(urn.NOT_POISONED, response.result)

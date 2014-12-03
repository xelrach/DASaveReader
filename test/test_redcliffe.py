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

from choice.redcliffe import prepare, fight
import choice.plot as plot
import choice.quest_guid as quest_guid

class recliff_test(unittest.TestCase):
	def test_prepare_yes(self):
		mine = [35659947, 0, 0, 0]

		data = {}
		data[quest_guid.A_VILLAGE_UNDER_SIEGE] = plot.plot(*mine)

		response = prepare.get_result(data)

		self.assertEquals(prepare.YES, response.result)

	def test_fight_yes(self):
		mine = [2795782181, 671, 0, 0]

		data = {}
		data[quest_guid.THE_ATTACK_AT_NIGHTFALL] = plot.plot(*mine)

		response = fight.get_result(data)

		self.assertEquals(fight.YES, response.result)

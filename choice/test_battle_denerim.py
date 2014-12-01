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

from choice.battle_denerim import battle_denerim
import choice.companion.fate as fate
import choice.plot as plot
import choice.quest_guid as quest_guid

class battle_denerim_test(unittest.TestCase):
	def test_battle_denerim_alistair(self):
		mine = [196, 0, 0, 0]

		data = {}
		data[quest_guid.CLIMAX_ARCHDEMON] = plot.plot(*mine)

		response = battle_denerim.get_result(data)

		self.assertEquals(battle_denerim.ALISTAIR, response.result)

	def test_battle_denerim_warden(self):
		lyna = [208, 0, 0, 0]

		data = {}
		data[quest_guid.CLIMAX_ARCHDEMON] = plot.plot(*lyna)

		response = battle_denerim.get_result(data)

		self.assertEquals(battle_denerim.WARDEN, response.result)

	def test_battle_denerim_loghain(self):
		flags = 2**fate.LOGHAIN_KILL_FLAG

		data = {}
		data[quest_guid.CLIMAX_ARCHDEMON] = plot.plot(flags)

		response = battle_denerim.get_result(data)

		self.assertEquals(battle_denerim.LOGHAIN, response.result)

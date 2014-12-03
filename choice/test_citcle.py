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

from choice.circle import broken_circle, irving, cullen
import choice.plot as plot
import choice.quest_guid as quest_guid

class circle_test(unittest.TestCase):
	def test_broken_circle_mages(self):
		mine = [4032342447, 406428, 0, 0]

		data = {}
		data[quest_guid.BROKEN_CIRCLE] = plot.plot(*mine)

		response = broken_circle.get_result(data)

		self.assertEquals(broken_circle.MAGES, response.result)

	def test_broken_circle_templars(self):
		flags = 2**broken_circle.TEMPLAR_FLAG

		data = {}
		data[quest_guid.BROKEN_CIRCLE] = plot.plot(flags)

		response = broken_circle.get_result(data)

		self.assertEquals(broken_circle.TEMPLARS, response.result)

	def test_irving_alive(self):
		mine = [14, 0, 0, 0]

		data = {}
		data[quest_guid.CODEX_IRVING] = plot.plot(*mine)

		response = irving.get_result(data)

		self.assertEquals(irving.ALIVE, response.result)

	def test_irving_dead(self):
		flags = 2**irving.IRVING_DEAD_FLAG

		data = {}
		data[quest_guid.CODEX_IRVING] = plot.plot(flags)

		response = irving.get_result(data)

		self.assertEquals(irving.DEAD, response.result)

	def test_cullen_no(self):
		mine = [4032342447, 406428, 0, 0]
		agree_but_not_killed = [2**cullen.AGREED_FLAG]

		for character in [mine, agree_but_not_killed]:
			data = {}
			data[quest_guid.BROKEN_CIRCLE] = plot.plot(*character)

			response = cullen.get_result(data)

			self.assertEquals(cullen.NO, response.result)

	def test_cullen_yes(self):
		flags = 2**cullen.AGREED_FLAG | 2**cullen.MAGES_DEAD_FLAG

		data = {}
		data[quest_guid.BROKEN_CIRCLE] = plot.plot(flags)

		response = cullen.get_result(data)

		self.assertEquals(cullen.YES, response.result)

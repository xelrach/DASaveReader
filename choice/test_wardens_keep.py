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

import quest_guid
import plot
import wardens_keep

class wardens_keep_test(unittest.TestCase):
	MY_AVERNUS_FLAGS = 9334414
	MY_SOPHIA_FLAGS = 3778019584

	def test_soldiers_peak_mine(self):
		data = {}
		data[quest_guid.CHARACTER_AVERNUS] = plot.plot(wardens_keep_test.MY_AVERNUS_FLAGS)
		data[quest_guid.CHARACTER_SOPHIA] = plot.plot(wardens_keep_test.MY_SOPHIA_FLAGS)

		response = wardens_keep.soldiers_peak.get_result(data)

		self.assertEquals(wardens_keep.soldiers_peak.GOOD_RESEARCH, response.result)


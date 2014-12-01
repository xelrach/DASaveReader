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

import choice.plot as plot
import choice.quest_guid as quest_guid
import choice.companion.recruit as recruit

class recruit_test(unittest.TestCase):
	MY_PARTY_FLAGS = 134874067

	def test_alistair_recruited(self):
		data = {}
		data[quest_guid.PARTY] = plot.plot(recruit_test.MY_PARTY_FLAGS)

		value = recruit.alistair_recruited(data)

		self.assertEquals(True, value)

	def test_dog_recruited(self):
		data = {}
		data[quest_guid.PARTY] = plot.plot(recruit_test.MY_PARTY_FLAGS)

		value = recruit.dog_recruited(data)

		self.assertEquals(True, value)

	def test_leliana_recruited(self):
		data = {}
		data[quest_guid.PARTY] = plot.plot(recruit_test.MY_PARTY_FLAGS)

		value = recruit.leliana_recruited(data)

		self.assertEquals(True, value)

	def test_oghren_recruited(self):
		data = {}
		data[quest_guid.PARTY] = plot.plot(recruit_test.MY_PARTY_FLAGS)

		value = recruit.oghren_recruited(data)

		self.assertEquals(True, value)

	def test_shale_recruited(self):
		data = {}
		data[quest_guid.PARTY] = plot.plot(recruit_test.MY_PARTY_FLAGS)

		value = recruit.shale_recruited(data)

		self.assertEquals(True, value)

	def test_wynne_recruited(self):
		data = {}
		data[quest_guid.PARTY] = plot.plot(recruit_test.MY_PARTY_FLAGS)

		value = recruit.wynne_recruited(data)

		self.assertEquals(True, value)

	def test_zevran_recruited(self):
		data = {}
		data[quest_guid.PARTY] = plot.plot(recruit_test.MY_PARTY_FLAGS)

		value = recruit.zevran_recruited(data)

		self.assertEquals(True, value)

	def test_loghain_recruited(self):
		data = {}
		data[quest_guid.PARTY] = plot.plot(recruit_test.MY_PARTY_FLAGS)

		value = recruit.loghain_recruited(data)

		self.assertEquals(False, value)

	def test_sten_recruited(self):
		data = {}
		data[quest_guid.PARTY] = plot.plot(recruit_test.MY_PARTY_FLAGS)

		value = recruit.sten_recruited(data)

		self.assertEquals(False, value)

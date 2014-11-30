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

"""Stone Prisoner choices"""

import quest_guid
import recruit
import result
import responses
from utils import has_flag, get_plot

class shale_recruit:
	ORDER = 2
	TITLE = "Did the Warden recruit Shale?"

	NO = "Shale not recruited"
	YES = "Shale recruited"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(shale_recruit.ORDER, shale_recruit.TITLE)

		if recruit.shale_recruited(data):
			response.result = shale_recruit.YES
		else:
			response.result = shale_recruit.NO

		return response

class shale_fate:
	ORDER = 0
	TITLE = "What happened to Shale?"

	ATTACK_FLAG = 9
	DEAD_FLAG = 4

	NO_RECRUIT = "Didn't recruit Shale"
	ALIVE = "Shale is alive and well"
	DIED = "Shale died when the Warden sided with Branka"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(shale_fate.ORDER, shale_fate.TITLE)

		shale_data = get_plot(data, quest_guid.SHALE_ANVIL)
		codex_data = get_plot(data, quest_guid.CODEX_SHALE)

		if recruit.shale_recruited(data):
			if has_flag(shale_data, shale_fate.ATTACK_FLAG) \
					or has_flag(codex_data, shale_fate.DEAD_FLAG):
				response.result = shale_fate.DIED
			else:
				response.result = shale_fate.ALIVE
		else:
			response.result = shale_fate.NO_RECRUIT

		return response

class amalia_fate:
	ORDER = 1
	TITLE = "What was the fate of Kitty and Amalia?"

	MATTHIAS_DEAD_FLAG = 0
	BOTH_FREE_FLAG = 24
	AMALIA_POSSESSED_FLAG = 25
	MATTHIAS_ALONE_FLAG = 26
	MATTHIAS_POSSESSED_FLAG = 27

	BOTH_ALIVE = "Matthias and Amalia both alive, neither possessed"
	AMALIA_POSSESSED = "Matthias and Amalia both alive, Amalia possessed"
	MATTHIAS_POSSESSED = "Matthias and Amalia both alive, Matthias possessed"
	MATTHIAS_DEAD = "Amalia is alive, Matthias is dead"
	AMALIA_DEAD = "Amalia is dead, Matthias is alive"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(amalia_fate.ORDER, amalia_fate.TITLE)

		quest_data = get_plot(data, quest_guid.GOLEM)

		if has_flag(quest_data, amalia_fate.BOTH_FREE_FLAG):
			response.result = amalia_fate.BOTH_ALIVE
		elif has_flag(quest_data, amalia_fate.AMALIA_POSSESSED_FLAG):
			response.result = amalia_fate.AMALIA_POSSESSED
		elif has_flag(quest_data, amalia_fate.MATTHIAS_ALONE_FLAG):
			response.result = amalia_fate.AMALIA_DEAD
		elif has_flag(quest_data, amalia_fate.MATTHIAS_POSSESSED_FLAG):
			response.result = amalia_fate.MATTHIAS_POSSESSED
		elif has_flag(quest_data, amalia_fate.MATTHIAS_DEAD_FLAG):
			response.result = amalia_fate.MATTHIAS_DEAD
		else:
			response.result = result.DEFAULT

		return response

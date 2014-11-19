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

"""Warden's Keep choices"""

import quest_guid
import result
import responses
from utils import has_flag, get_plot

class soldiers_peak:
	ORDER = 1
	TITLE = "How did the Warden deal with Avernus?"

	GOOD_FLAG = 3
	BAD_FLAG = 5
	AVERNUS_DEAD_FLAG = 20
	SOPHIA_DEAD_FLAG = 20

	BOTH_DEAD = "Both Sophia and Avernus perished"
	AVERNUS_DEAD = "Slayed Avernus"
	BAD_RESEARCH = "Slayed Sophia and Avernus continued research"
	GOOD_RESEARCH = "Slayed Sophia and allowed Avernus ethical research"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(soldiers_peak.ORDER, soldiers_peak.TITLE)

		avernus_data = get_plot(data, quest_guid.CHARACTER_AVERNUS)
		sophia_data = get_plot(data, quest_guid.CHARACTER_SOPHIA)

		if has_flag(sophia_data, soldiers_peak.SOPHIA_DEAD_FLAG):
			if has_flag(avernus_data, soldiers_peak.GOOD_FLAG):
				response.result = soldiers_peak.GOOD_RESEARCH
			elif has_flag(avernus_data, soldiers_peak.BAD_FLAG):
				response.result = soldiers_peak.BAD_RESEARCH
			elif has_flag(avernus_data, soldiers_peak.AVERNUS_DEAD_FLAG):
				response.result = soldiers_peak.BOTH_DEAD
			else:
				response.result = result.DEFAULT
		elif has_flag(avernus_data, soldiers_peak.AVERNUS_DEAD_FLAG):
			response.result = soldiers_peak.AVERNUS_DEAD
		else:
			response.result = result.DEFAULT

		return response

class blood:
	ORDER = 0
	TITLE = "Did the Warden drink Avernus' alchemical concoction?"

	YES_FLAG = 0
	NO_FLAG = 1

	GAINED = "Gained Power of Blood"
	NO_DRINK = "Didn't drink concoction"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(blood.ORDER, blood.TITLE)

		quest_data = get_plot(data, quest_guid.BLOOD_ABILITIES)

		if has_flag(quest_data, blood.YES_FLAG):
			response.result = blood.GAINED
		elif has_flag(quest_data, blood.NO_FLAG):
			response.result = blood.NO_DRINK
		else:
			response.result = result.DEFAULT

		return response

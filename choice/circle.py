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

"""Broken Circle choices"""

import quest_guid
import result
import responses
from utils import has_flag, get_plot

def mages_dead(data):
	circle_data = get_plot(data, quest_guid.BROKEN_CIRCLE)
	return has_flag(circle_data, cullen.MAGES_DEAD_FLAG)

def wynne_killed(data):
	quest_data = get_plot(data, quest_guid.BROKEN_CIRCLE)
	return has_flag(quest_data, broken_circle.WYNNE_KILLED_FLAG) \
			or has_flag(quest_data, broken_circle.WYNNE_KILLED_CULLEN_FLAG)

class broken_circle:
	ORDER = 0
	TITLE = "Who did the Warden support at the Broken Circle?"

	MAGE_FLAG = 5
	TEMPLAR_FLAG = 4
	WYNNE_DOESNT_JOIN_FLAG = 25
	WYNNE_KILLED_FLAG = 6
	WYNNE_KILLED_CULLEN_FLAG = 51

	MAGES = "Mages supported"
	TEMPLARS = "Templars supported"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(broken_circle.ORDER, broken_circle.TITLE)

		quest_data = get_plot(data, quest_guid.BROKEN_CIRCLE)

		if has_flag(quest_data, broken_circle.MAGE_FLAG):
			response.result = broken_circle.MAGES
		elif has_flag(quest_data, broken_circle.TEMPLAR_FLAG):
			response.result = broken_circle.TEMPLARS
		else:
			response.result = result.DEFAULT

		return response

class irving:
	ORDER = 1
	TITLE = "Did First Enchanter Irving survive the battle against Uldred?"

	IRVING_DEAD_FLAG = 4

	DEAD = "First Enchanter Irving died in battle"
	ALIVE = "First Enchanter Irving survived battle"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(irving.ORDER, irving.TITLE)

		quest_data = get_plot(data, quest_guid.CODEX_IRVING)

		if has_flag(quest_data, irving.IRVING_DEAD_FLAG):
			response.result = irving.DEAD
		else:
			response.result = irving.ALIVE

		return response

class cullen:
	ORDER = 2
	TITLE = "Did the Warden agree to Cullen's request to kill the mages in the Tower?"

	AGREED_FLAG = 20
	MAGES_DEAD_FLAG = 12

	NO = "Did not agree to Cullen's request"
	YES = "Agreed to Cullen's request"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(cullen.ORDER, cullen.TITLE)

		circle_data = get_plot(data, quest_guid.BROKEN_CIRCLE)

		if has_flag(circle_data, cullen.AGREED_FLAG) and mages_dead(data):
			response.result = cullen.YES
		else:
			response.result = cullen.NO

		return response

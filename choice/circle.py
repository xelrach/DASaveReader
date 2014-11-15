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

# Borken Circle choices

import quest_guid
import result
import responses
from flag import has_flag

class broken_circle:
	ORDER = 0
	TITLE = "Who did the Warden support at the Broken Circle?"

	MAGE_FLAG = 5
	TEMPLAR_FLAG = 4

	MAGES = "Mages supported"
	TEMPLARS = "Templars supported"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(broken_circle.ORDER, broken_circle.TITLE)

		quest_data = data.get(quest_guid.BROKEN_CIRCLE, 0)

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

	DIED = "First Enchanter Irving died in battle"
	ALIVE = "First Enchanter Irving survived battle"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(irving.ORDER, irving.TITLE)

		quest_data = data.get(quest_guid.CODEX_IRVING, 0)

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
		response = responses.side_quest_response(irving.ORDER, irving.TITLE)

		cullen_data = data.get(quest_guid.BROKEN_CIRCLE, 0)
		circle_data = data.get(quest_guid.BROKEN_CIRCLE, 0)

		if has_flag(cullen_data, cullen.AGREED_FLAG) and has_flag(circle_data, cullen.MAGES_DEAD_FLAG):
			response.result = cullen.YES
		else:
			response.result = cullen.NO

		return response

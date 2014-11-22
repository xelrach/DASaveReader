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

"""Witch Hunt choices"""

import quest_guid
import result
import responses
from utils import has_flag, get_plot

class witch_hunt:
	ORDER = 0
	TITLE = "Did the Warden go through the eluvian with Morrigan?"

	ALONE_FLAG = 0
	WARDEN_FLAG = 1
	STAB_FLAG = 2

	YES = "Went through the eluvian"
	NO = "Didn't go through the eluvian"
	STAB = "Warden stabbed Morrigan"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(witch_hunt.ORDER, witch_hunt.TITLE)

		quest_data = get_plot(data, quest_guid.MORRIGAN_ELUVIAN)

		if has_flag(quest_data, witch_hunt.ALONE_FLAG):
			response.result = witch_hunt.NO
		elif has_flag(quest_data, witch_hunt.WARDEN_FLAG):
			response.result = witch_hunt.YES
		elif has_flag(quest_data, witch_hunt.STAB_FLAG):
			response.result = witch_hunt.STAB
		else:
			response.result = result.DEFAULT

		return response


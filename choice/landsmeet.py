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

# Landsmeet choices

import quest_guid
import result
import responses
from flag import has_flag
import companions

def alistair_executed(data):
		quest_data = data.get(quest_guid.THE_LANDSMEET, 0)
		return has_flag(quest_data, landsmeet.ALISTAIR_KILLED_FLAG)

class landsmeet:
	ORDER = 0
	TITLE = "Who now rules Ferelden?"

	ALISTAIR_FLAG = 1
	ALISTAIR_ANORA_FLAG = 3
	ANORA_FLAG = 4
	ANORA_WARDEN_FLAG = 5
	ALISTAIR_KILLED_FLAG = 17
	ALISTAIR_WAREDN_FLAG = 56

	ALISTAIR = "Alistair rules"
	ALISTAIR_ANORA = "Alistair & Anora rule"
	ALISTAIR_WARDEN = "Alistair & the Warden rule"
	ANORA = "Anora rules"
	ANORA_WARDEN = "Anora & the Warden rule"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(landsmeet.ORDER, landsmeet.TITLE)
		response.result = result.DEFAULT

		quest_data = data.get(quest_guid.THE_LANDSMEET, 0)

		if companions.alistair_dead(data):
				if has_flag(quest_data, landsmeet.ALISTAIR_FLAG) \
						or has_flag(quest_data, landsmeet.ALISTAIR_ANORA_FLAG) \
						or has_flag(quest_data, landsmeet.ANORA_FLAG) \
						or has_flag(quest_data, landsmeet.ALISTAIR_WAREDN_FLAG):
					response.result = landsmeet.ANORA
				elif has_flag(quest_data, landsmeet.ANORA_WARDEN_FLAG):
					response.result = landsmeet.ANORA_WARDEN
		else:
				if has_flag(quest_data, landsmeet.ALISTAIR_FLAG):
					response.result = landsmeet.ALISTAIR
				elif has_flag(quest_data, landsmeet.ALISTAIR_ANORA_FLAG):
					response.result = landsmeet.ALISTAIR_ANORA
				elif has_flag(quest_data, landsmeet.ANORA_FLAG):
					response.result = landsmeet.ANORA
				elif has_flag(quest_data, landsmeet.ANORA_WARDEN_FLAG):
					response.result = landsmeet.ANORA_WARDEN
				elif has_flag(quest_data, landsmeet.ALISTAIR_WAREDN_FLAG):
					response.result = landsmeet.ALISTAIR_WAREDN_FLAG

		return response

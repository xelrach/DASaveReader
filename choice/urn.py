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

# The Urn of Sacred Ashes choices

import quest_guid
import responses
from utils import has_flag, get_plot

class urn:
	ORDER = 0
	TITLE = "Did the Warden poison the Urn of Sacred Ashes?"

	POORED_BLOOD_FLAG = 8
	CULT_FLAG = 0

	NOT_POISONED = "Urn not poisoned"
	POISONED = "Urn poisoned"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(urn.ORDER, urn.TITLE)

		quest_data = get_plot(data, quest_guid.THE_HIGH_DRAGONS_CHAMPION)

		if has_flag(quest_data, urn.CULT_FLAG):
			response.result = urn.POISONED
		else:
			response.result = urn.NOT_POISONED

		return response

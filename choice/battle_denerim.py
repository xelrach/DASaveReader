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

"""Battle of Denerim choices"""

import choice.result as result
import choice.responses as responses
import choice.companion.fate as fate

class battle_denerim:
	ORDER = 0
	TITLE = "Who killed the Archdemon?"

	WARDEN = "Warden killed Archdemon"
	ALISTAIR = "Alistair killed Archdemon"
	LOGHAIN = "Loghain killed Archdemon"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(battle_denerim.ORDER, \
				battle_denerim.TITLE)

		if fate.alistair_killed_archdemon(data):
			response.result = battle_denerim.ALISTAIR
		elif fate.loghain_killed_archdemon(data):
			response.result = battle_denerim.LOGHAIN
		elif fate.warden_killed_archdemon(data):
			response.result = battle_denerim.WARDEN
		else:
			response.result = result.DEFAULT

		return response

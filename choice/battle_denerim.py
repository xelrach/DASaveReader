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

# Battle of Denerim choices

import quest_guid
import result
import responses
from utils import has_flag, get_plot

def alistair_killed_archdemon(data):
	quest_data = get_plot(data, quest_guid.CLIMAX_ARCHDEMON)
	return has_flag(quest_data, battle_denerim.ALISTAIR_KILL_FLAG) \
			or has_flag(quest_data, battle_denerim.ALISTAIR_KISS_KILL_FLAG)

def warden_killed_archdemon(data):
	quest_data = get_plot(data, quest_guid.CLIMAX_ARCHDEMON)
	return has_flag(quest_data, battle_denerim.PC_KILL_FLAG)

def loghain_killed_archdemon(data):
	quest_data = get_plot(data, quest_guid.CLIMAX_ARCHDEMON)
	return has_flag(quest_data, battle_denerim.LOGHAIN_KILL_FLAG)

class battle_denerim:
	ORDER = 0
	TITLE = "Who killed the Archdemon?"

	ALISTAIR_KILL_FLAG = 2
	ALISTAIR_KISS_KILL_FLAG = 3
	PC_KILL_FLAG = 4
	LOGHAIN_KILL_FLAG = 5

	WARDEN = "Warden killed Archdemon"
	ALISTAIR = "Alistair killed Archdemon"
	LOGHAIN = "Loghain killed Archdemon"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(battle_denerim.ORDER, \
				battle_denerim.TITLE)

		if alistair_killed_archdemon(data):
			response.result = battle_denerim.ALISTAIR
		elif loghain_killed_archdemon(data):
			response.result = battle_denerim.LOGHAIN
		elif warden_killed_archdemon(data):
			response.result = battle_denerim.WARDEN
		else:
			response.result = result.DEFAULT

		return response

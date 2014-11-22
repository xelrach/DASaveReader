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

"""Hero choices"""

import quest_guid
import result
import responses
from utils import has_flag, get_plot
import battle_denerim
import companions

def is_human_noble(data):
	origin_data = get_plot(data, quest_guid.HERO_ORIGIN)
	return has_flag(origin_data, hero.HUMAN_NOBLE_FLAG)

class hero:
	ORDER = 0
	TITLE = "Hero"

	CIRCLE_FLAG = 0
	DWARF_COMMON_FLAG = 1
	DWARF_NOBLE_FLAG = 2
	ELF_CITY_FLAG = 3
	ELF_DALISH_FLAG = 4
	HUMAN_NOBLE_FLAG = 7

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(hero.ORDER, hero.TITLE)

		origin_data = get_plot(data, quest_guid.HERO_ORIGIN)

		if has_flag(origin_data, hero.HUMAN_NOBLE_FLAG):
			response.result = "Human Noble"
		elif has_flag(origin_data, hero.DWARF_COMMON_FLAG):
			response.result = "Dwarf Commoner"
		elif has_flag(origin_data, hero.DWARF_NOBLE_FLAG):
			response.result = "Dwarf Noble"
		elif has_flag(origin_data, hero.ELF_CITY_FLAG):
			response.result = "City Elf"
		elif has_flag(origin_data, hero.ELF_DALISH_FLAG):
			response.result = "Dalish Elf"
		elif has_flag(origin_data, hero.CIRCLE_FLAG):
			response.result = "Circle Mage"
		else:
			response.result = result.DEFAULT

		return response

class hero_fate:
	ORDER = 1
	TITLE = "What happened to the Warden at the end of Dragon Age Origins?"

	ALIVE = "Warden alive & well"
	DEAD = "Warden died killing Archdemon"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(hero_fate.ORDER, hero_fate.TITLE)

		if battle_denerim.warden_killed_archdemon(data) \
				and not companions.morrgans_ritual_completed(data):
			response.result = hero_fate.DEAD
		else:
			response.result = hero_fate.ALIVE

		return response

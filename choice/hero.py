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

import choice.quest_guid as quest_guid
import choice.result as result
import choice.responses as responses
from choice.utils import has_flag, get_plot

import choice.companion.fate as fate

def is_human_noble(data):
	origin_data = get_plot(data, quest_guid.HERO_ORIGIN)
	return has_flag(origin_data, hero.HUMAN_NOBLE_FLAG)

def get_gender(data):
	MALE = 1
	FEMALE = 2
	if data.get_gender() == MALE:
		return 'Male'
	elif data.get_gender() == FEMALE:
		return 'Female'
	return 'Unknown'

def get_race(data):
	HUMAN = 1
	ELF = 2
	DWARF = 3
	if data.get_gender() == HUMAN:
		return 'Human'
	elif data.get_gender() == ELF:
		return 'Elf'
	elif data.get_gender() == DWARF:
		return 'Dwarf'
	return 'Unknown'

def get_class(data):
	WARRIOR = 1
	MAGE = 2
	ROUGE = 3
	if data.get_class() == WARRIOR:
		return 'Warrior'
	elif data.get_class() == MAGE:
		return 'Mage'
	elif data.get_class() == ROUGE:
		return 'Rouge'
	return 'Unknown'

class hero:
	ORDER = 0
	TITLE = "Hero"

	CIRCLE_FLAG = 0
	DWARF_COMMON_FLAG = 1
	DWARF_NOBLE_FLAG = 2
	ELF_CITY_FLAG = 3
	ELF_DALISH_FLAG = 4
	HUMAN_NOBLE_FLAG = 7

	def __init__(self):
		raise NotImplementedError

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

		response.result += ' Origin -- ' + get_gender(data) + ' ' + get_race(data) + ' ' \
				+ get_class(data)

		return response

class hero_fate:
	ORDER = 1
	TITLE = "What happened to the Warden at the end of Dragon Age Origins?"

	ALIVE = "Warden alive & well"
	DEAD = "Warden died killing Archdemon"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(hero_fate.ORDER, hero_fate.TITLE)

		if fate.warden_killed_archdemon(data) \
				and not fate.morrigans_ritual_completed(data):
			response.result = hero_fate.DEAD
		else:
			response.result = hero_fate.ALIVE

		return response

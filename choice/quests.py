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

import inspect

import choice.awakening as awakening
import choice.battle_denerim as battle_denerim
import choice.circle as circle
import choice.companions as companions
import choice.denerim as denerim
import choice.hero as hero
import choice.landsmeet as landsmeet
import choice.nature as nature
import choice.paragon as paragon
import choice.prologue as prologue
import choice.redcliffe as redcliffe
import choice.stone as stone
import choice.urn as urn
import choice.wardens_keep as wardens_keep
import choice.witch_hunt as witch_hunt

def get_quest_results(data, quest):
	quest_results = []
	for side_quest_name, side_quest in quest.get_side_quests():
		result = side_quest.get_result(data)
		if not isinstance(result.result, basestring):
			raise ValueError('Result for quest "' + str(side_quest_name) + '" (' \
					+ str(result.result) + ") is not a string, result=" + str(result))
		quest_results.append(result)
	quest_results.sort(key=lambda result: result.order)

	return quest_results

class Hero:
	ORDER = 0

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_name():
		return "Hero"

	@staticmethod
	def get_side_quests():
		return inspect.getmembers(hero, inspect.isclass)

class Companions:
	ORDER = 1

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_name():
		return "Companions"

	@staticmethod
	def get_side_quests():
		return inspect.getmembers(companions, inspect.isclass)

class Prolog:
	ORDER = 2

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_name():
		return "Prolog"

	@staticmethod
	def get_side_quests():
		return inspect.getmembers(prologue, inspect.isclass)

class NatureOfTheBeast:
	ORDER = 5

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_name():
		return "Nature of the Beast"

	@staticmethod
	def get_side_quests():
		return inspect.getmembers(nature, inspect.isclass)

class BrokenCircle:
	ORDER = 7

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_name():
		return "Broken Circle"

	@staticmethod
	def get_side_quests():
		return inspect.getmembers(circle, inspect.isclass)

class ParagonOfHerKind:
	ORDER = 6

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_name():
		return "A Paragon of Her Kind"

	@staticmethod
	def get_side_quests():
		return inspect.getmembers(paragon, inspect.isclass)

class TheArlOfRedcliff:
	ORDER = 4

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_name():
		return "The Arl of Redcliff"

	@staticmethod
	def get_side_quests():
		return inspect.getmembers(redcliffe, inspect.isclass)

class TheUrnOfSacredAshes:
	ORDER = 3

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_name():
		return "The Urn Of Sacred Ashes"

	@staticmethod
	def get_side_quests():
		return inspect.getmembers(urn, inspect.isclass)

class Denerim:
	ORDER = 8

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_name():
		return "Denerim"

	@staticmethod
	def get_side_quests():
		return inspect.getmembers(denerim, inspect.isclass)

class Landsmeet:
	ORDER = 9

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_name():
		return "Landsmeet"

	@staticmethod
	def get_side_quests():
		return inspect.getmembers(landsmeet, inspect.isclass)

class BattleOfDenerim:
	ORDER = 10

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_name():
		return "Battle of Denerim"

	@staticmethod
	def get_side_quests():
		return inspect.getmembers(battle_denerim, inspect.isclass)

class Awakening:
	ORDER = 11

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_name():
		return "Awakening"

	@staticmethod
	def get_side_quests():
		return inspect.getmembers(awakening, inspect.isclass)

class WitchHunt:
	ORDER = 12

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_name():
		return "Witch Hunt"

	@staticmethod
	def get_side_quests():
		return inspect.getmembers(witch_hunt, inspect.isclass)

class WardensKeep:
	ORDER = 13

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_name():
		return "Warden's Keep"

	@staticmethod
	def get_side_quests():
		return inspect.getmembers(wardens_keep, inspect.isclass)

class StonePrisoner:
	ORDER = 14

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_name():
		return "Stone Prisoner"

	@staticmethod
	def get_side_quests():
		return inspect.getmembers(stone, inspect.isclass)

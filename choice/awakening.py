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

"""Awakening choices"""

import choice.quest_guid as quest_guid
import choice.result as result
import choice.responses as responses
from choice.utils import has_flag, get_plot

class architect:
	ORDER = 0
	TITLE = "What happened to the Architect?"

	ALIVE_FLAG = 4
	DEAD_FLAG = 5

	DEAD = "Warden killed the Architect"
	ALIVE = "Warden allowed Architect to live"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(architect.ORDER, architect.TITLE)

		quest_data = get_plot(data, quest_guid.ARCHITECT)

		if has_flag(quest_data, architect.ALIVE_FLAG):
			response.result = architect.ALIVE
		elif  has_flag(quest_data, architect.DEAD_FLAG):
			response.result = architect.DEAD
		else:
			response.result = result.DEFAULT

		return response

class keep:
	ORDER = 1
	TITLE = "Did the Warden protect Vigil's Keep or the city of Amaranthine?"

	AMARANTHINE_SAVED_FLAG = 7
	KEEP_LOST_FLAG = 8

	KEEP = "Keep protected"
	CITY = "Amaranthine protected"
	BOTH = "Keep and Amaranthine protected"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(keep.ORDER, keep.TITLE)

		vigil_data = get_plot(data, quest_guid.SIEGE_VIGILS_KEEP)
		amaranthine_data = get_plot(data, quest_guid.ASSAULT_AMARANTHINE)

		if has_flag(amaranthine_data, keep.AMARANTHINE_SAVED_FLAG):
			if has_flag(vigil_data, keep.KEEP_LOST_FLAG):
				response.result = keep.CITY
			else:
				response.result = keep.BOTH
		else:
			response.result = keep.KEEP

		return response

class nathaniel_fate:
	ORDER = 2
	TITLE = "What happened to Nathaniel?"

	HANGED_FLAG = 5
	KILLED_FLAG = 12
	JOINED_FLAG = 27

	DEAD = "Nathaniel died"
	ALIVE = "Nathaniel alive & well"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(nathaniel_fate.ORDER, \
				nathaniel_fate.TITLE)

		quest_data = get_plot(data, quest_guid.HOWE_FAMILY)

		if has_flag(quest_data, nathaniel_fate.HANGED_FLAG) \
				or has_flag(quest_data, nathaniel_fate.KILLED_FLAG):
				response.result = nathaniel_fate.DEAD
		else:
			response.result = nathaniel_fate.ALIVE

		return response

class felsi:
	ORDER = 3
	TITLE = "Did Oghren re-unite with his child and Felsi?"

	NOTHING = "The Warden did not help"
	NO = "Oghren and Felsi parted on bad terms"
	YES = "Oghren and Felsi reunited"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(felsi.ORDER, felsi.TITLE)

		quest_data = get_plot(data, quest_guid.FAMILY_MAN)

		response.result = result.INCOMPLETE

		return response


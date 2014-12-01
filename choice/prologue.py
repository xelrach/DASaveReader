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

"""Prologue choices"""

import choice.quest_guid as quest_guid
import choice.responses as responses
from choice.utils import has_flag, get_plot

class prisoner:
	ORDER = 0
	TITLE = "What did the Warden do with the hungry deserter in Ostagar?"

	KILLED_FLAG = 1
	KEY_FLAG = 5
	BRIBED_FLAG = 6
	FOOD_FLAG = 7

	NOTHING = "Ostagar prisoner left alone"
	KILLED = "Ostagar prisoner killed"
	FED_STOLEN = "Fed Ostagar prisoner stolen food"
	FED_SHARED = "Fed Ostagar prisoner guard's lunch"
	FED_BOUGHT = "Bought food to feed Ostagar prisoner"
	STOLE = "Key stolen from Ostagar prisoner"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(prisoner.ORDER, prisoner.TITLE)

		quest_data = get_plot(data, quest_guid.THE_HUNGRY_DESERTER)

		if has_flag(quest_data, prisoner.KILLED_FLAG):
			response.result = prisoner.KILLED
		else:
			if has_flag(quest_data, prisoner.KEY_FLAG):
				if has_flag(quest_data, prisoner.BRIBED_FLAG):
					response.result = prisoner.FED_BOUGHT
				elif has_flag(quest_data, prisoner.FOOD_FLAG):
					# Not sure how to differentiate between these
					response.result = 'Either "' + prisoner.FED_SHARED + '" or "' \
							+ prisoner.FED_STOLEN + '"'
				else:
					response.result = prisoner.STOLE
			else:
				response.result = prisoner.NOTHING

		return response

class mabari:
	ORDER = 1
	TITLE = "What did the Warden do with the mabari hound in Ostagar?"

	HEALED_FLAG = 4
	KILLED_FLAG = 5
	FLOWER_NO_QUEST_FLAG = 9

	NOTHING = "Didn't help mabari hound"
	CURED = "Cured mabari hound"
	KILLED = "Put mabari hound out of its misery"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(mabari.ORDER, mabari.TITLE)

		quest_data = get_plot(data, quest_guid.THE_MABARI_HOUND)

		if has_flag(quest_data, mabari.HEALED_FLAG) \
				or has_flag(quest_data, mabari.FLOWER_NO_QUEST_FLAG):
			response.result = mabari.CURED
		elif has_flag(quest_data, mabari.KILLED_FLAG):
			response.result = mabari.KILLED
		else:
			response.result = mabari.NOTHING

		return response

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

"""Nature of the Beast choices"""

import quest_guid
import result
import responses
from utils import has_flag, get_plot

class nature_of_the_beast:
	ORDER = 0
	TITLE = "How did the Warden resolve the problems between the werewolves and the elves?"

	ELF_FLAG = 0
	WEREWOLF_FLAG = 13
	ZATHRIAN_FLAG = 14

	PEACE = "Brokered peace"
	WEREWOLVES = "Sided with werewolves"
	ELVES = "Sided with elves"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(nature_of_the_beast.ORDER, nature_of_the_beast.TITLE)

		quest_data = get_plot(data, quest_guid.NATURE_OF_THE_BEAST)

		if has_flag(quest_data, nature_of_the_beast.ZATHRIAN_FLAG):
			response.result = nature_of_the_beast.PEACE
		elif has_flag(quest_data, nature_of_the_beast.ELF_FLAG):
			response.result = nature_of_the_beast.ELVES
		elif has_flag(quest_data, nature_of_the_beast.WEREWOLF_FLAG):
			response.result = nature_of_the_beast.WEREWOLVES
		else:
			response.result = result.DEFAULT
		return response

class cammen:
	ORDER = 1
	TITLE = "How did the Warden handle Cammen's broken heart?"

	NOTHING = "Didn't encounter Cammen & Gheyna"
	BROKE_UP = "Broke Cammen & Gheyna up"
	TOGETHER = "Brought Cammen & Gheyna together"

	SEDUCED_FLAG = 2
	BROKE_UP_FLAG = 3
	TOGETHER_FLAG = 4
	BROKE_UP_2_FLAG = 29

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(cammen.ORDER, cammen.TITLE)

		quest_data = get_plot(data, quest_guid.CAMMENS_LAMENT)

		if has_flag(quest_data, cammen.SEDUCED_FLAG) or has_flag(quest_data, cammen.BROKE_UP_FLAG) or has_flag(quest_data, cammen.BROKE_UP_2_FLAG):
			response.result = cammen.BROKE_UP
		elif has_flag(quest_data, cammen.TOGETHER_FLAG):
			response.result = cammen.TOGETHER
		else:
			response.result = cammen.NOTHING
		return response

class elora:
	ORDER = 2
	TITLE = "How did the Warden handle Elora's sick halla?"

	MISSING_MATE_FLAG = 3
	KILLED_FLAG = 6
	LIED_FLAG = 7

	NOTHING = "Could not help Elora"
	SAVED = "Saved the halla"
	KILLED = "Allowed halla to be killed"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(elora.ORDER, elora.TITLE)

		quest_data = get_plot(data, quest_guid.ELORAS_HALLA)

		if has_flag(quest_data, elora.MISSING_MATE_FLAG):
			response.result = elora.SAVED
		elif has_flag(quest_data, elora.KILLED_FLAG):
			response.result = elora.KILLED
		else:
			response.result = elora.NOTHING

		return response

class athras:
	ORDER = 3
	TITLE = "Did the Warden tell Athras about the fate of his wife, Danyla?"

	TELL_FLAG = 3

	NO_TELL = "Didn't tell Athras about wife's fate"
	TOLD = "Told Athras about wife's fate"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(athras.ORDER, athras.TITLE)

		quest_data = get_plot(data, quest_guid.LOST_TO_THE_CURSE)

		if has_flag(quest_data, athras.TELL_FLAG):
			response.result = athras.TOLD
		else:
			response.result = athras.NO_TELL
		return response

class ironbark:
	ORDER = 4
	TITLE = "Did the Warden bring Varathorn the ironbark he needed?"

	BROUGHT_FLAG = 5
	BROUGHT_NO_CRAFTING_FLAG = 12

	NO = "Didn't bring Varathorn ironbark"
	YES = "Brought Varathorn ironbark"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(ironbark.ORDER, ironbark.TITLE)

		quest_data = get_plot(data, quest_guid.RARE_IRONBARK)

		if has_flag(quest_data, ironbark.BROUGHT_FLAG) or has_flag(quest_data, ironbark.BROUGHT_NO_CRAFTING_FLAG):
			response.result = ironbark.YES
		else:
			response.result = ironbark.NO
		return response

class deygan:
	ORDER = 5
	TITLE = "How did the Warden deal with Deygan in the Brecilian Forest?"

	COPRSE_CAMP_FLAG = 0
	ALIVE_CAMP_FLAG = 1
	HEALED_FLAG = 2
	KILLED_LEFT_FLAG = 28

	NOTHING = "Didn't encounter Deygan"
	RETURNED = "Returned Deygan to Dalish camp"
	KILLED = "Killed Deygan"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(deygan.ORDER, deygan.TITLE)

		quest_data = get_plot(data, quest_guid.WOUNDED_IN_THE_FOREST)

		if has_flag(quest_data, deygan.COPRSE_CAMP_FLAG) or has_flag(quest_data, deygan.KILLED_LEFT_FLAG):
			response.result = deygan.KILLED
		elif has_flag(quest_data, deygan.ALIVE_CAMP_FLAG) or has_flag(quest_data, deygan.HEALED_FLAG):
			response.result = deygan.RETURNED
		else:
			response.result = deygan.NOTHING
		return response

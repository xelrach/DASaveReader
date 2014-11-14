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

# Paragon of Her Kind and Orzammar choices

import quest_guid
import result
import responses
from flag import has_flag

class anvil_of_the_void:
	ORDER = 0
	TITLE = "What happened to the Anvil of the Void?"

	BRANKA_ALIVE_FLAG = 4
	BRANKA_SUICIDE_FLAG = 10
	BRANKA_KILLED_FLAG = 26

	BRANKA_DEFEATED = "Defeated Branka"
	BRNKA_SUICIDE = "Branka ended her own life"
	CARIDIN_DEFEATED = "Joined forces against Caridin"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(anvil_of_the_void.ORDER, anvil_of_the_void.TITLE)

		quest_data = data.get(quest_guid.ANVIL_OF_THE_VOID, 0)
		if has_flag(quest_data, anvil_of_the_void.BRANKA_ALIVE_FLAG):
			response.result = anvil_of_the_void.CARIDIN_DEFEATED
		elif has_flag(quest_data, anvil_of_the_void.BRANKA_SUICIDE_FLAG):
			response.result = anvil_of_the_void.BRNKA_SUICIDE
		elif has_flag(quest_data, anvil_of_the_void.BRANKA_KILLED_FLAG):
		    response.result = anvil_of_the_void.BRANKA_DEFEATED
		else:
			response.result = result.DEFAULT

		return response


class paragon_of_her_kind:
	ORDER = 1
	TITLE = "Who rules in Orzammar?"

	BHELEN_FLAG = 7
	HARROWMONT_FLAG = 8

	HARROWMONT = "Harrowmont rules Orzammar"
	BHELEN = "Bhelen rules Orzammar"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(paragon_of_her_kind.ORDER, paragon_of_her_kind.TITLE)

		quest_data = data.get(quest_guid.A_PARAGON_OF_HER_KIND, 0)
		if has_flag(quest_data, paragon_of_her_kind.BHELEN_FLAG):
			response.result = paragon_of_her_kind.BHELEN
		elif has_flag(quest_data, paragon_of_her_kind.HARROWMONT_FLAG):
			response.result = paragon_of_her_kind.HARROWMONT
		else:
			response.result = result.DEFAULT

		return response

class filda:
	ORDER = 2
	TITLE = "How did the Warden complete Filda's quest to find her son Ruck in the Deep Roads?"

	NOTHING = "Didn't speak to Filda"
	SAID_RUCK_DIED = "Said Ruck died"
	ALIVE_TRUTH = "Told truth about Ruck"
	KILLED_LIED = "Killed Ruck & lied"
	KILLED_TRUTH = "Killed Ruck & told truth"
	KILLED_HERO = "Killed Ruck, said he died heroically"

class the_chant_in_the_deeps:
	ORDER = 3
	TITLE = "Did the Warden help Brother Burkel create a Chantry in Orzammar?"

	HELPED_FLAG = 1

	NO = "Didn't help Burkel create Chantry"
	YES = "Helped Burkel create Chantry"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(the_chant_in_the_deeps.ORDER, the_chant_in_the_deeps.TITLE)

		quest_data = data.get(quest_guid.THE_CHANT_IN_THE_DEEPS, 0)
		if has_flag(quest_data, the_chant_in_the_deeps.HELPED_FLAG):
			response.result = the_chant_in_the_deeps.YES
		else:
			response.result = the_chant_in_the_deeps.NO

		return response

class zerlinda:
	ORDER = 4
	TITLE = "What was the fate of Zerlinda and her son?"

	REMAINED = "Zerlinda remained in Dust Town"
	FAMILY = "Helped Zerlinda reconcile with family"
	SURFACE = "Zerlinda left for the surface"
	CHANTRY = "Zerlinda taken in by Burkel's chantry"
	DEEP_ROADS = "Zerlinda left son in the Deep Roads"

class orta:
	ORDER = 5
	TITLE = "Did the Warden help Orta find the proof she needs to join the Assembly as a member of House Ortan?"

	ORTA_RETURNS_FLAG = 4

	NO = "Didn't help Orta join Assembly"
	YES = "Helped Orta join Assembly"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(orta.ORDER, orta.TITLE)

		quest_data = data.get(quest_guid.LOST_TO_THE_MEMORIES, 0)
		if has_flag(quest_data, orta.ORTA_RETURNS_FLAG):
			response.result = orta.YES
		else:
			response.result = orta.NO

		return response


class dagna:
	ORDER = 6
	TITLE = "How did the Warden deal with Dagna's request to become a scholar at the Circle Tower?"

	NOTHING = "Didn't talk to Dagna"
	REFUSED = "Refused to help Dagna"
	STAY = "Convince Dagna to stay with father"
	CIRCLE = "Dagna left to study"
	CIRCLE_DESTROYED = "Told Dagna the Circle destroyed"

class mardy:
	ORDER = 7
	TITLE = "Did the Warden have relations with Mardy before being cast out of Orzammar?"

	NOTHING = "Didn't encounter Mardy"
	NO = "Didn't have relations with Mardy"
	YES = "Had relations with Mardy"

class mardy_son:
	ORDER = 8
	TITLE = "Did the Warden restore Mardy's son's birthright?"

	NO_SON = "Didn't have son with Mardy"
	NO = "Didn't restore Mardy's son's birthright"
	YES = "Restored Mardy's son's birthright"
	NO_MEET = "Didn't encounter Mardy's son"

class legion_of_dead:
	ORDER = 9
	TITLE = "Did the Warden prove to the Shaperate that the Legion of the Dead was connected with a noble house?"

	ADDED_TO_MEMORIES_FLAG = 2

	NO = "Didn't prove Legion of Dead connected to noble house"
	YES = "Proved Legion of Dead connected to noble house"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(legion_of_dead.ORDER, legion_of_dead.TITLE)

		quest_data = data.get(quest_guid.THE_DEAD_CASTE, 0)
		if has_flag(quest_data, legion_of_dead.ADDED_TO_MEMORIES_FLAG):
			response.result = legion_of_dead.YES
		else:
			response.result = legion_of_dead.NO

		return response


class shaperate_tome:
	ORDER = 10
	TITLE = "What did the Warden decide to do with the tome stolen from the Shaperate?"

	RETURNED_FLAG = 3
	SOLD_FLAG = 4

	NOTHING = "Didn't look into stolen tome"
	RETURNED = "Returned tome to Shaperate"
	SOLD = "Sold tome to a fence"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(shaperate_tome.ORDER, shaperate_tome.TITLE)

		quest_data = data.get(quest_guid.THIEF_IN_THE_HOUSE_OF_LEARNING, 0)
		if has_flag(quest_data, shaperate_tome.RETURNED_FLAG):
			response.result = shaperate_tome.RETURNED
		elif has_flag(quest_data, shaperate_tome.SOLD_FLAG:
			response.result = shaperate_tome.SOLD
		else:
			response.result = shaperate_tome.NOTHING

		return response

class rogek:
	ORDER = 11
	TITLE = "Did the Warden complete Rogek's lyrium deal?"

	COMPLETED_FLAG = 5

	NO = "Didn't complete Rogek's lyrium deal"
	YES = "Completed Rogek's lyrium deal"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(rogek.ORDER, rogek.TITLE)

		quest_data = data.get(quest_guid.PRECIOUS_METALS, 0)
		if has_flag(quest_data, rogek.COMPLETED_FLAG):
			response.result = rogek.YES
		else:
			response.result = rogek.NO

		return response

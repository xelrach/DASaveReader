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

# Redcliffe choices

import quest_guid
import result
import responses
from flag import has_flag

class fight:
	ORDER = 0
	TITLE = "Did the Warden help the village of Redcliffe fight the undead hordes at nightfall?"

	SAVED_FLAG = 0
	DESTROYED_FLAG = 7

	NO = "Didn't help Redcliffe fight"
	YES = "Helped Redcliffe fight"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(fight.ORDER, fight.TITLE)

		quest_data = data.get(quest_guid.THE_ATTACK_AT_NIGHTFALL, 0)

		if has_flag(quest_data, fight.SAVED_FLAG):
			response.result = fight.YES
		elif has_flag(quest_data, fight.DESTROYED_FLAG):
			response.result = fight.NO
		else:
			response.result = result.DEFAULT

		return response

class prepare:
	ORDER = 1
	TITLE = "Did the Warden help the people of Redcliffe prepare for the attack of the undead hordes?"

	READY_FLAG = 21
	ABANDONED_FLAG = 12

	NO = "Didn't help Redcliffe prepare"
	YES = "Helped Redcliffe prepare"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(prepare.ORDER, prepare.TITLE)

		quest_data = data.get(quest_guid.A_VILLAGE_UNDER_SIEGE, 0)

		if has_flag(quest_data, prepare.READY_FLAG):
			response.result = prepare.YES
		elif has_flag(quest_data, prepare.ABANDONED_FLAG):
			response.result = prepare.NO
		else:
			response.result = result.DEFAULT

		return response

class connor:
	ORDER = 2
	TITLE = "What happened to Connor?"

	CONNOR_FREED_FLAG = 19
	DEMON_OFFER_ACCEPTED_FLAG = 7
	DEMON_INTEMIDATED_FLAG = 17

	DEAD = "Connor died"
	SAFE = "Connor alive, not possessed"
	POSSESSED = "Connor alive, possessed"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(connor.ORDER, connor.TITLE)

		connor_data = data.get(quest_guid.THE_POSSESSED_CHILD, 0)
		fade_data = data.get(quest_guid.INTO_THE_FADE, 0)

		if has_flag(connor_data, connor.CONNOR_FREED_FLAG):
			if has_flag(fade_data, connor.DEMON_OFFER_ACCEPTED_FLAG) and not has_flag(fade_data, connor.DEMON_INTEMIDATED_FLAG):
				response.result = connor.POSSESSED
			else:
				response.result = connor.SAFE
		else:
			response.result = connor.DEAD

		return response

def village_destroyed(data):
	prep_data = data.get(quest_guid.A_VILLAGE_UNDER_SIEGE, 0)
	fight_data = data.get(quest_guid.THE_ATTACK_AT_NIGHTFALL, 0)
	return has_flag(prep_data, prepare.ABANDONED_FLAG) or has_flag(fight_data, fight.DESTROYED_FLAG)

class bella:
	ORDER = 3
	TITLE = "What was the fate of Bella the tavern waitress?"

	BELLA_IN_CHARGE_FLAG = 14
	BELLA_BUYS_FLAG = 16
	BELLA_DENERIM = 18

	LEFT = "Bella left Redcliffe"
	OWNER = "Bella took tavern ownership"
	BREWERY = "Bella left to start a brewery"
	DIED = "Bella died in Redcliffe"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(bella.ORDER, bella.TITLE)

		quest_data = data.get(quest_guid.A_STIFF_DRINK, 0)

		if has_flag(quest_data, bella.BELLA_IN_CHARGE_FLAG) or has_flag(quest_data, bella.BELLA_BUYS_FLAG):
			response.result = bella.OWNER
		elif has_flag(quest_data, bella.BELLA_DENERIM):
			response.result = bella.BREWERY
		elif village_destroyed(data):
			response.result = bella.DIED
		else:
			response.result = bella.LEFT

		return response

class bevin:
	ORDER = 4
	TITLE = "What did the Warden do to help Kaitlyn find her brother Bevin?"

	BEVIN_FOUND_FLAG = 6
	BEVIN_DAMAGED = 7
	BEVIN_FEARFUL = 8
	HAVE_CHEST_KEY = 10
	KAITLYN_ALMOST_RICH = 15
	KAITLYN_RICH = 16
	BOUGHT_SMALL_MONRY = 19
	BOUGHT_TNIY_MONEY = 20

	NOTHING = "Did nothing to help find Bevin"
	FREED_TOOK = "Freed Bevin & took sword"
	FREED_PAID = "Freed Bevin & paid for sword"
	FREED_NOT_FIND = "Freed Bevin, did not find sword"
	SCARED = "Scared Bevin back to Chantry"
	FREED_RETRUNED = "Freed Bevin & returned sword"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(bevin.ORDER, bevin.TITLE)

		quest_data = data.get(quest_guid.A_MISSING_CHILD, 0)

		if has_flag(quest_data, bevin.BEVIN_FOUND_FLAG):
			if has_flag(quest_data, bevin.KAITLYN_RICH) or has_flag(quest_data, bevin.KAITLYN_ALMOST_RICH):
				response.result = bevin.FREED_PAID
			elif has_flag(quest_data, bevin.BOUGHT_SMALL_MONRY) or has_flag(quest_data, bevin.BOUGHT_TNIY_MONEY) or has_flag(quest_data, bevin.HAVE_CHEST_KEY):
				response.result = bevin.FREED_TOOK
			elif has_flag(quest_data, bevin.BEVIN_DAMAGED) or has_flag(quest_data, bevin.BEVIN_FEARFUL):
				response.result = bevin.SCARED
			else:
				response.result = bevin.FREED_NOT_FIND
		else:
			response.result = bevin.NOTHING

		return response

class valena:
	ORDER = 5
	TITLE = "Did the Warden rescue Owen the Blacksmith's daughter, Valena?"

	VALENA_SAFE_OWEN_SAFE_FLAG = 4
	VALENA_SAFE_OWEN_DEAD_FLAG = 5

	NO_RESCUE = "Never rescued Owen's daughter"
	RESCUE = "Helped Owen's daughter escape"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(valena.ORDER, valena.TITLE)

		quest_data = data.get(quest_guid.LOST_IN_THE_CASTLE, 0)

		if has_flag(quest_data, valena.VALENA_SAFE_OWEN_SAFE_FLAG) or has_flag(quest_data, valena.VALENA_SAFE_OWEN_DEAD_FLAG):
			response.result = valena.RESCUE
		else:
			response.result = valena.NO_RESCUE

		return response

class isolde:
	ORDER = 6
	TITLE = "What happened to Isolde?"

	# ISOLDE_SACRIFICE_FLAG = 21
	ISOLDE_DIES_FLAG = 2

	ALIVE = "Isolde is alive"
	SACRIFICED = "Isolde sacrificed herself"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(isolde.ORDER, isolde.TITLE)

		connor_data = data.get(quest_guid.THE_POSSESSED_CHILD, 0)
		isolde_codex = data.get(quest_guid.CODEX_ISOLDE, 0)

		if has_flag(isolde_codex, isolde.ISOLDE_DIES_FLAG):
			response.result = isolde.SACRIFICED
		else:
			response.result = isolde.ALIVE

		return response

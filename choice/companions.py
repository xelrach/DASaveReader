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

"""Companion choices"""

import choice.quest_guid as quest_guid
import choice.responses as responses
from choice.utils import has_flag, get_plot

import choice.circle as circle
import choice.companion.landsmeet as landsmeet
import choice.companion.recruit as recruit
import choice.companion.fate as fate
import choice.companion.romance as romance

class warden_romance:
	ORDER = 0
	TITLE = "Whom did the Warden romance?"

	ALISTAIR = "Romanced Alistair"
	MORRIGAN = "Romanced Morrigan"
	LELIANA = "Romanced Leliana"
	ZEVRAN = "Romanced Zevran"
	NONE = "No one romanced"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(warden_romance.ORDER, \
				warden_romance.TITLE)

		if romance.morrigan_romanced(data):
			response.result = warden_romance.MORRIGAN
		elif romance.alistair_romanced(data):
			response.result = warden_romance.ALISTAIR
		elif romance.leliana_romanced(data):
			response.result = warden_romance.LELIANA
		elif romance.zevran_romanced(data):
			response.result = warden_romance.ZEVRAN
		else:
			response.result = warden_romance.NONE

		return response

class dog_recruit:
	ORDER = 1
	TITLE = "Did the Warden recruit Dog?"

	NO = "Didn't recruit Dog"
	YES = "Recruited Dog"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(dog_recruit.ORDER, \
				dog_recruit.TITLE)

		if recruit.dog_recruited(data):
			response.result = dog_recruit.YES
		else:
			response.result = dog_recruit.NO

		return response

class sten_free:
	ORDER = 2
	TITLE = "What did the Warden do about Sten's imprisonment in Lothering?"

	RELASED_FLAG = 0
	AGREED_RELASE_FLAG = 9
	HAS_KEY_FLAG = 7

	CLERIC_THREATENED_FLAG = 0

	NOT_FREED = "Didn't free Sten"
	PICKED_LOCK = "Picked lock to free Sten"
	PERSUATION = "Persuaded Revered Mother to free Sten"
	COERCE = "Intimidated Revered Mother to free Sten"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(sten_free.ORDER, sten_free.TITLE)

		quest_data = get_plot(data, quest_guid.THE_QUNARI_PRISONER)
		cleric_data = get_plot(data, quest_guid.GRAND_CLERIC)

		if has_flag(quest_data, sten_free.RELASED_FLAG):
			if has_flag(quest_data, sten_free.HAS_KEY_FLAG):
				if has_flag(cleric_data, sten_free.CLERIC_THREATENED_FLAG):
					response.result = sten_free.COERCE
				else:
					response.result = sten_free.PERSUATION
			else:
				response.result = sten_free.PICKED_LOCK
		else:
			response.result = sten_free.NOT_FREED

		return response

class sten_recruit:
	ORDER = 3
	TITLE = "Did the Warden recruit Sten?"

	NO = "Didn't recruit Sten"
	YES = "Recruited Sten"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(sten_recruit.ORDER, \
				sten_recruit.TITLE)

		if recruit.sten_recruited(data):
			response.result = sten_recruit.YES
		else:
			response.result = sten_recruit.NO

		return response

class sten_sword:
	ORDER = 4
	TITLE = "Did the Warden return Sten's sword to him?"

	SWORD_FLAG = 13

	NOT_RECRUITED = "Didn't recruit Sten"
	NO = "Didn't return Sten's sword"
	YES = "Returned Sten's sword"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(sten_sword.ORDER, \
				sten_sword.TITLE)

		quest_data = get_plot(data, quest_guid.STEN_SWORD)

		if has_flag(quest_data, sten_sword.SWORD_FLAG):
			response.result = sten_sword.YES
		elif recruit.sten_recruited(data):
			response.result = sten_sword.NO
		else:
			response.result = sten_sword.NOT_RECRUITED

		return response

class wynne_recruit:
	ORDER = 9
	TITLE = "Did the Warden recruit Wynne?"

	RECRUITED_FLAG = 5

	NO = "Didn't recruit Wynne"
	YES = "Recruited Wynne"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(wynne_recruit.ORDER, \
				wynne_recruit.TITLE)

		if recruit.wynne_recruited(data):
			response.result = wynne_recruit.YES
		else:
			response.result = wynne_recruit.NO

		return response

class wynne_fate:
	ORDER = 10
	TITLE = "What was Wynne's fate?"

	NOT_RECRUITED = "Wynne not recruited"
	ALIVE = "Wynne alive & well"
	DIED_BROKEN_CIRCLE = "Wynne died at Broken Circle"
	WARDEN_KILLED = "Warden killed Wynne"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(wynne_fate.ORDER, \
				wynne_fate.TITLE)

		if circle.wynne_killed(data):
			response.result = wynne_fate.DIED_BROKEN_CIRCLE
		elif False:
			response.result = wynne_fate.WARDEN_KILLED
		elif recruit.wynne_recruited(data):
			response.result = wynne_fate.ALIVE
		else:
			response.result = wynne_fate.NOT_RECRUITED

		return response

class morrigan_baby:
	ORDER = 11
	TITLE = "Did Morrigan have a baby?"

	NO = "Morrigan did not have a baby"
	WARDEN_OLD_GOD = "Morrigan had an old god baby with the Warden"
	ALISTAIR_OLD_GOD = "Morrigan had an old god baby with Alistair"
	LOGHAIN_OLD_GOD = "Morrigan had an old god baby with Loghain"
	WARDEN_HUMAN = "Morrigan had a human baby with the Warden"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(morrigan_baby.ORDER, \
				morrigan_baby.TITLE)

		if fate.old_god_baby_alistair(data):
			response.result = morrigan_baby.ALISTAIR_OLD_GOD
		elif fate.old_god_baby_loghain(data):
			response.result = morrigan_baby.LOGHAIN_OLD_GOD
		elif fate.old_god_baby_warden(data):
			response.result = morrigan_baby.WARDEN_OLD_GOD
		elif romance.morrigan_romanced(data):
			response.result = morrigan_baby.WARDEN_HUMAN
		else:
			response.result = morrigan_baby.NO

		return response

class loghain:
	ORDER = 5
	TITLE = "What happened to Loghain?"

	KILLED_FLAG = 6
	LIVES_FLAG = 8
	PC_EXECUTE_FLAG = 20
	ALISTAIR_EXECUTE_FLAG = 22
	ALISTAIR_DUEL_FLAG = 24

	WARDEN_EXECUTED = "Loghain executed by Warden"
	ALISTAIR_EXECUTED = "Loghain executed by Alistair"
	ALISTAIR_DUEL = "Loghain was killed by Alistair in duel"
	ARCHDEMON = "Loghain died killing Archdemon"
	ALIVE = "Loghain alive & well"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(loghain.ORDER, loghain.TITLE)

		quest_data = get_plot(data, quest_guid.THE_LANDSMEET)

		if has_flag(quest_data, loghain.ALISTAIR_EXECUTE_FLAG):
			response.result = loghain.ALISTAIR_EXECUTED
		elif has_flag(quest_data, loghain.PC_EXECUTE_FLAG):
			response.result = loghain.WARDEN_EXECUTED
		elif has_flag(quest_data, loghain.ALISTAIR_DUEL_FLAG) \
				and has_flag(quest_data, loghain.KILLED_FLAG):
			response.result = loghain.ALISTAIR_DUEL
		elif fate.loghain_killed_archdemon(data) \
				and not fate.morrigans_ritual_completed(data):
			response.result = loghain.ARCHDEMON
		else:
			response.result = loghain.ALIVE

		return response

class oghren_recruit:
	ORDER = 6
	TITLE = "Did the Warden recruit Oghren?"

	NO = "Didn't recruit Oghren"
	YES = "Recruited Oghren"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(oghren_recruit.ORDER, \
				oghren_recruit.TITLE)

		if recruit.oghren_recruited(data):
			response.result = oghren_recruit.YES
		else:
			response.result = oghren_recruit.NO

		return response

class zevran_recruit:
	ORDER = 7
	TITLE = "Did the Warden recruit Zevran?"

	NO = "Didn't recruit Zevran"
	YES = "Recruited Zevran"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(zevran_recruit.ORDER, \
				zevran_recruit.TITLE)

		if recruit.zevran_recruited(data):
			response.result = zevran_recruit.YES
		else:
			response.result = zevran_recruit.NO

		return response

class zevran_fate:
	ORDER = 8
	TITLE = "What happened to Zevran?"

	KILLED_NOT_HIRED_FLAG = 34
	KILLED_HIRED_FLAG = 20

	DEAD = "Zevran died"
	ALIVE = "Zevran alive & well"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(zevran_fate.ORDER, \
				zevran_fate.TITLE)

		quest_data = get_plot(data, quest_guid.CHARACTER_ZEVRAN)

		if has_flag(quest_data, zevran_fate.KILLED_NOT_HIRED_FLAG) \
				or has_flag(quest_data, zevran_fate.KILLED_HIRED_FLAG):
			response.result = zevran_fate.DEAD
		else:
			response.result = zevran_fate.ALIVE

		return response

class alistair_fate:
	ORDER = 12
	TITLE = "What happened to Alistair?"

	DIED_ARCHDEMON = "Alistair died killing Archdemon"
	DIED_EXECUTED = "Alistair was executed"
	KING = "Alistair became King"
	WARDEN = "Alistair stayed with Wardens"
	DRUNK = "Alistair became a drunk"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(alistair_fate.ORDER, \
				alistair_fate.TITLE)

		if fate.alistair_died_killing_archdemon(data):
			response.result = alistair_fate.DIED_ARCHDEMON
		elif landsmeet.alistair_executed(data):
			response.result = alistair_fate.DIED_EXECUTED
		elif landsmeet.alistair_king(data):
			response.result = alistair_fate.KING
		elif landsmeet.alistair_exiled(data):
			response.result = alistair_fate.DRUNK
		else:
			response.result = alistair_fate.WARDEN

		return response

class alistair_mistress:
	ORDER = 13
	TITLE = "Did the Warden remain as King Alistair's mistress?"

	NOT_MISTRESS_FLAG = 2

	NOT_LOVERS = "Warden & Alistair were not lovers"
	MISTRESS = "Remained Alistair's mistress"
	NOT_MISTRESS = "Didn't remain Alistair's mistress"
	QUEEN = "Warden is Alistair's Queen"
	WARDENS = "Remained with Grey Wardens and the Warden"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(alistair_mistress.ORDER, \
				alistair_mistress.TITLE)

		quest_data = get_plot(data, quest_guid.LANDSMEET_ALISTAIR)

		if romance.alistair_romanced(data) and not fate.alistair_dead(data):
			if landsmeet.alistair_king(data):
				if landsmeet.alistair_with_warden_queen(data):
					response.result = alistair_mistress.QUEEN
				elif has_flag(quest_data, alistair_mistress.NOT_MISTRESS_FLAG):
					response.result = alistair_mistress.NOT_MISTRESS
				else:
					response.result = alistair_mistress.MISTRESS
			else:
				response.result = alistair_mistress.WARDENS
		else:
			response.result = alistair_mistress.NOT_LOVERS

		return response

class leliana_fate:
	ORDER = 14
	TITLE = "What happened to Leliana?"

	JOIN_FLAG = 43
	ATTACK_PC_FLAG = 41
	LEAVES_FLAG = 42

	NOT_RECRUITED = "Didn't recruit Leliana"
	ALIVE = "Leliana alive & well"
	KILLED = "Killed Leliana after poisoning the Urn"
	LEFT = "Leliana Left"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(leliana_fate.ORDER, \
				leliana_fate.TITLE)

		quest_data = get_plot(data, quest_guid.LELIANAS_PAST)

		if has_flag(quest_data, leliana_fate.ATTACK_PC_FLAG):
			response.result = leliana_fate.KILLED
		elif has_flag(quest_data, leliana_fate.LEAVES_FLAG):
			response.result = leliana_fate.LEFT
		elif recruit.leliana_recruited(data):
			response.result = leliana_fate.ALIVE
		else:
			response.result = leliana_fate.NOT_RECRUITED

		return response

class grimoire:
	ORDER = 15
	TITLE = "Did the Warden find Flemeth's grimoire for Morrigan?"

	FLEMETH_KILLED_FLAG = 7
	GAVE_GRIMOIRE_FLAG = 1

	NO = "Did not acquire grimoire"
	PEACEFUL = "Acquired grimoire peacefully"
	VIOLENT = "Acquired grimoire by defeating Flemeth"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(grimoire.ORDER, grimoire.TITLE)

		quest_data = get_plot(data, quest_guid.FLEMETHS_GRIMOIRE)

		if has_flag(quest_data, grimoire.GAVE_GRIMOIRE_FLAG):
			if has_flag(quest_data, grimoire.FLEMETH_KILLED_FLAG):
				response.result = grimoire.VIOLENT
			else:
				response.result = grimoire.PEACEFUL
		else:
			response.result = grimoire.NO

		return response

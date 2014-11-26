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

# Companion choices

import quest_guid
import result
import responses
from utils import has_flag, get_plot

import battle_denerim
import circle
import landsmeet
import recruit

def morrgans_ritual_completed(data):
	quest_data = get_plot(data, quest_guid.MORRIGANS_RITUAL)

	return has_flag(quest_data, morrigan_baby.ALISTAIR_FLAG) \
			or has_flag(quest_data, morrigan_baby.LOGHAIN_FLAG) \
			or has_flag(quest_data, morrigan_baby.PC_FLAG)

def alistair_died_killing_archdemon(data):
	return battle_denerim.alistair_killed_archdemon(data) \
			and not morrgans_ritual_completed(data)

def alistair_dead(data):
	return alistair_died_killing_archdemon(data) \
			or landsmeet.alistair_executed(data)

def morrigan_romanced(data):
	morrigan_data = get_plot(data, quest_guid.APPROVAL_MORRIGAN)
	return has_flag(morrigan_data, romance.ACTIVE_FLAG)

def alistair_romanced(data):
	alistair_data = get_plot(data, quest_guid.APPROVAL_ALISTAIR)
	return has_flag(alistair_data, romance.ACTIVE_FLAG)

class romance:
	ORDER = 0
	TITLE = "Whom did the Warden romance?"

	DUMPED_FLAG = 13
	ACTIVE_FLAG = 21
	CUT_OFF_FLAG = 27

	ALISTAIR = "Romanced Alistair"
	MORRIGAN = "Romanced Morrigan"
	LELIANA = "Romanced Leliana"
	ZEVRAN = "Romanced Zevran"
	NONE = "No one romanced"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(romance.ORDER, romance.TITLE)

		leliana_data = get_plot(data, quest_guid.APPROVAL_LELIANA)
		zevran_data = get_plot(data, quest_guid.APPROVAL_ZEVRAN)

		if morrigan_romanced(data):
			response.result = romance.MORRIGAN
		elif alistair_romanced(data):
			response.result = romance.ALISTAIR
		elif has_flag(leliana_data, romance.ACTIVE_FLAG):
			response.result = romance.LELIANA
		elif has_flag(zevran_data, romance.ACTIVE_FLAG):
			response.result = romance.ZEVRAN
		else:
			response.result = romance.NONE

		return response

class dog_recruit:
	ORDER = 1
	TITLE = "Did the Warden recruit Dog?"

	NO = "Didn't recruit Dog"
	YES = "Recruited Dog"

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

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(sten_sword.ORDER, \
				sten_sword.TITLE)

		quest_data = get_plot(data, quest_guid.THE_QUNARI_PRISONER)

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

	ALISTAIR_FLAG = 2
	PC_FLAG = 4
	LOGHAIN_FLAG = 12

	NO = "Morrigan did not have a baby"
	WARDEN_OLD_GOD = "Morrigan had an old god baby with the Warden"
	ALISTAIR_OLD_GOD = "Morrigan had an old god baby with Alistair"
	LOGHAIN_OLD_GOD = "Morrigan had an old god baby with Loghain"
	WARDEN_HUMAN = "Morrigan had a human baby with the Warden"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(morrigan_baby.ORDER, \
				morrigan_baby.TITLE)

		quest_data = get_plot(data, quest_guid.MORRIGANS_RITUAL)

		if has_flag(quest_data, morrigan_baby.ALISTAIR_FLAG):
			response.result = morrigan_baby.ALISTAIR_OLD_GOD
		elif has_flag(quest_data, morrigan_baby.LOGHAIN_FLAG):
			response.result = morrigan_baby.LOGHAIN_FLAG
		elif has_flag(quest_data, morrigan_baby.PC_FLAG):
			response.result = morrigan_baby.WARDEN_OLD_GOD
		elif morrigan_romanced(data):
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
		elif battle_denerim.loghain_killed_archdemon(data) \
				and not morrgans_ritual_completed(data):
			response.result = loghain.ARCHDEMON
		else:
			response.result = loghain.ALIVE

		return response

class oghren_recruit:
	ORDER = 6
	TITLE = "Did the Warden recruit Oghren?"

	NO = "Didn't recruit Oghren"
	YES = "Recruited Oghren"

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

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(alistair_fate.ORDER, \
				alistair_fate.TITLE)

		if alistair_died_killing_archdemon(data):
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

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(alistair_mistress.ORDER, \
				alistair_mistress.TITLE)

		quest_data = get_plot(data, quest_guid.LANDSMEET_ALISTAIR)

		if alistair_romanced(data) and not alistair_dead(data):
			if landsmeet.alistair_king(data):
				if landsmeet.warden_queen(data):
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

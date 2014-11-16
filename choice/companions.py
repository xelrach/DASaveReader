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
from flag import has_flag
import battle_denerim
import landsmeet

def morrgans_ritual_completed(data):
	quest_data = data.get(quest_guid.MORRIGANS_RITUAL, 0)

	return has_flag(quest_data, morrigan_baby.ALISTAIR_FLAG) \
			or has_flag(quest_data, morrigan_baby.LOGHAIN_FLAG) \
			or has_flag(quest_data, morrigan_baby.PC_FLAG)

def alistair_died_killing_archdemon(data):
	return battle_denerim.alistair_killed_archdemon(data) \
			and not morrgans_ritual_completed(data)

def alistair_dead(data):
	return alistair_died_killing_archdemon(data) or landsmeet.alistair_executed(data)

class romance:
	ORDER = 0
	TITLE = "Whom did the Warden romance?"
	ALISTAIR = "Romanced Alistair"
	MORRIGAN = "Romanced Morrigan"
	LELIANA = "Romanced Leliana"
	ZEVRAN = "Romanced Zevran"

class dog_recruit:
	ORDER = 1
	TITLE = "Did the Warden recruit Dog?"
	NO = "Didn't recruit Dog"
	YES = "Recruited Dog"

class sten_free:
	ORDER = 2
	TITLE = "What did the Warden do about Sten's imprisonment in Lothering?"
	NOT_FREED = "Didn't free Sten"
	PICKED_LOCK = "Picked lock to free Sten"
	PERSUATION = "Persuaded Revered Mother to free Sten"
	COERCE = "Intimidated Revered Mother to free Sten"

class sten_recruit:
	ORDER = 3
	TITLE = "Did the Warden recruit Sten?"
	NO = "Didn't recruit Sten"
	YES = "Recruited Sten"

class sten_sword:
	ORDER = 4
	TITLE = "Did the Warden return Sten's sword to him?"
	NOT_RECRUITED = "Didn't recruit Sten"
	NO = "Didn't return Sten's sword"
	YES = "Returned Sten's sword"

class wynne_recruit:
	ORDER = 5
	TITLE = "Did the Warden recruit Wynne?"
	NO = "Didn't recruit Wynne"
	YES = "Recruited Wynne"

class wynne_fate:
	ORDER = 6
	TITLE = "What was Wynne's fate?"
	NOT_RECRUITED = "Wynne not recruited"
	ALIVE = "Wynne alive & well"
	DIED_BROKEN_CIRCLE = "Wynne died at Broken Circle"
	WARDEN_KILLED = "Warden killed Wynne"

class morrigan_baby:
	ORDER = 7
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
		response = responses.side_quest_response(morrigan_baby.ORDER, morrigan_baby.TITLE)

		quest_data = data.get(quest_guid.TORTURD_NOBLE, 0)

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
	ORDER = 8
	TITLE = "What happened to Loghain?"
	WARDEN_EXECUTED = "Loghain executed by Warden"
	ALISTAIR_EXECUTED = "Loghain executed by Alistair"
	ALISTAIR_DUEL = "Loghain was killed by Alistair in duel"
	ARCHDEMON = "Loghain died killing Archdemon"
	ALIVE = "Loghain alive & well"

class oghren_recruit:
	ORDER = 9
	TITLE = "Did the Warden recruit Oghren?"
	NO = "Didn't recruit Oghren"
	YES = "Recruited Oghren"

class zevran_recruit:
	ORDER = 10
	TITLE = "Did the Warden recruit Zevran?"
	NO = "Didn't recruit Zevran"
	YES = "Recruited Zevran"

class zevran_fate:
	ORDER = 11
	TITLE = "What happened to Zevran?"
	DEAD = "Zevran died"
	ALIVE = "Zevran alive & well"

class alistair_fate:
	ORDER = 12
	TITLE = "What happened to Alistair?"
	DIED_ARCHDEMON = "Alistair died killing Archdemon"
	DIED_EXECUTED = "Alistair was executed"
	KING = "Alistair became King"
	WARDEN = "Alistair stayed with Wardens"
	DRUNK = "Alistair became a drunk"

class alistair_mistress:
	ORDER = 13
	TITLE = "Did the Warden remain as King Alistair's mistress?"
	NOT_LOVERS = "Warden & Alistair were not lovers"
	MISTRESS = "Remained Alistair's mistress"
	NOT_MISTRESS = "Didn't remain Alistair's mistress"
	QUEEN = "Warden is Alistair's Queen"
	WARDENS = "Remained with Grey Wardens and the Warden"

class leliana_fate:
	ORDER = 14
	TITLE = "What happened to Leliana?"
	NOT_RECRUITED = "Didn't recruit Leliana"
	ALIVE = "Leliana alive & well"
	KILLED = "Killed Leliana after poisoning the Urn"
	LEFT = "Leliana Left"

class grimoire:
	ORDER = 15
	TITLE = "Did the Warden find Flemeth's grimoire for Morrigan?"
	NO = "Did not acquire grimoire"
	PEACEFUL = "Acquired grimoire peacefully"
	VIOLENT = "Acquired grimoire by defeating Flemeth"

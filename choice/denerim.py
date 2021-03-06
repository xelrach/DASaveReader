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

"""Denerim choices"""

import choice.quest_guid as quest_guid
import choice.responses as responses
from choice.utils import has_flag, get_plot

class ser_landry:
	ORDER = 0
	TITLE = "Did the Warden kill Ser Landry?"

	KILLED_IN_DUEL_FLAG = 6

	ALIVE = "Ser Landry alive"
	DEAD = "Ser Landry killed"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(ser_landry.ORDER, \
				ser_landry.TITLE)

		quest_data = get_plot(data, quest_guid.HONOR_BOUND)

		if has_flag(quest_data, ser_landry.KILLED_IN_DUEL_FLAG):
			response.result = ser_landry.DEAD
		else:
			response.result = ser_landry.ALIVE

		return response


class oswyn:
	ORDER = 1
	TITLE = "Did the Warden tell Bann Sighard about finding Oswyn in Arl Howe's torture room?"

	TOLD_REWARD_FLAG = 1
	TOLD_NO_REWARD_FLAG = 2

	NO = "Didn't tell Bann Sighard about Oswyn"
	YES = "Told Bann Sighard about Oswyn"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(oswyn.ORDER, oswyn.TITLE)

		quest_data = get_plot(data, quest_guid.TORTURD_NOBLE)

		if has_flag(quest_data, oswyn.TOLD_REWARD_FLAG) \
				or has_flag(quest_data, oswyn.TOLD_NO_REWARD_FLAG):
			response.result = oswyn.YES
		else:
			response.result = oswyn.NO

		return response

class crime_wave:
	ORDER = 2
	TITLE = "Did the Warden complete Slim Couldry's crime wave?"

	DONE_FLAG = 9

	NO = "Didn't complete Slim Couldry's crime wave"
	YES = "Completed Slim Couldry's crime wave"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(crime_wave.ORDER, \
				crime_wave.TITLE)

		quest_data = get_plot(data, quest_guid.CRIME_WAVE)

		if has_flag(quest_data, crime_wave.DONE_FLAG):
			response.result = crime_wave.YES
		else:
			response.result = crime_wave.NO

		return response

class irminric_ring:
	ORDER = 3
	TITLE = "Did the Warden give Alfstanna her brother Irminric's ring?"

	GAVE_RING_LOCATION_FLAG = 1
	GAVE_RING_NO_LOCATION_FLAG = 2

	NO = "Didn't give Alfstanna Irminric's ring"
	YES = "Gave Alfstanna Irminric's ring"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(irminric_ring.ORDER, \
				irminric_ring.TITLE)

		quest_data = get_plot(data, quest_guid.LOST_TEMPLAR)

		if has_flag(quest_data, irminric_ring.GAVE_RING_LOCATION_FLAG) \
				or has_flag(quest_data, irminric_ring.GAVE_RING_NO_LOCATION_FLAG):
			response.result = irminric_ring.YES
		else:
			response.result = irminric_ring.NO

		return response

class amulet:
	ORDER = 4
	TITLE = "Did the Warden return the worn amulet to the beggar woman in Denerim's alienage?"

	GAVE_FLAG = 1

	NO = "Didn't return amulet to beggar"
	YES = "Returned amulet to beggar"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(amulet.ORDER, amulet.TITLE)

		quest_data = get_plot(data, quest_guid.HEARING_VOICES)

		if has_flag(quest_data, amulet.GAVE_FLAG):
			response.result = amulet.YES
		else:
			response.result = amulet.NO

		return response


class goldanna:
	ORDER = 9
	TITLE = "Did the Warden help Alistair track down his half-sister Goldanna?"

	WANT_TO_MEET_GOLDANNA = 16
	MET_GOLDANNA = 12

	NOTHING = "Did not encounter Goldanna"
	YES = "Helped Alistair find Goldanna"
	NO = "Did not help Alistair find Goldanna"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(goldanna.ORDER, goldanna.TITLE)

		quest_data = get_plot(data, quest_guid.ALISTAIRS_FAMILY)

		if has_flag(quest_data, goldanna.MET_GOLDANNA):
			response.result = goldanna.YES
		elif has_flag(quest_data, goldanna.WANT_TO_MEET_GOLDANNA):
			response.result = goldanna.NO
		else:
			response.result = goldanna.NOTHING

		return response

class scroll:
	ORDER = 5
	TITLE = "Did the Warden bring the ancient encrypted scroll to Sister Justine in Denerim?"

	BROUGHT_SCROLL_FLAG = 6

	NO = "Didn't bring scroll to Sister Justine"
	YES = "Brought scroll to Sister Justine"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(scroll.ORDER, scroll.TITLE)

		quest_data = get_plot(data, quest_guid.FORGOTTEN_VERSES)

		if has_flag(quest_data, scroll.BROUGHT_SCROLL_FLAG):
			response.result = scroll.YES
		else:
			response.result = scroll.NO

		return response

class pearl:
	ORDER = 6
	TITLE = "Did the Warden help Sergeant Kylon clear the White Falcons out of the Pearl?"

	MERCENARIES_LEFT_FLAG = 5
	MERCENARIES_KILLED_FLAG = 8

	NO = "Didn't help clear customers out of Pearl"
	YES = "Helped clear customers out of Pearl"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(pearl.ORDER, pearl.TITLE)

		quest_data = get_plot(data, quest_guid.PEARLS_BEFORE_SWINE)

		if has_flag(quest_data, pearl.MERCENARIES_LEFT_FLAG):
			response.result = pearl.YES
		else:
			response.result = pearl.NO

		return response

class crimson_oars:
	ORDER = 7
	TITLE = "Did the Warden handle the Crimson Oars for Sergeant Kylon in Denerim?"

	OARS_GONE_OR_DEAD_FLAG = 1

	NO = "Didn't handle the Crimson Oars"
	YES = "Handled the Crimson Oars"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(crimson_oars.ORDER, \
				crimson_oars.TITLE)

		quest_data = get_plot(data, quest_guid.THE_CRIMSON_OARS)

		if has_flag(quest_data, crimson_oars.OARS_GONE_OR_DEAD_FLAG):
			response.result = crimson_oars.YES
		else:
			response.result = crimson_oars.NO

		return response

class ignacio:
	ORDER = 8
	TITLE = "Did the Warden complete Master Ignacio's assassination missions?"

	KILLED_IGNACIO_FLAG = 17
	RANSOM_DONE_FLAG = 1

	NO = "Didn't complete Master Ignacio's assassinations"
	YES = "Completed Master Ignacio's assassinations"
	KILLED_IGNACIO = "Warden killed Master Ignacio"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(ignacio.ORDER, ignacio.TITLE)

		ransom_data = get_plot(data, quest_guid.THE_RANSOM)
		crow_data = get_plot(data, quest_guid.THE_TRIAL_OF_CROWS)

		if has_flag(crow_data, ignacio.KILLED_IGNACIO_FLAG):
			response.result = ignacio.KILLED_IGNACIO
		elif has_flag(ransom_data, ignacio.RANSOM_DONE_FLAG):
			response.result = ignacio.YES
		else:
			response.result = ignacio.NO

		return response

class marjolaine:
	ORDER = 10
	TITLE = "Did Leliana have Marjolaine killed or let her go?"

	KILLED_FLAG = 10
	SPARED_FLAG = 31

	NOTHING = "Did not encounter Marjolaine"
	SENT_AWAY = "Sent Marjolaine away"
	KILLED = "Had Marjolaine killed"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(marjolaine.ORDER, \
				marjolaine.TITLE)

		quest_data = get_plot(data, quest_guid.LELIANAS_PAST)

		if has_flag(quest_data, marjolaine.KILLED_FLAG):
			response.result = marjolaine.KILLED
		elif has_flag(quest_data, marjolaine.SPARED_FLAG):
			response.result = marjolaine.SENT_AWAY
		else:
			response.result = marjolaine.NOTHING

		return response

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

# Denerim choices

import quest_guid
import result

class ser_landry:
	ORDER = 0
	TITLE = "Did the Warden kill Ser Landry?"
	ALIVE = "Ser Landry alive"
	DEAD = "Ser Landry killed"

class oswyn:
	ORDER = 1
	TITLE = "Did the Warden tell Bann Sighard about finding Oswyn in Arl Howe's torture room?"
	NO = "Didn't tell Bann Sighard about Oswyn"
	YES = "Told Bann Sighard about Oswyn"

class crime_wave:
	ORDER = 2
	TITLE = "Did the Warden complete Slim Couldry's crime wave?"
	NO = "Didn't complete Slim Couldry's crime wave"
	YES = "Completed Slim Couldry's crime wave"

class irminric_ring:
	ORDER = 3
	TITLE = "Did the Warden give Alfstanna her brother Irminric's ring?"
	NO = "Didn't give Alfstanna Irminric's ring"
	YES = "Gave Alfstanna Irminric's ring"

class amulet:
	ORDER = 4
	TITLE = "Did the Warden return the worn amulet to the beggar woman in Denerim's alienage?"
	NO = "Didn't return amulet to beggar"
	YES = "Returned amulet to beggar"

class goldanna:
	ORDER = 5
	TITLE = "Did the Warden help Alistair track down his half-sister Goldanna?"
	NOTHING = "Did not encounter Goldanna"
	YES = "Helped Alistair find Goldanna"
	NO = "Did not help Alistair find Goldanna"

class scroll:
	ORDER = 6
	TITLE = "Did the Warden bring the ancient encrypted scroll to Sister Justine in Denerim?"
	NO = "Didn't bring scroll to Sister Justine"
	YES = "Brought scroll to Sister Justine"

class pearl:
	ORDER = 7
	TITLE = "Did the Warden help Sergeant Kylon clear the White Falcons out of the Pearl?"
	NO = "Didn't help clear customers out of Pearl"
	YES = "Helped clear customers out of Pearl"

class crimson_oars:
	ORDER = 8
	TITLE = "Did the Warden handle the Crimson Oars for Sergeant Kylon in Denerim?"
	NO = "Didn't handle the Crimson Oars"
	YES = "Handled the Crimson Oars"

class ignacio:
	ORDER = 9
	TITLE = "Did the Warden complete Master Ignacio's assassination missions?"
	NO = "Didn't complete Master Ignacio's assassinations"
	YES = "Completed Master Ignacio's assassinations"
	KILLED_IGNACIO = "Warden killed Master Ignacio"

class marjolaine:
	ORDER = 10
	TITLE = "Did Leliana have Marjolaine killed or let her go?"
	NOTHING = "Did not encounter Marjolaine"
	SENT_AWAY = "Sent Marjolaine away"
	KILLED = "Had Marjolaine killed"

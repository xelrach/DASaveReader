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

class fight:
	ORDER = 0
	TITLE = "Did the Warden help the village of Redcliffe fight the undead hordes at nightfall?"
	NO = "Didn't help Redcliffe fight"
	YES = "Helped Redcliffe fight"

class prepare:
	ORDER = 1
	TITLE = "Did the Warden help the people of Redcliffe prepare for the attack of the undead hordes?"
	NO = "Didn't help Redcliffe prepare"
	YES = "Helped Redcliffe prepare"

class conor:
	ORDER = 2
	TITLE = "What happened to Connor?"
	DIED = "Connor died"
	SAFE = "Connor alive, not possessed"
	POSSESSED = "Connor alive, possessed"

class bella:
	ORDER = 3
	TITLE = "What was the fate of Bella the tavern waitress?"
	LEFT = "Bella left Redcliffe"
	OWNER = "Bella took tavern ownership"
	BREWERY = "Bella left to start a brewery"
	DIED = "Bella died in Redcliffe"

class bevin:
	ORDER = 4
	TITLE = "What did the Warden do to help Kaitlyn find her brother Bevin?"
	NOTHING = "Did nothing to help find Bevin"
	FREED_TOOK = "Freed Bevin & took sword"
	FREED_PAID = "Freed Bevin & paid for sword"
	FREED_NOT_FIND = "Freed Bevin, did not find sword"
	SCARED = "Scared Bevin back to Chantry"
	FREED_RETRUNED = "Freed Bevin & returned sword"

class valena:
	ORDER = 5
	TITLE = "Did the Warden rescue Owen the Blacksmith's daughter, Valena?"
	NO_RESCUE = "Never rescued Owen's daughter"
	RESCUE = "Helped Owen's daughter escape"

class isolde:
	ORDER = 6
	TITLE = "What happened to Isolde?"
	ALIVE = "Isolde is alive"
	SACRIFICED = "Isolde sacrificed herself"

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

"""Functions for various companion fates"""

import choice.quest_guid as quest_guid
from choice.utils import has_flag, get_plot
import choice.companion.landsmeet as landsmeet

# Who killed the archdemon flags
ALISTAIR_KILL_FLAG = 2
ALISTAIR_KISS_KILL_FLAG = 3
PC_KILL_FLAG = 4
LOGHAIN_KILL_FLAG = 5

# Morrigan old god baby
ALISTAIR_BABY_FLAG = 2
PC_BABY_FLAG = 4
LOGHAIN_BABY_FLAG = 12

def alistair_died_killing_archdemon(data):
	return alistair_killed_archdemon(data) \
			and not morrigans_ritual_completed(data)

def alistair_dead(data):
	return alistair_died_killing_archdemon(data) \
			or landsmeet.alistair_executed(data)

def old_god_baby_alistair(data):
	quest_data = get_plot(data, quest_guid.MORRIGANS_RITUAL)
	return has_flag(quest_data, ALISTAIR_BABY_FLAG)

def old_god_baby_warden(data):
	quest_data = get_plot(data, quest_guid.MORRIGANS_RITUAL)
	return has_flag(quest_data, PC_BABY_FLAG)

def old_god_baby_loghain(data):
	quest_data = get_plot(data, quest_guid.MORRIGANS_RITUAL)
	return has_flag(quest_data, LOGHAIN_BABY_FLAG)

def morrigans_ritual_completed(data):
	return old_god_baby_alistair(data) \
			or old_god_baby_warden \
			or old_god_baby_loghain

def alistair_killed_archdemon(data):
	quest_data = get_plot(data, quest_guid.CLIMAX_ARCHDEMON)
	return has_flag(quest_data, ALISTAIR_KILL_FLAG) \
			or has_flag(quest_data, ALISTAIR_KISS_KILL_FLAG)

def warden_killed_archdemon(data):
	quest_data = get_plot(data, quest_guid.CLIMAX_ARCHDEMON)
	return has_flag(quest_data, PC_KILL_FLAG)

def loghain_killed_archdemon(data):
	quest_data = get_plot(data, quest_guid.CLIMAX_ARCHDEMON)
	return has_flag(quest_data, LOGHAIN_KILL_FLAG)

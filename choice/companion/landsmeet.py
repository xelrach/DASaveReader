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

"""Functions for various Landsmeet fates"""

import choice.quest_guid as quest_guid
from choice.utils import has_flag, get_plot

ALISTAIR_FLAG = 1
ALISTAIR_ANORA_FLAG = 3
ANORA_FLAG = 4
ANORA_WARDEN_FLAG = 5
ALISTAIR_LEAVES_FOREVER_FLAG = 16
ALISTAIR_KILLED_FLAG = 17
ALISTAIR_WARDEN_FLAG = 56

def alistair_executed(data):
	quest_data = get_plot(data, quest_guid.THE_LANDSMEET)
	return has_flag(quest_data, ALISTAIR_KILLED_FLAG)

def alistair_king(data):
	return alistair_king_alone(data) \
			or alistair_with_anora_queen(data) \
			or alistair_with_warden_queen(data)

def alistair_exiled(data):
	quest_data = get_plot(data, quest_guid.THE_LANDSMEET)
	return has_flag(quest_data, ALISTAIR_LEAVES_FOREVER_FLAG)

def alistair_with_warden_queen(data):
	quest_data = get_plot(data, quest_guid.THE_LANDSMEET)
	return has_flag(quest_data, ALISTAIR_WARDEN_FLAG)

def anora_with_warden_king(data):
	quest_data = get_plot(data, quest_guid.THE_LANDSMEET)
	return has_flag(quest_data, ANORA_WARDEN_FLAG)

def anora_queen_alone(data):
	quest_data = get_plot(data, quest_guid.THE_LANDSMEET)
	return has_flag(quest_data, ANORA_FLAG)

def alistair_king_alone(data):
	quest_data = get_plot(data, quest_guid.THE_LANDSMEET)
	return has_flag(quest_data, ALISTAIR_FLAG)

def alistair_with_anora_queen(data):
	quest_data = get_plot(data, quest_guid.THE_LANDSMEET)
	return has_flag(quest_data, ALISTAIR_ANORA_FLAG)

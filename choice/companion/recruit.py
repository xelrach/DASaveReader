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

"""Recruitment choices"""

import choice.quest_guid as quest_guid
from choice.utils import has_flag, get_plot

ALISTAIR_FLAG = 0
DOG_FLAG = 1
LELIANA_FLAG = 4
OGHREN_FLAG = 6
SHALE_FLAG = 7
WYNNE_FLAG = 8
ZEVRAN_FLAG = 9
LOGHAIN_FLAG = 10
STEN_FLAG = 13

def alistair_recruited(data):
	quest_data = get_plot(data, quest_guid.PARTY)
	return has_flag(quest_data, ALISTAIR_FLAG)

def dog_recruited(data):
	quest_data = get_plot(data, quest_guid.PARTY)
	return has_flag(quest_data, DOG_FLAG)

def leliana_recruited(data):
	quest_data = get_plot(data, quest_guid.PARTY)
	return has_flag(quest_data, LELIANA_FLAG)

def oghren_recruited(data):
	quest_data = get_plot(data, quest_guid.PARTY)
	return has_flag(quest_data, OGHREN_FLAG)

def shale_recruited(data):
	quest_data = get_plot(data, quest_guid.PARTY)
	return has_flag(quest_data, SHALE_FLAG)

def wynne_recruited(data):
	quest_data = get_plot(data, quest_guid.PARTY)
	return has_flag(quest_data, WYNNE_FLAG)

def zevran_recruited(data):
	quest_data = get_plot(data, quest_guid.PARTY)
	return has_flag(quest_data, ZEVRAN_FLAG)

def loghain_recruited(data):
	quest_data = get_plot(data, quest_guid.PARTY)
	return has_flag(quest_data, LOGHAIN_FLAG)

def sten_recruited(data):
	quest_data = get_plot(data, quest_guid.PARTY)
	return has_flag(quest_data, STEN_FLAG)

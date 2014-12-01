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

"""Functions for romance choices"""

import choice.quest_guid as quest_guid
from choice.utils import has_flag, get_plot

DUMPED_FLAG = 13
ACTIVE_FLAG = 21
CUT_OFF_FLAG = 27

def morrigan_romanced(data):
	morrigan_data = get_plot(data, quest_guid.APPROVAL_MORRIGAN)
	return has_flag(morrigan_data, ACTIVE_FLAG)

def alistair_romanced(data):
	alistair_data = get_plot(data, quest_guid.APPROVAL_ALISTAIR)
	return has_flag(alistair_data, ACTIVE_FLAG)


def leliana_romanced(data):
	leliana_data = get_plot(data, quest_guid.APPROVAL_LELIANA)
	return  has_flag(leliana_data, ACTIVE_FLAG)

def zevran_romanced(data):
	zevran_data = get_plot(data, quest_guid.APPROVAL_ZEVRAN)
	return has_flag(zevran_data, ACTIVE_FLAG)

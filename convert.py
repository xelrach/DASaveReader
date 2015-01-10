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

"""Convert a save file into a dict of plot GUIDs to flags"""

from __future__ import print_function

import sys
from pygff.lazy import LazyGFF4
from io import BytesIO

import choice.plot as plot
from choice.save_data import SaveData

PLAYER_CHAR = 16002
PLAYER_CHAR_CHAR = 16208
STATS = 16209
STAT_LIST = 16350
STAT_BASE = 16300
STAT_INDEX = 16353
CLASS_INDEX = 27
APPEARANCE = 16320
GENDER = 16322
RACE = 16460
PARTY_LIST = 16003
PLOT_MANAGER = 16400
PLOT_LIST = 16401
PLOT_GUID = 16402
PLOT_FLAGS_1 = 16403
PLOT_FLAGS_2 = 16404
PLOT_FLAGS_3 = 16405
PLOT_FLAGS_4 = 16406

def convert_file(filename):
	"""Open a save file and convert it into a dict of GUID to plot"""
	data, _ = open_file(filename)
	results = convert_data(data)
	return results

def open_file(filename):
	"""Open and parse a GFF file"""
	with open(filename, 'rb') as handle:
		mem = BytesIO(handle.read())
	gff = LazyGFF4(mem)
	return gff.root, gff.header

def convert_data(data):
	"""Convert GFF data into a dict of GUID to plot"""
	results = SaveData()

	# Pull quests
	quests = data[PARTY_LIST][PLOT_MANAGER][PLOT_LIST]
	for quest in quests:
		guid = str(quest[PLOT_GUID]).rstrip("\0")
		saved_plot = plot.plot(quest[PLOT_FLAGS_1], quest[PLOT_FLAGS_2], quest[PLOT_FLAGS_3], \
			quest[PLOT_FLAGS_4])
		results.set_plot(guid, saved_plot)

	# Pull race, class, gender
	player = data[PLAYER_CHAR][PLAYER_CHAR_CHAR]
	results.set_race(player[RACE])
	results.set_gender(player[APPEARANCE][GENDER])
	for stat in player[STATS][STAT_LIST]:
		if stat[STAT_INDEX] == CLASS_INDEX:
			results.set_class(int(stat[STAT_BASE]))
			break

	return results

if __name__ == '__main__':
	save_filename = sys.argv[1]
	print(convert_file(save_filename))

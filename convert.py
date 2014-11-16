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

import sys
from pygff.lazy import LazyGFF4
from cStringIO import StringIO

import choice.plot

PARTY_LIST = 16003
PLOT_MANAGER = 16400
PLOT_LIST = 16401
PLOT_GUID = 16402
PLOT_FLAGS_1 = 16403
PLOT_FLAGS_2 = 16404
PLOT_FLAGS_3 = 16405
PLOT_FLAGS_4 = 16406

def convert_file(filename):
  data, header = open_file(filename)
  results = convert_data(data)
  return results

def open_file(filename):
  with open(filename, 'rb') as f:
      mem = StringIO(f.read())
  gff = LazyGFF4(mem)
  return gff.root, gff.header

def convert_data(data):
  results = {}
  quests = data[PARTY_LIST][PLOT_MANAGER][PLOT_LIST]
  for quest in quests:
    guid = str(quest[PLOT_GUID]).rstrip("\0")
    p = choice.plot.plot(quest[PLOT_FLAGS_1], quest[PLOT_FLAGS_2], quest[PLOT_FLAGS_3], quest[PLOT_FLAGS_4])
    results[guid] = p
  return results

if __name__ == '__main__':
  filename = sys.argv[1]
  print(convert_file(filename))

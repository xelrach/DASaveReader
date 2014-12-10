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

import inspect
import sys

import choice.quests
import convert

class quest_result:
	def __init__(self, name, order, results):
		self.name = name
		self.order = order
		self.results = results

def read(filename):
	"""Reads a save file and returns the choices made"""
	data = convert.convert_file(filename)
	results = get_results(data)
	return results

def format_results(results):
	"""Formats the results for CLI output"""
	formatted = ""
	for result in results:
		formatted += result.name + "\n"
		for subquest in result.results:
			formatted += "  " + subquest.title + "\n"
			formatted += "    " + subquest.result + "\n"
		formatted += "\n"
	return formatted

def get_results(data):
	"""Takes a dict of GUID to plot and returns the choices that were made"""
	results = []
	quests = inspect.getmembers(choice.quests, inspect.isclass)
	for _, quest in quests:
		results.append(quest_result(quest.get_name(), quest.ORDER, \
				choice.quests.get_quest_results(data, quest)))
	results.sort(key = lambda result: result.order)

	return results

if __name__ == "__main__":
	quest_results = read(sys.argv[1])
	print(format_results(quest_results))

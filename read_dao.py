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

def read(filename):
	data = convert.convert_file(filename)
	results = get_results(data)
	return format_results(results)

def format_results(results):
	formatted = ""
	for quest_name, quest_results in results.iteritems():
		formatted += quest_name + "\n"
		for subquest in quest_results:
			formatted += "  " + subquest.title + "\n"
			formatted += "    " + subquest.result + "\n"
		formatted += "\n"
	return formatted


def get_results(data):
	results = {}
	quests = inspect.getmembers(choice.quests, inspect.isclass)
	for quest_name, quest in quests:
		quest_results = []
		for side_quest_name, side_quest in quest.get_side_quests():
			result = side_quest.get_result(data)
			quest_results.append(result)
		quest_results.sort(key=lambda result: result.order)
		results[quest.get_name()] = quest_results

	return results

if __name__ == "__main__":
	results = read(sys.argv[1])
	print(results)

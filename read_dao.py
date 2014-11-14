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

def main(args):
	data = {}
	results = get_results(data)
	print_results(results)

def print_results(results):
	for quest_name, quest_results in results.iteritems():
		print(quest_name)
		for subquest in quest_results:
			print("  " + subquest.title)
			print("    " + subquest.result)
		print("")


def get_results(data):
	results = {}
	quests = inspect.getmembers(choice.quests, inspect.isclass)
	for quest_name, quest in quests:
		quest_results = []
		for side_quest_name, side_quest in quest.get_side_quests():
#			quest_results[side_quest.TITLE] = side_quest.get_result(data)
			result = side_quest.get_result(data)
			quest_results.append(result)
		quest_results.sort(key=lambda result: result.order)
		results[quest.get_name()] = quest_results

	return results

if __name__ == "__main__":
	main(sys.argv)

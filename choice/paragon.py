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

# Paragon of Her Kind and Orzammar choices

import quest_guid
import result

class paragon_of_her_kind:
	ORDER = 0
	TITLE = "Who Rules"
	def get_result(data):
		HARROWMONT = 1234
		BHELEN = 1235
		quest_data = data[quest_guid.PARAGON_OF_HER_KIND]
		if (quest_data & HARROWMONT):
			return "123 Harrowmont Rules"
		if (quest_data & BHELEN):
			return "123 Bhelen Rules"
		return result.DEFAULT

class the_chant_in_the_deep:
	ORDER = 1
	TITLE = "Channtry?"
	def get_result(data):
		quest_data = data[quest_guid.THE_CHANT_IN_THE_DEEPS]

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

import numbers

class side_quest_response:
	result = ""

	def __init__(self, order, title):
		if not isinstance(order, numbers.Number):
			raise ValueError(str(order) + " is not a number")
		if not isinstance(title, basestring):
			raise ValueError(str(title) + " is not a string")
		self.order = order
		self.title = title

	def __repr__(self):
		return self.title + ": " + self.result

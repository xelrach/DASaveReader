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

class plot:
	def __init__(self, flags1, flags2 = 0, flags3 = 0, flags4 = 0):
		self.flags1 = flags1
		self.flags2 = flags2
		self.flags3 = flags3
		self.flags4 = flags4

	def __repr__(self):
		return "plot: [" + str(self.flags1) + ", " + str(self.flags2) \
				+ ", " + str(self.flags3) + ", " + str(self.flags4) + "]"

	def __eq__(self, other):
		return self.flags1 == other.flags1 and self.flags2 == other.flags2 \
				and self.flags3 == other.flags3 and self.flags4 == other.flags4

	def __ne__(self, other):
		return not self.__eq__(other)

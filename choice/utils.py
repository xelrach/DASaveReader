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

import plot

def has_flag(match_plot, flag):
	if flag < 32:
		return bool((2**flag) & match_plot.flags1)
	elif flag < 64:
		return bool((2**(flag - 32)) & match_plot.flags2)
	elif flag < 96:
		return bool((2**(flag - 64)) & match_plot.flags3)
	elif flag < 128:
		return bool((2**(flag - 96)) & match_plot.flags4)
	else:
		raise ValueError("flag is over 127")

def get_plot(data, guid):
	return data.get(guid, plot.plot(0, 0, 0, 0))

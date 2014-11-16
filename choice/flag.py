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

def has_flag(plot, flag):
	if flag < 32:
		return (2**flag) & plot.flags1
	elif flag < 64:
		return (2**(flag-32)) & plot.flags2
	elif flag < 96:
		return (2**(flag-64)) & plot.flags3
	elif flag < 128:
		return (2**(flag-96)) & plot.flags4
	else:
		raise ValueError("flag is over 127")

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

# Prolog choices

import quest_guid
import result

class prisoner:
	ORDER = 0
	TITLE = "What did the Warden do with the hungry deserter in Ostagar?"
	LEFT = "Ostagar prisoner left alone"
	KILLED = "Ostagar prisoner killed"
	FED_STOLEN = "Fed Ostagar prisoner stolen food"
	FED_SHARED = "Fed Ostagar prisoner guard's lunch"
	FED_BOUGHT = "Bought food to feed Ostagar prisoner"
	STOLE = "Key stolen from Ostagar prisoner"

class mabari:
	ORDER = 1
	TITLE = "What did the Warden do with the mabari hound in Ostagar?"
	NOTHING = "Didn't help mabari hound"
	CURED = "Cured mabari hound"
	KILLED = "Put mabari hound out of its misery"

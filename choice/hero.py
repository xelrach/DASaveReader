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

# Hero choices

import quest_guid
import result
import responses

class hero:
	ORDER = 0
	TITLE = "Hero"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(hero.ORDER, hero.TITLE)

		response.result = result.INCOMPLETE
		return response

class hero_alive:
	ORDER = 1
	TITLE = "What happened to the Warden at the end of Dragon Age Origins?"
	ALIVE = "Warden alive & well"
	DEAD = "Warden died killing Archdemon"

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(hero_alive.ORDER, hero_alive.TITLE)

		response.result = result.INCOMPLETE
		return response

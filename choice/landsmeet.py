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

"""Landsmeet choices"""

import choice.result as result
import choice.responses as responses

import choice.companion.fate
from choice.companion.landsmeet import alistair_king, alistair_king_alone, \
		alistair_with_anora_queen, alistair_with_warden_queen, \
		anora_queen_alone, anora_with_warden_king

class landsmeet:
	ORDER = 0
	TITLE = "Who now rules Ferelden?"

	ALISTAIR = "Alistair rules"
	ALISTAIR_ANORA = "Alistair & Anora rule"
	ALISTAIR_WARDEN = "Alistair & the Warden rule"
	ANORA = "Anora rules"
	ANORA_WARDEN = "Anora & the Warden rule"

	def __init__(self):
		raise NotImplementedError

	@staticmethod
	def get_result(data):
		response = responses.side_quest_response(landsmeet.ORDER, landsmeet.TITLE)
		response.result = result.DEFAULT

		if choice.companion.fate.alistair_dead(data):
			if alistair_king(data) or anora_queen_alone(data):
				response.result = landsmeet.ANORA
			elif anora_with_warden_king(data):
				response.result = landsmeet.ANORA_WARDEN
		else:
			if alistair_king_alone(data):
				response.result = landsmeet.ALISTAIR
			elif alistair_with_anora_queen(data):
				response.result = landsmeet.ALISTAIR_ANORA
			elif anora_queen_alone(data):
				response.result = landsmeet.ANORA
			elif anora_with_warden_king(data):
				response.result = landsmeet.ANORA_WARDEN
			elif alistair_with_warden_queen(data):
				response.result = landsmeet.ALISTAIR_WARDEN

		return response


class SaveData:
	quests = {}
	race = 0
	_class = 0
	gender = 0

	def set_plot(self, guid, plot):
		self.quests[guid] = plot

	def __getitem__(self, key):
		return self.quests[key]

	def get(self, key, default):
		return self.quests.get(key, default)

	def get_race(self):
		return self.race

	def set_race(self, race):
		self.race = race

	def get_class(self):
		return self._class

	def set_class(self, _class):
		self._class = _class

	def get_gender(self):
		return self.gender

	def set_gender(self, gender):
		self.gender = gender;

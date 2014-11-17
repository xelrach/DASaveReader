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

from os.path import expanduser
import wx
import wx.richtext

import da_reader

class reader_frame(wx.Frame):
	"""We simply derive a new class of Frame"""
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(640, 700))
		self.control = wx.richtext.RichTextCtrl(self, style = wx.TE_MULTILINE | wx.TE_READONLY)

		menu_bar = wx.MenuBar()
		self.SetMenuBar(menu_bar)

		file_menu = wx.Menu()
		menu_bar.Append(file_menu, "&File")

		menu_open = file_menu.Append(wx.ID_OPEN, "&Open", " Open save file")
		menu_exit = file_menu.Append(wx.ID_EXIT,"E&xit", " Terminate the program")

		self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)
		self.Bind(wx.EVT_MENU, self.on_open, menu_open)

		self.Show(True)

	def on_open(self, e):
		dlg = wx.FileDialog(self, "Choose a save file", expanduser("~"), "", "*.das", wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
				filename = dlg.GetPath()
				results = da_reader.read(filename)
				self.set_text(results)
		dlg.Destroy()

	def on_exit(self, e):
		self.Close(True)

	def set_text(self, results):
		for result in results:
			self.control.BeginBold()
			self.control.BeginUnderline()
			self.control.WriteText(result.name)
			self.control.EndBold()
			self.control.EndUnderline()
			self.control.Newline()
			for subquest in result.results:
				self.control.BeginBold()
				self.control.WriteText("  " + subquest.title)
				self.control.EndBold()
				self.control.Newline()
				self.control.BeginItalic()
				self.control.WriteText("    " + subquest.result)
				self.control.EndItalic()
				self.control.Newline()
			self.control.Newline()

app = wx.App(False)
frame = reader_frame(None, "Dragon Age Save Reader")
frame.Show(True)
app.MainLoop()

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os.path
from graphical import *
from extract import *

class Application(object):
	def __init__(self):
		self.__window = Graphical("Playlist extract")
		self.__user = Extractor()

	@property
	def window(self):
		return self.__window

	@property
	def user(self):
		return self.__user


if __name__ == '__main__':
	app = Application()
	new_listbox = app.window.create_listbox_from_list(app.window.main_window, app.user.playlist_list)
	new_listbox.pack()
	app.window.main_window.mainloop()

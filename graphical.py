#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk

class Application():
	def __init__(self):
		self.__main_window = tk.Tk()

	@property
	def main_window(self):
		return self.__main_window


if __name__ == '__main__':
	main_window = tk.Tk()

	playlist_list = tk.Listbox(main_window)
	playlist_list.insert(1, "Un truc calme")
	playlist_list.pack()

	main_window.mainloop()

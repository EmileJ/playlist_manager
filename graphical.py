#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk

class Graphical(object):
	def __init__(self, window_name):
		self.__main_window = tk.Tk()
		self.__buttons = [tk.Button(self.__main_window, text = "QUIT", command = quit).pack()]

	@property
	def main_window(self):
		return self.__main_window

	##
	## @brief      Creates a tk listbox object from a list of strings.
	##
	## @param      master  The master window
	## @param      l       The list
	##
	## @return     A tk listbox object containing the list. The object is not
	##             packed (use .pack() method from tkinter to pack it)
	##
	def create_listbox_from_list(self, master, l):
		new_listbox = tk.Listbox(master)
		for i in range(len(l)):
			new_listbox.insert(i, l[i])
		return new_listbox


if __name__ == '__main__':
	main_window = tk.Tk()

	playlist_list = tk.Listbox(main_window)
	playlist_list.insert(1, "Un truc calme")
	playlist_list.pack()

	main_window.mainloop()

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.filedialog
from extract import *

class Graphical(object):
	def __init__(self, window_name):
		self.main_window = tk.Tk()
		self.user = Extractor()

		self.playlist_listbox = tk.Listbox()
		self.playlist_listbox.grid(column = 0, columnspan = 2, row = 0)

		self.buttons = {
			tk.Button(self.main_window, text = "PLAYLIST", command = lambda : self.ask_for_file("your playlist folder")).grid(column = 0, row = 1),
			tk.Button(self.main_window, text = "QUIT", command = quit).grid(column = 1, row = 1)
		}
		self.__last_file_chosen_by_user = ""

	@property
	def last_file_chosen_by_user(self):
		return self.__last_file_chosen_by_user

	@last_file_chosen_by_user.setter
	def last_file_chosen_by_user(self, new_file):
		self.__last_file_chosen_by_user = new_file


	##
	## @brief      Adds a list of strings to a listbox. The listbox must be
	##             empty
	##
	## @param      l     The list
	## @param      lb    The listbox
	##
	## @return     The new listbox containing the list. If the listbox wasn't
	##             empty, returns the same listbox as passed as a paramter
	##
	def add_list_to_listbox(self, l, lb):
		if lb.size() > 0:
			return lb
		for i in range(len(l)):
			lb.insert(i, l[i])
		return lb

	##
	## @brief      Asks the user to open a file using tkinter. The chosen file
	##             is stored in the object's, accessible by using the
	##             get_last_chosen_file() method
	##
	## @param      file_name  The name of the file the program wants the user to
	##                        open
	##
	##
	def ask_for_file(self, file_name):
		# Lets the user choose a directory
		self.last_file_chosen_by_user = tk.filedialog.askdirectory(title = "Please choose where " + file_name + " is")
		# Lists the chosen directory
		self.user.playlist_list = self.last_file_chosen_by_user
		# Updates the listbox
		self.add_list_to_listbox(self.user.playlist_list, self.playlist_listbox)

	def get_last_chosen_file(self):
		if self.last_file_chosen_by_user == "":
			print("User has not chosen a file yet")
		else:
			return self._last_file_chosen_by_user()


if __name__ == '__main__':
	print("Do not launch this. Ever. Again.")

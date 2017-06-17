#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.filedialog
from extract import *


class AvailableWindows():
	def __init__(self):
		self.MAIN = "MAIN"
		self.PLAYLIST_SELECTED = "PLAYLIST_SELECTED"

class Graphical(object):
	def __init__(self, window_name):
		self.available_widows = AvailableWindows()

		# Inits
		self.root = tk.Tk()
		self.root.title(window_name)

		self.main_window = tk.Frame(self.root)
		self.main_window.grid(column = 0, row = 0)

		# Infos and functions related to the user
		self.user = Extractor()

		# When the program inits, the user is on the main window
		self.state = self.available_widows.MAIN

		self.__last_file_chosen_by_user = ""

		self.__createWidgets()

	@property
	def last_file_chosen_by_user(self):
		return self.__last_file_chosen_by_user

	@last_file_chosen_by_user.setter
	def last_file_chosen_by_user(self, new_file):
		self.__last_file_chosen_by_user = new_file



	##
	## @brief      Inits all the widgets on the window
	##
	def __createWidgets(self):
		# Inits the playlist's listbox
		self.playlist_listbox = tk.Listbox(self.main_window)
		self.playlist_listbox.grid(column = 0, columnspan = 2, row = 0)

		# Inits the clickeable buttons
		self.buttons = [
			tk.Button(self.main_window, text = "PLAYLIST", command = lambda : self.updatePlaylistButton("your playlist folder", 0)),
			tk.Button(self.main_window, text = "QUIT", command = quit)
		]
		self.buttons[0].grid(column = 0, row = 1)
		self.buttons[1].grid(column = 1, row = 1)


	##
	## @brief      Adds a list of strings to a listbox.
	##
	## @param      l     The list
	## @param      lb    The listbox
	##
	## @return     The new listbox containing the list.
	##
	def addListToListbox(self, l, lb):
		for i in range(len(l)):
			lb.insert(tk.END, l[i])
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
	def askForFile(self, file_name):
		# Lets the user choose a directory
		self.last_file_chosen_by_user = tk.filedialog.askdirectory(title = "Please choose where " + file_name + " is")
		# Lists the chosen directory
		self.user.playlist_list = self.last_file_chosen_by_user
		# Updates the listbox
		self.addListToListbox(self.user.playlist_list, self.playlist_listbox)

	def updatePlaylistButton(self, file_name, index):
		self.askForFile(file_name)
		self.state = self.available_widows.PLAYLIST_SELECTED
		# Disables the button
		self.buttons[index].config(state = tk.DISABLED)





if __name__ == '__main__':
	print("Do not launch this. Ever. Again.")

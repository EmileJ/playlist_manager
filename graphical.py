#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.filedialog
from extract import *

# Padding with window's borders applied on every TK widget
DEFAULT_PADDING = 10


class AvailableWindows():
	def __init__(self):
		self.MAIN = "MAIN"
		self.PLAYLIST_SELECTED = "PLAYLIST_SELECTED"

class Graphical(object):
	def __init__(self, window_name):
		self.available_widows = AvailableWindows()

		# Root window is the window where Tk is first set. We don't use it for an other reason
		# than intiating the main window wich contains all the elems
		self.root = tk.Tk()
		self.root.title(window_name)
		self.root.rowconfigure(0, weight = 1)
		self.root.columnconfigure(0, weight = 1)

		self.__initMainWindow(self.root.winfo_screenwidth(), self.root.winfo_screenheight())

		self.__initWidgets()

		# Infos and functions related to the user
		self.user = Extractor()

		# When the program inits, the user is on the main window
		self.state = self.available_widows.MAIN

		self.__last_file_chosen_by_user = ""


	@property
	def last_file_chosen_by_user(self):
		return self.__last_file_chosen_by_user

	@last_file_chosen_by_user.setter
	def last_file_chosen_by_user(self, new_file):
		if new_file != "":
			self.__last_file_chosen_by_user = new_file




	def __initMainWindow(self, w, h):
		"""Inits the main window containing all the widgets by creating
		a new attribute to the class

		Args:
		    w (int): The width of the widow
		    h (int): The height of the window
		"""

		self.main_window = tk.Frame(self.root, width = w, height = h)
		self.main_window.grid(column = 0, row = 0, sticky = tk.S+tk.E+tk.W+tk.N)
		# self.main_window.rowconfigure(0, weight = 1)
		self.main_window.columnconfigure(0, weight = 1)
		self.main_window.columnconfigure(1, weight = 3)

		self.main_window.grid_propagate(0)

	def __initWidgets(self):
		"""Inits all the widgets on the window by creating attributes to
		the class
		"""

		# Inits the clickeable buttons
		self.buttons = [
			tk.Button(self.main_window, text = "PLAYLIST", command = lambda : self.askForFile("your playlist folder")),
			tk.Button(self.main_window, text = "QUIT", command = quit)
		]
		# The grid method returns None, we can't concat this line with the initialisation of the buttons on the list above
		self.buttons[0].grid(column = 0, row = 0, sticky = tk.W)
		self.buttons[1].grid(column = 1, row = 0, sticky = tk.W)

		# Inits the playlist's listbox
		self.playlist_listbox = tk.Listbox(self.main_window, width = 50, selectmode = tk.SINGLE)
		self.playlist_listbox.grid(column = 0, columnspan = 2, row = 1, padx = DEFAULT_PADDING, sticky = tk.W)


	def updateListbox(self, l, lb):
		"""Resets and adds items contaned in a list to a TK listbox

		Args:
		    l (list): The list containg the items
		    lb (tkinter.Listbox): The listbox

		Returns:
		    tkinter.Listbox: The updated listbox
		"""

		lb.delete(0, tk.END)
		for i in range(len(l)):
			lb.insert(tk.END, l[i])
		return lb


	def askForFile(self, file_name = ""):
		"""Asks the user to open a file using tkinter. The chosen file
		is stored in the object as "last_file_chosen_by_user"

		Args:
		    file_name (str): The name of the file the program wants the user to open.
		    				 Please note that this string is only here to help the user by printing
		    				 a little headline in the selection box

		"""

		printed_string = ""
		if file_name = "":
			printed_string = "Please choose where the file is"
		else:
			printed_string = "Please choose where " + file_name + " is"

		# Lets the user choose a directory
		self.last_file_chosen_by_user = tk.filedialog.askdirectory(title = printed_string)
		# Lists the chosen directory
		self.user.playlist_list = self.last_file_chosen_by_user
		# Updates the listbox
		self.updateListbox(self.user.playlist_list, self.playlist_listbox)





if __name__ == '__main__':
	print("Do not launch this. Ever. Again.")

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import threading
import queue
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
from enum import Enum

from extract import *
from error import *

# Padding with window's borders applied on every TK widget
DEFAULT_PADDING = 10


class Folder(Enum):
	"""Describes the limited kind of folders this program has to manage.

	Attributes:
	    PLAYLIST_FOLDER (int): The folder where the user's playlists are stored
	    SOUNDS_DST (int): The destination of the sounds
	    SOUNDS_SRC (int): The source of the sounds
	"""
	PLAYLIST_FOLDER = 0
	SOUNDS_SRC = 1
	SOUNDS_DST = 2



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

		screen_width = self.root.winfo_screenwidth()
		if screen_width > 1500:
			screen_width = 1366
		screen_height = self.root.winfo_screenheight()
		if screen_height > 1500:
			screen_height = 768

		self.__initMainWindow(screen_width, screen_height)

		self.__initWidgets()

		# Infos and functions related to the user
		self.user = Extractor()

		# When the program inits, the user is on the main window
		self.state = self.available_widows.MAIN

		self.__playlist_chosen_by_user = ""


	@property
	def playlist_chosen_by_user(self):
		return self.__playlist_chosen_by_user

	@playlist_chosen_by_user.setter
	def playlist_chosen_by_user(self, new_file):
		if new_file != "":
			self.__playlist_chosen_by_user = new_file




	def __initMainWindow(self, w, h):
		"""Inits the main window containing all the widgets by creating
		a new attribute to the class

		Args:
		    w (int): The width of the widow
		    h (int): The height of the window
		"""

		self.main_window = tk.Frame(self.root, width = w, height = h)
		self.main_window.grid(column = 0, row = 0, sticky = tk.S+tk.E+tk.W+tk.N)

		# Sets the size of each row
		self.main_window.rowconfigure(0, weight = 1)
		self.main_window.rowconfigure(1, weight = 1)
		self.main_window.rowconfigure(2, weight = 1)
		self.main_window.rowconfigure(3, weight = 1)
		self.main_window.rowconfigure(4, weight = 1)
		self.main_window.rowconfigure(5, weight = 1)
		self.main_window.rowconfigure(6, weight = 1)
		self.main_window.rowconfigure(7, weight = 1)
		self.main_window.rowconfigure(8, weight = 10)

		# Sets the size of each column
		self.main_window.columnconfigure(0, weight = 1)
		self.main_window.columnconfigure(1, weight = 2)
		self.main_window.columnconfigure(2, weight = 1)
		self.main_window.columnconfigure(3, weight = 3)
		self.main_window.columnconfigure(4, weight = 2)
		self.main_window.columnconfigure(5, weight = 3)

		self.main_window.grid_propagate(0)

	def __initWidgets(self):
		"""Inits all the widgets on the window by creating attributes to
		the class
		"""

		self.buttons = {
			'playlist' : tk.Button(self.main_window, text = "PLAYLIST",
				command = lambda : self.askForFile(Folder.PLAYLIST_FOLDER, file_name = "your playlist folder")),
			'sounds_source' : tk.Button(self.main_window, text = "SOURCE",
				command = lambda : self.askForFile(Folder.SOUNDS_SRC, file_name = "your sounds source folder")),
			'sounds_destination' : tk.Button(self.main_window, text = "DESTINATION",
				command = lambda : self.askForFile(Folder.SOUNDS_DST, file_name = "your sounds destination folder")),
			'extract' : tk.Button(self.main_window, text = "EXTRACT",
				command = lambda : self.errorHandlerMessageBox(lambda : self.user.copyPlaylist(self.playlist_chosen_by_user)))
		}
		# Place the buttons
		self.buttons['playlist'].grid(column = 0, row = 1, padx = DEFAULT_PADDING, sticky = tk.W)
		self.buttons['sounds_source'].grid(column = 0, row = 3, padx = DEFAULT_PADDING, sticky = tk.W)
		self.buttons['sounds_destination'].grid(column = 0, row = 5, padx = DEFAULT_PADDING, sticky = tk.W)
		self.buttons['extract'].grid(column = 3, row = 7, pady = DEFAULT_PADDING, sticky = tk.N)

		self.labels = {
			'playlist' : tk.Label(self.main_window, background = '#fff', relief = tk.SUNKEN),
			'sounds_source' : tk.Label(self.main_window, background = '#fff', relief = tk.SUNKEN),
			'sounds_destination' : tk.Label(self.main_window, background = '#fff', relief = tk.SUNKEN)
		}
		self.labels['playlist'].grid(column = 1, row = 1, columnspan = 3, padx = DEFAULT_PADDING, sticky = tk.W+tk.E)
		self.labels['sounds_source'].grid(column = 1, row = 3, columnspan = 3, padx = DEFAULT_PADDING, sticky = tk.W+tk.E)
		self.labels['sounds_destination'].grid(column = 1, row = 5, columnspan = 3, padx = DEFAULT_PADDING, sticky = tk.W+tk.E)


		self.listboxs = {
			'playlists' : tk.Listbox(self.main_window, selectmode = tk.SINGLE),
			'sounds' : tk.Listbox(self.main_window, selectmode = tk.MULTIPLE)
		}

		# Place the listboxs
		self.listboxs['playlists'].grid(column = 0, columnspan = 3, row = 7, rowspan = 2, padx = DEFAULT_PADDING, pady = DEFAULT_PADDING, sticky = tk.W+tk.N+tk.S+tk.E)
		self.listboxs['sounds'].grid(column = 4, columnspan = 2, row = 7, rowspan = 2, padx = DEFAULT_PADDING, pady = DEFAULT_PADDING, sticky = tk.W+tk.N+tk.S+tk.E)

	def updateListbox(self, l, lb):
		"""Resets and adds items contaned in a list to a TK listbox

		Args:
		    l (list): The list containg the items
		    lb (tkinter.Listbox): The listbox
		"""

		lb.delete(0, tk.END)
		for i in range(len(l)):
			lb.insert(tk.END, l[i])


	def errorHandlerMessageBox(self, f):
		"""Prints an error message if an error is raised during the call to the f function

		Args:
		    f (function): The function to be called
		"""
		try:
			f()

		# Manages critical errors
		except FileError as e:
			tk.messagebox.showerror("ERROR: File not found", e)
		except FolderError as e:
			tk.messagebox.showerror("ERROR: Folder not found", e)

		# Manages warnings
		except NotImplementedError as e:
			tk.messagebox.showwarning("WARNING: No directory created", e)





	def __getAndUpdateListbox(self, event):
		"""Updates the sounds listbox when the user clicks on a playlist

		Args:
		    event (tkinter.Event): The event passed by tkinter. Not used in this function
		"""

		# Gets the full path of the playlist's location
		playlist_full_path = self.user.playlist_src + "/" + self.listboxs['playlists'].get(tk.ACTIVE)
		self.playlist_chosen_by_user = playlist_full_path

		# If the playlist was not already listed
		if self.user.files_in_playlist.get(playlist_full_path) is None:
			# Lists the files contained in the playlist
			self.user.files_in_playlist[playlist_full_path] = self.user.getFilesInPlaylist(playlist_full_path)

			# Cleans the playlist with all the unwanted strings
			self.user.files_in_playlist[playlist_full_path] = self.user.cleanList(self.user.files_in_playlist[playlist_full_path], delete_extension = True)
			self.user.files_in_playlist[playlist_full_path].sort()

		# Updates the sounds listbox
		self.updateListbox(self.user.files_in_playlist[playlist_full_path], self.listboxs['sounds'])


	def askForFile(self, required_folder, file_name = ""):
		"""Asks the user to open a file using tkinter.

		Args:
			required_folder (Folder): The type of folder required
		    file_name (str): The name of the file the program wants the user to open.

		"""

		printed_string = ""

		if file_name == "":
			printed_string = "Please choose where the file is"
		else:
			printed_string = "Please choose where " + file_name + " is"

		# Lets the user choose a directory
		user_folder = tk.filedialog.askdirectory(title = printed_string)

		if required_folder == Folder.PLAYLIST_FOLDER:
			self.user.playlist_list = user_folder # Updates the users info
			self.updateListbox(self.user.playlist_list, self.listboxs['playlists']) # Updates the playlists listbox
			self.labels['playlist'].configure(text = user_folder)

			# When the user clicks on a playlist in the listbox, updates self.playlist_chosen_by_user
			self.listboxs['playlists'].bind('<<ListboxSelect>>', self.__getAndUpdateListbox)

		elif required_folder == Folder.SOUNDS_SRC:
			self.user.sounds_src = user_folder
			self.labels['sounds_source'].configure(text = user_folder)

		elif required_folder == Folder.SOUNDS_DST:
			self.user.sounds_dst = user_folder







if __name__ == '__main__':
	print("Do not launch this. Ever. Again.")

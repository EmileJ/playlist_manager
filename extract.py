#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys # Useful everywhere
import os.path # Manage file's paths
import queue # Used for threading
from os import mkdir # Create directories
from shutil import copy2 as copy_file
from enum import Enum # Allow enumerations

from error import *


# List of the available audio file extensions.
BAD_EXTENSIONS = [".mp3", ".wav", ".ogg", ".wma"]

"""Colors the print() function

Values:
    BLUE (str): Blue color
    BOLD (str): Bold text
    ENDC (str): Ends coloring
    FAIL (str): Red color
    GREEN (str): Green color
    PINK (str): Pink color
    UNDERLINE (str): Underline text
    YELLOW (str): Yellow color
"""
COLORS = {
	'GREEN' : '\033[92m',
	'BLUE' : '\033[94m',
	'PINK' : '\033[95m',
	'YELLOW' : '\033[93,m',
	'BOLD' : '\033[1m',
	'UNDERLINE' : '\03,3[4m',
	'FAIL' : '\033[91m',
	'ENDC' : '\033[0m' # Ends the colored string
}

##
## @brief      Default settings for playlist (will be removed later)
##
class DefaultSettings(object):
	def __init__(self):
		self.DEFAULT_PLAYLIST_SRC = "/home/emile/Documents/programmation/python/playlist_manager/playlist"
		self.DEFAULT_SOUNDS_DST = "/home/emile/Documents/programmation/python/playlist_manager/sounds"
		self.DEFAULT_SOUNDS_SRC = "/home/emile/Musique/"
		self.DEFAULT_DELETABLE_STRING = "/storage/9016-4EF8/Sounds/"



class Setup(object):
	"""Informations about the user's setup: where are his playlists,
	where are the source of his sounds, where does he want to copy
	his sounds to

	Attributes:
	    deletable_string (str): TO BE REMOVED
	    playlist_src (str): The full path to the directory where playlists are stored
	    sounds_dst (str): The full path to the directory where sounds will be copied
	    sounds_src (str): The full path to the directory where sounds are stored
	"""
	def __init__(self, playlist_src, sounds_src, sounds_dst, deletable_string):
		self.playlist_src = playlist_src
		self.sounds_src = sounds_src
		self.sounds_dst = sounds_dst
		self.deletable_string = deletable_string




class Extractor(Setup):
	"""This object's purpose is to extract sounds contained in a playlist

	Attributes:
	    playlist_src (str): Inherited by the Setup object
	    files_in_playlist (dict): Contains lists of files in playlists. Keys are the playlists names
	"""

	def __init__(self, playlist_src = DefaultSettings().DEFAULT_PLAYLIST_SRC, sounds_src = DefaultSettings().DEFAULT_SOUNDS_SRC, sounds_dst = DefaultSettings().DEFAULT_SOUNDS_DST, deletable_string = DefaultSettings().DEFAULT_DELETABLE_STRING):
		super().__init__(playlist_src, sounds_src, sounds_dst, deletable_string)
		self.__playlist_list = os.listdir(self.playlist_src)
		self.files_in_playlist = {}


	@property
	def playlist_list(self):
		"""This private attribute is a list of the files contained in the folder self.playlist_src
		"""
		return self.__playlist_list

	@playlist_list.setter
	def playlist_list(self, directory):
		self.playlist_src = directory
		self.__playlist_list = os.listdir(directory)


	def getFilesInPlaylist(self, playlist):
		"""Gets the path to the files contained in a playlist and puts it into a
		python list

		Args:
		    playlist (str): The full path to the playlist

		Returns:
		    list: A list of strings corresponding to the full path of the files in the playlist. Empty list if the playlist argument is not valid
		"""

		if playlist is "":
			raise FileError("ERROR: The playlist is not selected")
			return []
		if not playlist.endswith(".txt"):
			raise FileError("ERROR: The playlist is not ending with \".txt\"")
			return []

		l = []
		f = open(playlist, "r")
		for line in f:
			l = l + [line.strip('\n')]
		f.close()

		return l


	def cleanList(self, list_to_be_cleaned, delete_extension = False):
		"""Cleans a list of strings using this method:
		Removes the local, unwanted file's path written in the
		playlist. Sanitzes the string too (deletes \n).

		Args:
		    list_to_be_cleaned (list): A list of strings to be cleaned

		Returns:
		   list: A list of the cleaned strings contained in the playlist
		"""

		cleaned_list = []
		for i in list_to_be_cleaned:
			cleaned_file = os.path.basename(i.strip('\n'))
			if delete_extension:
				for i in BAD_EXTENSIONS:
					cleaned_file = cleaned_file.strip(i)
			cleaned_list = cleaned_list + [cleaned_file]
		return cleaned_list



	def __putSourcePathWithList(self, list_of_files_in_playlist):
		"""Concatenates the sounds source folder's name with all the
		file's names

		Args:
		    list_of_files_in_playlist (list): A list of strings corresponding to the file's names

		Returns:
		    list: A list of string corresponding to all the concatenations of the source path and the file's names. Empty list if error.
		"""

		if self.sounds_src is "":
			raise FolderError("ERROR: No source for sounds was defined")
			return []

		l = []
		for i in list_of_files_in_playlist:
			l = l + [self.sounds_src + i]
		return l


	def printPlaylist(self, playlist):
		"""Prints the files contained in a playlist

		Args:
		    playlist (str): The full path to the playlist to copy
		"""
		files_list = self.getFilesInPlaylist(playlist)
		for i in self.cleanList(files_list):
			print(i)


	def copyPlaylist(self, playlist):
		"""Copy the playlist to the folder specified in the class's
		private arguments

		Args:
		    playlist (str): The full path to the playlist to copy

		Returns:
			NoneType: Returns None if an error is encountered
		"""

		if self.sounds_dst is "":
			raise FolderError("ERROR: No destination folder was defined")
			return None

		try:
			files_list = self.getFilesInPlaylist(playlist)
		except:
			raise # Re-raises the last raise again, so the error handler can catch the exception
			return None

		playlist_basename = os.path.basename(playlist)
		print(COLORS['PINK'] + "Copying playlist : " + playlist_basename + COLORS['ENDC'])

		files_names = self.cleanList(files_list) # Name of the files, solely
		list_of_files_with_path = self.__putSourcePathWithList(files_names) # Name of the source folder's path concatenated with files names

		file_count = 0
		copied_files = 0

		local_dst = self.sounds_dst + "/" + playlist_basename

		try:
			mkdir(local_dst)
		except NotImplementedError:
			print(COLORS['YELLOW'] + "The mkdir method is not implemented by the kernel. No directory was created" + COLORS['ENDC'])
			local_dst = "." # Resets the destination of the copy to the current folder
		except FileExistsError:
			pass

		for i in list_of_files_with_path:
			current_file = files_names[file_count]
			try:
				if not os.path.exists(i):
					raise FileNotFoundError
				copy_file(i, local_dst + "/" + current_file)
			except FileNotFoundError:
				try:
					# Tries again with no "/" added
					copy_file(i, local_dst + current_file)
				except FileNotFoundError:
					print(COLORS['FAIL'] + "FILE NOT FOUND: " + current_file.strip(".mp3") + COLORS['ENDC'])
					continue
			finally:
				file_count += 1

			print(COLORS['GREEN'] + "File number " + str(file_count) + " successfully copied : " + str(current_file).strip(".mp3") + COLORS['ENDC'])
			copied_files += 1
		print(COLORS['YELLOW'] + "This program successfully copied " + str(copied_files) + " files out of " + str(file_count) + COLORS['ENDC'])




if __name__ == '__main__':
	print("You can't launch this")
	sys.exit(0)

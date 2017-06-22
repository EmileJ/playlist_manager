#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys # Useful everywhere
import os.path # Manage file's paths
from os import mkdir # Create directories
from shutil import copy2 as copy_file


##
## @brief      Default settings for playlist (will be removed later)
##
class DefaultSettings(object):
	def __init__(self):
		self.DEFAULT_PLAYLIST_SRC = "/home/emile/Documents/programmation/python/playlist_manager/playlist"
		self.DEFAULT_SOUNDS_DST = "/home/emile/Documents/programmation/python/playlist_manager/sounds"
		self.DEFAULT_SOUNDS_SRC = "/home/emile/Musique/"
		self.DEFAULT_DELETABLE_STRING = "/storage/9016-4EF8/Sounds/"


##
## @brief      Colors inside the print() function
##
class Colors(object):
	def __init__(self):
		self.GREEN = '\033[92m'
		self.BLUE = '\033[94m'
		self.PINK = '\033[95m'
		self.YELLOW = '\033[93m'
		self.BOLD = '\033[1m'
		self.UNDERLINE = '\033[4m'
		self.FAIL = '\033[91m'
		self.ENDC = '\033[0m' # Ends the colored string


##
## @brief      Informations about the user's setup: where are his playlists,
##             where are the source of his sounds, where does he want to copy
##             his sounds to
##
class Setup(object):
	def __init__(self, playlist_src, sounds_src, sounds_dst, deletable_string):
		self.__playlist_src = playlist_src
		self.sounds_src = sounds_src
		self.sounds_dst = sounds_dst
		self.deletable_string = deletable_string

	@property
	def playlist_src(self):
		return self.__playlist_src

	@playlist_src.setter
	def playlist_src(self, new_src):
		self.__playlist_src = new_src

##
## @brief      Contains the list of the files contained in the playlsit folder
##             and in the sounds folder
##
class Extractor(Setup):
	default_setting = DefaultSettings()
	def __init__(self, playlist_src = default_setting.DEFAULT_PLAYLIST_SRC, sounds_src = default_setting.DEFAULT_SOUNDS_SRC, sounds_dst = default_setting.DEFAULT_SOUNDS_DST, deletable_string = default_setting.DEFAULT_DELETABLE_STRING):
		super().__init__(playlist_src, sounds_src, sounds_dst, deletable_string)
		self.__playlist_list = os.listdir(self.playlist_src)
		# Allows the concatenation of the playlist's location with its name
		self.playlist_list_with_path = [self.playlist_src + "/" + p for p in self.playlist_list]
		self.colors = Colors()

	@property
	def playlist_list(self):
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
		    list: A list of strings corresponding to the full path of the files in the playlist
		"""

		l = []
		if not playlist.endswith(".txt"):
			raise TypeError("The playlist is not ending with \".txt\"")
			sys.exit(1)
		f = open(playlist, "r")
		for line in f:
			l = l + [line.strip('\n')]
		f.close()
		return l


	def __cleanList(self, playlist):
		"""Cleans a list of strings using this method:
		Removes the local, unwanted file's path written in the
		playlist. Sanitzes the string too (deletes \n).

		Args:
		    playlist (TYPE): The full path to the playlist

		Returns:
		   list: A list of the cleaned strings contained in the playlist
		"""

		cleaned_list = []
		for i in self.getFilesInPlaylist(playlist):
			cleaned_list = cleaned_list + [i.replace(self.deletable_string, "").strip('\n')]
		return cleaned_list



	def __putSourcePathWithList(self, files_in_playlist):
		"""Concatenates the sounds source folder's name with all the
		file's names

		Args:
		    files_in_playlist (list): A list of strings corresponding to the file's names

		Returns:
		    list: A list of string corresponding to all the concatenations of the source path and the file's names
		"""

		l = []
		for i in files_in_playlist:
			l = l + [self.sounds_src + file_name]
		return l


	def printPlaylist(self, playlist):
		"""Prints the files contained in a playlist

		Args:
		    playlist (str): The full path to the playlist to copy
		"""
		for i in self.__cleanList(playlist):
			print(i)


	def copyPlaylist(self, playlist):
		"""Copy the playlist to the folder specified in the class's
		private arguments

		Args:
		    playlist (str): The full path to the playlist to copy
		"""

		playlist_basename = os.path.basename(playlist)
		print(self.colors.PINK + "Copying playlist : " + playlist_basename + self.colors.ENDC)

		# These 2 lists have the same length, so we can use files_names[i]
		# when i parses files_in_playlist
		files_names = self.__cleanList(playlist) # Name of the files, solely
		files_in_playlist = self.__putSourcePathWithList(files_names) # Name of the source folder's path concatenated with files names

		file_count = 0
		copied_files = 0

		local_dst = self.sounds_dst + "/" + playlist_basename

		try:
			mkdir(local_dst)
		except NotImplementedError:
			print(self.colors.YELLOW + "The mkdir method is not implemented by the kernel. No directory was created" + self.colors.ENDC)
		except FileExistsError:
			pass

		for i in files_in_playlist:
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
					print(self.colors.FAIL + "FILE NOT FOUND: " + current_file.strip(".mp3") + self.colors.ENDC)
					continue
			finally:
				file_count += 1

			print(self.colors.GREEN + "File number " + str(file_count) + " successfully copied : " + str(current_file).strip(".mp3") + self.colors.ENDC)
			copied_files += 1
		print(self.colors.YELLOW + "This program successfully copied " + str(copied_files) + " files out of " + str(file_count) + self.colors.ENDC)




if __name__ == '__main__':
	user = Extractor()
	colors = Colors()
	for l in user.playlist_list_with_path:
		user.copyPlaylist(l)

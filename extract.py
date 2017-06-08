#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys # Useful everywhere
import os.path # Manage file's paths
from os import mkdir # Create directories
from shutil import copy2 # Copy files


DEFAULT_PLAYLIST_SRC = "/home/emile/Documents/Programmation/C/playlist_extract/playlist"
DEFAULT_SOUNDS_DST = "/home/emile/Documents/Programmation/C/playlist_extract/sounds/"
DEFAULT_SOUNDS_SRC = "/home/emile/Musique/"
DEFAULT_DELETABLE_STRING = "/storage/9016-4EF8/Sounds/"


class Colors():
	def __init__(self):
		self.ENDC = '\033[0m'
		self.OKGREEN = '\033[92m'
		self.FAIL = '\033[91m'
		self.OKBLUE = '\033[94m'
		self.HEADER = '\033[95m'
		self.WARNING = '\033[93m'
		self.BOLD = '\033[1m'
		self.UNDERLINE = '\033[4m'


##
## @brief      Informations about the user's setup: where are his playlists,
##             where are the source of his sounds, where does he want to copy
##             his sounds to
##
class Setup():
	def __init__(self, playlist_src = DEFAULT_PLAYLIST_SRC, sounds_src = DEFAULT_SOUNDS_SRC, sounds_dst = DEFAULT_SOUNDS_DST, deletable_string = DEFAULT_DELETABLE_STRING):
		self.__playlist_src = playlist_src
		self.__sounds_src = sounds_src
		self.__sounds_dst = sounds_dst
		self.__deletable_string = deletable_string

	@property
	def playlist_src(self):
		return self.__playlist_src
	@property
	def sounds_src(self):
		return self.__sounds_src
	@property
	def sounds_dst(self):
		return self.__sounds_dst
	@property
	def deletable_string(self):
		return self.__deletable_string


##
## @brief      Contains the list of the files contained in the playlsit folder
##             and in the sounds folder
##
class Extractor(Setup):
	def __init__(self, playlist_src = DEFAULT_PLAYLIST_SRC, sounds_src = DEFAULT_SOUNDS_SRC, sounds_dst = DEFAULT_SOUNDS_DST, deletable_string = DEFAULT_DELETABLE_STRING):
		super().__init__(playlist_src, sounds_src, sounds_dst, deletable_string)
		# Permet la concaténation du chemin du fichier avec son nom
		self.__playlist_list = [self.playlist_src + "/" + p for p in os.listdir(self.playlist_src)]

	@property
	def playlist_list(self):
		return self.__playlist_list


	##
	## @brief      Gets the files contained in a playlist and puts it into a
	##             python list
	##
	## @param      playlist  The playlist
	##
	## @return     The list matching the playlist
	##
	def get_files_in_playlist(self, playlist):
		l = []
		if not playlist.endswith(".txt"):
			raise TypeError("The playlist is not ending with \".txt\"")
			sys.exit(1)
		f = open(playlist, "r")
		for line in f:
			l = l + [line.strip('\n')]
		f.close()
		return l


	##
	## @brief      Removes the local, unwanted file's path written in the
	##             playlist. Sanitzes the string too.
	##
	## @param      name  The name of the file to clean
	##
	## @return     The cleaned name
	##
	def __clean_name(self, name):
		return name.replace(self.deletable_string, "").strip('\n')


	##
	## @brief      Cleans a list of strings as specified upper
	##
	## @param      playlist  The playlist to clean
	##
	## @return     A list of cleaned strings
	##
	def __clean_list(self, playlist):
		cleaned_list = []
		for i in self.get_files_in_playlist(playlist):
			cleaned_list = cleaned_list + [self.__clean_name(i)]
		return cleaned_list


	##
	## @brief      Concatenates the sounds source folder's name with the file's
	##             name
	##
	## @param      file_name  The file's name
	##
	## @return     A string corresponding to the concatenation
	##
	def __put_correct_path_with_file(self, file_name):
		return self.sounds_src + file_name


	##
	## @brief      Concatenates the sounds source folder's name with all the
	##             file's names
	##
	## @param      files_in_playlist  The files in playlist
	##
	## @return     A list of string corresponding to all the concatenations
	##
	def __put_correct_path_(self, files_in_playlist):
		l = []
		for i in files_in_playlist:
			l = l + [self.__put_correct_path_with_file(i)]
		return l


	##
	## @brief      Prints the files contained in a playlist
	##
	## @param      playlist  The playlist
	##
	def print_playlist(self, playlist):
		for i in self.__clean_list(playlist):
			print(i)


	##
	## @brief      Copy the playlist to the folder specified in the class's
	##             private arguments
	##
	## @param      playlist  The playlist to copy
	##
	def copy_playlist(self, playlist):
		playlist_basename = os.path.basename(playlist)
		print(colors.HEADER + "Copying playlist : " + playlist_basename + colors.ENDC)

		# These 2 lists have the same length, so we can use files_names[i]
		# when i parses files_in_playlist
		files_names = self.__clean_list(playlist) # Name of the files, solely
		files_in_playlist = self.__put_correct_path_(files_names) # Names of the path concatenated with names of the files

		file_count = 0
		copied_files = 0

		local_dst = self.sounds_dst + playlist_basename

		try:
			os.mkdir(local_dst)
		except NotImplementedError:
			print(colors.WARNING + "The mkdir method wasn't implemented. No directory was created" + colors.ENDC)
		except FileExistsError:
			pass

		for i in files_in_playlist:
			current_file = files_names[file_count]
			try:
				if not os.path.exists(i):
					raise FileNotFoundError
				shutil.copy2(i, local_dst + "/" + current_file)
			except FileNotFoundError:
				try:
					# Tries again with no "/" added
					shutil.copy2(i, local_dst + current_file)
				except FileNotFoundError:
					print(colors.FAIL + "FILE NOT FOUND: " + current_file.strip(".mp3") + colors.ENDC)
					continue
			finally:
				file_count += 1

			print(colors.OKGREEN + "File number " + str(file_count) + " successfully copied : " + str(current_file).strip(".mp3") + colors.ENDC)
			copied_files += 1
		print(colors.WARNING + "This program successfully copied " + str(copied_files) + " files out of " + str(file_count) + colors.ENDC)




if __name__ == '__main__':
	user = Extractor()
	colors = Colors()
	for l in user.playlist_list:
		user.copy_playlist(l)
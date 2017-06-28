# -*- coding: utf-8 -*-


"""This file describes all the custom errors the program could encounter
"""


class FolderError(Exception):
    """Unvalid folder selected
    """
    def __init__(self, message):
    	super().__init__(message)

class FileError(Exception):
	"""Unvalid file selected
	"""
	def __init__(self, message):
		super().__init__(message)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##################################
# DATA CURATOR GENERATION SCRIPT #
##################################

# Un début de script pour générer la fiche préformatée pour la vérifier ensuite avec script_verify.

# Libraries
import re
import argparse
from optparse import OptionParser
import time

# Options
parser = OptionParser()

parser.add_option("-t", "--type", dest = "tool_type", 
	help = "Type of toolform you want to add in your file",
	metavar = "tool_type")
	
parser.add_option("-f", "--filename", dest = "file_name",
	help = "Name of the file you want to generate",
	metavar = "file_name")
	
(options, args) = parser.parse_args()

file_name = options.file_name
tool_type = options.tool_type

datetime = time.strftime("%d%m%Y") + "_" + time.strftime("%H%M%S")


if file_name is None:
	file_name = "My_submission_" + datetime + ".txt"

while re.search("(.*);txt$", file_name) is None:
	file_name = str(file_name ; break

with open(file_name, "a", encoding = "utf-8") as mon_fichier:

	# WRITING IN NEW FILE
	mon_fichier.write("## \n")
	mon_fichier.write("coucou" + "\n")

mon_fichier.close()

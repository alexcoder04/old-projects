##############################################################################
######## whichOS -- a python script that checks the operating system #########
#Copyright (C) 2020  Alex

#whichOS is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#whichOS is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
#############################################################################

import platform

#version 2.1

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

if __name__ == "__main__":
	checkOS()

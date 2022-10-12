##############################################################################
############# settings_lib_l.py -- this file is part of callix ###############
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

import os
import xml.dom.minidom
import whichOS
import subprocess


class Setting:
    def __init__(self, name, value, attribute="in"):
        self.name = name
        self.value = value
        self.attribute = attribute

#read and return the path where this file is
def getpath():
    #read the path
    path = os.getcwd()
    return path

#version 1.0
def buildPath(temp):
    #print("debug: Auf die Festplatte wurde zugegriffen.")
    system = whichOS.checkOS(0)
    if "//" in temp or "$$" in temp:
        temp = temp.replace("//", "/")
        temp = temp.replace("$$", "$")
    provis = temp.replace("%", getpath())
    provis = provis.replace("$", "/user/folders/")
    if system == "Windows":
        #print("Windows-Pfad gebaut: " + provis.replace("/", "\\"))
        return provis.replace("/", "\\")
    elif system == "Linux":
        return provis
    else:
        return provis

#imported from the python documentation
#needed for getSetting()
def getText(nodelist):
	rc = []
	for node in nodelist:
		if node.nodeType == node.TEXT_NODE:
			rc.append(node.data)
	return ''.join(rc)

#changes the settings in xml-files
def setSetting(fileName, settingName, attributeName, content):
    global path
    settingValue = getSetting(fileName, settingName, attributeName)
    pathToFile = path + "/config/" + fileName + ".config"
    f = open(pathToFile)
    fileContent = f.read()
    f.close()
    if attributeName == "in":
        fileContent = fileContent.replace("<"+settingName+">"+settingValue+"</"+settingName+">", "<"+settingName+">"+content+"</"+settingName+">")
        f = open(pathToFile, "w")
        f.write(fileContent)
        f.close()

#returns the content of settings are saved in xml-files
def getSetting(fileName, settingName, attributeName="in"):
    pathToFile = "%" + "/config/" + fileName + ".config"
    xmldoc = xml.dom.minidom.parse(buildPath(pathToFile))
    itemlist = xmldoc.getElementsByTagName(settingName)
    endlist = []
    for x in itemlist:
        if attributeName == "in":
            endlist.append(getText(x.childNodes))
        else:
            endlist.append(x.attributes[attributeName].value)
    if len(endlist) == 1:
        return endlist[0]
    else:
        return endlist

def startFileBrowser():
    yos = whichOS.checkOS(0)
    if yos == "Windows":
        print("Kann nicht in deinen callix-Ordner gehen: du nutzt Windows.")
        subprocess.call("start explorer")
    elif yos == "Linux":
        proc = subprocess.Popen(getSetting("main", "file-browser", "in")+" "+buildPath(getpath() + "$"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = proc.stdout.read()
    else:
        print("Kann nicht den Dateibrowser öffnen: unbekanntes Betriebssystem.")

def unumlaut(str):
    if "ä" in str:
        str.replace("ä", "ae")
    if "ö" in str:
        str.replace("ö", "oe")
    if "ü" in str:
        str.replace("ü", "ue")
    if "Ü" in str:
        str.replace("Ü", "Ue")
    if "Ä" in str:
        str.replace("Ä", "Ae")
    if "Ö" in str:
        str.replace("Ö", "Oe")
    if "ß" in str:
        str.replace("ß", "ss")
    return str

path = getpath()

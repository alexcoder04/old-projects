##############################################################################
############### files_lib_l.py -- this file is part of callix ################
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
import shutil as sh
from datetime import datetime
import xml.dom.minidom
import history
import settings_lib_l as syst
import Motal2 as motal
import whichOS

#some notes for me about functions
#os.path.exists() = os.path.isfile() && os.path.ifdir()

# current path and blocked chars
currentPath = "$"
username = syst.getSetting("main", "user", "in")
IN_WINDOWS_BLOCKED_CHARS = ['~', '"', '#', '%', '&', '*', ':', '<', '>', '?', '/', '\\', '{', '|', '}']
BLOCKED_CHARS = ['%', '$', '&']

#save the folder's table of contents using xml
def writeFolderInfIntoFile(filesList, folder, created, size):
    f = open(syst.buildPath(folder) + "/0.cdfi", "w")
    print("debug: writing folder infs into this file: "+syst.buildPath(folder) + "/0.cdfi")
    f.write('<?xml version="1.0"?>\n\n<data>\n')
    folderName = folder.split("/")[-1].replace("%$", "")
    f.write('  <folder created="' + created + '" size="' + str(size) + '">' + folderName + '</folder>\n\n')
    for w in filesList:
        if w.type == "file":
            f.write('  <worksheet created="' + w.created + '" changed="' + w.changed + '">' + w.name + '</worksheet>\n')
        else:
            f.write('  <subfolder created="'+w.created+'" changed="'+w.changed+'">'+w.name+'</subfolder>\n')
    f.write('</data>')
    f.close()
    print("debug: file saved")

# for refreshFolder()-loop that checks the files in a folder
class ElementMetaData:
    def __init__(self, name, created, changed, type):
        self.name = name
        self.created = created
        self.changed = changed
        self.type = type

#refresh folder contents
def refreshFolder(folderName):
    pathToDir = "%$" + folderName
    print("debug: Pfad zum refreshen: "+pathToDir)
    # create a fileslist and read metadata of each file
    filesList = os.listdir(syst.buildPath(pathToDir))
    filesListWithData = []
    for file in filesList:
        if file != "0.cdfi" and not os.path.isdir(syst.buildPath("%$" + folderName + "/" + file)):
            print("debug: "+pathToDir)
            print("debug: "+file)
            print("debug: "+syst.buildPath(pathToDir + "/" + file))
            xmldoc = xml.dom.minidom.parse(syst.buildPath(pathToDir + "/" + file))
            xmlhead = motal.getHead(xmldoc)
            name = syst.unumlaut(motal.getName(xmlhead))
            created = motal.getCreated(xmlhead)
            changed = motal.getChanged(xmlhead)
            thisElementMetaData = ElementMetaData(name, created, changed, "file")
            filesListWithData.append(thisElementMetaData)
        elif os.path.isdir(syst.buildPath("%$" + folderName + "/" + file)):
            thisElementMetaData = ElementMetaData(file, "created", "changed", "folder")
            filesListWithData.append(thisElementMetaData)
    # if the cdfi-file exists, read when the folder was created
    if os.path.isfile(syst.buildPath(pathToDir + "/0.cdfi")):
        print("debug: " + syst.buildPath(pathToDir + "/0.cdfi"))
        xmldoc = xml.dom.minidom.parse(syst.buildPath(pathToDir + "/0.cdfi"))
        itemlist = xmldoc.getElementsByTagName('folder')
        created = itemlist[0].attributes['created'].value
    # if not, say the folder was created now
    else:
        now = datetime.now()
        today = now.strftime("%Y_%m_%d %H:%M:%S")
        created = today
    # check the number of files in the folder
    size = len(filesListWithData)
    print("debug: writing folder informations into a file")
    writeFolderInfIntoFile(filesListWithData, pathToDir, created, size)
    print("Inhaltsverzeichnis von " + folderName + " wurde aktualisiert.")

#copied from the Python documentation
#needed for getFilesList()
def getText(nodelist):
	rc = []
	for node in nodelist:
		if node.nodeType == node.TEXT_NODE:
			rc.append(node.data)
	return ''.join(rc)

# table of content
class itemInTableOfContent:
    def __init__(self, created, changed, name, type):
        self.created = created
        self.changed = changed
        self.name = name
class TableOfContent:
    def __init__(self, name, created, size, worksheets, folders):
        self.name = name
        self.created = created
        self.size = size
        self.worksheets = worksheets
        self.folders = folders

# reads and returns the folder information from the cdfi-file
def getFolderInf(folderName):
    if folderName != "$":
        # if the file exists, read
        if os.path.isfile(syst.buildPath("%$" + folderName + "/0.cdfi")):
            xmldoc = xml.dom.minidom.parse(syst.buildPath("%$" + folderName + "/0.cdfi"))
            # folder metadata
            itemlist = xmldoc.getElementsByTagName('folder')
            created = itemlist[0].attributes['created'].value
            size = int(itemlist[0].attributes['size'].value)
            name = getText(itemlist[0].childNodes)
            # worksheets in the folder list
            worksheets = []
            itemlist = xmldoc.getElementsByTagName('worksheet')
            for w in itemlist:
                wCreated = w.attributes['created'].value
                wChanged = w.attributes['changed'].value
                wName = getText(w.childNodes)
                worksheets.append(itemInTableOfContent(wCreated, wChanged, wName, "file"))
            # subfolders in the folder list
            folders = []
            itemlist = xmldoc.getElementsByTagName('subfolder')
            for s in itemlist:
                fCreated = s.attributes['created'].value
                fChanged = s.attributes['changed'].value
                fName = getText(s.childNodes)
                folders.append(itemInTableOfContent(fCreated, fChanged, fName, "folder"))
            thisTOC = TableOfContent(name, created, size, worksheets, folders)
            return thisTOC
        # if not, refresh (=create) it and read
        else:
            refreshFolder(folderName)
            print("debug: "+folderName)
            return getFolderInf(folderName)
    else:
        return getFolderInf("")

def listThisElements(list):
    if len(list.folders) > 0:
        print("\n    Mappen:\n")
        for x in list.folders:
            print(x.name)
    if len(list.worksheets) > 0:
        print("\n    Dateien:\n")
        for x in list.worksheets:
            print(x.name)
    if len(list.folders) == 0 and len(list.worksheets) == 0:
        print("Dieser Ordner ist leer.")

#list the content of a folder
def ls(folderName):
    global currentPath
    # root ($) folder
    if folderName == "root" or folderName == "$":
        print("Inhalt der Ordnerübersicht:\n")
        refreshFolder("")
        listThisElements(getFolderInf("$"))
        print()
    # current folder
    elif folderName == "this":
        # if current is not root
        if currentPath != "$":
            refreshFolder(currentPath.replace("$", ""))
            print("Inhalt des Ordners " + currentPath.replace("$", "") + ":\n")
            listThisElements(getFolderInf(currentPath.replace("$", "")))
        # if current IS root
        else:
            print("Inhalt der Ordnerübersicht:\n")
            refreshFolder("")
            listThisElements(getFolderInf("$"))
            print()
    # any other folder
    else:
        pathToDir = "%" + currentPath + "/" + folderName
        if os.path.isdir(syst.buildPath(pathToDir)):
            refreshFolder(folderName)
            print("Inhalt des Ordners " + folderName + ":\n")
            listThisElements(getFolderInf(currentPath + "/" + folderName))
        else:
            print("Die angeforderte Mappe existiert nicht.")
            print("'mkfold' " + folderName + "' eingeben, um sie zu erstellen.")
    history.add("info", "ls succesfully")

#change directory
def cd(folder):
    global currentPath
    # go one folder up
    if folder == "..":
        if currentPath != "$":
            while True:
                if currentPath[-1] != "/":
                    currentPath = currentPath[:-1]
                else:
                    break
            print("Mappe gewechselt.")
        else:
            print("Du bist schon in der Ordnerübersicht.")
    # go to root folder
    elif folder == "$" or folder == "root":
        currentPath = "$"
        print("Mappe gewechselt.")
    # go to any other folder
    else:
        # go to the folder if it exists
        if os.path.isdir(syst.buildPath("%" + currentPath + "/" + folder)):
            currentPath = currentPath + "/" + folder
            print("Mappe gewechselt.")
        # if the folder not exists
        else:
            # if the user wrote the folder name lowercase, we wtry to capitalize
            # it and check if those folder exists
            firstChar = folder[0]
            otherChars = folder[1:]
            maybeItIs = firstChar[0].swapcase() + otherChars
            if os.path.isdir(syst.buildPath("%" + currentPath + "/" + maybeItIs)):
                print("Wechseln in " + maybeItIs + " statt " + folder + ", da " + folder + " nicht existiert.")
                currentPath = currentPath + "/" + maybeItIs
                print("Mappe gewechselt.")
            else:
                print("Die angeforderte Mappe existiert nicht.")
                print("Gib 'mkfold " + folder + "' ein, um sie zu erstellen.")
    history.add("info", "cd succesfully")
    # returns the new current path, so the main program knows it
    return currentPath

#make a directory
def folder(folder_name):
    yos = whichOS.checkOS(0)
    global IN_WINDOWS_BLOCKED_CHARS
    global BLOCKED_CHARS
    allowedInWindows = True
    allowed = True
    for x in BLOCKED_CHARS:
        if x in folder_name:
            char = x
            allowed = False
    for x in IN_WINDOWS_BLOCKED_CHARS:
        if x in folder_name:
            wChar = x
            allowedInWindows = False
    if not allowedInWindows:
        if yos == "Windows":
            print("Ordner kann nicht erstellt werden: ungültiger Name.")
            print("Zeichen '" + wChar + "' ist in Windows blockiert.")
        else:
            if allowed:
                print("Achtung! Zeichen '" + wChar + "' kann unter Linux, aber nicht unter Windows verwendet werden.")
                print("Fortfahren (j/n) ?")
                if input() != "j":
                    allowed = False
                    char = wChar
    if not allowed:
        print("Ordner kann nicht erstellt werden: ungültiger Name.")
        print("Zeichen '" + char + "' ist von callix reserviert.")
    global currentPath
    pathToDir = "%" + currentPath + "/" + folder_name
    if not os.path.isdir(syst.buildPath(pathToDir)):
        if allowed == True:
            os.mkdir(syst.buildPath(pathToDir))
            print("debug: " + syst.buildPath(pathToDir))
            refreshFolder(folder_name)
            print("Ordner erstellt.")
            history.add("info", "created a folder")
    else:
        print("Ordner mit gleichem namen existiert bereits.")

#delete a directory
def rmdir(folder_name):
    #global path
    pathToDir = "%" + currentPath + folder_name
    if os.path.isdir(syst.buildPath(pathToDir)):
        print("Bist du dir sicher (j/n)?")
        if input() == "j":
            # remove all files of the directory
            filesList = os.listdir(syst.buildPath(pathToDir))
            for x in filesList:
                os.remove(syst.buildPath(pathToDir + "/" + x))
            # remove the directory
            os.rmdir(syst.buildPath(pathToDir))
            print("Ordner gelöscht.")
            history.add("info", "removed a folder")
    else:
        print("Die angeforderte Mappe existiert nicht.")

#create a new file
def new():
    global username
    motal.init("de")
    now = datetime.now()
    now = now.strftime("%Y_%m_%d %H:%M:%S")
    body = motal.editBody("empty", "de")
    head = motal.editHead(now, "empty", "de", 1, username)
    worksheet = motal.WorkSheet(4.0, head, body)
    while True:
        try:
            print("Speichern in der Mappe:")
            fileName = "%" + "$" + input() + "/" + worksheet.head.name + ".dab"
            motal.saveFile(worksheet, syst.buildPath(fileName))
            break
        except:
            print("\nEtwas ist schief gelaufen.")
            print("Versuche es bitte nochmal.")
    history.add("info", "created and saved a new file")

# open a file with Motal
def open_file(file_name):
    global currentPath
    pathToFile = "%" + currentPath + "/" + file_name + ".dab"
    if os.path.isfile(syst.buildPath(pathToFile)):
        motal.init("de")
        file = motal.readFile(syst.buildPath(pathToFile))
        motal.showFile(file, "de")
        history.add("info", "opened a file")
    else:
        print("Die angeforderte Datei existiert nicht.")
        print("'new' eingeben, um sie zu erstellen.")

# edit a file with Motal
def edit_file(file_name, mode=0):
    if mode == 1:
        pathToFile = file_name
    else:
        pathToFile = "%" + currentPath + "/" + file_name + ".dab"
    if os.path.isfile(syst.buildPath(pathToFile)):
        motal.init()
        file = motal.readFile(syst.buildPath(pathToFile))
        motal.showFile(file)
        body = motal.editBody(file.body, "de")
        head = file.head
        worksheet = motal.WorkSheet(4.0, head, body)
        sumPath = "%" + currentPath + "/" + worksheet.head.name + ".dab"
        motal.saveFile(worksheet, syst.buildPath(sumPath))
        history.add("info", "edited and saved a file")
    else:
        print("Die angeforderte datei existiert nicht.")
        print("'new' eingeben, um sie zu erstellen.")

# autoimport if the app starts
def searchAutoimport(path):
    filesList = os.listdir(path)
    imported = 0
    if len(filesList) != 0:
        for x in filesList:
            if x.endswith(".dab"):
                print("Datei " + x + " gefunden.")
                import_file(0, syst.buildPath(path + "/" + x))
                imported += 1
        print("Insgesamt " + str(imported) + " Dateien importiert.")
    else:
        print("Keine zu importierenden Dateien gefunden.")

#import a file from an external folder
def import_file(mode=1, fp=0):
    if mode == 1:
        print("Gebe den (absoluten) Pfad der zu importierenden Datei an:")
        fromPath = input()
        fileName = fromPath.split("/")[-1]
        print("In welche Mappe willst du die Datei importieren?")
        folder = input()
        toPath = "%" + currentPath + "/" + folder + "/" + fileName
        sh.copyfile(fromPath, buildPath(toPath))
    elif mode == 0:
        fromPath = fp
        fileName = fromPath.split("/")[-1]
        toPath = "%$/" + fileName
        sh.copyfile(fromPath, syst.buildPath(toPath))
        os.remove(fromPath)
        folder = "$"
    print("Datei erfolgreich nach " + folder + " als " + fileName + " importiert und vom Ursprungsort gelöscht.")
    history.add("info", "imported a file")

# copy a file
def cp(fromPath, toPath):
    try:
        sh.copyfile(syst.buildPath("%$" + fromPath + ".dab"), syst.buildPath("%$" + toPath + ".dab"))
        print("Datei kopiert.")
    except:
        print("Etwas ist falsch gelaufen. Bitte versuche es nochmal.")

# cut a file
def mv(fromPath, toPath):
    try:
        sh.copyfile(syst.buildPath(fromPath), syst.buildPath(toPath + ".dab"))
        os.remove(syst.buildPath(fromPath))
        print("Datei verschoben.")
    except:
        print("Etwas ist falsch gelaufen. Bitte versuche es nochmal.")

#delete a file
def delete(file):
    file_name = "%" + currentPath + "/" + file + ".dab"
    if os.path.isfile(syst.buildPath(file_name)):
        print("Bist du dir sicher (j/n)?")
        if input() == "j":
            os.remove(syst.buildPath(file_name))
            print("Datei gelöscht.")
            history.add("info", "deleted a file")
    else:
        print("Die angeforderte Datei existiert nicht.")

def exportAsHTML(file):
    global currentPath
    pathToFile = "%" + currentPath + "/" + file + ".dab"
    if os.path.isfile(syst.buildPath(pathToFile)):
        motal.init("de")
        w = motal.readFile(syst.buildPath(pathToFile))
        tagslist = ""
        for x in w.head.tags:
            tagslist = tagslist + " " + x
        f = open(input("Wo soll die Enddatei gespeichert werden? ") + "/" + w.head.name + ".html", "w")
        f.write("""
<!DOCTYPE html>
<html>
<head>
  <title>"""+w.head.name+"""</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>\n""")
        css = open(syst.buildPath("%/data/css.css"))
        f.write(css.read())
        css.close()
        f.write("""
  </style>
</head>
<body>
  <div class='note'>Dieses Dokument wurde mithilfe von callix aus der Datei """ + w.head.name + """.dab konvertiert.</div>
  <h1 class='heading'>"""+w.head.name+"""</h1>
  <div class='header'>
    <table class='header'>
      <tr><td>Erstellt:</td><td>"""+w.head.created+"""</td></tr>
      <tr><td>Zuletzt geändert:</td><td>"""+w.head.changed+"""</td></tr>
      <tr><td>Author:</td><td>"""+w.head.author+"""</td></tr>
      <tr><td>Fach:</td><td>"""+w.head.subject+"""</td></tr>
      <tr><td>Tags:</td><td>"""+tagslist+"""</td></tr>
    </table>
  </div>
  <br/><br/>
  <div class='content'>""")
        for x in w.body:
            if x.eType == "p":
                f.write("  <p>"+x.eContent+"</p>\n")
        f.write("""
  </div>
</body>
</html>""")
        f.close()
        print("Datei wurde exportiert.")
        history.add("info", "exported into HTML")
    else:
        print("Die angeforderte Datei existiert nicht.")
        print("'new' eingeben, um sie zu erstellen.")

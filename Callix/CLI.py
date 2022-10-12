##!/usr/bin/python3
#If you are using Linux you can remove one of # above and make this file executable

##############################################################################
######## callix, a Program for everything around school, main part ###########
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

import advanced as adv
import apps
import files_lib_l
import history
import infos_lib_l as infos
import notes_lib_l as notes
import planner_lib_l as planner
import settings_lib_l as syst
import subprocess
from init import init
import whichOS

#declare global vars
cmdnumb = 0
historyList = []

class Command:
    def __init__(self, cmd, opts, fls):
        self.cmd = cmd
        self.opts = opts
        self.fls = fls

def getCmd(inp):
    components = inp.split()
    options = []
    files = []
    if len(components) > 0:
        for x in components:
            if x[0] == "-":
                for w in x.replace("-", ""):
                    options.append(w)
            elif x[0] == "*":
                files.append(x.replace("*", ""))
            else:
                cmd = x
    else:
        cmd = ""
    return Command(cmd, options, files)

def exeCmd(inp, prgm):
    if inp.cmd == prgm.cmds.exit or inp.cmd == "q" or inp.cmd == ":q":
        print("Verlassen der Kommandozeile...")
        # main loop will only break if exeCmd() returns 0
        return 0
    elif inp.cmd == prgm.cmds.adv:
        adv.main()
    elif inp.cmd == prgm.cmds.cmds:
        print("Aktuell installierter Befehlssatz:", cmds.packName)
    elif inp.cmd == prgm.cmds.clear:
        if prgm.yos == "Windows":
            subprocess.call("cls", shell=True)
        else:
            subprocess.call("clear", shell=True)
    elif inp.cmd == prgm.cmds.cp:
        files_lib_l.cp(inp.fls[0], inp.fls[1])
    elif inp.cmd == prgm.cmds.fb:
        print("Starte Dateibrowser...")
        syst.startFileBrowser()
    elif inp.cmd == prgm.cmds.help:
        infos.help()
    elif inp.cmd == prgm.cmds.importWS:
        files_lib_l.import_file(0, inp.fls[0])
    elif inp.cmd == prgm.cmds.info:
        infos.info()
    elif inp.cmd == prgm.cmds.list:
        files_lib_l.ls(inp.fls[0])
    elif inp.cmd == prgm.cmds.mv:
        files_lib_l.mv(inp.fls[0], inp.fls[1])
    elif inp.cmd == prgm.cmds.new:
        files_lib_l.new()
    elif inp.cmd == prgm.cmds.notes:
        notes.main()
    elif inp.cmd == prgm.cmds.path:
        global currentPath
        print(currentPath)
    elif inp.cmd == prgm.cmds.planner:
        planner.main("de")
    elif inp.cmd == prgm.cmds.play:
        apps.play()
    elif inp.cmd == prgm.cmds.repeat:
        global historyList
        if len(historyList) > 1:
            inputed = historyList[-2]
            if inputed != "r":
                inputed = getCmd(inputed)
                exeCmd(inputed)
            else:
                print("Der letzte ausgeführte Befehl war 'r'.")
        else:
            print("In dieser Sitzung noch keine Befehle eingegeben.")
    else:
        print("Befehl '" + inp.cmd + "' nicht gefunden.")

#commands without an attribute
#def which_cmd(cmd):
#    # the object where command names are saved
#    global cmds
#    # checking and executing the command
#    if cmd == prgm.cmds.exit or cmd == "q":
#        print("Verlassen der Kommandozeile...")
#        # main loop will only break if which_cmd() returns 0
#        return 0
#    #elif cmd == "calc":
#    #    apps.calc()
#    #elif cmd == "gui":
#    #	print("you cannot switch to the graphic mode")
#    elif cmd == prgm.cmds.adv:
#        adv.main()
#    elif cmd == prgm.cmds.cmds:
#        print("Aktuell installierter Befehlssatz: " + cmds.packName)
#    elif cmd == prgm.cmds.clear:
#        subprocess.call("clear", shell=True)
#    elif cmd == prgm.cmds.cp:
#        fromPath = "%$" + input("Was? ")
#        toPath = "%$" + input("Wohin? ")
#        files_lib_l.cp(fromPath, toPath)
#    elif cmd == prgm.cmds.help:
#        infos.help()
#    elif cmd == prgm.cmds.importWS:
#        files_lib_l.import_file()
#    elif cmd == prgm.cmds.info:
#        infos.info()
#    elif cmd == prgm.cmds.mv:
#        fromPath = "%$" + input("Was? ") + ".dab"
#        toPath = "%$" + input("Wohin? ") + ".dab"
#        files_lib_l.mv(fromPath, toPath)
#    elif cmd == prgm.cmds.new:
#        files_lib_l.new()
#    elif cmd == prgm.cmds.notes:
#        notes.main()
#    elif cmd == prgm.cmds.path:
#        global currentPath
#        print(currentPath)
#    elif cmd == prgm.cmds.planner:
#        planner.main("de")
#    #elif shell_extension(command) != 0:
#        #extension
#        #print("Erweiterung erfolgreich ausgeführt")
#    elif cmd == prgm.cmds.play:
#        apps.play()
#    elif cmd == prgm.cmds.repeat:
#        global historyList
#        if len(historyList) > 1:
#            inputed = historyList[-2]
#            if inputed != "r":
#                inputed = inputed.split()
#                if len(inputed) == 1:
#                    which_cmd(inputed[0])
#                elif len(inputed) == 2:
#                    command = inputed[0]
#                    argument = inputed[1]
#                    which_cmd_and_arg(command, argument)
#            else:
#                print("Der letzte ausgeführte Befehl war 'r'.")
#        else:
#            print("In dieser Sitzung noch keine Befehle eingegeben.")
#
#    else:
#    	print("Befehl '" + cmd + "' nicht gefunden.")
#    	print("Möglicherweise hast du das Argument vergessen.")
#
#commands that need an attribute
#def which_cmd_and_arg(cmd, arg):
#    #if cmd == "calc":
#    #    apps.calc(1, arg)
#    if cmd == prgm.cmds.cd:
#        global currentPath
#        currentPath = files_lib_l.cd(arg)
#    elif cmd == prgm.cmds.delFile:
#        files_lib_l.delete(arg)
#    elif cmd == prgm.cmds.delFold:
#        files_lib_l.rmdir(arg)
#    elif cmd == prgm.cmds.edit:
#        files_lib_l.edit_file(arg)
#    elif cmd == prgm.cmds.htmlout:
#        files_lib_l.exportAsHTML(arg)
#    elif cmd == prgm.cmds.list:
#        files_lib_l.ls(arg)
#    elif cmd == prgm.cmds.mkfold:
#        files_lib_l.folder(arg)
#    elif cmd == prgm.cmds.open:
#        files_lib_l.open_file(arg)
#    else:
#    	print("Befehl " + cmd + " nicht gefunden.")

#MAIN FUNCTION
def main(prgm):
    global historyList
    print("\n" + prgm.username + ", willkommen zur Kommandozeile von callix!")
    print("Gib 'help' ein, um Liste aller Befehle zu sehen.")
    while True:
        #input the command
        inputed = input(">>> ")
        # counting the number of inputed commands
        global cmdnumb
        cmdnumb += 1
        inp = getCmd(inputed)
        if exeCmd(inp, prgm) == 0:
            break
        # split the command into command and attribute
        #inputed = inputed.split()
        ## commands that don't need an attribute
        #if len(inputed) == 1:
        #    command = inputed[0]
        #    #execute the command and quit, if "exit" inputed
        #    if which_cmd(command) == 0:
        #        break
        ## commands that need ONE attribute
        #elif len(inputed) == 2:
        #    command = inputed[0]
        #    argument = inputed[1]
        #    #execute the command with an argument
        #    which_cmd_and_arg(command, argument)
        # if 10 commands were inputed show the feedback reminding
        if cmdnumb % 10 == 0:
            print("""
########################################################
Vergiss nicht, dem Entwickler etwas Feedback zu geben :)
########################################################""")
    if prgm.yos == "Windows":
        subprocess.call("cls", shell=True)
    else:
        subprocess.call('clear', shell=True)
    print("Kommandozeile von callix beendet.\n")

# this happens if the program is started
if __name__ == "__main__":
    # check the OS
    print("Betriebssystem wird geprüft...")
    yos = whichOS.checkOS(1, "de")
    # case Linux: everything is fine
    if yos == "Linux":
        prgm = init()
        if prgm.start:
            main(prgm)
        else:
            print("callix beendet.\n")
    # case Windows: a warning
    elif yos == "Windows":
        print("ACHTUNG ! ! ! Du benutzt Windows!")
        print("Unter Windows kann das Programm jederzeit ohne einen sichtbaren Grund abstürzen!")
        print("Deshalb wird die Benutzung unter Linux empfohlen.")
        # but the program starts
        prgm = init()
        if prgm.start:
            main(prgm)
        else:
            print("callix beendet.\n")
    # case other OS: ask if the user really wants to run the program
    else:
        print("""Dein Betriebssystem: """ + yos + """
Du kannst trotzdem fortfahren, wir als Entwickler haften aber NICHT für Schäden, die evtl. entstehen können.
Falls du fortfahren möchtest, gib '$continue$' ein.""")
        you = input()
        if you == "$continue$":
            prgm = init()
            if prgm.start:
                main(prgm)
            else:
                print("callix beendet.")
        else:
            print("callix beendet.")

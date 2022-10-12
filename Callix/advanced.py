##############################################################################
################# advanced.py -- this file is part of callix #################
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

import history
import settings_lib_l as syst
import os
from datetime import datetime

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

def main():
    print("Achtung! Du bist im Teil des Programms, das für fortgeschrittene Nutzer gedacht ist.")
    print("Mache hier nur etwas, wenn du genau weißt, wozu das führen wird!")
    print("Ansonsten könntest du dein Programm kaputt machen.")
    while True:
        inp = input("adv> ")
        history.add("input>adv", inp)
        #inputed = inputed.split()
        inp = getCmd(inp)
        #if len(inputed) == 0:
        #    continue
        #elif inputed[0] == "exit" or inputed[0] == "q":
        #    break
        #elif inputed[0] == "build":
        #    buildNum = syst.getSetting("app-data", "build", "in")
        #    print("Build-number: " + buildNum)
        #elif inputed[0] == "clear":
        #    print("Removing old planner files...")
        #    plannersList = os.listdir(syst.buildPath("%/user/planner"))
        #    numbersList = []
        #    for x in plannersList:
        #        if x != "0.ctt":
        #            numbersList.append(x.replace(".cdc", ""))
        #    currentWeek = datetime.now().isocalendar()[1]
        #    toRemove = []
        #    if len(toRemove) != 0:
        #        for x in numbersList:
        #            if int(x) < currentWeek:
        #                toRemove.append(x)
        #        for x in toRemove:
        #            os.remove(syst.buildPath("%/user/planner/" + x + ".cdc"))
        #        print("Old planners removed.")
        #    else:
        #        print("No old planners to remove.")
        #elif inputed[0] == "history":
        #    print("\nHistory files:\n")
        #    historylist = os.listdir(syst.buildPath("%/user/history"))
        #    historylist.sort()
        #    for x in historylist:
        #        print(x)
        #    print()
        #    for x in historylist:
        #        print("\n##### new history file #####\n")
        #        f = open(syst.buildPath("%/user/history/" + x))
        #        print(f.read())
        #        f.close()
        #elif inputed[0] == "read":
        #    try:
        #        f = open(syst.buildPath("%" + "/" + input("File: ")), "r")
        #        print(f.read())
        #        f.close()
        #    except:
        #        print("An error was occured. Maybe the file doesn't exist.")
        #else:
        #    print("Command '" + inputed[0] + "' not found.")
        #    print("Input 'q' or 'exit' to quit")
        if inp.cmd == None:
            continue
        elif inp.cmd == "exit" or inp.cmd == "q" or inp.cmd == ":q":
            break
        elif inp.cmd == "build":
            print("Build-Number: " + str(syst.getSetting("app-data", "build", "in")))
        elif inp.cmd == "clear":
            # remove old planners
            print("Removing old planners...")
            plannersList = os.listdir(syst.buildPath("%/user/planner"))
            numbersList = []
            for x in plannersList:
                if x != "0.ctt":
                    numbersList.append(x.replace(".cdc", ""))
            currentWeek = datetime.now().isocalendar()[1]
            toRemove = []
            if len(toRemove) != 0:
                for x in numbersList:
                    if int(x) < currentWeek:
                        toRemove.append(x)
                for x in toRemove:
                    os.remove(syst.buildPath("%/user/planner/" + x + ".cdc"))
                print("Old planners removed.")
            else:
                print("No old planners to remove.")
        elif inp.cmd == "history":
            print("\nHistory files:\n")
            historylist = os.listdir(syst.buildPath("%/user/history"))
            historylist.sort()
            for x in historylist:
                print(x)
            print()
            for x in historylist:
                print("\n##### new history file #####\n")
                f = open(syst.buildPath("%/user/history/" + x))
                print(f.read())
                f.close()
        elif inp.cmd == "read":
            try:
                f = open(syst.buildPath("%" + "/" + inp.fls[0]), "r")
                print(f.read())
                f.close()
            except FileNotFoundError:
                print("The file doesn't exist.")
            except:
                print("An unknown error was occured.")
        else:
            print("command '" + inp.cmd + "' not found.")
            print("input 'exit' to quit.")

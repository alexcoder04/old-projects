##############################################################################
################# history.py -- this file is part of callix ##################
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

import settings_lib_l as syst
import os.path

def add(mode, text):
    currentNumber = checkCurrentNumber()
    size = checkSize(currentNumber)
    if size > 8192:
        currentNumber = str(int(currentNumber) + 1)
        syst.setSetting("main", "histnumb", "in", currentNumber)
    if not os.path.isfile(syst.buildPath("%/user/history/history" + currentNumber + ".txt")):
        f = open(syst.buildPath("%/user/history/history" + currentNumber + ".txt"), "x")
        f.close()
    f = open(syst.buildPath("%/user/history/history" + currentNumber + ".txt"), "a")
    f.write("\n" + mode + ": " + text)
    f.close()

def checkSize(number):
    return os.path.getsize(syst.buildPath("%/user/history/history" + number + ".txt"))

def checkCurrentNumber():
    return syst.getSetting("main", "histnumb", "in")

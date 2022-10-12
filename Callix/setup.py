##############################################################################
################## setup.py -- this file is part of callix ###################
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

from app import settings_lib_l as syst
from time import sleep as wait
import os.path

def showLicense():
    print("Du kannst die Lizenz auch in der LICENSE.txt-Datei finden.")
    print()
    f = open(syst.buildPath("%/readme/LICENSE.txt"))
    print(f.read())
    f.close()
    print("Scroll hoch! ^^^\n")
    print("[y = zustimmen und fortfahren / n = abbrechen")
    you = input()
    if you == "y":
        return True
    else:
        return False

# configurating the program if it was started the first time
def firstStart():
    print("\nDu benutzt callix zum ersten Mal.")
    print("\nLizenzvereinbarung:\n")
    print("""
Das Programm steht unter der GNU GPL-3-Lizenz.
Um das Programm zu benutzen, musst du den Bedingungen dieser Lizenz zustimmen.
Du kannst die Lizenz jederzeit in der LICENSE.txt-Datei oder auf <https://www.gnu.org/licenses/> nachlesen.

[y = zustimmen und fortfahren / n = abbrechen / r = Lizenz jetzt lesen.]""")
    you = input()
    if you == "r":
        cont = showLicense()
    elif you == "y":
        cont = True
    else:
        cont = False
    if cont:
        print("""
Datenschutzhinweis:
Dieses Programm sammelt KEINE persönlichen Daten ihrer Nutzer, wie E-Mail-Addresse,
Telefonnummer etc.
AUSNAHME: lediglich der Benutzername wird lokal auf dem Gerät gespeichert und
für ein persönlicheres Erlebnis, wie eine Begrüßung mit dem Namen, verwendet.
Außerdem werden alle einegegebenen Befehle in einer Liste auf dem Endgerät gespeichert.
Diese werden nur zur Verbesserung von callix verwendet und nur wenn Sie diese selbst
an die Entwickler schicken. Selbstverständlich werden diese NICHT an Dritte weitergegeben.\n""")
        wait(3)
        print("Jetzt richten wir die App für dich ein.")
        user = input("Wie heißt du? ")
        syst.setSetting("main", "user", "in", user)
        print("Das Programm ist nur in Deutsch verfügbar, also wird Deutsch als Sprache gesetzt.")
        syst.setSetting("main", "lang", "in", "de")
        print("Möchtest du bei jedem Start von callix automatisch Dateien aus einem bestimmten Ordner importieren?")
        you = input("j/n: ")
        if you == "j":
            syst.setSetting("main", "ai-yes-no", "in", "YES")
            while True:
                print("Gebe den absoluten Pfad des Ordners hier ein:")
                folder = input()
                if os.path.isdir(folder):
                    syst.setSetting("main", "ai-src", "in", folder)
                    break
                else:
                    print("Dieser Ordner existiert nicht.")
        else:
            syst.setSetting("main", "ai-yes-no", "in", "NO")
            print("Autoimport-Einstellungen wurden übernommen.")
        syst.setSetting("main", "first", "in", "NO")
        syst.setSetting("main", "cmdnumb", "in", "0")
        print("""Nun ist die Einrichtung abgeschlossen.\nViel Spaß mit callix!""")
        return True
    else:
        return False

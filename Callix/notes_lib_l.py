##############################################################################
############### notes_lib_l.py -- this file is part of callix ################
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
import settings_lib_l as syst


def main():
    print("Willkommen im Notizmanager von callix!")
    show_notes()
    while True:
        you = input("notes> ")
        if you == "new":
            new_note()
        elif you == "del":
            remove_note()
        elif you == "list":
            show_notes()
        elif you == "help":
            show_help()
        elif you == "open":
            open_note()
        elif you == "exit" or you == "q":
            break
        else:
            print("Befehl nicht gefunden.")
    print("Notizmanager verlassen.")

def show_notes():
    print("Deine Notizen:\n")
    global path
    names = os.listdir(syst.buildPath("%" + "/user/notes"))
    print()
    for x in names:
        print(x)
    print()

def new_note():
    global path
    print("Titel der Notiz:")
    f = open(syst.buildPath("%" + "/user/notes/" + input()), "w")
    print("Inhalt der Notiz: ")
    f.write(input())
    f.close()
    print("Notiz gespeichert.")

def remove_note():
    global path
    print("Welche Notiz möchtest du löschen?")
    os.remove(syst.buildPath("%" + "/user/notes/" + input()))
    print("Notiz gelöscht.")

def open_note():
    try:
        global path
        print("Welche Notiz möchtest du öffnen?")
        f = open(syst.buildPath("%" + "/user/notes/" + input()), "r")
        print(f.read())
        f.close()
    except:
        print("\nEtwas ist falsch gelaufen. Bitte versuche es nochmal.")

def show_help():
    print("Liste der Befehle des Notizmanagers:\n")
    print("del:     löscht eine Notiz")
    print("exit:    beenden des Notizmanagers")
    print("help:    zeigt diese Hilfe an")
    print("list:    zeigt Titeln aller Notizen an")
    print("new:     erstellt eine neue Notiz")
    print("open:    zeigt den Text einer bestimmten Notiz an")
    print("\nBeachte: der Notiztext darf nur eine Zeile lang sein!")

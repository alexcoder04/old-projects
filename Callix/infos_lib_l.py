##############################################################################
############### infos_lib_l.py -- this file is part of callix ################
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

from settings_lib_l import getSetting

#show app-info
def info():
    version = getSetting("app-data", "version", "in")
    date = getSetting("app-data", "date", "in")
    print("################## callix  Copyright (C) 2020  Alex ################")
    print("################## Version: " + version + " vom " + date + " ###################")
    print("This program comes with ABSOLUTELY NO WARRANTY.")
    print("This is free software, and you are welcome to redistribute it")
    print("under certain conditions; for more details see the LICENSE.txt-file.")
    print("\nDanksagungen:")
    print("Software, mit deren Hilfe das Programm erstellt wurde:")
    print(" - PYTHON und dessen Librarys")
    print(" - Atom: a hackable text editor for the 21st Century")
    print(" - Betriebssystem Ubuntu und dessen Standard-Tools")
    print(" - Firefox-Webrowser")
    print("Danke an die Beta-tester:")
    print()
    print("Besonderen Dank an:")
    print("Free Software Foundation, gnu.org, Morpheus Tutorials, stackoverflow.com, ubuntuusers.de")

#show help
def help():
    print("""
Eine Eingabe in die Kommandozeile sieht folgendermaßen aus:

befehl -option *dateiname1 *dateiname2

Hinweis:
 * nicht alle Befehle brauchen eine Option oder eine zugehörige Datei
 * um genauere Informationen zu einem bestimmten Befehl zu bekommen, gib ein:
         befehl -h

Mögliche Befehle:""")
    print("(Standard-Bibliothek!)\n")

    #print("#calc (*):  Taschenrechner")
    print("~adv:       erweiterte Optionen (nur für fortgeschrittene Nutzer)")
    print(":cd *:      wechselt in eine Mappe")
    print(":clear:     den Bildschirm leeren")
    print(":cmds:      zeigt den aktuell installierten Befehlssatz an")
    print(":cp:        Datei kopieren")
    print(":del *:     löscht eine Datei")
    print(":delfold *: löscht einen Ordner")
    print(":edit *:    bearbeiten einer Datei")
    print(":exit:      beendet callix")
    print(":fb:        startet den Dateibrowser")
    print(":import:    kopiert eine Datei aus einem externen Ordner in eine Mappe")
    print(":mkfold *:  erstellt einen Ordner")
    #print("#gui:       wechselt zur grafischen Benutzeroberfläche")
    print(":help:      zeigt diese Hilfe an")
    print(":htmlout:   exportiert ein AB als HTML")
    print(":info:      zeigt Informationen über das Programm an")
    print(":list *:    listet den Inhalt des Benutzerordners auf")
    print(":mv:        Datei verschieben")
    print(":new:       erstellt eine Datei")
    print("~notes:     startet den Notiz-Manager")
    print(":open *:    öffnet eine Datei")
    print(":path:      zeigt das aktuelle Verzeichnis an")
    print("~planner:   startet den Planer")
    print(":play:      Minispiel spielen")
    print(":q:         beendet callix")
    print(":r:         führt den letzten Befehl nochmal aus")

    print("\n* bedeutet, dass der Befehl ein Argument braucht")
    #print("(*) bedeutet, dass das Argument auch weggelassen werden kann")
    #print("# steht für einen derzeit nicht verfügbaren Befehl")
    print("~ bedeutet, dass der Befehl einen Manager startet")

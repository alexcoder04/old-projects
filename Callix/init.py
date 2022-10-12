from whichOS import checkOS
import settings_lib_l as syst


class Prgm:
    def __init__(self, start=False, currentPath=False, cmds=False, username=False):
        self.start = start
        self.yos = checkOS(0)
        self.currentPath = currentPath
        self.cmds = cmds
        self.username = username

# informes the user if he uses the beta-version
def betaWarning():
    print("Du benutzt die Beta-Version von callix.")
    print("""
Dieses Programm befindet sich noch in Entwicklung (sog. Alpha-/Betaversion).
Das heißt, dass es noch viele Fehler enthält und öfters abstürzen wird.
Wir bitten dich, jeden Absturz zu dokumentieren und den Entwicklern mitzuteilen.
Eine ausführliche Information, wie du das machst findest du im Dokument "BugsReports.txt".
Alle möglichen Ideen, Anregungen und Verbesserungsvorschläge sind herzlich willkommen!
Die aktuelle Version des Programms, das du benutzt, ermittelst du, wenn du in der App 'info' eingibst.
Vielen Dank für deine Hilfe!""")
    print("Wenn du fortfährst, hast du dies zur Kenntis genommen.")
    print("Fortfahren (c) / Fortfahren und diese Meldung nicht mehr anzeigen (n) / Abbrechen (beliebige Taste) ?")
    you = input()
    if you == "n":
        # do not show this message again
        syst.setSetting("main", "showbeta", "in", "NO")
        print("Diese Meldung wird in Zukunft nicht mehr angezeigt.")
        return True
    elif you == "c":
        return True
    else:
        return False

#initialization function
def init():
    # standard output with program name etc
    print("""
##########################################################################
callix  Copyright (C) 2020  Alex
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions; for more details see the LICENSE.txt-file.
##########################################################################
ACHTUNG !
Benutze das Programm nur, wenn du das ReadMe-Dokument gelesen hast!
##########################################################################
""")
    # continue only if not beta-version or the user said continue in the beta warning
    beta = syst.getSetting("app-data", "beta", "in")
    if beta == "YES":
        showbeta = syst.getSetting("main", "showbeta", "in")
        if showbeta == "YES":
            # do what user says in the beta warning
            cont = betaWarning()
        else:
            # the user said not to show the beta-warning => continue
            cont = True
    else:
        # not beta-version => continue
        cont = True
    if cont:
        # check if is the first start and if it is configurate the app
        first = syst.getSetting("main", "first", "in")
        if first == "YES":
            # configurating the program if it was started the first time
            cont = setup.firstStart()
        if cont:
            print("\nInizialisierung wird gestartet...")
            # inform the user where he is
            print("Aktueller Ordner:")
            currentPath = "$"
            print(syst.getpath() + "/user/folders/ => " + currentPath)
            # import the command names from commandsLib.py
            print("Lese Befehlssätze...")
            from commandsLib import Commands
            cmds = Commands
            print("Befehlssatz als " + cmds.packName + " festgelegt.")
            if syst.getSetting("main", "ai-yes-no", "in") == "YES":
                print("Suche zu importierende Dateien...")
                files_lib_l.searchAutoimport(syst.getSetting("main", "ai-src", "in"))
            # read the username
            print("Lese Benutzername...")
            username = syst.getSetting("main", "user", "in")
            print("Als " + username + " eingeloggt.")
            return Prgm(True, currentPath, cmds, username)
        else:
            return Prgm(False)
    else:
        # if init() returns false, the main function will be not started
        return Prgm(False)

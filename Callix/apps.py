##############################################################################
################## apps.py -- this file is part of callix ####################
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

#import re
import random

# a minigame: guess the number from 1 to 15
def play():
    number = random.randint(1, 15)
    attempts = 4
    won = False
    print("Errate meine Zahl von 1 bis 15!")
    while attempts > 0 and not won:
        you = int(input("Ich denke, die Zahl ist: "))
        if number == you:
            print("Gewonnen!")
            won = True
        else:
            if you > number:
                print("Zu hoch!")
            else:
                print("Zu niedrig!")
            attempts -= 1
    if not won:
        print("Verloren")
    print("Die Zahl war " + str(number))

# calculator: not aviable yet
#def calc(mode=0, expression=0):
#    if mode == 1:
#        calculate(expression)
#    else:
#        while True:
#            exprsn = input("calc> ")
#            if exprsn == "exit":
#                break
#            else:
#                calculate(exprsn)
#        print("Taschenrechner verlassen.")
#
#def calculate(what):
#    term = what
#    numbers = re.split('\+|\-|\*|/', term)
#    operators = re.split('1|2|3|4|5|6|7|8|9|0', term)
#    print(term)
#    print(operators)

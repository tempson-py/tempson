# -*- coding: utf-8 -*-

# colors
COLOR = {
    'NORMAL'  : '1',
    'GRAY'    : '2',
    'ITALIC'  : '3',
    'UDLNE'   : '4',
    'REVERSE' : '7',
    'BLACK'   : '30',
    'RED'     : '31',
    'GREEN'   : '32',
    'YELLOW'  : '33',
    'BLUE'    : '34',
    'PURPLE'  : '35',
    'CYAN'    : '36'
}


# print string with color
def coloredPrint(string, c):
    print('\033[1;%sm %s\x1b[0m' % (COLOR[c], string))

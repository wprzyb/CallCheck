#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Name: Maciek's aMazing Windows
# Author: Maciek
import sys
import re
# import functools
import os
import copy

try:
    import termios
    import tty
except ImportError:
    pass
try:
    import logger as log
    loggingEnabled = True
except ImportError:
    loggingEnabled = False

# def deprecated(func):
#     @functools.wraps(func)
#     def new_func(*args, **kwargs):
#         print("Call to deprecated function {}".format(func.__name__))
#         return func(*args, **kwargs)
#     return new_func


def printList(list):
    for i in range(len(list)):
        print(list[i])


def longInput(prompt, end="empty"):
    string = ""
    while 1:
        try:
            a = input(prompt)
        except Exception as e:
            return string
        if a == "" and end.lower() == "empty":
            return string
        else:
            string = string + "\n" + a

# Font: Basic
# Styles
# .d8888. d888888b db    db db      d88888b .d8888.
# 88'  YP `~~88~~' `8b  d8' 88      88'     88'  YP
# `8bo.      88     `8bd8'  88      88ooooo `8bo.
#   `Y8b.    88       88    88      88~~~~~   `Y8b.
# db   8D    88       88    88booo. 88.     db   8D
# `8888Y'    YP       YP    Y88888P Y88888P `8888Y'


POS_CENTER = "center"
POS_LEFT = "left"
POS_RIGHT = "right"
POS_UP = 'up'
POS_DOWN = 'down'


class Styles():
    """The default styles
    examples:
     UNICODE:
      \u250C\u2500TEST\u2500\u2510
      \u2502      \u2502
      \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2518
     UNICODE_BOLD:
      \u250F\u2501TEST\u2501\u2513
      \u2503      \u2503
      \u2517\u2501\u2501\u2501\u2501\u2501\u2501\u251B
     DEFAULT:
      +-TEST-+
      |      |
      +------+
     ALTERNATE:
      /-TEST-\\
      |      |
      \\------/
      """
    UNICODE = {
        "CornerUpLeft": "\u250C", "CornerUpRight": "\u2510",
        "CornerDownLeft": "\u2514", "CornerDownRight": "\u2518",
        "TitleFiller": "\u2500", "TextFiller": " ",
        "ButtonSelected": " [>{button}<] ",
        "ButtonNotSelected": " [ {button} ] ",
        "BorderVertical": "\u2502", "BorderHorizontal": "\u2500",
        "MenuBar": "{name}  ", "MenuBarSelected": " [{name}] ",
        "CornerGeneric": "+",
        "MenuChildUnselected": " {name}", "MenuChildSelected": ">{name}",
        "Format": "N/A"}
    UNICODE_BOLD = {
        "CornerUpLeft": "\u250F", "CornerUpRight": "\u2513",
        "CornerDownLeft": "\u2517", "CornerDownRight": "\u251B",
        "TitleFiller": "\u2501", "TextFiller": " ",
        "ButtonSelected": " [>{button}<] ",
        "ButtonNotSelected": " [ {button} ] ",
        "BorderVertical": "\u2503", "BorderHorizontal": "\u2501",
        "MenuBar": "{name}   ", "MenuBarSelected": " [{name}] ",
        "CornerGeneric": "+",
        "MenuChildUnselected": " {name}", "MenuChildSelected": ">{name}",
        "Format": "N/A"}
    DEFAULT = {
        "CornerUpLeft": "+", "CornerUpRight": "+",
        "CornerDownLeft": "+", "CornerDownRight": "+",
        "TitleFiller": "-", "TextFiller": " ",
        "ButtonSelected": " [>{button}<] ",
        "ButtonNotSelected": " [ {button} ] ",
        "BorderVertical": "|", "BorderHorizontal": "-",
        "MenuBar": "{name}  ", "MenuBarSelected": "|{name}| ",
        "CornerGeneric": "+",
        "MenuChildUnselected": " {name}", "MenuChildSelected": ">{name}",
        "Format": "N/A"}
    ALTERNATE = {
        "CornerUpLeft": "/", "CornerUpRight": "\\",
        "CornerDownLeft": "\\", "CornerDownRight": "/",
        "TitleFiller": "-", "TextFiller": " ",
        "ButtonSelected": " [>{button}<] ",
        "ButtonNotSelected": " [ {button} ] ",
        "BorderVertical": "|", "BorderHorizontal": "-",
        "MenuBar": "{name}  ", "MenuBarSelected": " [{name}] ",
        "CornerGeneric": "+",
        "MenuChildUnselected": " {name}", "MenuChildSelected": ">{name}",
        "Format": "N/A"}
    STYLE_LIST = ["UNICODE", "UNICODE_BOLD", "DEFAULT", "ALTERNATE"]

# Drawable
# d8888b. d8888b.  .d8b.  db   d8b   db  .d8b.  d8888b. db      d88888b
# 88  `8D 88  `8D d8' `8b 88   I8I   88 d8' `8b 88  `8D 88      88'
# 88   88 88oobY' 88ooo88 88   I8I   88 88ooo88 88oooY' 88      88ooooo
# 88   88 88`8b   88~~~88 Y8   I8I   88 88~~~88 88~~~b. 88      88~~~~~
# 88  .8D 88 `88. 88   88 `8b d8'8b d8' 88   88 88   8D 88booo. 88.
# Y8888D' 88   YD YP   YP  `8b8' `8d8'  YP   YP Y8888P' Y88888P Y88888P


lastid = 0


class Drawable():
    """A drawable base"""
    def __init__(self, name):
        self.name = name
        self.isDestroyed = False
        self.x = 1
        self.y = 1
        self.forcedWidth = 0
        self.forcedHeigth = 0
        self.parent = None
        global lastid
        self.id = lastid + 1
        lastid = lastid + 1
        self.priority = 0
        self.lastDraw = "N/A"
        self.hidden = False
        self.requiresRedrawing = False

    def draw(self):
        """This method should return a list of strings(rendered object)"""
        win = []
        self.lastDraw = win
        return win

    def destroy(self, destroyChild=False):
        """Destroy the object"""
        self.checkDestroyed()
        self.x = None
        self.y = None
        self.forcedWidth = None
        self.forcedHeigth = None
        self.isDestroyed = True
        self.hidden = True
        self.lastDraw = "N/A"
        if destroyChild:
            for widget in self.widgets:
                widget.destroy(True)

    def checkDestroyed(self):
        """Check if this object is already destoryed"""
        if self.isDestroyed:
            raise InvalidStateError(self.name
                                    + ": This Object is already destoryed.")
        return
# .88b  d88. d88888b d8b   db db    db
# 88'YbdP`88 88'     888o  88 88    88
# 88  88  88 88ooooo 88V8o 88 88    88
# 88  88  88 88~~~~~ 88 V8o88 88    88
# 88  88  88 88.     88  V888 88b  d88
# YP  YP  YP Y88888P VP   V8P ~Y8888P'


class Menu(Drawable):
    def selectorHandler(self, char):
        """Select a button"""
        log.slog('selectorHandler', repr(char))
        key = ""
        if char == "\x1b":
            more = self.parent.getChar()
            log.slog('selectorHandler', 'more '+repr(more))
            if more == "[":
                evenMore = self.parent.getChar()
                log.slog('selectorHandler', 'evenmore '+repr(evenMore))
                if evenMore == "A":
                    key = "ARROW_UP"
                elif evenMore == "B":
                    key = "ARROW_DOWN"
                elif evenMore == "C":
                    key = "ARROW_RIGHT"
                elif evenMore == "D":
                    key = "ARROW_LEFT"
        if key == "ARROW_RIGHT":
            if self.open < len(self.elements)-1:
                self.open += 1
        if key == "ARROW_LEFT":
            if self.open > 0:
                self.open -= 1
        if key == "ARROW_DOWN":
            if self.childopen < len(self.elements[self.open]['children'])-1:
                self.childopen += 1
        if key == "ARROW_UP":
            if self.childopen > 0:
                self.childopen -= 1
        if char == "\r":
            return self.handlers["menuClicked"](self)

    def __init__(self, name):
        super().__init__(name)
        self.elements = []
        self.handlers = {'menuClicked': lambda: None,
                         'loop': self.selectorHandler}
        self.style = Styles.DEFAULT
        self.open = -1
        self.childopen = -1
        self.x = 1
        self.y = 1
        self.hasTitle = False

    def draw(self):
        """Return a list of strings"""
        win = [""]
        offset = 0
        for element in self.elements:
            highLen = 0
            for child in element["children"]:
                child["vislen"] = len(re.sub(r"\$\([A-Za-z_0-9]*\)", "",
                                             child["name"]))
                if child["vislen"] > highLen:
                    highLen = child["vislen"]
            element["highLen"] = highLen
            element["offset"] = offset
            offset = offset\
                + len(self.style["MenuBar"]
                      .replace("{name}", element["name"]))
        for element in enumerate(self.elements):
            if self.open == element[0]:
                # if self.hasTitle:
                win[0] = win[0] + self.style["TextFiller"]\
                    + self.style["MenuBarSelected"]\
                    .replace("{name}", element[1]["name"])
                win[0] = re.sub(r"^\s*", r"", win[0])
                genericCorner = self.style["CornerGeneric"]\
                    if len(element[1]["name"]) < element[1]["highLen"]\
                    else ""
                offseter = self.style["TextFiller"]\
                    * (element[1]["offset"]+1) if element[1]["offset"] > 0\
                    else ""
                win.append(offseter
                           + self.style["CornerUpLeft"] + "\033[0m"
                           + (self.style["BorderHorizontal"]
                              * len(element[1]["name"]))
                           + "\033[0m"
                           + (genericCorner if self.hasTitle
                              else self.style["BorderHorizontal"])
                           + "\033[0m"
                           + ((element[1]["highLen"]
                               - len(element[1]["name"]))
                              * self.style["BorderHorizontal"])
                           + "\033[0m"
                           + self.style["CornerUpRight"]
                           + "\033[0m")
                for childE in enumerate(element[1]["children"]):
                    child = childE[1]
                    filler = self.style["TextFiller"]\
                        * (element[1]["highLen"] - child["vislen"])\
                        if element[1]["highLen"] - child["vislen"] > 0\
                        else ""
                    name = "\033[0m" + self.style["MenuChildSelected"].replace(
                        "{name}", child["name"])\
                        + "\033[0m"\
                        if self.childopen == childE[0]\
                        else self.style["MenuChildUnselected"].replace(
                            "{name}", child["name"]) + "\033[0m"
                    win.append(offseter
                               + "\033[0m"
                               + self.style["BorderVertical"]
                               + "\033[0m"
                               + name
                               + "\033[0m"
                               + filler
                               + "\033[0m"
                               + self.style["BorderVertical"]
                               + "\033[0m")
                win.append(offseter
                           + "\033[0m"
                           + self.style["CornerDownLeft"]
                           + "\033[0m"
                           + (self.style["BorderHorizontal"]
                              * (element[1]["highLen"]+1))
                           + "\033[0m"
                           + self.style["CornerDownRight"]
                           + "\033[0m")
            else:
                win[0] = win[0] + self.style["TextFiller"]\
                    + "\033[0m"\
                    + self.style["MenuBar"]\
                    .replace("{name}", element[1]["name"])\
                    + "\033[0m"
                # print(win)
        # print(win)
        self.lastDraw = win
        return win

# db   d8b   db d888888b d8b   db d8888b.  .d88b.  db   d8b   db
# 88   I8I   88   `88'   888o  88 88  `8D .8P  Y8. 88   I8I   88
# 88   I8I   88    88    88V8o 88 88   88 88    88 88   I8I   88
# Y8   I8I   88    88    88 V8o88 88   88 88    88 Y8   I8I   88
# `8b d8'8b d8'   .88.   88  V888 88  .8D `8b  d8' `8b d8'8b d8'
#  `8b8' `8d8'  Y888888P VP   V8P Y8888D'  `Y88P'   `8b8' `8d8'


class Window(Drawable):
    """- a window class
    attributes (own):
        text (default = "")
        buttons (default = [])
        selectedButton (default = -1)
        autoWindowResize (default = True)
         True - expand the window to the texts size,
         False - Don't expand
        handlers (default = {"loop": self.buttonSelectorHandler})
        style (default = Styles.DEFAULT)
         *check the class Styles for more info
    """
    def destroy(self, destroyChild=False):
        """Destroy the window"""
        super().destroy(destroyChild)
        self.isDestroyed = True
        self.text = None
        self.buttons = None
        self.selectedButton = None

    def __init__(self, name):
        super().__init__(name)
        self.text = ""
        self.buttons = []
        self.widgets = {}
        self.selectedButton = -1
        self.autoWindowResize = True
        # True - expand the window to the texts size,
        # False - Don't expand
        self.handlers = {"loop": self.buttonSelectorHandler}
        self.style = Styles.DEFAULT
        self.styleOptions = {"ButtonAlignment": "N/A"}

    def loop(self):
        """Run self.handlers["loop"] unless it
returns something that is not "OK" """
        while 1:
            if self.parent is None:
                raise InvalidStateError("Window Parent is None")
            self.parent.draw(self, "clear")
            print()
            try:
                char = self.parent.getChar()
            except Exception as e:
                raise InvalidStateError("Window Parent is None")
            a = self.handlers["loop"]({"Character": char, "Window": self})
            if a != "OK":
                break

    def buttonSelectorHandler(self, options):
        """Select a button"""
        # print(options)
        key = ""
        if options["Character"] == "\x1b":
            more = self.parent.getChar()
            if more == "[":
                evenMore = self.parent.getChar()
                if evenMore == "A":
                    key = "ARROW_UP"
                elif evenMore == "B":
                    key = "ARROW_DOWN"
                elif evenMore == "C":
                    key = "ARROW_RIGHT"
                elif evenMore == "D":
                    key = "ARROW_LEFT"
        if key == "ARROW_RIGHT":
            if self.selectedButton < len(self.buttons)-1:
                self.selectedButton = self.selectedButton + 1
        if key == "ARROW_LEFT":
            if self.selectedButton > 0:
                self.selectedButton = self.selectedButton - 1
        if options["Character"] == "\r":
            return "END"
        return "OK"
        # a = input()

    def draw(self):
        """Internal use; Use screen.draw(window); Returns a the window as a
list of strings"""
        super().checkDestroyed()
        if self.hidden:
            return ['']
        width = 0
        # w = 0
        text = self.text
        buttons = ""
        if self.buttons is not None:
            for i in range(len(self.buttons)):
                if self.selectedButton == i:
                    buttons = buttons + \
                        self.style["ButtonSelected"].\
                        replace("{button}", self.buttons[i])
                    # " [>"+self.buttons[i]+"<] "
                else:
                    buttons = buttons + \
                        self.style["ButtonNotSelected"].\
                        replace("{button}", self.buttons[i])
                    # " [ "+self.buttons[i]+" ] "
            visbuttons = re.sub(r"\$\([A-Za-z_0-9]\)", "", buttons)
            if len(visbuttons) > width:
                width = len(visbuttons)
        if self.forcedWidth <= 0:
            temp = re.sub(r"\$\([a-zA-Z_0-9]*\)", "", text)
            temp = temp.split("\n")
            if self.autoWindowResize:
                for i in range(len(temp)):
                    if len(temp[i]) > width:
                        width = len(temp[i])
                if len(self.name) > width:
                    width = len(self.name)
            else:
                raise InvalidStateError("forcedWidth is required, "
                                        "if text wrap is on.")
        else:
            if self.autoWindowResize:
                temp = text.split("\n")
                i = -1
                for elem in temp:
                    i = i + 1
                    if len(temp[i]) > self.forcedWidth:
                        string = temp.pop(i)
                        for char in range(len(string)):
                            if char == self.forcedWidth:
                                temp.insert(i+1, string[:char])
                                temp.insert(i+1, string[char+1:])
                                print(temp)
                newtext = ""
                for i in temp:
                    newtext = newtext + "\n" + i
                text = newtext
            # w = self.forcedWidth
            width = self.forcedWidth + 1

        visname = re.sub(r"\$\([A-Za-z_0-9]*\)", "", self.name)
        spl = round((width - len(visname))/2)
        spr = width - (spl+len(visname))
        win = [self.style["CornerUpLeft"]
               + (self.style["TitleFiller"]*spl)
               + self.name
               + (self.style["TitleFiller"]*spr)
               + self.style["CornerUpRight"]]
        if "menu" in self.widgets.keys():
            # state = self.widgets["menu"].open
            self.widgets["menu"].forcedWidth = width
            if not self.widgets["menu"].hidden:
                self.widgets["menu"].x = self.x + 1
                self.widgets["menu"].y = self.y + 1
                menu = self.widgets["menu"].draw()
                win.append(self.style["BorderVertical"]
                           + menu[0]
                           + (self.style["TextFiller"] *
                              (width - len(menu[0]))
                              )
                           + self.style["BorderVertical"])

            # if state["hideParent"]:
            #     textToDraw = self.widgets["menu"].draw()
            #     for i in textToDraw:
            #         win.append(self.style["BorderVertical"] + i
            #                    + self.style["TextFiller"]*(width - len(i))
            #                    + self.style["BorderVertical"])
        vistext = re.sub(r"\$\([A-Za-z_0-9]*\)", "", text).split("\n")
        text = text.split("\n")
        # print('vtxt', vistext)
        # print('w', width)
        for i in range(len(vistext)):
            diff = 0
            temptext = vistext[i]
            # print('lvtxt', len(temptext))
            if len(temptext) < width:
                diff = (width) - len(temptext)
                # print("@ line "+str(i)+" diff "+repr(diff))
                text[i] = text[i] + self.style["TextFiller"]*diff
            win.append(self.style["BorderVertical"]+text[i]
                       + self.style["BorderVertical"])
            # print "zzz"
        if self.forcedHeigth != -1:
            win.append(self.style["BorderVertical"]
                       + self.style["TextFiller"]*(width)
                       + self.style["BorderVertical"])
            # print "aaaa"
        visbuttons = re.sub(r"\$\([A-Za-z_0-9]*\)", "", buttons)
        if buttons != [] and buttons != "":
            fillerL = ""
            fillerR = ""
            if self.styleOptions["ButtonAlignment"] != "N/A":
                if self.styleOptions["ButtonAlignment"] == \
                        POS_LEFT:
                    fillerL = " "
                    fillerR = self.style["TextFiller"]\
                        * (width - len(visbuttons) - 1)
                elif self.styleOptions["ButtonAlignment"] == \
                        POS_RIGHT:
                    fillerL = self.style["TextFiller"]\
                        * (width - len(visbuttons) - 1)
                    fillerR = " "
                elif self.styleOptions["ButtonAlignment"] == \
                        POS_CENTER:
                    pass
                else:
                    raise InvalidStateError("ButtonAlignment can only be right"
                                            " or left or center.")

            spl = round((width - len(visbuttons))/2)
            # spl = spl - len(fillerL)
            spr = width - (spl+len(visbuttons))
            # spr = spr - len(fillerR)
            print("spl:", spl)
            print("spr:", spr)
            win.append(self.style["BorderVertical"]
                       + ((spl*self.style["TextFiller"]) if fillerL == ""
                       else "")
                       + fillerL
                       + buttons
                       + fillerR
                       + ((spr*self.style["TextFiller"]) if fillerR == ""
                       else "")
                       + self.style["BorderVertical"])
        win.append(self.style["CornerDownLeft"]
                   + (self.style["BorderHorizontal"]*width)
                   + self.style["CornerDownRight"])
        if "menu" in self.widgets.keys():
            if not self.widgets["menu"].hidden:
                menu = self.widgets["menu"].draw()
                # print(menu)
                lwin = []
                offseter = 2
                voffset = 1
                for line in win:
                    lwin.append(list(line))
                for lineNum, line in enumerate(menu):
                    # print(lineNum, line)
                    try:
                        for charNum, char in enumerate(line):
                            try:
                                lwin[lineNum+voffset][charNum+offseter] = char
                            except IndexError:
                                lwin[lineNum+voffset].append(char)
                    except IndexError:
                        lwin.append(list(offseter*" ")+list(line))
                win = []
                for line in lwin:
                    newline = ""
                    for char in line:
                        newline = newline + char
                    win.append(newline)
                    # print(newline)
        self.lastDraw = win
        # print(win)

        self.width = len(win[0])
        self.height = len(win)
        return win
# Z: Text area
# d888888b d88888b db    db d888888b    .d8b.  d8888b. d88888b  .d8b.
# `~~88~~' 88'     `8b  d8' `~~88~~'   d8' `8b 88  `8D 88'     d8' `8b
#    88    88ooooo  `8bd8'     88      88ooo88 88oobY' 88ooooo 88ooo88
#    88    88~~~~~  .dPYb.     88      88~~~88 88`8b   88~~~~~ 88~~~88
#    88    88.     .8P  Y8.    88      88   88 88 `88. 88.     88   88
#    YP    Y88888P YP    YP    YP      YP   YP 88   YD Y88888P YP   YP


class TextArea(Drawable):
    def __init__(self, name, startPoint=(0, 0), endPoint=(24, 80)):
        """Init the TextArea obj. Parameters (in order):
         self,
         name - name/title that will be displayed,
         startPoint - a tuple of coordinates that indicate the first point of
          a rectagle (eg. (0,0), (10,28))
         endPoint - same as startPoint but indicates the other needed endPoint
          to draw a rectagle
         """
        super().__init__(name)
        self.name = name
        self.text = []
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.parent = None
        self.isScrollable = False

    def draw(self):
        """Draw the object"""
        text = copy.copy(self.text)
        Screen.setCur(self, self.startPoint[0], self.startPoint[1])
        locY = 0
        output = []
        size = [self.endPoint[0] - self.startPoint[0],
                self.endPoint[1] - self.startPoint[1]]
        # print(size)
        for num, line in enumerate(text):
            # print(num, line, locY)
            if len(line) > size[0]:
                output.append(line[:size[0]-1])
            else:
                output.append(line)
            if locY >= self.endPoint[1] and not self.isScrollable:
                break
            locY += 1
        return output
# Z: Screen
# .d8888.  .o88b. d8888b. d88888b d88888b d8b   db
# 88'  YP d8P  Y8 88  `8D 88'     88'     888o  88
# `8bo.   8P      88oobY' 88ooooo 88ooooo 88V8o 88
#   `Y8b. 8b      88`8b   88~~~~~ 88~~~~~ 88 V8o88
# db   8D Y8b  d8 88 `88. 88.     88.     88  V888
# `8888Y'  `Y88P' 88   YD Y88888P Y88888P VP   V8P


class Screen():
    """A screen object.
    This class contains:
     a list of foreground colors
     a list of background colors
     a list of effects(The mostly supported ones)
     colors:
      black, red, green, yellow, blue, magenta, cyan, white, gray, bright_red,
      bright_green, bright_yellow, bright_blue, bright_magenta, bright_cyan,
      bright_white
     effects:
      bold(reset_intensity), faint(reset_intensity),
      italic, underline(underline_off), slow_blink(blink_off),
      rapid_blink(blink_off), reverse(reverse_off),
      conceal(conceal_off/reveal), crossed_out(crossed_out_off),
      """
    fgcolors = {
        "black": "30", "red": "31", "green": "32", "yellow": "33",
        "blue": "34", "magenta": "35", "cyan": "36", "white": "37",
        "grey": "31;1",
        "gray": "30;1", "bright_red": "31;1", "bright_green": "32;1",
        "bright_yellow": "33;1", "bright_blue": "34;1",
        "bright_magenta": "35;1", "bright_cyan": "36;1",
        "bright_white": "37;1"  # If you think this makes no sense, you're
                                # right. This is here to provide a more white
                                # white, since some terminals treated white as
                                # gray
    }
    bgcolors = {
        "black": "40", "red": "41", "green": "42", "yellow": "43",
        "blue": "44", "magenta": "45", "cyan": "46", "white": "47",
        "gray": "100", "bright_red": "101", "bright_green": "102",
        "bright_yellow": "103",
        "bright_blue": "104", "bright_magenta": "105", "bright_cyan": "106",
        "bright_white": "107"  # Same as in foreground colors.
    }
    effects = {
        "bold": "1", "faint": "2", "italic": "3", "underline": "4",
        "slow_blink": "5", "rapid_blink": '6', 'reverse': '7',
        'conceal': '8', 'hide': '8', 'crossed_out': '9', 'italic_off': '23',
        'underline_off': '24', 'bold_off': '22', 'faint_off': '22',
        'blink_off': '25', 'reset_intensity': '22',
        'reverse_off': '27', 'conceal_off': '28', 'reveal': '28',
        'show': '28', 'crossed_out_off': '29', 'reset': "0"
    }

    inDebug = False
    allowColor = True

    def __init__(self):
        # self.getChar = self.getGetChar()
        self.size = os.get_terminal_size()
        self.windows = []
        self.background = []
        self.binds = []
        try:
            import msvcrt

            def getChar():
                """Get a char from STDIN (using msvcrt)"""
                return msvcrt.getch()  # noqa: F821

            self.platform = "win"
            self.getChar = getChar
        except ImportError:
            self.platform = "linux"

            def getChar(forceBufferReading=False):
                """Get a char from STDIN (using tty, termios, sys)"""
                fd = sys.stdin.fileno()
                old = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd)
                    if forceBufferReading:
                        return sys.stdin.buffer.read(1)
                    try:
                        return sys.stdin.read(1)
                    except Exception:
                        return sys.stdin.buffer.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old)
            self.getChar = getChar

    def setCur(self, x, y, returnTheEscape=False):
        """Move the cursor the x and y.
        Return the ANSI Escape, if returnTheEscape is True"""
        if returnTheEscape:
            return '\033['+str(y)+';'+str(x)+'H'
        else:
            print('\033['+str(y)+';'+str(x)+'H', end='', flush=True)

    def draw_no_redraw(self, window):
        """Draw a window onto the screen without redrawing other windows.
        Returns True if window was drawn False otherwise."""
        if window.isDestroyed:
            return False
        a = window.draw()
        x = window.x
        y = window.y
        for i in range(len(a)):
            self.setChar(self.format(a[i]), x, y+i)
        return True

    def draw(self, window=None, forceRedrawMode="clear"):
        """
        Redraw a window onto the screen with max priority
        forceRedrawMode can be:
            - "clear"
            - "oldAsBackground"
            - "forcedBackground"
        """
        if forceRedrawMode.lower() == "clear":
            self.clear()
        # if forceRedrawMode.lower() == "oldasbackground":
        #     print("\033[s")
        if forceRedrawMode.lower() == "forcedbackground":
            self.setScreen(self.background)
        windows = sorted(self.windows,
                         key=lambda window: window.priority,
                         reverse=False)
        # self.clear()
        for i in range(len(windows)):
            if windows[i].isDestroyed:
                continue
            if windows[i] is not None:
                if window is not None:
                    if windows[i].id == window.id:
                        continue
                for line in range(len(windows[i].lastDraw)):
                    # print(windows[i].lastDraw)
                    if not windows[i].lastDraw == "N/A" and \
                            not windows[i].requiresRedrawing:
                        self.setChar(self.format(windows[i].lastDraw[line]),
                                     windows[i].x,
                                     windows[i].y+line)
                        # print("zzzzzzzzzzzzzzzz")
                    else:
                        self.draw_no_redraw(windows[i])
        if window is not None:
            self.draw_no_redraw(window)
        # if forceRedrawMode.lower() == "oldasbackground":
        #     print("\033[u")

    def setScreen(self, screen, alternateScreen=False):
        """Set the screen to the list in the screen variable"""
        print('\033[2J\033[0;0H', end='', flush=True)
        y = self.size[1]
        for i in range(y):
            try:
                print(screen[i])
                # '\033[0;'+i+'H'+
            except Exception as e:
                pass
                # raise Exception("WARNING: List smaller than the screen")
        return

    def clear(self):
        """Clear the screen(print \\033[2J)"""
        print('\033[2J', end='', flush=True)

    def getColor(self, color, bg=False):
        """Return a color"""
        try:
            if bg:
                return self.bgcolors[color]
            else:
                return self.fgcolors[color]
        except Exception:
            return "0"

    @staticmethod
    def format(string):
        """Format the STRING.
        ex.:
        $(COLOR) - This will be replaced with a foreground color
        $(b_COLOR) - But this will be replaced with a background color
        $(EFFECT) - And this will be replaced with a effect code"""
        if not Screen.allowColor:
            return re.sub(r"\$\([A-Za-z_0-9]*\)", "", string)
        for effect in Screen.effects.keys():
            string = string.replace("$("+effect.lower()+")",
                                    "\033["+Screen.effects[effect]+"m")
        for color in Screen.bgcolors.keys():
            string = string.replace("$(b_"+color.lower()+")",
                                    "\033["+Screen.bgcolors[color.lower()]+"m")
        for color in Screen.fgcolors.keys():
            string = string.replace("$("+color.lower()+")",
                                    "\033["+Screen.fgcolors[color.lower()]+"m")
        return string

    def setChar(self, char, x, y, color="0"):
        """ color - color name (case insensitive)
            string with \\ as the first char will not be interpreted
            instead it will be used directly in the ANSI Escape sequence."""  # noqa
        if color[0] != "\\":
            color = self.getColor(color)
        else:
            color = color[1:]
        print('\033['+str(y)+';'+str(x)+'H\033['+str(color)+'m'+char,
              end='', flush=True)

    def add_window(self, window, setParent=True):
        """Add the window the the screen
        The window will be drawn unless window.hidden is True."""
        self.windows.append(window)
        if setParent:
            window.parent = self

    def loop(self, activeWindow, **kwargs):
        char = ""
        activeWin = activeWindow
        menuOpen = False
        menu = Menu("Tab menu")
        if loggingEnabled:
            log.defaultSource = 'loop'
            log.log('Screen.loop')
        while 1:
            if self.inDebug:
                log.log(repr(char))
                log.log(activeWin.name)
            char = self.getChar()
            press = {}
            if not menuOpen:
                if activeWin.handlers["loop"](char) == 'END':
                    return
            if (char == "\r" or char == "\n") and menuOpen:
                windows = self.windows.copy()
                windows.reverse()
                windows.remove(activeWin)
                windows.insert(1, activeWin)
                activeWin = windows[menu.childopen]
                menu.hidden = True
                menuOpen = False

            if char == "\t":
                if not menuOpen:
                    windows = self.windows.copy()
                    windows.reverse()
                    windows.remove(activeWin)
                    windows.insert(1, activeWin)
                    self.size = os.get_terminal_size()
                    # Repostion the menu if the terminal resized.
                    menu.x = round(self.size[0]/2)
                    menu.y = round(self.size[1]/2)
                    children = []
                    for window in windows:
                        name = window.name if not len(window.name) > 30\
                            else window.name[:30]+"..."
                        children.append({"name": name})
                    menu.elements = [{"name": "Windows", "children": children}]
                    menu.open = 0
                    menu.childopen = 0
                    menu.hidden = False
                    self.draw(menu)
                    menuOpen = True
                    continue
                else:
                    if menu.open == 0:
                        windows = self.windows.copy()
                        windows.reverse()
                        windows.remove(activeWin)
                        windows.insert(1, activeWin)
                        activeWin = windows[0]
                    menu.hidden = True
                    menuOpen = False
            elif char == "\033":
                if menuOpen:
                    b = self.getChar()
                    if b == "[":
                        c = self.getChar()
                        if c == "A":  # ARROW_UP
                            if menu.childopen > 0:
                                menu.childopen -= 1
                        if c == "B":  # ARROW_DOWN
                            if menu.childopen < \
                                    len(menu.elements[0]["children"])-1:
                                menu.childopen += 1
                        if c == "F":  # END
                            menu.childopen = len(
                                menu.elements[0]["children"])-1
                        if c == "H":
                            menu.childopen = 0
                else:
                    b = self.getChar()
                    if b == "[":
                        c = self.getChar()
                        if c == "M":
                            t = self.getChar()
                            x = self.getChar()
                            y = self.getChar()
                            press = KeyMap.mouseClickDecode([t, x, y])
                            if self.inDebug:
                                print("press:", press)
                            for bind in self.binds:
                                if bind["keySeq"][0] != "\\M":
                                    if self.inDebug:
                                        print("skipping: ", bind)
                                    continue
                                x_ok1 = press["x"] >= \
                                    bind["keySeq"][1]["xStart"]
                                x_ok2 = press["x"] <= \
                                    bind["keySeq"][1]["xEnd"]
                                x_ok = x_ok1 and x_ok2
                                # del x_ok1, x_ok2
                                y_ok1 = press["y"] >= \
                                    bind["keySeq"][1]["yStart"]
                                y_ok2 = press["y"] <= \
                                    bind["keySeq"][1]["yEnd"]
                                y_ok = y_ok1 and y_ok2
                                # del y_ok1, y_ok2
                                if self.inDebug:
                                    print("x_ok1", x_ok1)
                                    print("x_ok2", x_ok2)
                                    print("x_ok", x_ok)

                                    print("y_ok1", y_ok1)
                                    print("y_ok2", y_ok2)
                                    print("y_ok", y_ok)

                                if x_ok and y_ok:
                                    bind["function"]({"eventType":
                                                      "mouseClick",
                                                      "eventSource":
                                                      "Screen.loop",
                                                      "click": press,
                                                      "bind": bind})
                                    if self.inDebug:
                                        log.log("called")
            elif char == "\x1c":
                exit(0)
            elif char not in KeyMap.specialChars and not menuOpen:
                for bind in self.binds:
                    if bind["keySeq"] == char:
                        bind["function"]({"eventType": "keyPress",
                                          "eventSource": "Screen.loop",
                                          "bind": bind})
                        break

            if not menuOpen:

                self.draw(activeWin)
            else:
                self.draw(menu)
            if loggingEnabled:
                log.log(repr(char))

    def bind(self, keySeq, function):
        if keySeq is None:
            raise InvalidStateError("keySeq cannot be None\n"
                                    "Screen.bind(self, >keySeq...)")
        if function is None:
            raise InvalidStateError("The function cannot be None\n"
                                    "Screen.bind(self, keySeq, >function)")
        bind = {"keySeq": keySeq, "function": function}
        self.binds.append(bind)
        return bind

    def custom_input(self, prompt, handler=None):
        inputed = ""
        waiting = []
        inMouseMode = False
        while 1:
            if not inMouseMode:
                char = self.getChar()
            else:
                char = "x"+str(ord(self.getChar(True)))
            print("char: ", repr(char), "waiting: ", waiting, "imm",
                  inMouseMode)
            # Call self.getChar() forcing to output a string with the special
            # formatting
            # ex. "33"(ASCII !)
            # (required for mouse detection, since there is no char
            # staring with 0xFF in UTF-8)
            if char == "\x1c" or char == "x28":
                print("(Force exiting)")
                exit(0)
            if char == "\033":
                # print('033')
                b = self.getChar(True)
                if b == b"[":
                    # print('[')
                    c = self.getChar(True)
                    if c == b"M":
                        # print("M")
                        ptype = self.getChar(True)
                        x = self.getChar(True)
                        y = self.getChar(True)
                        etype = "UNKNOWN"
                        if ptype == b" ":
                            etype = "LMB_PRESS"
                        elif ptype == b"#":
                            etype = "UNPRESS"
                        elif ptype == b"0":
                            etype = "CTRL_LMB_PRESS"
                        elif ptype == b"3":
                            etype = "CTRL_UNPRESS"
                        print("event type: "+str(etype)+", x: "+str(ord(x)-33)
                              + ", y: "
                              + str(ord(y)-33),
                              end='\n', flush=True)
                        result = handler(eventType="Mouse",
                                         mousePress={"type": etype,
                                                     "x": ord(x)-33,
                                                     "y": ord(y)-33})
            elif char != b"\033":
                result = handler(eventType="CharInputEvent", char=char,
                                 self=self, string=inputed)
                if result[0].lower() == "ok":
                    inputed = inputed + char
                elif result[0].lower() == "end":
                    return inputed
                elif result[0].lower() == "cancel":
                    pass
                else:
                    raise InterruptedError(
                        result[0].lower()+" is not 'ok', 'end' or 'cancel'")
            elif char == "~":
                result = handler(eventType="KeyboardKey", char=waiting,
                                 self=self, string=inputed)
                if result[0].lower() == "set":
                    inputed = result[1]
                waiting = []
            else:
                waiting.append(char)

            # if len(waiting) > 10:
                # print("Ups Move Mode triggered")


class InvalidStateError(Exception):
    def __init__(self, message):
        self.message = message


class Layout():
    def __init__(self, parent=None):
        self.size = os.get_terminal_size()
        self.pos = [0, 0]
        self.windows = []
        self.window_positions = {1: (POS_CENTER, POS_CENTER)}
        self.parent = None
        if not isinstance(parent, Screen):
            raise TypeError("Layout's parent has to be a Screen object.")

    def reposition(self):
        size = self.size
        for window in self.windows:
            window.draw()
            pos = ('N/A', 'N/A')
            for windowId in self.window_positions:
                if windowId == window.id:
                    pos = self.window_positions[windowId]
            horCentered = round(size[0]/2)-window.width
            horCentered += self.pos[0]
            vertCentered = round(size[1]/2)-window.height
            vertCentered += self.pos[1]
            if pos[0] == POS_CENTER:
                window.x = horCentered
            elif pos[0] == POS_LEFT:
                window.x = horCentered - pos[2]
            elif pos[0] == POS_RIGHT:
                window.x = horCentered + pos[2]

            if pos[1] == POS_CENTER:
                window.y = vertCentered
            elif pos[1] == POS_UP:
                window.y = vertCentered - pos[3]
            elif pos[1] == POS_DOWN:
                window.y = vertCentered + pos[3]
            # window.requiresRedrawing = True
        if isinstance(self.parent, Screen):
            self.parent.draw()

    def set_window_position(self, windowId, posHor=POS_CENTER,
                            posVert=POS_CENTER, horShift=0, vertShift=0):
        self.window_positions[windowId] = (posHor, posVert, horShift,
                                           vertShift)

    def add_window(self, window):
        self.windows.append(window)
        self.window_positions[window.id] = (POS_CENTER, POS_CENTER, 0, 0)
        self.reposition()


class KeyList():
    ARROW_UP = 'ARROW_UP'
    ARROW_DOWN = 'ARROW_DOWN'
    ARROW_LEFT = 'ARROW_LEFT'
    ARROW_RIGHT = 'ARROW_RIGHT'
    INSERT = 'INSERT'
    DELETE = 'DELETE'
    HOME = 'HOME'
    END = 'END'
    PAGE_UP = 'PAGE_UP'
    PAGE_DOWN = 'PAGE_DOWN'
    TAB = 'TAB'
    RETURN = 'RETURN'


class FormattedString(str):
    def __init__(self, string):
        self.allowColor = True
        self.string = Screen.format(string)
        self.unformattedString = string
        self.noCodeString = re.sub(r"\$\([A-Za-z_0-9]*\)", "", string)

    def __len__(self):
        return len(self.noCodeString)

    def __eq__(self, anotherString):
        if isinstance(anotherString, FormattedString):
            return self.unformattedString == anotherString.unformattedString
        else:
            return self.noCodeString == anotherString


class KeyMap():
    specialChars = ["\033", "\x1c"]

    @staticmethod
    def decode(keySeq):
        if keySeq[0] == '\t':
            return KeyList.TAB
        if keySeq[0] == '\r':
            return KeyList.RETURN
        if keySeq[0] != '\033':
            return keySeq
        if keySeq[1] == '[':
            # pointer = 2
            # if keySeq[pointer] == '1':
            #     pointer += 1
            #     modifier += '?'
            # if keySeq[pointer] == ';':
            #     pointer += 1
            #     modifier += ' '
            if keySeq[-1] == 'A':
                return KeyList.ARROW_UP
            if keySeq[-1] == 'B':
                return KeyList.ARROW_DOWN
            if keySeq[-1] == 'D':
                return KeyList.ARROW_LEFT
            if keySeq[-1] == "C":
                return KeyList.ARROW_RIGHT

    @staticmethod
    def mouseClickDecode(charSeq):
        space = charSeq[0]
        x = charSeq[1]
        y = charSeq[2]
        code = format(ord(space), "=7b").replace(" ", "0")
        # code = code
        # print(code)
        # R0CMSXX
        # R scRoll
        # M Meta/Alt
        # C Control
        # S Shift
        # XX Mouse bttn vvv
        #  00 LMB
        #  01 MMB
        #  11 RMB
        modifiers = ""
        bttn = "?"
        if code[-2:] == "00" and code[0] == "0":
            bttn = "LEFT"
        elif code[-2:] == "01" and code[0] == "0":
            bttn = "MIDDLE"
        elif code[-2:] == "10":
            bttn = "RIGHT"
        elif code[-2:] == "11":
            bttn = "UNPRESS"
        elif code[-2:] == "00" and code[0] == "1":
            bttn = "SCROLL_UP"
        elif code[-2:] == "01" and code[0] == "1":
            bttn = "SCROLL_DOWN"
        if code[-3] == "1":
            modifiers = modifiers + ", SHIFT" if len(modifiers) > 1\
                else "SHIFT"
        if code[-4] == "1":
            modifiers = modifiers + ", META" if len(modifiers) > 1\
                else "META"
        if code[-5] == "1":
            modifiers = modifiers + ", CONTROL" if len(modifiers) > 1\
                else "CONTROL"
        etype = {}
        etype["button"] = bttn
        etype["modifiers"] = modifiers.split(", ")
        etype["x"] = ord(x)-33
        etype["y"] = ord(y)-33
        return etype


if __name__ == "__main__":
    s = Screen()
    w = Window("$(slow_blink)$(red)MMW for Python 3$(reset)")
    w.text = "$(green)[$(cyan)Do not adjust your TV$(green)]$(reset)"\
        "\nThis is $(red)not$(reset) a normal python program."\
        "\nThis is a library for creating ncurses-like windows"\
        "\nPress $(red)RETURN$(reset) to click this button and exit."\
        "\nOr you can press the $(red)LEFT ARROW$(reset) to select "\
        "the other button"
    w.x = 1
    w.y = 1
    w.buttons = ["$(cyan)Show me the docs$(reset)", "$(green)EXIT$(reset)"]
    w.styleOptions["ButtonAlignment"] = POS_CENTER
    w.selectedButton = 1
    s.add_window(w)
    s.draw(w)
    s.allowColor = True
    w.loop()
    if w.selectedButton == 1:
        exit(0)
    else:
        help(__file__[:-3])
        w.name = "$(cyan)Info - mmw(py3)$(reset)"
        w.text = "$(b_bright_blue)$(bright_white)Type \"python3 -m pydoc"\
            "mmw3\" to see the documentation$(reset)"
        for key in w.style.keys():
            w.style[key] = "$(b_bright_blue)$(bright_white)"+w.style[key]
        w.style["CornerDownRight"] = w.style["CornerDownRight"]+"$(reset)"
        w.buttons = []
        w.selectedButton = -1
        w.requiresRedrawing = True
        s.draw()
        print()
        exit(0)

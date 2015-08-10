# -*- coding: utf-8 -*-
# (c) 2015 Nicolò Valigi
# Author:  Nicolò Valigi
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""
Adds an icon to the system tray menu with a simple menu.

"Add new card" by default opens a new window. If an "Add card" window
is already on the foreground, the item doesn't do anything. If an "Add card"
window with data is already open, but not on the foreground, it raises it.
If an empty "Add card" window is already open, it closes it and reopens a new
one. This works around OSX's behaviour of switching Spaces when the same window
is opened somewhere else.
"""

from PyQt4.QtGui import *
from PyQt4 import QtCore
import aqt
import os, time
from anki.hooks import addHook

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

def showCardAdder():
    (creator, instance) = aqt.dialogs._dialogs["AddCards"]
    if instance:
        if instance.isActiveWindow():
            return
        if instance.editor.fieldsAreBlank():
            #closing an existing empty editor
            instance.close() #it's safe, I've already checked the fields
            aqt.dialogs.close("AddCards")
    #The second "open" I run raises the add card window even if the main one isn't
    aqt.mw.onAddCard()
    aqt.dialogs.open("AddCards", aqt.mw)


def createSysTray():
    if hasattr(aqt.mw, 'trayIcon'):
        return

    trayIcon = QSystemTrayIcon(aqt.mw)
    aqt.mw.trayIcon = trayIcon
    
    ankiLogo = QIcon()
    ankiLogo.addPixmap(QPixmap(_fromUtf8(":/icons/anki.png")), QIcon.Normal, QIcon.Off)
    trayIcon.setIcon(ankiLogo)
    
    trayMenu = QMenu(aqt.mw)
    trayIcon.setContextMenu(trayMenu)
    
    addNewAction = QAction("Create new card", aqt.mw)
    addNewAction.triggered.connect(showCardAdder)
    trayMenu.addAction(addNewAction)
    
    raiseWindowAction = QAction("Raise Anki Window", aqt.mw)
    raiseWindowAction.triggered.connect(lambda: aqt.mw.app.emit(QtCore.SIGNAL("appMsg"), "raise"))
    trayMenu.addAction(raiseWindowAction)
    
    trayMenu.addSeparator()
    
    quitAction = QAction("Quit Anki", aqt.mw)
    aqt.mw.connect(quitAction, QtCore.SIGNAL("triggered()"), aqt.mw, QtCore.SLOT("close()"))
    trayMenu.addAction(quitAction)
    
    trayIcon.setVisible(True)
    trayIcon.show()

addHook("profileLoaded", createSysTray)

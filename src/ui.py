# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="rremer"
__date__ ="$Feb 27, 2010 4:06:18 PM$"


import res
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt, QVariant
from ui_AppWindow import Ui_AppWindow
from ui_OpenDialog import Ui_OpenDialog
from cn import ConnectionString


class AppWindow( QtGui.QMainWindow ):
    def __init__( self, app ):
        QtGui.QMainWindow.__init__( self )

        self.app = app
        self.app.setActiveWindow( self )
        self.ui = Ui_AppWindow()
        self.ui.setupUi( self )

        self._history = []
        self._historyIndex = -1

        # check for startup message and set status appropriately
        lastMessage = self.app.getLastMessage()
        if lastMessage:
            self.ui.statusbar.showMessage( lastMessage )

        self.ui.entryBox.setFocus()

        #try:
        #    highlightDoc = self.ui.entryBox.document()
        #    sql.SyntaxHighlighter( highlightDoc )
        #except Exception as e:
        #    print "Exception:", e

    @QtCore.pyqtSignature( "" )
    def on_action_Clone_triggered( self ):
        self.app.clone()

    @QtCore.pyqtSignature( "" )
    def on_action_Open_triggered( self ):
        self.app.open()

    @QtCore.pyqtSignature( "" )
    def on_action_Reconnect_triggered( self ):
        self.app.connect()

    @QtCore.pyqtSignature( "" )
    def on_action_Execute_triggered( self ):
        model = self.app.execute()
        if model:
            self.ui.resultView.setModel( model )
        if self.ui.action_InteractiveMode.isChecked():
            if self._historyIndex >= 0:
                i = self._historyIndex
                self._history = self._history[0:i] + self._history[i+1:]
                self._historyIndex = -1
            self._history.append( self.ui.entryBox.toPlainText() )
            self.ui.entryBox.setPlainText( "" )

    @QtCore.pyqtSignature( "" )
    def on_action_NextResultset_triggered( self ):
        model = self.app.getNextResultSet()
        if model:
            self.ui.resultView.setModel( model )

    @QtCore.pyqtSignature( "" )
    def on_action_PreviousQuery_triggered( self ):
        if not self.ui.action_InteractiveMode.isChecked():
            return
        if len(self._history) == 0 or self._historyIndex == 0:
            return

        if self._historyIndex == -1:
            self._historyIndex = len(self._history) - 1
            if str(self.ui.entryBox.toPlainText()).strip() != "":
                self._history.append( self.ui.entryBox.toPlainText() )
        else:
            self._historyIndex -= 1

        self.ui.entryBox.setPlainText( self._history[self._historyIndex] )

    @QtCore.pyqtSignature( "" )
    def on_action_NextQuery_triggered( self ):
        if not self.ui.action_InteractiveMode.isChecked():
            return
        if len(self._history) == 0 or self._historyIndex == -1 or \
                self._historyIndex == len(self._history)-1:
            return

        self._historyIndex += 1
        self.ui.entryBox.setPlainText( self._history[self._historyIndex] )

    @QtCore.pyqtSignature( "" )
    def on_action_PyExecute_triggered( self ):
        self.app.pyExecute()

    @QtCore.pyqtSignature( "" )
    def on_action_Copy_triggered( self ):
        widget = self.app.focusWidget()
        if widget is self.ui.resultView:
            pass
        elif widget is self.ui.entryBox:
            print "entryBox"

    def on_entryBox_textChanged( self ):
        doc = self.ui.entryBox.document()
        text = str(doc.toPlainText())
        self.app.currentQuery = text
        if self.ui.action_InteractiveMode.isChecked():
            self._historyIndex = -1     # editing creates new history

    @QtCore.pyqtSlot( str )
    def showMessage( self, message ):
        self.ui.statusbar.showMessage( message )


class QListWidgetValueItem( QtGui.QListWidgetItem ):
    def __init__( self, value, caption=None, parent=None, icon=None ):
        QtGui.QListWidgetItem.__init__( self, parent )

        if caption is None:
            caption = str(value)

        self._value = value
        self.setData( Qt.DisplayRole, caption )
        
        if icon:
            self.setData( Qt.DecorationRole, QVariant(icon) )

    def value( self ):
        return self._value

class OpenDialog( QtGui.QDialog ):
    def __init__( self ):
        QtGui.QDialog.__init__( self )

        self.ui = Ui_OpenDialog()
        self.ui.setupUi( self )

        f = res.GetText( "Connections", "" )
        cns = [ line for line in f
                if len(line.strip()) > 0
                and line.strip()[0] != "#" ]
        for cn in cns:
            # load appropriate icon based on connection params
            _, host, _, _, password, description = ConnectionString.parse( cn )
            icon = "DB"
            if host == "localhost":
                icon += "Local"
            elif host == ".":
                icon += "User"
            elif host == "":
                icon += "None"
            else:
                icon += "Remote"
            if password == ".":
                icon += "Locked"
            icon = res.GetIcon( icon )

            if description == "":
                description = "<%s>" % cn

            QListWidgetValueItem( cn, description, self.ui.connectionList, icon )

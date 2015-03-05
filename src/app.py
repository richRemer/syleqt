# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="rremer"
__date__ ="$Feb 27, 2010 4:44:07 PM$"


import os
import sys
from subprocess import Popen
from PyQt4 import QtCore, QtGui, QtSql
import sql


class Application( QtGui.QApplication ):
    def __init__( self, args ):
        QtGui.QApplication.__init__( self, args )

        self._currentQuery = ""
        self._activeWindow = None
        self._database = None
        self._lastMessage = ""
        self._currentConnectionParams = {}
        self._model = None

        self.dbDriver = None
        self.dbHost = None
        self.dbUsername = None
        self.dbPassword = None
        self.dbName = None

        self.statusChanged.connect( self.setLastMessage )



    def clone( self ):
        args = []


        # load the currently running script name as first arg
        # this will be the program executed
        args.append( os.path.join( sys.path[0],
            os.path.split( sys.argv[0] )[-1:][0] ) )

        if self._currentConnectionParams.has_key( "driver" ):
            args.append( "-q" + self._currentConnectionParams["driver"] )
        if self._currentConnectionParams.has_key( "host" ):
            args.append( "-h" + self._currentConnectionParams["host"] )
        if self._currentConnectionParams.has_key( "username" ):
            args.append( "-u" + self._currentConnectionParams["username"] )
        if self._currentConnectionParams.has_key( "password" ):
            args.append( "-p." )
        if self._currentConnectionParams.has_key( "name" ):
            args.append( "-d" + self._currentConnectionParams["name"] )

        p = Popen( args )
        
        return p


    def open( self ):
        args = []

        # load the currently running script name as first arg
        # this will be the program executed
        args.append( os.path.join( sys.path[0],
            os.path.split( sys.argv[0] )[-1:][0] ) )

        args.append( "--open" )

        p = Popen( args )

        return p


    def get_activeWindow( self ):
        return self._activeWindow
    def setActiveWindow( self, window ):
        self._activeWindow = window
        self.statusChanged.connect( window.showMessage )
    activeWindow = property( get_activeWindow )

    def get_currentQuery( self ):
        return self._currentQuery
    def set_currentQuery( self, value ):
        self._currentQuery = value
    currentQuery = property( get_currentQuery, set_currentQuery )

    def get_database( self ):
        return self._database
    database = property( get_database )





    def execute( self ):
        self._rowsReturned = "unknown"
        self._rowsAffected = "unknown"

        ret = []

        stmts = sql.tokenizeStatements( self.currentQuery )
        stmtIndex = 0

        # begin a transaction
        self._database.transaction()

        model = QtSql.QSqlQueryModel()
        while stmtIndex < len(stmts):
            model.setQuery( stmts[stmtIndex], self._database )
            if ( model.lastError().isValid() ):
                # Notify user of error
                errorText = model.lastError().databaseText()
                self.statusChanged.emit( errorText )

                # If this was a connection problem, we can try to fix it
                reconnect = False
                if model.lastError().type() == QtSql.QSqlError.ConnectionError:
                    reconnect = True
                elif self.dbDriver == "QMYSQL" and model.lastError().number() == 2006:
                    reconnect = True

                # Clean up since we failed
                model = None
                self._database.rollback()

                # Try to reconnect if appropriate
                if reconnect:
                    self.statusChanged.emit( "Problem with connection.  Reconnecting..." )
                    self.connect()
                    self.statusChanged.emit( "OK" )
                
                return None
            else:
                self.statusChanged.emit( "OK" )
                query = model.query()
                rows = query.size()
                if rows >= 0:
                    self._rowsReturned = rows
                rows = query.numRowsAffected()
                if rows >= 0:
                    self._rowsAffected = rows
                if query.isSelect():
                    ret.append( model )
                    model = QtSql.QSqlQueryModel()
            stmtIndex += 1

        ret, self._pendingResults = ret[0], ret[1:]

        self._database.commit()

        return ret


    def hasMoreResults( self ):
        return len(self._pendingResults) > 0


    def getNextResultSet( self ):
        ret, self._pendingResults = self._pendingResults[0], \
            self._pendingResults[1:]
        return ret


    def pyExecute( self ):
        exec self.currentQuery in {
            "app": self,
            "window": self.activeWindow
        }


    def getInput( self, title, prompt, mask=False ):
        if mask:
            opts = QtGui.QLineEdit.Password
        else:
            opts = 0

        result, valid = QtGui.QInputDialog.getText( QtGui.QWidget(), title,
            prompt, opts )

        if valid:
            return result


    def resetConnectionParams( self ):
        self.dbDriver = None
        self.dbHost = None
        self.dbName = None
        self.dbPassword = None
        self.dbUsername = None


    def connect( self ):
        newParams = {}

        db = QtSql.QSqlDatabase( self.dbDriver )
        newParams["driver"] = self.dbDriver
        
        if self.dbHost and self.dbHost != ".":
            db.setHostName( self.dbHost )
            newParams["host"] = self.dbHost
        if self.dbName and self.dbName != ".":
            db.setDatabaseName( self.dbName )
            newParams["database"] = self.dbName
        if self.dbUsername and self.dbUsername != ".":
            db.setUserName( self.dbUsername )
            newParams["username"] = self.dbUsername
        if self.dbPassword and self.dbPassword != ".":
            db.setPassword( self.dbPassword )
            newParams["password"] = self.dbPassword

        if self.dbHost == ".":
            value = self.getInput( "Host", "Host name of database server" )
            if value:
                db.setHostName( value )
                newParams["host"] = value
        if self.dbName == ".":
            value = self.getInput( "Database", "Database name" )
            if value:
                db.setDatabaseName( value )
                newParams["database"] = value
        if self.dbUsername == ".":
            value = self.getInput( "Username", "Username to connect with" )
            if value:
                db.setUserName( value )
                newParams["username"] = value
        if self.dbPassword == ".":
            value = self.getInput( "Password", "Password to authenticate", True )
            if value:
                db.setPassword( value )
                newParams["password"] = value
        if not db.open():
            self.statusChanged.emit( "Could not open connection: %s" %
                db.lastError().text() )

        self._database = db
        self._currentConnectionParams = newParams

        return db


    def connectTo( self, driver, host=None, username=None, password=None,
            database=None ):
        self.dbDriver = driver
        if host: self.dbHost = host
        if username: self.dbUsername = username
        if password: self.dbPassword = password
        if database: self.dbName = database

        return self.connect()


    statusChanged = QtCore.pyqtSignal( str )
    @QtCore.pyqtSlot( str )
    def setLastMessage( self, message ):
        self._lastMessage = message
    def getLastMessage( self ):
        return self._lastMessage

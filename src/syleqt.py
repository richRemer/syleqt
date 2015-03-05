#!/usr/bin/env python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="rremer"
__date__ ="$Feb 27, 2010 3:58:39 PM$"


import sys
from PyQt4.QtGui import QDialog
from app import Application
from ui import AppWindow, OpenDialog
from cn import ConnectionString
from getopt import getopt, GetoptError


def processArgs( app, args ):
    try:
        opts, args = getopt( args, "q:h:u:p:d:",
            [ "driver=", "host=", "username=", "password=", "database=",
              "open" ] )
    except GetoptError, err:
        print str(err)
        sys.exit( 2 )

    options = {}

    for o, a in opts:
        if o in ( "-q", "--driver" ):
            options["driver"] = a
            app.dbDriver = a
        elif o in ( "-h", "--host" ):
            options["host"] = a
            app.dbHost = a
        elif o in ( "-u", "--username" ):
            options["username"] = a
            app.dbUsername = a
        elif o in ( "-p", "--password" ):
            options["password"] = a
            app.dbPassword = a
        elif o in ( "-d", "--database" ):
            options["database"] = a
            app.dbName = a
        elif o in ( "--open" ):
            options["open"] = True
            dlg = OpenDialog()
            dlg.exec_()
            if dlg.result() == QDialog.Accepted:
                if len(dlg.ui.connectionList.selectedItems()) > 0:
                    item = dlg.ui.connectionList.selectedItems()[0]
                    driver, host, database, username, password, _ = \
                        ConnectionString.parse( item.value() )
                    app.connectTo( driver, host, username, password, database )
                    return options
            sys.exit(0)


    if options.has_key( "driver" ):
        app.connectTo( options["driver"] )

    return options


def main( args ):
    app = Application( args )
    window = AppWindow( app )

    processArgs( app, args )

    window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit( main( sys.argv[1:] ) );

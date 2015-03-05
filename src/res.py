# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="rremer"
__date__ ="$Mar 13, 2010 5:22:42 PM$"


import os
import sys
import resources
from PyQt4 import QtGui


__home = os.getenv("HOME")


ResourcePaths = [
    os.path.join( __home, ".syleqt" ),      # User overrides
    sys.path[0],                            # Path of script
    ":"                                     # Embedded resource
]


def GetResourceSearchPaths( name, group, exts=[] ):
    files = []

    for resPath in ResourcePaths:
        path = os.path.join( resPath, group )
        file = os.path.join( path, name )
        files.append( file )
        for ext in exts:
            files.append( "%s.%s" % ( file, ext ) )

    return files



def GetResource( name, group, exts=[] ):
    fileset = GetResourceSearchPaths( name, group, exts )
    for file in fileset:
        if os.path.isfile( file ):
            return open( file ).read()

    raise Exception( "Could not find icon: %s" % name )


def GetIcon( name, group="image" ):
    fileset = GetResourceSearchPaths( name, group, [ "png" ] )
    for file in fileset:
        try:
            icon = QtGui.QIcon( file )
            if len(icon.availableSizes()) > 0:
                return icon
        except:
            pass

    raise Exception( "Could not find icon: %s" % name )

def GetText( name, group="string" ):
    fileset = GetResourceSearchPaths( name, group, [ "txt" ] )
    for file in fileset:
        if os.path.isfile( file ):
            return open( file ).readlines()

    raise Exception( "Could not find text reource: %s" % name )

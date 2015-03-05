# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="rremer"
__date__ ="$Mar 6, 2010 1:46:08 PM$"


class ConnectionString:
    def __init__( self, cn=None ):
        if cn:
            driver, host, database, username, password, description = \
                ConnectionString.parse( cn )
            self.driver = driver
            self.host = host
            self.database = database
            self.username = username
            self.password = password
            self.description = description

    @classmethod
    def parse( cls, cn ):
        cn = cn.strip()

        try:
            cn, _, description = cn.rpartition( "?" )
            driver, _, cn = cn.partition( "\\" )
            cn, _, host = cn.partition( "@" )
            username, _, password = cn.partition( ":" )
            host, _, _ = host.partition( "?" )      # remainder is comment
            host, _, database = host.partition( "/" )
        except:
            return None

        return driver, host, database, username, password, description.strip()

    def __str__( self ):
        if self.database:
            database = "/%s" % self.database
        target = "%s%s" % ( self.host, database )

        if self._password:
            password = ":%s" % self.password
        auth = "%s%s" % ( self.username, password )

        if auth:
            auth += "@"
        path = "%s%s" % ( auth, target )

        cn = self.driver + "\\" + path
        if self.description:
            description = "?%s" % self.description
        cn += description

        return cn

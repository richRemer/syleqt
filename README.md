Dependencies
------------
You must have the python-qt4-sql package (and it's dependencies) installed
for Syleqt to function.  On Ubuntu, this can be installed using apt.

Development requires the following packages
qtcreator
pyqt4-dev-tools

Change Log
----------
0.x

 Known Issues / Desired Feature:
 
   - someway to get entire error message as statusbar is too short
   - reconnect does not work; segfaults in some cases
   - add queries as bookmarks
   - SQuirreL-style macros
   - save current query
   - save current result
   - copy results
   - Bookmarks / Browser / Shortcuts sidebar
   - Bookmarks (connection bookmarks and show current)
   - Browser (schema browser and table-relation view)
   - Shortcuts (saved SQL queries)
   - syntax highlighting
   - auto-reconnect ?
   - open with no connection file show error to console
   - open dialog requires mouse to select connection if there is only
     a single connection
   - ability to execute SQL from commandline and pop a dialog with
     results only (no query area) and title
   - ability to call scripts as above from a configurable hot key


0.5.2

 * Added Focus Entry and Focus Results in Edit menu to allow keyboard
   navigation between the two areas

0.5.1

 * parseConnectionString refactored to ConnectionString.parse and
   fixed bug with comments between the ?? in connection strings
 * Added Reconnect action in Connection menu (Alt+R)
 * Executes multi-statement queries in a transaction

0.5

 * Cloning a connection with empty driver now "works" in that a new
   instance is opened with the same invalid connection
 * Resources are now loaded through a simplified module, "res".  This
   module's functions are responsible for coalescing resources from
   the user's profile directory, the script install location, and from
   embedded resources, in that order.  The module has several functions
   that return the resources as useful types.

   This change breaks compatibility with configuration file locations
   from previous versions.  To migrate connection settings, move any
   existing file found in ~/.syleqt to ~/.syleqt/Connections.  This
   is to support future modifications.
 * Fixed a bug where parseConnectionString was returning an extra
   newline at the end of the description.  Relatedly, fixed the open
   dialog text descriptions, which now makes each entry one text line
   in height.

0.4.3

 * Focus entry box upon startup
 * Various hotkey changes
 * Double clicking in open dialog now activates the OK button
 
0.4.2

 * More icons in open dialog:
   
    - Blue (Remote system)
    - Green (Local connection)
    - Gray (No connection)
    - Yellow (User supplied connection)
   
   All of the icons also will have a padlock on them when the
   connection requires that the user provide a password.

0.4.1

 * Icons now shown in open dialog.  Green for connections that
   point to localhost, blue for those that point at remote hosts,
   and with a locked icon if the connection requires the user
   to provide a password.   

0.4

 * Added limited connection management support; connections are
   created by placing a line in ~/.syleqt in the following format:
   
    - DRIVER\USER:PASS@HOST\DB?COMMENT?DESCRIPTION
   
   The only required part is the driver.  Without going into detail,
   Syleqt tries to intelligently determine which parts are there and
   which are not.  Empty values are not used, while a value of "."
   for any of the connection values will cause Syleqt to prompt for
   the value.  The DRIVER value is required and cannot be prompted.
   
   To open a connection, start Syleqt with the --open option or use
   the Connection -> Open menu.

0.3

 * Support for multi-statement queries via semicolon (;) delimiter
 * Resultset no longer disappears when executing writes

0.2.2

 * Only shows database errors, rather than driver errors as well

0.2.1

 * Statusbar will now show startup errors

0.2

 * Added statusbar messaging upon query execution and database errors

0.1

 * Initial release

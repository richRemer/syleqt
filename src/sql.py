# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="rremer"
__date__ ="$Feb 28, 2010 12:50:23 PM$"


from PyQt4 import QtGui
from PyQt4.QtCore import QRegExp
from PyQt4.QtGui import QColor


class FormatElement():
    def __init__( self, id, pattern=None, openPattern=None, closePattern=None,
            matchOptions=None, color=None, bold=False, name="" ):
        # check for invalid params
        if pattern and openPattern:
            raise ValueError, "Must provide pattern or openPattern only"
        if openPattern and not closePattern:
            raise ValueError, "Must provide closePattern if openPattern is provided"
        if not ( pattern or openPattern ):
            raise ValueErorr, "Must provide pattern or openPattern"

        self._formatInvalid = True
        self._patternsInvalid = True
        self._pattern = None
        self._closePattern = None

        self.id = id
        self.name = name
        if pattern:
            self._pattern = pattern
        if openPattern:
            self._pattern = openPattern
        self._closePattern = closePattern
        self._color = color
        self._bold = bold
        if matchOptions:
            for c in matchOptions:
                if c == "i":
                    self.insensitiveCaseMatch = True
                else:
                    raise ValueError, "Unknown matchOption: %s" % c


    def _compilePatterns( self ):
        if self.pattern:
            self._matchExpression = QRegExp( self.pattern )
        else:
            self._matchExpression = None

        if self.closePattern:
            self._closeExpression = QRegExp( self.closePattern )
        else:
            self._closeExpression = None

    def getPattern( self ):
        return self._pattern
    def setPattern( self, value ):
        self._pattern = value
        self._patternsInvalid = True
    pattern = property( getPattern, setPattern )
    openPattern = property( getPattern, setPattern )

    def getClosePattern( self ):
        return self._closePattern
    def setClosePattern( self ):
        self._closePattern = value
        self._patternsInvalid = True
    closePattern = property( getClosePattern, setClosePattern )

    def getMatchExpression( self ):
        if self._patternsInvalid:
            self._compilePatterns()
        return self._matchExpression
    matchExpression = property( getMatchExpression )
    openExpression = property( getMatchExpression )

    def getCloseExpression( self ):
        if self._patternsInvalid:
            self._compilePatterns()
        return self._closeExpression
    closeExpression = property( getCloseExpression )

    def getIsContainer( self ):
        if self.closePattern:
            return True
        else:
            return False
    isContainer = property( getIsContainer )

    def getColor( self ):
        return self._color
    def setColor( self, value ):
        self._color = value
        self._formatInvalid = True
    color = property( getColor, setColor )

    def getBold( self ):
        return self._bold
    def setBold( self, value ):
        self._bold = value
        self._formatInvalid = True
    bold = property( getBold, setBold )

    def getFormat( self ):
        if self._formatInvalid:
            self._format = QtGui.QTextCharFormat()
            if self.color:
                self._format.setForeground( self.color )
            if self.bold:
                self._format.setFontWeight( QtGui.QFont.Bold )
            self._formatInvalid = False
        return self._format

UNSET = -1
DEFAULT = 0
COMMENT = 1
KEYWORD = 2

class SyntaxHighlighter( QtGui.QSyntaxHighlighter ):
    def __init__( self, parent ):
        QtGui.QSyntaxHighlighter.__init__( self, parent )
        self.parent = parent

        formatElements = [
            FormatElement( COMMENT, name="Comment",
                openPattern=r"/\*", closePattern=r"\*/",
                color=QColor("gray") ),
            FormatElement( KEYWORD, name="Keyword",
                pattern=r"\b(SELECT|DELETE|INSERT)\b",   matchOptions="i",
                color=QColor("blue"), bold=True )
        ]

        self._formatElements = {}
        for element in formatElements:
            self._formatElements[element.id] = element


    def highlightBlock( self, text ):
        # grab in existing state of parsing at the beginning of the line
  #      print "Entering with state %i" % self.currentBlockState()
        
        # initial run should set default state
        if self.currentBlockState() == UNSET:
            self.setCurrentBlockState( DEFAULT )

        # if in state, look for closer
        if self.currentBlockState() != DEFAULT and self._formatElements.has_key( state ):
            f = self._formatElements[state]
 #           print "...looking for close: %s" % f.name
            closeIndex = text.indexOf( f.closeExpression )
            if closeIndex >= 0:     # allow =0 for zero-width asserts
                bodyLength = closeIndex
                closerLength = f.closeExpression.matchLength()
                self.setFormat( 0, bodyLength + closerLength, f.getFormat() )
                self.setCurrentBlockState( DEFAULT )
                index = closeIndex + closerLength
            else:
                # match not closed, format to end of line
                length = text.length
                self.setFormat( 0, length, f.getFormat() )
                self.setCurrentBlockState( COMMENT )
                return
        else:
            index = 0
        
        while index >= 0:
            matchIndex = text.length
            matchKey = ""
            for k,f in self._formatElements.items():
#                print "...looking for: %s" % f.name
                testIndex = text.indexOf( f.matchExpression, index )
                if testIndex >= 0 and testIndex < lowestIndex:
                    matchIndex = textIndex
                    matchKey = k
                    matchLength = f.matchExpression.matchedLength()
                    matchFormat = f.getFormat()
                    # @type f FormatElement
                    matchIsContainer = f.isContainer
                    if matchIsContainer:
                        matchCloser = f.closeExpression
            if matchKey != "":
                self.setFormat( matchIndex, matchLength, matchFormat )
                index = matchIndex + matchLength
                if matchIsContainer:
                    closeIndex = text.indexOf( matchCloser, index )
                    if closeIndex >= 0:     # allow =0 for zero-width asserts
                        bodyLength = closeIndex - index
                        closerLength = matchClose.matchLength()
                        self.setFormat( index, bodyLength + closerLength,
                            matchFormat )
                        index = closeIndex + closerLength
                    else:
                        # match not closed, format to end of line
                        length = text.length - index
                        self.setFormat( index, length, matchFormat )
                        self.setCurrentBlockState( COMMENT )
                        return


def tokenizeStatements( query ):
    tokens = [ query ]
    seps = [ "'", '"', "\\", ";" ]
    statements = []


    beginIndex = 0
    lastCount = 0   # when we haven't managed to increase tokens, we're done
    while beginIndex < len(tokens):
        for sep in seps:
            tokens = tokens[0:beginIndex] + \
                list(tokens[beginIndex].partition( sep )) + \
                tokens[beginIndex+1:]
        tokens = [ token for token in tokens if token != '' ]
        if len(tokens) == lastCount:
            beginIndex += 1
        lastCount = len(tokens)


    currentStatement = ""
    inString = False
    strTerm = ""
    escaped = False
    skipToken = False
    for token in tokens:
        if inString:
            if escaped:
                escaped = False
            elif token == strTerm:
                inString = False
            elif token == "\\":
                escaped = True
        elif token == "'" or token == '"':
            inString = True
            strTerm = token
        elif token == ";":
            statements.append( currentStatement.strip() )
            currentStatement = ""
            skipToken = True
        if skipToken:
            skipToken = False
        else:
            currentStatement += token

    if len(currentStatement) > 0:
        statements.append( currentStatement.strip() )

    return statements
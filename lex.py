import enum
import sys

class Lexer:
    def __init__(self,source):
        self.source = source + "\n" # Source code to lex as a stirng. Append a newline to simplify lexing/parsing the last token/statement.
        self.curChar = "" # Current character in the string
        self.curPos = -1 # Current position in the string
        self.nextChar()
            
    # process the next character
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = "\0" # EOF
        else:
            self.curChar = self.source[self.curPos]
    
    # Return the lookahead character
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos + 1]
    
    # Invalid token found, print error message and exit
    def abort(self,message):
        sys.exit("Lexing error." + message)
    
    # Skip whitespace except newlines, which we will  use to indicate the end of a statement
    def skipWhitespace(self):
        while self.curChar == " " or self.curChar == "\t" or self.curChar == "\r":
            self.nextChar()
    
    # Skip comments in the code
    def skipComment(self):
        if self.curChar == "#":
            while self.curChar != "\n":
                self.nextChar()
    
    # Return the next token
    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = None
        
        if self.curChar == "+":
            token = Token(self.curChar, TokenType.PLUS)
            
        elif self.curChar == "-":
            token = Token(self.curChar, TokenType.MINUS)
            
        elif self.curChar == "*":
            token = Token(self.curChar, TokenType.ASTERISK)
            
        elif self.curChar == "/":
            token = Token(self.curChar, TokenType.SLASH)
            
        elif self.curChar == "=":
            # check if this token is "=" or "=="
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)
                
        elif self.curChar == ">":
            # check if this token is ">" or ">="
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)
                
        elif self.curChar == "<":
            # check if this token is "<" pr "<=":
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                
                token = Token(lastChar + self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LT)
        
        elif self.curChar == "!":
            # check if this token is "!" or "!="
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())
        
        elif self.curChar in ["'",'"']:
            # the type of quote used to start the string
            startQuote = self.curChar
            # Get characters between quotations.
            self.nextChar()
            startPos = self.curPos
            
            while self.curChar != startQuote:
                # Don't allow special characters in the string. No escape characters, newlines, tabs, or % .
                # We will be using C's printf on this string.
                if self.curChar in ["\r","\n","\t","\\","%"]:
                    self.abort("Illegal character in string")
                self.nextChar()
                
            tokText = self.source[startPos: self.curPos] # Get the substring
            token = Token(tokText, TokenType.STRING)
        
        elif  self.curChar.isdigit():
            # Leading character is a digit, so this must be a number.
            # Get all consecutive digits and decimal if there is one.
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == ".": #Decimal !
                self.nextChar()
                
                # Must have at least one digit after decimal
                if not self.peek().isdigit():
                    # Error!
                    self.abort("Illegal character in number")
                while self.peek().isdigit():
                    self.nextChar()
            
            tokText = self.source[startPos:self.curPos+1] # Get the substring
            token = Token(tokText, TokenType.NUMBER)
            
        
        elif self.curChar.isalpha():
            # Leading character is a letter, so this must be an identifier or a keyword
            # Get all consecutive alpha numeric characters
            startPos = self.curPos
            while self.peek().isalnum():
                self.nextChar()
                
                # Check if the token is in the list of keywords.
            tokText = self.source[startPos: self.curPos+1] # Get the substring.
            keyword = Token.checkIfKeyword(tokText)
            if keyword == None:
                token = Token(tokText, TokenType.IDENT)
            else:
                token = Token(tokText, keyword)
                        
        elif self.curChar == "\n":
            token = Token(self.curChar, TokenType.NEWLINE)
            
        elif self.curChar == "\0":
            token = Token(self.curChar, TokenType.EOF)
            
        else:
            # Unkown Token!
            self.abort("Unknown Token: " + self.curChar)
        
        self.nextChar()
        return token
    
    
    
    
    
class Token:
    def __init__(self,tokenText, tokenKind):
        self.text = tokenText
        self.kind = tokenKind
        
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            # Relies on all keyword enum values being 1xx.
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        return None
        
        
        
class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    
    # Keywords.
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    
    # Operators
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211


from ._tokens import *

class Lexer:
    def __init__(self):
        pass

    def sub_string(self, string, left, right):
        return string[left:right]

    def is_escape_char(self, ch):
        if ch == BACKTICK or ch == BEEP or ch == BACKSPACE or\
        ch == FORMFEED or  ch == NEWLINE  or  ch == CARRIAGERET or\
        ch == TABHORIZONTAL or ch == TABVERTICAL or ch == BACKSLASH or\
        ch == SINGLEQUOTE or ch == DOUBLEQUOTE or ch == QUESTIONMARK or ch == NULL:
        # ch == OCTALNUM or ch == HEXNUM or ch == NULL:
            return True         
        else:
            return False

    
    def is_delimiter(self, ch):
        if ch == SPACE or ch == NEWLINE or ch == ADD or ch == SUB or\
        ch == MUL or ch == DIV or ch == COMA or ch == SEMI or\
        ch == COLON or ch == G_THAN or ch == S_THAN or\
        ch == EQUALS or ch == LEFTBRACK or ch == RIGHTBRACK or\
        ch == LEFTCURL or ch == RIGHTCURL:
            return True
        else:
	        return False
    
    def is_operator(self, ch):
        if ch == ADD or ch == SUB or ch == MUL or\
        ch == DIV or ch == G_THAN or ch == S_THAN or\
        ch == EQUALS or ch == COLON or ch == COMA:
            return True
        else:
            return False
    
    def is_valid_identifier(self, string):
        if string[0] == ZERO or string[0] == ONE or\
        string[0] == TWO or string[0] == THREE or\
        string[0] == FOUR or string[0] == FIVE or\
        string[0] == SIX or string[0] == SEVEN or\
        string[0] == EIGHT or string[0] == NINE or self.is_delimiter(string[0]):
            return False
        else:
            return True

    def is_keyword(self, string):
        if string == LET or string == LOOP or\
	    string ==  BREAK or string ==  CONTINUE or\
	    string ==  IF or string ==  ELIF or\
	    string ==  ELSE or string ==  RETURN or\
	    string ==  INT or string ==  UINT or\
	    string ==  BOOL or string ==  FLOAT or\
	    string ==  STR:
            return True
        else:
	        return False
    
    def is_int(self, string):
        if string[0] != TICK:
            if string.find(".") != -1:
                return False
            else:
                return True
        return False

    def is_float(self, string):
        if string[0] != TICK:
            if string.find(".") != -1:
                return True
            else:
                return False
        return False

    def is_string(self, string):
        if string[0] == TICK and string[-1] == TICK:
            return True
        return False
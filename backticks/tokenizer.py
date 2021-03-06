from ._tokens import *
from .lexer import Lexer

class Tokenizer(Lexer):
    def __init__(self, bt_file_path):
        super().__init__()
        self.bt_file_path = bt_file_path
        self.bt_file_name = ""
        self.bin_name = ""
        self.c_file_name = ""
        self.h_file_name = ""
        self.current_line_no = 0
        self.tokens = []
        # try:
        self._tokenizer()
        # except IndexError:
        #     print("Error Occured")
        #     print(f"Total Lines: {self.current_line_no}")
            
        
    def __read_sc_file(self):
        
        with open(self.bt_file_path, "r") as sc_read:
            sc = sc_read.read()
            sc += "\n"

            self.bt_file_name = self.bt_file_path[self.bt_file_path.rfind("/")+1:]
        
            self.bin_name = self.bt_file_name[:self.bt_file_name.find(".bt")]
            self.c_file_name = self.bin_name + ".c"
            self.h_file_name = self.bin_name + ".h"

            return sc

    
    def _tokenizer(self, buf=None):
        from_file = False
        if buf == None:
            from_file = True
            buf = self.__read_sc_file()
        

        length = len(buf)
        left = 0
        right = 0

        tokens = []

        while (right < length):
            
            
            # COMMENTS

            # Single line
            if buf[right] == COMMENT:
                self.current_line_no += 1
                right += 1
                while right < length and buf[right] != NEWLINE:
                    right += 1

                if right < length:
                    right += 1
                    
                left = right
            
            elif buf[right] == SLASH and buf[right+1] == COMMENT:
                self.current_line_no += 1
                right += 2

                while right < length - 1 and (buf[right] != COMMENT and buf[right+1] != SLASH):
                    right += 1

                    if buf[right] == NEWLINE:
                        self.current_line_no += 1
                
                if right < length - 1:
                    right += 2

                left = right
            
            # Lists
            elif buf[right] == LEFTSQUARE:
                while right < length and not buf[right].endswith(RIGHTSQUARE):
                    right += 1
            
                
            else:

                # When string is found
                if buf[right] == TICK:
                    # left = right

                    right += 1

                    while right < length:
                        if buf[right] == TICK and buf[right-1] != BACKSLASH:
                            break
                        right += 1
                    right += 1

                    sub_str = self.sub_string(buf, left, right)

                    # Replace "\`" with "`"
                    sub_str = sub_str.replace(BACKTICK, TICK)
                    # print(sub_str)
                    # print("\n")
                    tokens.append(sub_str)
                    left = right+1

                # Simply increament if delimiter not found
                # print(right)
                if not self.is_delimiter(buf[right]):
                    right += 1


                if self.is_delimiter(buf[right]) and left == right:
                    
                    if buf[right] == NEWLINE:
                        self.current_line_no += 1

                    elif buf[right] == LEFTCURL or buf[right] == RIGHTCURL or\
                        buf[right] == LEFTBRACK or buf[right] == RIGHTBRACK or\
                        buf[right] == SEMI:
                        tokens.append(buf[right])

                    elif self.is_operator(buf[right]):
                        tokens.append(buf[right])
                    
                    right += 1
                    left = right

                # Extract substring
                elif self.is_delimiter(buf[right]) and left != right or (right == length and left != right):
                    sub_str = self.sub_string(buf, left, right)
                    tokens.append(sub_str)

                    left = right

        
        # Remove empty strings
        for i in tokens:
            if i == "":
                tokens.pop(tokens.index(i))
        
        # print(tokens)

        if from_file:
            # try:
            count = 0
            while (count < len(tokens)):
                if tokens[count] in [FUNCTION, PUB_FUNC, IF, ELIF, ELSE, LOOP, FOR]:
                    funcs = []

                    closing = 0
                    while count <= len(tokens):
                        
                        if tokens[count] == RIGHTCURL:
                            funcs.append(tokens[count])
                            closing -= 1

                            if closing <= 0:
                                break
                            else:
                                count += 1

                        # If another curl found
                        elif tokens[count] == LEFTCURL:
                            funcs.append(tokens[count])
                            closing += 1
                            count += 1
                        
                        else:
                            funcs.append(tokens[count])
                            count += 1

                            
                    # print(closing)
                    if closing != 0:
                        print("No closing bracket found!")
                        return 
                    else:
                        self.tokens.append(funcs)
                        count += 1
                

                else:
                    non_func = []
                    while tokens[count] != SEMI:
                        if tokens[count] != IMPORT:
                            non_func.append(tokens[count])
                        else:
                            non_func.append(tokens[count])
                            if tokens[count+2] == AS:
                                if tokens[count+4] != SEMI:
                                    tokens.insert(count+4, SEMI)
                            elif tokens[count+2] != SEMI:
                                tokens.insert(count+2, SEMI)
                        count += 1
                        
                    non_func.append(tokens[count])
                    self.tokens.append(non_func)
                    count += 1

                # for i in self.tokens:
                # print(self.tokens)

            # except IndexError:
                # print(f"Current Line: {self.current_line_no}")

        else:
            return tokens


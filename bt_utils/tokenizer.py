from ._tokens import *
from .lexer import Lexer

class Tokenizer(Lexer):
    def __init__(self, bt_file_name):
        super().__init__()
        self.bt_file_name = bt_file_name
        self.bin_name = self.bt_file_name.strip(".bt")
        self.c_file_name = self.bin_name + ".c"
        self.h_file_name = self.bin_name + ".h"
        self.tokens = []
        self.__tokenizer()
        
    def __read_sc_file(self):
        with open(self.bt_file_name, "r") as sc_read:
            sc = sc_read.read()
            sc += "\n"
            return sc

    
    def __tokenizer(self):
        buf = self.__read_sc_file()
        length = len(buf)
        left = 0
        right = 0

        tokens = []

        while (right < length):
            
            
            # COMMENTS

            # Single line
            if buf[right] == COMMENT:
                right += 1
                while (buf[right] != NEWLINE and right < length):
                    right += 1

                if right < length:
                    right += 1
                    
                left = right

            # # Multi line
            # elif buf[right] == TICK and buf[right+1] == TICK and buf[right+2] == TICK:
            #         right += 3 
            #         while ((buf[right] != TICK and buf[right+1] != TICK and buf[right+2] != TICK) and right < length):
            #             right += 1

            #         if right < length-3:
            #             right += 3

            #         left = right


            else:

                # TODO


                # if buf[right] == TICK and buf[right+1] == TICK and buf[right+2] == TICK:
                #     right += 3 
                #     while (buf[right] != TICK and buf[right+1] != TICK and buf[right+2] != TICK):
                #         right += 1

                #     if right < length-3:
                #         right += 3
                

                #     left = right

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

                    if buf[right] == LEFTCURL or buf[right] == RIGHTCURL or\
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



        count = 0
        while (count < len(tokens)):
            if tokens[count] == FUNCTION or tokens[count] == PUB_FUNC:
                funcs = []
                while tokens[count] != RIGHTCURL:
                    funcs.append(tokens[count])
                    count += 1
                funcs.append(tokens[count])
                self.tokens.append(funcs)
                count += 1

            else:
                non_func = []
                while tokens[count] != SEMI:
                    non_func.append(tokens[count])
                    count += 1
                non_func.append(tokens[count])
                self.tokens.append(non_func)
                count += 1

        # for i in self.tokens:
        #     print(i)

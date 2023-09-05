DIGITS = '0123456789'
after_kw = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'

###tokens###
T_INT = "INT"
T_FLOAT = "FLOAT"
T_STRING = "STRING"
T_ARRAY = "ARRAY"
T_BOOLEAN = "BOOL"
T_PLUS = "PLUS"
T_MINUS = "MINUS"
T_MUL = "MUL"
T_DIV = "DIV"
T_POW = "POW"
T_SQRT = "SQRT"
T_GRT = "GRT"
T_LST = "LST"
T_GOE = "GOE"
T_LOE = "LOE"
T_LPAR = "LPAR"
T_RPAR = "RPAR"
T_LGPAR = "LGPAR"
T_RGPAR = "RGPAR"
T_EQUAL = "EQUAL"
T_NOTEQUAL = "NOTEQUAL"
T_KEYWORD = "KW"
T_IDENTIFIER = "ID"
T_NEWLINE = "NEWLINE"
T_EOF = "EOF"
T_ERROR = "ERROR"
T_TRUE = "TRUE"
T_FALSE = "FALSE"
###tokens###

###keywords, Operations###
keywords = [
    "if",
    "else",
    "for",
    "while",
    "func",
    "store",
    "print",
    "func",
    "in",
    "GOE",
    "LOE",
    "NOE",
    "getAV",
    "setAV",
    "TRUE",
    "FALSE",
    "return",
    "append"
]

operations = [
    "+",
    "-",
    "*",
    "/",
    "**",
    "#",
    "=",
    ">",
    "<",
    "{",
    "}",
    "(",
    ")",
    ";",
]

operations_dict = {
    "+" : T_PLUS,
    "-" : T_MINUS,
    "*" : T_MUL,
    "/" : T_DIV,
    "**": T_POW,
    "#" : T_SQRT,
    "=" : T_EQUAL,
    ">" : T_GRT,
    "<" : T_LST,
    "{" : T_LGPAR,
    "}" : T_RGPAR,
    "(" : T_LPAR,
    ")" : T_RPAR,
    ";" : "SC",
}
###keywords###

def is_int(n):
    try:
        float_n = float(n)
        int_n = int(float_n)
    except ValueError:
        return False
    else:
        return float_n == int_n

def is_float(n):
    try:
        float_n = float(n)
    except ValueError:
        return False
    else:
        return True

class Token:
    def __init__(self, T_TYPE, value=None, arrLen=None):
        self.T_TYPE = T_TYPE
        self.value = value
        self.arrLen = arrLen

    def __repr__(self):
        if self.value:
            if self.arrLen: return f"{self.T_TYPE}: {self.value}"
            return f"{self.T_TYPE}: {self.value}"
        else:
            if self.value == 0:
                return f"{self.T_TYPE}: {self.value}"
            return f"{self.T_TYPE}"

    def matches(self, type_, value_):
        return self.T_TYPE == type_ and self.value == value_

class Lexer:
    def __init__(self, filename):
        self.lines = self.initialize(filename)
        self.currline = 0
        self.linepos = -1
        self.not_known_str = ""
        self.next_char = ""
        self.file_ended = False
        self.tokens = None
        self.found = False
        self.advance()

    def advance(self):
        if self.currline < len(self.lines):
            self.linepos+=1
            if self.linepos < len(self.lines[self.currline]):
                self.not_known_str+=self.lines[self.currline][self.linepos]
                if self.linepos+1 < len(self.lines[self.currline]):
                    self.next_char=self.lines[self.currline][self.linepos+1]
                elif self.currline+1<len(self.lines):
                    self.next_char=self.lines[self.currline+1][0]
            else:
                self.linepos=-1
                self.currline+=1
        else:
            self.file_ended=True

    def check_kw(self):
        if self.found:
            return None
        if self.not_known_str in keywords:
            if self.next_char in operations or self.next_char == " ":
                ret_str = self.not_known_str
                self.not_known_str = ""
                self.found = True
                if ret_str not in ("GOE","LOE","NOE","TRUE","FALSE"):
                    return Token(T_KEYWORD, ret_str)
                else:
                    if ret_str=="GOE":
                        return Token(T_GOE)
                    elif ret_str=="LOE":
                        return Token(T_LOE)
                    elif ret_str == "TRUE":
                        return Token(T_INT, 1)
                    elif ret_str == "FALSE":
                        return Token(T_INT, 0)
                    else:
                        return Token(T_NOTEQUAL)
        return None

    def check_id(self):
        if self.found:
            return None
        if (self.next_char in operations or self.next_char == " ") and self.not_known_str!="":
            ret_str = self.not_known_str
            self.not_known_str = ""
            self.found = True
            return Token(T_IDENTIFIER, ret_str)

    def check_op(self):
        if self.found:
            return None
        if self.not_known_str in operations:
            ret_str = self.not_known_str
            self.not_known_str = ""
            self.found = True
            needed_T = operations_dict[ret_str]
            if needed_T!="SC" and needed_T!=T_LGPAR and needed_T!=T_RGPAR:
                return [Token(needed_T)]
            elif needed_T=="SC":
                return [Token(T_KEYWORD, ";"), Token(T_NEWLINE)]
            else:
                return [Token(needed_T), Token(T_NEWLINE)]

    def check_num(self):
        num = self.not_known_str
        if self.found:
            return None

        while is_int(num+self.next_char) or is_float(num+self.next_char):
            self.advance()
            num=self.not_known_str
        #try to add if something doesnt work
        #num=self.not_known_str
        if is_int(num) or is_float(num):
            self.not_known_str = ""
            try:
                self.found=True
                return Token(T_INT, int(num))
            except:
                self.found=True
                return Token(T_FLOAT, float(num))
        else:
            return None

    #is used in check_arr for multidimensional arrays
    def find_inside_arr(self, arrvals, arrval, i):
        new_arr = [arrval[1:]]
        i += 1
        opened = 1
        while opened != 0 and i < len(arrvals):
            arrval = arrvals[i]
            if arrval == "]":
                opened -= 1
            elif arrval[0] == "[":
                ret_arr, i = self.find_inside_arr(arrvals,arrval,i)
                new_arr.append(ret_arr)
            else:
                new_arr.append(arrval)
            i += 1
        final_ret_arr = []
        for val in new_arr:
            if type(val)!=Token:
                if is_int(val):
                    final_ret_arr.append(int(val))
                elif is_float(val):
                    final_ret_arr.append(float(val))
                else:
                    final_ret_arr.append(str(val).strip('"'))
            else:
                final_ret_arr.append(val)
        return Token(T_ARRAY, final_ret_arr, len(final_ret_arr)), i-1

    #checks first part of an array
    def check_arr(self):
        arr = self.not_known_str
        lpar=0
        if self.found:
            return None
        # Tries to create an array
        if arr == "[":
            lpar+=1
        while lpar != 0:
            if self.next_char=="[":
                lpar+=1
            elif self.next_char == "]":
                lpar-=1
            self.advance( )
            arr = self.not_known_str
        arrvals = []
        #separates values with "," or " "
        if arr != "":
            if arr[0]=="[" and arr[-1]=="]":
                arr=arr[1:]
                val = ""
                for char in arr:
                    if char!=",":
                        val+=char
                    else:
                        arrvals.append(val)
                        val=""

        #checks if each value is a string, an int, a float or another array.
        final_ret_arr = []
        i=0
        while i < len(arrvals):
            arrval = arrvals[i]
            if is_int(arrval):
                final_ret_arr.append(int(arrval))
            elif is_float(arrval):
                final_ret_arr.append(float(arrval))
            elif arrval.find("[")!=-1:
                #if theres an open "[", checks for the possibility of a multi-dimensional array
                new_arr, i = self.find_inside_arr(arrvals,arrval,i)
                final_ret_arr.append(new_arr)
            else:
                final_ret_arr.append(str(arrval).strip('"'))
            i+=1
        if final_ret_arr!=[]:
            self.found=True
            self.not_known_str=""
            return Token(T_ARRAY, final_ret_arr, len(final_ret_arr))

    def check_string(self):
        if self.found:
            return None
        if len(self.not_known_str)>=2:
            if self.not_known_str[0] == '"' and self.not_known_str[-1]=='"':
                self.found=True
                found = self.not_known_str
                self.not_known_str=""
                return Token(T_STRING, found.strip('"'))

    def RUN(self):
        tokens = []
        while self.file_ended==False:
            self.not_known_str = self.not_known_str.strip()
            #print(f".{self.not_known_str}.")
            self.found=False
            _kw = self.check_kw()
            _ops = self.check_op()
            _num = self.check_num()
            _arr = self.check_arr()
            _str = self.check_string()
            _id = self.check_id()
            #done so to be simple to understand
            if _kw:
                tokens.append(_kw)
            elif _ops:
                for op in _ops:
                    tokens.append(op)
            elif _num:
                tokens.append(_num)
            elif _arr:
                tokens.append(_arr)
            elif _str:
                tokens.append(_str)
            elif _id:
                tokens.append(_id)


            self.advance()
        tokens.append(Token(T_EOF))
        for tok in tokens:
            if tok==None:
                tokens.remove(tok)
        self.tokens = tokens

    def initialize(self, filename):
        f = open(filename)
        lines = []
        for line in f:
            lines.append(line)
        return lines
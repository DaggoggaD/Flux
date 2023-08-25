DIGITS = '0123456789'
after_kw = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'

###tokens###
T_INT = "INT"
T_FLOAT = "FLOAT"
T_STRING = "STRING"
T_ARRAY = "ARRAY"
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
    "setAV"
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
                return Token(T_KEYWORD, ret_str)
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
            if needed_T!="SC":
                return [Token(needed_T)]
            else:
                return [Token(T_KEYWORD, ";"), Token(T_NEWLINE)]

    def check_num(self):
        num = self.not_known_str
        if self.found:
            return None
        while is_int(num+self.next_char) or is_float(num+self.next_char):
            num = self.not_known_str
            self.advance()
        num=self.not_known_str

        if is_int(num) or is_float(num):
            self.not_known_str = ""
            try:
                return Token(T_INT, int(num))
            except:
                return Token(T_FLOAT, float(num))
        else:
            return None

    def check_arr(self):
        arr = self.not_known_str
        lpar=0
        if self.found:
            return None
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
        if arr != "":
            if arr[0]=="[" and arr[-1]=="]":
                arr=arr[1:]
                val = ""
                print(arr)
                for char in arr:
                    if char!=",":
                        val+=char
                    else:
                        arrvals.append(val)
                        val=""
        print(arrvals)
        #CONTINUE HERE, array is splitted in chars if one dimension, in string if multidim or float
        #check if each value is a number, if so add to array as number
        #check if it contains [ or ] in a new func to create arrays in arrays


        return

    def RUN(self):
        tokens = []
        while self.file_ended==False:
            self.not_known_str = self.not_known_str.strip()
            self.found=False
            _kw = self.check_kw()
            _ops = self.check_op()
            _num = self.check_num()
            _arr = self.check_arr()
            #_str = self.check_string()
            _id = self.check_id()
            #done so to be simple to understand
            if _kw:
                tokens.append(_kw)
            if _ops:
                for op in _ops:
                    tokens.append(op)
            if _num:
                tokens.append(_num)
            if _id:
                tokens.append(_id)

            self.advance()
        print(tokens)

    def initialize(self, filename):
        f = open(filename)
        lines = []
        for line in f:
            lines.append(line)
        return lines


Lex = Lexer("test.flux")
Lex.RUN()
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
    ";",
    "if",
    "else",
    "for",
    "while",
    "func",
    "store",
    "print",
    "func",
    "{",
    "}",
    "(",
    ")",
    "in",
    ">",
    "<",
    "GOE",
    "LOE",
    "NOE",
    "getAV"
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
]
###keywords###

class Token:
    def __init__(self, T_TYPE, value=None, arrLen=None):
        self.T_TYPE = T_TYPE
        self.value = value
        self.arrLen = arrLen

    def __repr__(self):
        if self.value:
            if self.arrLen: return f"{self.T_TYPE}: {self.value}, lenght:{self.arrLen}"
            return f"{self.T_TYPE}: {self.value}"
        else:
            if self.value == 0:
                return f"{self.T_TYPE}: {self.value}"
            return f"{self.T_TYPE}"

    def matches(self, type_, value_):
        return self.T_TYPE == type_ and self.value == value_

class Lexer:

    def check_array_in_string(self, Varr, Vstring):
        for val in Varr:
            if val in Vstring:
                return True

    def openfile(self, filename):
        f = open(filename)
        tokens = []
        for line in f:
            nline = line.split( )
            nline.append('NEWLINE')
            tokens.append(nline)
        return tokens

    def array_finder(self, token):
        values = token[1:]
        arrVals = []
        numv = ""
        dotn2 = 0
        arrLen = 0
        sqn = 1
        i=0
        while i < len(values):
            ArrVal = values[i]
            if ArrVal == "[":
                new_arr = ""
                while ArrVal!="]" or sqn!=1:
                    if ArrVal == "[":
                        sqn+=1
                    elif ArrVal == "]":
                        sqn-=1
                    if sqn!=1:
                        new_arr+=ArrVal
                    else:
                        if ArrVal=="]":
                            i += 1
                            if i < len(values):
                                ArrVal = values[i]
                            break
                    i+=1
                    if i < len(values):
                        ArrVal=values[i]
                new_arr+="]"
                new_arr=new_arr[0:]
                print(new_arr)
                arrVals.append(self.array_finder(new_arr))
            elif ArrVal != ",":
                if ArrVal == "." and dotn2 == 0:
                    dotn2 += 1
                    numv += ArrVal
                if ArrVal != ".":
                    numv += ArrVal
            else:
                dotn2 = 0
                arrLen +=1
                try:
                    try:
                        arrVals.append(int(numv))
                    except:
                        arrVals.append(float(numv))
                except:
                    arrVals.append(numv.strip('"'))
                numv = ""
            i+=1
        return Token(T_ARRAY, arrVals, arrLen)

    def find_tokens(self, lines):
        tokens = []
        for line in lines:
            for token in line:
                if token == '=':
                    tokens.append(Token(T_EQUAL))
                elif token == '+':
                    tokens.append(Token(T_PLUS))
                elif token == '-':
                    tokens.append(Token(T_MINUS))
                elif token == '*':
                    tokens.append(Token(T_MUL))
                elif token == '/':
                    tokens.append(Token(T_DIV))
                elif token == '**':
                    tokens.append(Token(T_POW))
                elif token == '#':
                    tokens.append(Token(T_SQRT))
                elif token == '>':
                    tokens.append(Token(T_GRT))
                elif token == '<':
                    tokens.append(Token(T_LST))
                elif token == 'GOE':
                    tokens.append(Token(T_GOE))
                elif token == 'LOE':
                    tokens.append(Token(T_LOE))
                elif token == 'NOE':
                    tokens.append(Token(T_NOTEQUAL))
                elif token == '(':
                    tokens.append(Token(T_LPAR))
                elif token == ')':
                    tokens.append(Token(T_RPAR))
                elif token == '{':
                    tokens.append(Token(T_LGPAR))
                elif token == '}':
                    tokens.append(Token(T_RGPAR))
                elif token == 'NEWLINE':
                    tokens.append(Token(T_NEWLINE))
                elif token == 'if':
                    tokens.append(Token(T_KEYWORD, token))
                elif token == 'elif':
                    tokens.append(Token(T_KEYWORD, token))
                elif token == 'else':
                    tokens.append(Token(T_KEYWORD, token))
                elif token == 'for':
                    tokens.append(Token(T_KEYWORD, token))
                elif token == 'while':
                    tokens.append(Token(T_KEYWORD, token))
                elif token == 'func':
                    tokens.append(Token(T_KEYWORD, token))
                elif token == 'store':
                    tokens.append(Token(T_KEYWORD, token))
                elif token in keywords:
                    tokens.append(Token(T_KEYWORD, token))
                else:
                    if token[0]=='"':
                        if token[-1]=='"':
                            print(tokens)
                            tokens.append(Token(T_STRING, token))
                    elif token[0]=='[':
                        if token[-1]==']':
                            tokens.append(self.array_finder(token))
                    else:
                        #first try handles integers or floats
                        try:
                            try:
                                tokens.append(Token(T_INT,int(token)))

                            except:
                                tokens.append(Token(T_FLOAT, float(token)))

                        #except handles identifiers, keywords and operators when no space is given
                        except:
                            opening_quotes = 0
                            fullstr = token
                            fs_l = len(fullstr)
                            idx = 0
                            not_known_string = ""
                            while idx < fs_l:
                                #handles one char keywords
                                if fullstr[idx] in keywords:
                                    if fullstr[idx] == '(':
                                        tokens.append(Token(T_LPAR))
                                    elif fullstr[idx] == ')':
                                        tokens.append(Token(T_RPAR))
                                    elif fullstr[idx] == '{':
                                        tokens.append(Token(T_LGPAR))
                                    elif fullstr[idx] == '}':
                                        tokens.append(Token(T_RGPAR))
                                    elif fullstr[idx] == '>':
                                        tokens.append(Token(T_GRT))
                                    elif fullstr[idx] == '<':
                                        tokens.append(Token(T_LST))
                                    elif fullstr[idx] == 'GOE':
                                        tokens.append(Token(T_GOE))
                                    elif fullstr[idx] == 'LOE':
                                        tokens.append(Token(T_LOE))
                                    else:
                                        tokens.append(Token(T_KEYWORD, fullstr[idx]))
                                #handles one char operators (and power operator)
                                elif fullstr[idx] in operations:
                                    if fullstr[idx] == "*":
                                        try:
                                            if fullstr[idx+1] == "*":
                                                tokens.append(Token(T_POW))
                                                idx+=1
                                            else:
                                                tokens.append(Token(T_MUL))
                                        except:
                                            tokens.append(Token(T_MUL))
                                    elif fullstr[idx] == '=':
                                        tokens.append(Token(T_EQUAL))
                                    elif fullstr[idx] == '+':
                                        tokens.append(Token(T_PLUS))
                                    elif fullstr[idx] == '-':
                                        tokens.append(Token(T_MINUS))
                                    elif fullstr[idx] == '/':
                                        tokens.append(Token(T_DIV))
                                    elif fullstr[idx] == '#':
                                        tokens.append(Token(T_SQRT))
                                #handles longer keywords or identifiers or numbers
                                else:
                                    not_known_string+=fullstr[idx]
                                    if not_known_string=='"':
                                        while idx+1 < len(fullstr) and fullstr[idx+1]!='"':
                                            idx+=1
                                            not_known_string+=fullstr[idx]
                                        not_known_string+='"'
                                        idx+=1
                                        tokens.append(Token(T_STRING,not_known_string.strip('"')))
                                        not_known_string=""
                                    elif not_known_string=='[':
                                        while idx+1 < len(fullstr) and fullstr[idx+1]!=']':
                                            idx+=1
                                            not_known_string+=fullstr[idx]
                                        not_known_string+=']'
                                        idx+=1
                                        if not_known_string[0] == '[':
                                            if not_known_string[-1] == ']':
                                                values = not_known_string[1:-1]
                                                arrVals = []
                                                numv = ""
                                                dotn2 = 0
                                                for ArrVal in values:
                                                    if ArrVal != ",":
                                                        if ArrVal == "." and dotn2 == 0:
                                                            dotn2 += 1
                                                            numv += ArrVal
                                                        if ArrVal != ".":
                                                            numv += ArrVal
                                                    else:
                                                        dotn2 = 0
                                                        try:
                                                            try:
                                                                arrVals.append(int(numv))
                                                            except:
                                                                arrVals.append(float(numv))
                                                        except:
                                                            arrVals.append(numv.strip('"'))
                                                        numv = ""
                                                tokens.append(Token(T_ARRAY, arrVals))

                                        not_known_string=""
                                    #handles long keywords
                                    elif not_known_string in keywords:
                                        id2x = idx+1
                                        if id2x < len(fullstr):
                                            if fullstr[id2x] in after_kw:
                                                not_known_string+=fullstr[id2x]
                                                idx = id2x
                                            else:
                                                tokens.append(Token(T_KEYWORD,not_known_string))
                                                not_known_string = ""
                                        else:
                                            tokens.append(Token(T_KEYWORD, not_known_string))
                                            not_known_string = ""
                                    # handles long numbers
                                    elif not_known_string.isdigit():
                                        nums = not_known_string
                                        id2x = idx + 1
                                        numnotended = True
                                        dotn = 0
                                        while numnotended:
                                            if id2x < len(fullstr):
                                                if fullstr[id2x].isdigit():
                                                    nums+=fullstr[id2x]
                                                    id2x += 1
                                                elif fullstr[id2x] == "." and dotn == 0:
                                                    nums+="."
                                                    dotn+=1
                                                    id2x+=1
                                                else:
                                                    numnotended=False
                                            else:
                                                numnotended=False

                                        try:
                                            tokens.append(Token(T_INT, int(nums)))
                                            not_known_string = ""
                                        except:
                                            tokens.append(Token(T_FLOAT, float(nums)))
                                            not_known_string = ""
                                        idx = id2x-1
                                    # handles long identifiers
                                    elif idx + 1 >= fs_l:
                                        tokens.append(Token(T_IDENTIFIER, not_known_string))
                                        not_known_string = ""
                                    elif fullstr[idx+1] not in after_kw:
                                        tokens.append(Token(T_IDENTIFIER, not_known_string))
                                        not_known_string = ""
                                    elif not_known_string in operations:
                                        if not_known_string == "*":
                                            tokens.append(Token(T_MUL))
                                        elif not_known_string == '=':
                                            tokens.append(Token(T_EQUAL))
                                        elif not_known_string == '+':
                                            tokens.append(Token(T_PLUS))
                                        elif not_known_string == '-':
                                            tokens.append(Token(T_MINUS))
                                        elif not_known_string == '/':
                                            tokens.append(Token(T_DIV))
                                        elif not_known_string == '#':
                                            tokens.append(Token(T_SQRT))
                                        not_known_string = ""

                                idx+=1


        return tokens


    def advance(self):
        self.tk_id+=1
        if self.tk_id < len(self.tokens):
            self.curr_token = self.tokens[self.tk_id+1]

    def RUN_lexer(self, filename):
        lines = self.openfile(filename)
        self.tokens = self.find_tokens(lines)
        self.tokens.append(Token(T_EOF))
        #self.tokens = self.split_special()
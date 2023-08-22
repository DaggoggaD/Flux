from _parser import *

class Interpreter:
    def __init__(self, filename):
        self.filename = filename
        self.expressions = self.initialize(filename)
        self.globalvars = []
        self.globalfunc = []

    def getVarVal(self, _token, knownVars):
        try:
            if _token.T_TYPE in (T_INT, T_FLOAT, T_STRING):
                return _token
            elif _token.T_TYPE in (T_IDENTIFIER):
                for knownVar in knownVars:
                    if knownVar[0].value == _token.value:
                        return knownVar[1]
                return None
        except:
            if type(_token) in (int, str, float):
                return _token


    def binop(self, expr, knownVars):
        TOK = {
            int:T_INT,
            float:T_FLOAT,
            str:T_STRING
        }
        left = expr.left
        op = expr.op
        right = expr.right
        if type(left) == BinOP:
            left = self.binop(left, knownVars)
        if type(right) == BinOP:
            right = self.binop(right, knownVars)
        if type(left) == GetAVStatement:
            left = self.getAVStat(left, knownVars)
        if type(right) == GetAVStatement:
            right = self.getAVStat(right, knownVars)

        opl = self.getVarVal(left.tok, knownVars)
        opr = self.getVarVal(right.tok, knownVars)
        if type(opl) == NumberNode:
            opl = opl.tok
        if type(opr) == NumberNode:
            opr = opr.tok
        opl = opl.value
        opr = opr.value

        if op.T_TYPE == T_PLUS:
            res = round(opl+opr,8)
            res_T = type(res)
            return NumberNode(Token(TOK[res_T],res))
        elif op.T_TYPE == T_MINUS:
            try:
                res = round(opl-opr,8)
                res_T = type(res)
                return NumberNode(Token(TOK[res_T],res))
            except:
                print("ERROR: Cannot perform - between string and string or subtract int/float and string")
                return None
        elif op.T_TYPE == T_DIV:
            try:
                res = round(opl/opr,8)
                res_T = type(res)
                return NumberNode(Token(TOK[res_T],res))
            except:
                print("ERROR: Cannot perform / between string and string or divide int/float and string.")
                return None
        elif op.T_TYPE == T_MUL:
            try:
                res = round(opl*opr,8)
                res_T = type(res)
                return NumberNode(Token(TOK[res_T],res))
            except:
                print("ERROR: Cannot perform * between string and string or multiply int/float and string.")
                return None
        elif op.T_TYPE == T_EQUAL:
            try:
                res = opl==opr
                if res == True:
                    return NumberNode(Token(T_TRUE))
                elif res == False:
                    return NumberNode(Token(T_FALSE))
            except:
                print("ERROR: Cannot perform > between string and string or > int/float and string.")
                return None
        elif op.T_TYPE == T_NOTEQUAL:
            try:
                res = opl!=opr
                if res == True:
                    return NumberNode(Token(T_TRUE))
                elif res == False:
                    return NumberNode(Token(T_FALSE))
            except:
                print("ERROR: Cannot perform > between string and string or > int/float and string.")
                return None
        elif op.T_TYPE == T_GRT:
            try:
                res = opl>opr
                if res == True:
                    return NumberNode(Token(T_TRUE))
                elif res == False:
                    return NumberNode(Token(T_FALSE))
            except:
                print("ERROR: Cannot perform > between string and string or > int/float and string.")
                return None
        elif op.T_TYPE == T_LST:
            try:
                res = opl<opr
                if res == True:
                    return NumberNode(Token(T_TRUE))
                elif res == False:
                    return NumberNode(Token(T_FALSE))
            except:
                print("ERROR: Cannot perform < between string and string or < int/float and string.")
                return None
        elif op.T_TYPE == T_GOE:
            try:
                res = opl>=opr
                if res == True:
                    return NumberNode(Token(T_TRUE))
                elif res == False:
                    return NumberNode(Token(T_FALSE))
            except:
                print("ERROR: Cannot perform >= between string and string or >= int/float and string.")
                return None
        elif op.T_TYPE == T_LOE:
            try:
                res = opl<=opr
                if res == True:
                    return NumberNode(Token(T_TRUE))
                elif res == False:
                    return NumberNode(Token(T_FALSE))
            except:
                print("ERROR: Cannot perform <= between string and string or <= int/float and string.")
                return None

    def storevar(self, expr, knownVars):
        found=0
        found_index = None
        for knownVar in knownVars:
            if knownVar[0].value == expr.var_name.value:
                found+=1
                found_index=knownVars.index(knownVar)
        if found == 0:
            value = expr.expr_value
            if type(value)==BinOP:
                value = self.binop(value, knownVars)
                knownVars.append([Token(T_IDENTIFIER,expr.var_name.value),value.tok])
            elif type(value)==GetAVStatement:
                value = self.getAVStat(value,knownVars)
                knownVars.append([Token(T_IDENTIFIER,expr.var_name.value),value.tok])
            elif type(value)==NumberNode:
                if value.tok.T_TYPE == T_IDENTIFIER:
                    value = self.getVarVal(value.tok,knownVars)
                    knownVars.append([Token(T_IDENTIFIER, expr.var_name.value), value])
                    print(knownVars)
                else:
                    knownVars.append([Token(T_IDENTIFIER, expr.var_name.value), value])
            else:
                knownVars.append([Token(T_IDENTIFIER,expr.var_name.value),expr.expr_value.tok])
        else:
            value = expr.expr_value
            if type(value) == BinOP:
                value = self.binop(value,knownVars)
                knownVars[found_index][1]= value.tok
            elif type(value) == GetAVStatement:
                value = self.getAVStat(value, knownVars)
                knownVars[found_index][1]=value.tok
            elif type(value) == NumberNode:
                if value.tok.T_TYPE == T_IDENTIFIER:
                    value = self.getVarVal(value.tok, knownVars)
                    knownVars[found_index][1]=value
                else:
                    knownVars[found_index][1]=value
            else:
                knownVars[found_index][1]= value.tok

    def printStat(self,expr, knownVars):
        if type(expr.value)==BinOP:
            printVal = self.binop(expr.value,knownVars)
            print(printVal.tok.value)
        elif type(expr.value) == GetAVStatement:
            printVal = self.getAVStat(expr.value, knownVars)
            print(printVal.tok.value)
        else:
            if type(expr.value) == NumberNode:
                printVal = self.getVarVal(expr.value.tok, knownVars)
                print(printVal.value)
            else:
                printVal = self.getVarVal(expr.value.tok,knownVars)
                print(printVal)

    def ifStat(self, expr, knownVars):
        compexpr = expr.compexpr
        ifexpr = expr.expression
        binOpResults = []
        if self.binop(compexpr,knownVars).tok.T_TYPE==T_TRUE:
            for lineExpr in ifexpr:
                if type(lineExpr) == BinOP:
                    binOpResults.append(self.binop(lineExpr, knownVars))
                elif type(lineExpr) == VarAssignNode:
                    self.storevar(lineExpr, knownVars)
                elif type(lineExpr) == PrintStatement:
                    self.printStat(lineExpr, knownVars)
                elif type(lineExpr) == IfStatement:
                    self.ifStat(lineExpr, knownVars)
                elif type(lineExpr) == WhileStatement:
                    self.whileStat(lineExpr, knownVars)
                elif type(lineExpr) == FuncStatement:
                    self.funcStat(lineExpr, knownVars)
                elif type(lineExpr) == GetAVStatement:
                    self.getAVStat(lineExpr, knownVars)

    def whileStat(self, expr, knownVars):
        compexpr = expr.compexpr
        ifexpr = expr.expression
        binOpResults = []
        while self.binop(compexpr, knownVars).tok.T_TYPE == T_TRUE:
            for lineExpr in ifexpr:
                if type(lineExpr) == BinOP:
                    binOpResults.append(self.binop(lineExpr, knownVars))
                elif type(lineExpr) == VarAssignNode:
                    self.storevar(lineExpr, knownVars)
                elif type(lineExpr) == PrintStatement:
                    self.printStat(lineExpr, knownVars)
                elif type(lineExpr) == IfStatement:
                    self.ifStat(lineExpr, knownVars)
                elif type(lineExpr) == WhileStatement:
                    self.whileStat(lineExpr, knownVars)
                elif type(lineExpr) == FuncStatement:
                    self.funcStat(lineExpr, knownVars)
                elif type(lineExpr) == GetAVStatement:
                    self.getAVStat(lineExpr, knownVars)
    #NEEDS TO BE IMPLEMENTED
    def elseStat(self, expr, knownVars):
        elsexpr = expr.expression
        binOpResults = []
        for lineExpr in elsexpr:
            if type(lineExpr) == BinOP:
                binOpResults.append(self.binop(lineExpr, knownVars))
            elif type(lineExpr) == VarAssignNode:
                self.storevar(lineExpr, knownVars)
            elif type(lineExpr) == PrintStatement:
                self.printStat(lineExpr, knownVars)
            elif type(lineExpr) == IfStatement:
                self.ifStat(lineExpr, knownVars)
            elif type(lineExpr) == ElseStatement:
                self.elseStat(lineExpr, knownVars)

    def getAVStat(self, expr,knownVars):
        TOK = {
            int:T_INT,
            float:T_FLOAT,
            str:T_STRING,
            Token:T_ARRAY
        }
        _array = self.getVarVal(expr.array,knownVars)
        neededvar = _array[self.getVarVal(expr.location, knownVars)]
        if type(neededvar) == Token:
            return NumberNode(Token(TOK[type(neededvar)],neededvar.value))
        else:
            return NumberNode(Token(TOK[type(neededvar)],neededvar))


    def initialize(self, filename):
        C_Lexer = Lexer()
        C_Lexer.RUN_lexer(filename)
        C_Parser = Parser(C_Lexer.tokens)
        C_expressions = C_Parser.run()
        print(C_Parser.tokens)
        print(C_expressions)
        return C_expressions

    def RUN(self):
        knownVars = []
        for lineExpr in self.expressions:
            if type(lineExpr) == BinOP:
                print(self.binop(lineExpr, knownVars))
            elif type(lineExpr) == VarAssignNode:
                self.storevar(lineExpr, knownVars)
            elif type(lineExpr) == PrintStatement:
                self.printStat(lineExpr, knownVars)
            elif type(lineExpr) == IfStatement:
                self.ifStat(lineExpr, knownVars)
            elif type(lineExpr) == WhileStatement:
                self.whileStat(lineExpr, knownVars)
            elif type(lineExpr) == FuncStatement:
                self.funcStat(lineExpr,knownVars)
            elif type(lineExpr) == GetAVStatement:
                self.getAVStat(lineExpr,knownVars)

"""EXAMPLE OF A GLOBALVAR FORMAT
_Interpreter.globalvars.append([Token(T_IDENTIFIER,"TESTVAR"),Token(T_INT,int(1))])
"""

import copy
import math

from _parser import *

class Interpreter:
    def __init__(self, filename):
        self.filename = filename
        self.expressions = self.initialize(filename)

    def getVarVal(self, _token, knownVars):
        try:
            if _token.T_TYPE in (T_INT, T_FLOAT, T_STRING, T_ARRAY):
                return _token
            elif _token.T_TYPE in (T_IDENTIFIER):
                for knownVar in knownVars:
                    if knownVar[0].value == _token.value:
                        if type(knownVar[1])==Token:
                            return knownVar[1]
                        return knownVar[1].tok
                return None
        except:
            if type(_token) in (int, str, float):
                return _token


    def binop(self, expr, knownFunc, knownVars):
        TOK = {
            int:T_INT,
            float:T_FLOAT,
            str:T_STRING
        }
        left = expr.left
        op = expr.op
        right = expr.right

        if type(left) == BinOP:
            left = self.binop(left, knownFunc,knownVars)
        elif type(left) == GetAVStatement:
            left = self.getAVStat(left, knownVars)
        elif type(left) == RunFuncStatement:
            left = NumberNode(self.runFuncStatement(left, knownFunc, knownVars))
        elif type(left) == RandomStatement:
            left = self.randStatement()
        elif type(left) == RandIntStatement:
            left = self.randIntStatement(left, knownVars)

        if type(right) == BinOP:
            right = self.binop(right, knownFunc, knownVars)
        elif type(right) == GetAVStatement:
            right = self.getAVStat(right, knownVars)
        elif type(right) == RunFuncStatement:
            right = NumberNode(self.runFuncStatement(right, knownFunc, knownVars))
        elif type(right) == RandomStatement:
            right = self.randStatement()
        elif type(right) == RandomStatement:
            right = self.randIntStatement(right, knownVars)

        opl = self.getVarVal(left.tok, knownVars)
        opr = self.getVarVal(right.tok, knownVars)

        if opl!=None and opr!=None:
            if type(opl) == NumberNode:
                opl = opl.tok
            if type(opr) == NumberNode:
                opr = opr.tok
            opl = opl.value
            opr = opr.value

        if op.T_TYPE == T_DOLLAR:
            classOBJ = opl
            neededclassv = right.tok
            if type(classOBJ) == Token:
                classvars = classOBJ.value[0]
                classfunc = classOBJ.value[1]
            if type(classOBJ) == list:
                classvars = classOBJ[0]
                classfunc = classOBJ[1]

            for var in classvars:
                if var[0].matches(T_IDENTIFIER, neededclassv.value):
                    return NumberNode(var[1])
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


    def storevar(self, expr, knownFunc, knownVars):
        found=0
        found_index = None
        for knownVar in knownVars:
            if knownVar[0].value == expr.var_name.value:
                found+=1
                found_index=knownVars.index(knownVar)
        if found == 0:
            value = expr.expr_value
            if type(value)==BinOP:
                value = self.binop(value, knownFunc,knownVars)
                knownVars.append([Token(T_IDENTIFIER,expr.var_name.value),value.tok])
            elif type(value)==GetAVStatement:
                value = self.getAVStat(value,knownVars)
                knownVars.append([Token(T_IDENTIFIER,expr.var_name.value),value.tok])
            elif type(value)==RunFuncStatement:
                value = self.runFuncStatement(value, knownFunc, knownVars)
                knownVars.append([Token(T_IDENTIFIER,expr.var_name.value),value])
            elif type(value)==NumberNode:
                if value.tok.T_TYPE == T_IDENTIFIER:
                    value = self.getVarVal(value.tok,knownVars)
                    knownVars.append([Token(T_IDENTIFIER, expr.var_name.value), value])
                else:
                    knownVars.append([Token(T_IDENTIFIER, expr.var_name.value), value])
            elif type(value) == RandomStatement:
                value = self.randStatement()
                knownVars.append([Token(T_IDENTIFIER,expr.var_name.value),value.tok])
            elif type(value) == RandIntStatement:
                value = self.randIntStatement(value, knownVars)
                knownVars.append([Token(T_IDENTIFIER, expr.var_name.value), value.tok])
            elif type(value) == RoundStatement:
                value = self.roundStatement(value, knownVars)
                knownVars.append([Token(T_IDENTIFIER, expr.var_name.value), value.tok])
            elif type(value) == RootStatement:
                value = self.rootStatement(value, knownVars)
                knownVars.append([Token(T_IDENTIFIER, expr.var_name.value), value.tok])
            elif type(value) == LogStatement:
                value = self.logStatement(value, knownVars)
                knownVars.append([Token(T_IDENTIFIER, expr.var_name.value), value.tok])
            elif type(value) == PowStatement:
                value = self.powStatement(value, knownVars)
                knownVars.append([Token(T_IDENTIFIER, expr.var_name.value), value.tok])
            elif type(value) == ToIntStatement:
                value = self.toIntStatement(value, knownVars)
                knownVars.append([Token(T_IDENTIFIER, expr.var_name.value), value.tok])
            elif type(value) == ToFloatStatement:
                value = self.toFloatStatement(value, knownVars)
                knownVars.append([Token(T_IDENTIFIER, expr.var_name.value), value.tok])
            elif type(value) == InputStatement:
                value = self.inputStatement(value, knownVars)
                knownVars.append([Token(T_IDENTIFIER, expr.var_name.value), value.tok])
            elif type(value) == ClassStatement:
                value = self.classStatement(value, knownVars)
                knownVars.append([Token(T_IDENTIFIER, expr.var_name.value), value.tok])
            elif type(value) == InstantiateStatement:
                value = self.instantiateStatement(value, knownVars)
                knownVars.append([Token(T_IDENTIFIER, expr.var_name.value), value.tok])
            else:
                knownVars.append([Token(T_IDENTIFIER,expr.var_name.value),expr.expr_value.tok])
        else:
            value = expr.expr_value
            if type(value) == BinOP:
                value = self.binop(value,knownFunc,knownVars)
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
            elif type(value) == RunFuncStatement:
                value = self.runFuncStatement(value,knownFunc,knownVars)
                knownVars[found_index][1] = value
            elif type(value) == RandomStatement:
                value = self.randStatement()
                knownVars[found_index][1] = value.tok
            elif type(value) == RandIntStatement:
                value = self.randIntStatement(value, knownVars)
                knownVars[found_index][1] = value.tok
            elif type(value) == RoundStatement:
                value = self.roundStatement(value, knownVars)
                knownVars[found_index][1] = value.tok
            elif type(value) == RootStatement:
                value = self.rootStatement(value, knownVars)
                knownVars[found_index][1] = value.tok
            elif type(value) == LogStatement:
                value = self.logStatement(value, knownVars)
                knownVars[found_index][1] = value.tok
            elif type(value) == PowStatement:
                value = self.powStatement(value, knownVars)
                knownVars[found_index][1] = value.tok
            elif type(value) == ToIntStatement:
                value = self.toIntStatement(value, knownVars)
                knownVars[found_index][1] = value.tok
            elif type(value) == ToFloatStatement:
                value = self.toFloatStatement(value, knownVars)
                knownVars[found_index][1] = value.tok
            elif type(value) == InputStatement:
                value = self.inputStatement(value, knownVars)
                knownVars[found_index][1] = value.tok
            elif type(value) == ClassStatement:
                value = self.classStatement(value, knownVars)
                knownVars[found_index][1] = value.tok
            elif type(value) == InstantiateStatement:
                self.instantiateStatement(value, knownVars)
                knownVars[found_index][1] = value.tok
            else:
                knownVars[found_index][1]= value.tok


    def printStat(self,expr, knownFunc, knownVars):
        if type(expr.value)==BinOP:
            printVal = self.binop(expr.value,knownFunc,knownVars)
            print(printVal.tok.value)
        elif type(expr.value) == GetAVStatement:
            printVal = self.getAVStat(expr.value, knownVars)
            print(printVal.tok.value)
        elif type(expr.value)==RunFuncStatement:
            printVal = self.runFuncStatement(expr.value, knownFunc, knownVars)
            print(printVal.value)
        elif type(expr.value) == RoundStatement:
            printval = self.roundStatement(expr.value, knownVars)
            print(printval.tok.value)
        elif type(expr.value) == RootStatement:
            printval = self.rootStatement(expr.value, knownVars)
            print(printval.tok.value)
        elif type(expr.value) == LogStatement:
            printval = self.logStatement(expr.value, knownVars)
            print(printval.tok.value)
        elif type(expr.value) == PowStatement:
            printval = self.powStatement(expr.value, knownVars)
            print(printval.tok.value)
        elif type(expr.value) == ToIntStatement:
            printval = self.toIntStatement(expr.value, knownVars)
            print(printval.tok.value)
        elif type(expr.value) == ToFloatStatement:
            printval = self.toFloatStatement(expr.value, knownVars)
            print(printval.tok.value)
        elif type(expr.value) == InputStatement:
            printval = self.inputStatement(expr.value, knownVars)
            print(printval.tok.value)
        elif type(expr.value) == ClassStatement:
            printval = self.classStatement(expr.value, knownVars)
            print(printval.tok.value)
        elif type(expr.value) == InstantiateStatement:
            printval = self.instantiateStatement(expr.value, knownVars)
            print(printval.tok.value)

        else:
            if type(expr.value) == NumberNode:
                printVal = self.getVarVal(expr.value.tok, knownVars)
                if printVal.T_TYPE == T_CLASS:
                    print("CLASS OBJ")
                else:
                    #When printing arrays of arrays, printval.value is a lst that contains another Token with type array, so it prints it in that form
                    print(printVal.value)
            else:
                printVal = self.getVarVal(expr.value.tok,knownVars)
                print(printVal)


    def ifStat(self, expr, knownFunc,knownVars):
        compexpr = expr.compexpr
        ifexpr = expr.expression
        old_expr = copy.deepcopy(ifexpr)
        binOpResults = []
        FUNCRES = None
        if self.binop(compexpr, knownFunc, knownVars).tok.T_TYPE==T_TRUE:
            ifexpr = copy.deepcopy(old_expr)
            for lineExpr in ifexpr:
                if type(lineExpr) == BinOP:
                    binOpResults.append(self.binop(lineExpr, knownFunc,knownVars))
                elif type(lineExpr) == VarAssignNode:
                    self.storevar(lineExpr, knownFunc, knownVars)
                elif type(lineExpr) == PrintStatement:
                    self.printStat(lineExpr, knownFunc, knownVars)
                elif type(lineExpr) == IfStatement:
                    FUNCRES = self.ifStat(lineExpr, knownFunc, knownVars)
                elif type(lineExpr) == WhileStatement:
                    FUNCRES = self.whileStat(lineExpr, knownFunc, knownVars)
                elif type(lineExpr) == FuncStatement:
                    self.funcStat(lineExpr, knownFunc)
                elif type(lineExpr) == GetAVStatement:
                    self.getAVStat(lineExpr, knownVars)
                elif type(lineExpr) == SetAVStatement:
                    self.setAVStat(lineExpr, knownVars)
                elif type(lineExpr) == ReturnStatement:
                    return self.returnStat(lineExpr, knownVars)
                elif type(lineExpr) == RunFuncStatement:
                    print(self.runFuncStatement(lineExpr, knownFunc, knownVars))
                elif type(lineExpr) == AppendStatement:
                    self.appendStat(lineExpr, knownVars)
                elif type(lineExpr) == RandomStatement:
                    self.randStatement( )
                elif type(lineExpr) == RandIntStatement:
                    self.randIntStatement(lineExpr, knownVars)
                elif type(lineExpr) == RemoveAVStatement:
                    self.remAVstat(lineExpr, knownVars)
                elif type(lineExpr) == RoundStatement:
                    self.roundStatement(lineExpr, knownVars)
                elif type(lineExpr) == RootStatement:
                    self.rootStatement(lineExpr, knownVars)
                elif type(lineExpr) == LogStatement:
                    self.logStatement(lineExpr, knownVars)
                elif type(lineExpr) == PowStatement:
                    self.powStatement(lineExpr, knownVars)
                elif type(lineExpr) == ToIntStatement:
                    self.toIntStatement(lineExpr, knownVars)
                elif type(lineExpr) == ToFloatStatement:
                    self.toFloatStatement(lineExpr, knownVars)
                elif type(lineExpr) == InputStatement:
                    self.inputStatement(lineExpr, knownVars)
                elif type(lineExpr) == ClassStatement:
                    self.classStatement(lineExpr, knownVars)
                elif type(lineExpr) == InstantiateStatement:
                    self.instantiateStatement(lineExpr, knownVars)
                elif type(lineExpr) == SetCVStatement:
                    self.setcvStatement(lineExpr, knownVars)
                if FUNCRES!=None:
                    return FUNCRES


    def whileStat(self, expr, knownFunc, knownVars):
        compexpr = expr.compexpr
        ifexpr = expr.expression
        old_expr = copy.deepcopy(ifexpr)
        binOpResults = []
        returned = False
        FUNCRES = None

        while self.binop(compexpr, knownFunc,knownVars).tok.T_TYPE == T_TRUE and returned==False:
            for lineExpr in ifexpr:
                if type(lineExpr) == BinOP:
                    binOpResults.append(self.binop(lineExpr, knownFunc,knownVars))
                elif type(lineExpr) == VarAssignNode:
                    self.storevar(lineExpr, knownFunc, knownVars)
                elif type(lineExpr) == PrintStatement:
                    self.printStat(lineExpr, knownFunc, knownVars)
                elif type(lineExpr) == IfStatement:
                    FUNCRES = self.ifStat(lineExpr, knownFunc, knownVars)
                elif type(lineExpr) == WhileStatement:
                    FUNCRES = self.whileStat(lineExpr, knownFunc, knownVars)
                elif type(lineExpr) == FuncStatement:
                    self.funcStat(lineExpr, knownFunc)
                elif type(lineExpr) == GetAVStatement:
                    self.getAVStat(lineExpr, knownVars)
                elif type(lineExpr) == SetAVStatement:
                    self.setAVStat(lineExpr, knownVars)
                elif type(lineExpr) == ReturnStatement:
                    return self.returnStat(lineExpr, knownVars)
                elif type(lineExpr) == RunFuncStatement:
                    print(self.runFuncStatement(lineExpr, knownFunc, knownVars))
                elif type(lineExpr) == AppendStatement:
                    self.appendStat(lineExpr, knownVars)
                elif type(lineExpr) == RandomStatement:
                    self.randStatement( )
                elif type(lineExpr) == RandIntStatement:
                    self.randIntStatement(lineExpr, knownVars)
                elif type(lineExpr) == RemoveAVStatement:
                    self.remAVstat(lineExpr, knownVars)
                elif type(lineExpr) == RoundStatement:
                    self.roundStatement(lineExpr, knownVars)
                elif type(lineExpr) == RootStatement:
                    self.rootStatement(lineExpr, knownVars)
                elif type(lineExpr) == LogStatement:
                    self.logStatement(lineExpr, knownVars)
                elif type(lineExpr) == PowStatement:
                    self.powStatement(lineExpr, knownVars)
                elif type(lineExpr) == ToIntStatement:
                    self.toIntStatement(lineExpr, knownVars)
                elif type(lineExpr) == ToFloatStatement:
                    self.toFloatStatement(lineExpr, knownVars)
                elif type(lineExpr) == InputStatement:
                    self.inputStatement(lineExpr, knownVars)
                elif type(lineExpr) == ClassStatement:
                    self.classStatement(lineExpr, knownVars)
                elif type(lineExpr) == InstantiateStatement:
                    self.instantiateStatement(lineExpr, knownVars)
                elif type(lineExpr) == SetCVStatement:
                    self.setcvStatement(lineExpr, knownVars)
                ifexpr = copy.deepcopy(old_expr)
                if FUNCRES!=None:
                    return FUNCRES


    def elseStat(self, expr, knownVars):
        """elsexpr = expr.expression
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
                self.elseStat(lineExpr, knownVars)"""
        return


    def getAVStat(self, expr,knownVars):
        TOK = {
            int:T_INT,
            float:T_FLOAT,
            str:T_STRING,
            list:T_ARRAY,
            Token:T_ARRAY
        }
        if type(expr.array)==GetAVStatement:
            _array = self.getAVStat(expr.array,knownVars).tok
        else:
            _array = self.getVarVal(expr.array, knownVars)
        location = self.getVarVal(expr.location, knownVars).value
        neededvar = _array.value[location]

        if type(neededvar) == Token:
            return NumberNode(Token(TOK[type(neededvar)],neededvar.value))
        else:
            return NumberNode(Token(TOK[type(neededvar)],neededvar))


    def find_var_by_name(self, name, knownVars):
        for var in knownVars:
            if var[0].value == name.value:
                return knownVars.index(var)


    def setAVStat(self, expr,knownVars):

        TOK = {
            int:T_INT,
            float:T_FLOAT,
            str:T_STRING,
            Token:T_ARRAY
        }
        _array_name = Token(T_IDENTIFIER, expr.array.value)
        _location = self.getVarVal(expr.location, knownVars).value
        _value = self.getVarVal(expr.value, knownVars).value
        index = self.find_var_by_name(_array_name,knownVars)
        if type(knownVars[index][1]) == NumberNode:
            knownVars[index][1].tok.value[_location]=_value
        else:
            knownVars[index][1].value[_location] = _value


    def remAVstat(self, expr,knownVars):
        _array_name = Token(T_IDENTIFIER, expr.array.value)
        _location = self.getVarVal(expr.location, knownVars).value
        index = self.find_var_by_name(_array_name, knownVars)
        if type(knownVars[index][1]) == NumberNode:
            del knownVars[index][1].tok.value[_location]
        else:
            del knownVars[index][1].value[_location]


    def funcStat(self, expr,globalfunc):
        globalfunc.append([expr.funcnametok, expr.arguments, expr.expression])


    def returnStat(self,expr,knownVars):
        expr_tok = expr.value
        ret_value = self.getVarVal(expr_tok,knownVars)
        return ret_value


    def runFuncStatement(self, expr, knownFunc, knownVars):
        TOK = {
            int: T_INT,
            float: T_FLOAT,
            str: T_STRING,
            list: T_ARRAY,
            Token : -1
        }
        nametok = expr.funcnametok
        args = expr.arguments
        FUNC = None
        ARGS = []
        FUNCRES = None
        FUNCKW = []
        for func in knownFunc:
            currf = func[0]
            if currf.value == nametok.value:
                FUNC = func
        for arg in args:
            if type(arg) == NumberNode:
                argtok = arg.tok
                if argtok.T_TYPE in (T_INT, T_STRING, T_FLOAT, T_BOOLEAN):
                    ARGS.append(argtok.value)
                else:
                    ARGS.append(self.getVarVal(argtok,knownVars))
            elif arg.T_TYPE in (T_INT,T_STRING,T_FLOAT,T_BOOLEAN):
                ARGS.append(arg.value)
            else:
                argtok = arg
                ARGS.append(self.getVarVal(argtok, knownVars))

        for arg in FUNC[1]:
            val = ARGS[FUNC[1].index(arg)]
            _TYPE = TOK[type(val)]
            if _TYPE==-1:
                val = self.getVarVal(val,knownVars).value
                _TYPE = TOK[type(val)]
            FUNCKW.append([arg.tok, Token(_TYPE,val)])

        expressions = FUNC[2]
        og_expr = copy.deepcopy(expressions)
        binOpResults = []
        for lineExpr in og_expr:
            if type(lineExpr) == BinOP:
                binOpResults.append(self.binop(lineExpr, knownFunc, FUNCKW))
            elif type(lineExpr) == VarAssignNode:
                self.storevar(lineExpr, knownFunc, FUNCKW)
            elif type(lineExpr) == PrintStatement:
                self.printStat(lineExpr, knownFunc, FUNCKW)
            elif type(lineExpr) == IfStatement:
                FUNCRES = self.ifStat(lineExpr, knownFunc, FUNCKW)
            elif type(lineExpr) == WhileStatement:
                FUNCRES = self.whileStat(lineExpr, knownFunc, FUNCKW)
            elif type(lineExpr) == FuncStatement:
                self.funcStat(lineExpr, FUNCKW)
            elif type(lineExpr) == GetAVStatement:
                self.getAVStat(lineExpr, FUNCKW)
            elif type(lineExpr) == SetAVStatement:
                self.setAVStat(lineExpr, FUNCKW)
            elif type(lineExpr) == ReturnStatement:
                FUNCRES = self.returnStat(lineExpr,FUNCKW)
            elif type(lineExpr) == RunFuncStatement:
                self.runFuncStatement(lineExpr, knownFunc, FUNCKW)
            elif type(lineExpr) == AppendStatement:
                self.appendStat(lineExpr,FUNCKW)
            elif type(lineExpr) == RandomStatement:
                self.randStatement()
            elif type(lineExpr) == RandIntStatement:
                self.randIntStatement(lineExpr, FUNCKW)
            elif type(lineExpr) == RemoveAVStatement:
                self.remAVstat(lineExpr, FUNCKW)
            elif type(lineExpr) == RoundStatement:
                self.roundStatement(lineExpr, FUNCKW)
            elif type(lineExpr) == RootStatement:
                self.rootStatement(lineExpr, FUNCKW)
            elif type(lineExpr) == LogStatement:
                self.logStatement(lineExpr, FUNCKW)
            elif type(lineExpr) == PowStatement:
                self.powStatement(lineExpr, FUNCKW)
            elif type(lineExpr) == ToIntStatement:
                self.toIntStatement(lineExpr, FUNCKW)
            elif type(lineExpr) == ToFloatStatement:
                self.toFloatStatement(lineExpr, FUNCKW)
            elif type(lineExpr) == InputStatement:
                self.inputStatement(lineExpr, FUNCKW)
            elif type(lineExpr) == ClassStatement:
                self.classStatement(lineExpr, FUNCKW)
            elif type(lineExpr) == InstantiateStatement:
                self.instantiateStatement(lineExpr, FUNCKW)
            elif type(lineExpr) == SetCVStatement:
                self.setcvStatement(lineExpr, FUNCKW)
            if FUNCRES!=None:
                break

        return FUNCRES


    def appendStat(self, expr,knownVars):
        _array_name = Token(T_IDENTIFIER, expr.array.value)
        _value = self.getVarVal(expr.value, knownVars).value
        index = self.find_var_by_name(_array_name, knownVars)
        if type(knownVars[index][1]) == NumberNode:
            knownVars[index][1].tok.value.append(_value)
        else:
            knownVars[index][1].value.append(_value)


    def randStatement(self):
        return NumberNode(Token(T_FLOAT, random.random()))


    def randIntStatement(self, expr, knownVars):
        min_val = self.getVarVal(expr.min_val, knownVars)
        max_val = self.getVarVal(expr.max_val, knownVars)
        return NumberNode(Token(T_FLOAT, random.randint(min_val.value, max_val.value)))


    def importStatement(self, expr):
        filename = expr.import_name.value
        Lex2 = Lexer(filename)
        Lex2.RUN( )
        C_Parser2 = Parser(Lex2.tokens)
        C_expressions = C_Parser2.run( )
        return C_expressions


    def initialize(self, filename):
        #new lexer
        Lex = Lexer(filename)
        Lex.RUN( )
        #parser
        C_Parser = Parser(Lex.tokens)
        C_expressions = C_Parser.run()

        #debug mode (shows tokens and parse_result)
        debug_mode = True
        if debug_mode == True:
            print(C_Parser.tokens)
            print(C_expressions)
        return C_expressions


    def roundStatement(self, lineExpr, knownVars):
        num = self.getVarVal(lineExpr.value, knownVars)
        res = round(num.value)
        return NumberNode(Token(T_INT, res))


    def rootStatement(self, expr, knownVars):
        TOK = {
            int: T_INT,
            float: T_FLOAT,
            Token: -1
        }
        num = expr.root_val
        exp = expr.root_exp
        num = self.getVarVal(num, knownVars)
        exp = self.getVarVal(exp, knownVars)
        res = num.value**(1/exp.value)
        return NumberNode(Token(TOK[type(res)],res))


    def logStatement(self, expr, knownVars):
        TOK = {
            int: T_INT,
            float: T_FLOAT,
            Token: -1
        }
        base = expr.log_base
        num = expr.log_val
        num = self.getVarVal(num, knownVars)
        base = self.getVarVal(base, knownVars)
        res = math.log(num.value, base.value)
        return NumberNode(Token(TOK[type(res)],res))


    def powStatement(self, expr, knownVars):
        TOK = {
            int: T_INT,
            float: T_FLOAT,
            Token: -1
        }
        num = expr.pow_base
        exp = expr.pow_exp
        num = self.getVarVal(num, knownVars)
        base = self.getVarVal(exp, knownVars)
        res = num.value**exp.value
        return NumberNode(Token(TOK[type(res)],res))


    def toIntStatement(self, expr, knownVars):
        num = expr.value
        num = self.getVarVal(num, knownVars).value
        try:
            num = int(num)
            return NumberNode(Token(T_INT, num))
        except:
            print("can't convert value to integer")
            return NumberNode(Token(T_ERROR, "ERROR"))


    def toFloatStatement(self, expr, knownVars):
        num = expr.value
        num = self.getVarVal(num, knownVars).value
        try:
            num = float(num)
            return NumberNode(Token(T_FLOAT, num))
        except:
            print("can't convert value to integer")
            return NumberNode(Token(T_ERROR, "ERROR"))


    def tonum(self, value):
        try:
            try:
                return int(value)
            except:
                return float(value)
        except:
            return str(value)


    def inputStatement(self, expr, knownVars):
        TOK = {
            int: T_INT,
            float: T_FLOAT,
            str: T_STRING,
            Token: -1
        }
        n_info = expr.info_value
        res = input(n_info.value)
        res = self.tonum(res)
        return NumberNode(Token(TOK[type(res)], res))


    def type_switch(self, lineExpr, knownFunc, knownVars):
        if type(lineExpr) == BinOP:
            print(self.binop(lineExpr, knownFunc, knownVars))
        elif type(lineExpr) == VarAssignNode:
            self.storevar(lineExpr, knownFunc, knownVars)
        elif type(lineExpr) == PrintStatement:
            self.printStat(lineExpr, knownFunc, knownVars)
        elif type(lineExpr) == IfStatement:
            self.ifStat(lineExpr, knownFunc, knownVars)
        elif type(lineExpr) == WhileStatement:
            self.whileStat(lineExpr, knownFunc, knownVars)
        elif type(lineExpr) == FuncStatement:
            self.funcStat(lineExpr, knownFunc)
        elif type(lineExpr) == GetAVStatement:
            self.getAVStat(lineExpr, knownVars)
        elif type(lineExpr) == SetAVStatement:
            self.setAVStat(lineExpr, knownVars)
        elif type(lineExpr) == ReturnStatement:
            print(self.returnStat(lineExpr, knownVars))
        elif type(lineExpr) == RunFuncStatement:
            print(self.runFuncStatement(lineExpr, knownFunc, knownVars))
        elif type(lineExpr) == AppendStatement:
            self.appendStat(lineExpr, knownVars)
        elif type(lineExpr) == RandomStatement:
            self.randStatement( )
        elif type(lineExpr) == RandIntStatement:
            self.randIntStatement(lineExpr, knownVars)
        elif type(lineExpr) == ImportStatement:
            res = self.importStatement(lineExpr)
            exprind = self.expressions.index(lineExpr)
            i = 1
            for sres in res:
                self.expressions.insert(exprind + i, sres)
                i += 1
        elif type(lineExpr) == RoundStatement:
            self.roundStatement(lineExpr, knownVars)
        elif type(lineExpr) == RootStatement:
            self.rootStatement(lineExpr, knownVars)
        elif type(lineExpr) == LogStatement:
            self.logStatement(lineExpr, knownVars)
        elif type(lineExpr) == PowStatement:
            self.powStatement(lineExpr, knownVars)
        elif type(lineExpr) == ToIntStatement:
            self.toIntStatement(lineExpr, knownVars)
        elif type(lineExpr) == ToFloatStatement:
            self.toFloatStatement(lineExpr, knownVars)
        elif type(lineExpr) == InputStatement:
            self.inputStatement(lineExpr, knownVars)
        elif type(lineExpr) == ClassStatement:
            self.classStatement(lineExpr, knownVars)
        elif type(lineExpr) == InstantiateStatement:
            self.instantiateStatement(lineExpr, knownVars)
        elif type(lineExpr) == SetCVStatement:
            self.setcvStatement(lineExpr, knownVars)


    def classStatement(self, expr, knownVars):
        class_type_name = expr.class_name_token
        expressions = expr.expression
        class_funcs = []
        class_vars = []
        for exprs in expressions:
            self.type_switch(exprs,class_funcs, class_vars)
        knownVars.append([Token(T_IDENTIFIER, class_type_name.value), Token(T_CLASS, [class_vars, class_funcs])])


    def instantiateStatement(self, expr, knownVars):
        class_name = expr.class_name
        class_found = copy.deepcopy(self.getVarVal(class_name,knownVars))
        if class_found.T_TYPE == T_CLASS:
            return NumberNode(Token(T_CLASS, class_found.value))


    def setcvStatement(self, lineExpr, knownVars):
        class_name = lineExpr.class_name
        class_value = lineExpr.class_value
        class_new_value = lineExpr.class_new_value

        classOBJ = copy.deepcopy(self.getVarVal(class_name, knownVars))
        classVars = classOBJ.value[0]
        classFunc = classOBJ.value[1]
        class_new_value = self.getVarVal(class_new_value, knownVars)
        idx = None
        for var in classVars:
            if var[0].matches(class_value.T_TYPE, class_value.value):
                idx = classVars.index(var)

        classVars = self.getVarVal(class_name, knownVars).value[0]
        classVars[idx][1]=class_new_value


    def RUN(self):
        knownVars = []
        knownFunc = []
        for lineExpr in self.expressions:
            self.type_switch(lineExpr, knownFunc, knownVars)



"""EXAMPLE OF A GLOBALVAR FORMAT
_Interpreter.globalvars.append([Token(T_IDENTIFIER,"TESTVAR"),Token(T_INT,int(1))])
"""
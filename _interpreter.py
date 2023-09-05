from _parser import *
import _lexerOLD
class Interpreter:
    def __init__(self, filename):
        self.filename = filename
        self.expressions = self.initialize(filename)

    def getVarVal(self, _token, knownVars):
        try:
            if _token.T_TYPE in (T_INT, T_FLOAT, T_STRING):
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
        if type(right) == BinOP:
            right = self.binop(right, knownFunc, knownVars)
        if type(left) == GetAVStatement:
            left = self.getAVStat(left, knownVars)
        if type(right) == GetAVStatement:
            right = self.getAVStat(right, knownVars)
        if type(left) == RunFuncStatement:
            left = NumberNode(self.runFuncStatement(left, knownFunc, knownVars))
        if type(right) == RunFuncStatement:
            right = NumberNode(self.runFuncStatement(right, knownFunc, knownVars))

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
        else:
            if type(expr.value) == NumberNode:
                printVal = self.getVarVal(expr.value.tok, knownVars)
                #When printing arrays of arrays, printval.value is a lst that contains another Token with type array, so it prints it in that form
                print(printVal.value)
            else:
                printVal = self.getVarVal(expr.value.tok,knownVars)
                print(printVal)

    def ifStat(self, expr, knownFunc,knownVars):
        compexpr = expr.compexpr
        ifexpr = expr.expression
        binOpResults = []
        FUNCRES = None
        if self.binop(compexpr, knownFunc, knownVars).tok.T_TYPE==T_TRUE:
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

                if FUNCRES!=None:
                    return FUNCRES

    def whileStat(self, expr, knownFunc, knownVars):
        compexpr = expr.compexpr
        ifexpr = expr.expression
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

                if FUNCRES!=None:
                    return FUNCRES

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
        knownVars[index][1].tok.value[_location]=_value

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
        binOpResults = []
        for lineExpr in expressions:
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
            if FUNCRES!=None:
                break

        return FUNCRES

    def appendStat(self, expr,knownVars):
        TOK = {
            int: T_INT,
            float: T_FLOAT,
            str: T_STRING,
            Token: T_ARRAY
        }
        _array_name = Token(T_IDENTIFIER, expr.array.value)
        _value = self.getVarVal(expr.value, knownVars).value
        index = self.find_var_by_name(_array_name, knownVars)
        knownVars[index][1].tok.value.append(_value)

    def initialize(self, filename):
        #old lexer
        C_Lexer = _lexerOLD.Lexer()
        C_Lexer.RUN_lexer(filename)
        #new lexer
        Lex = Lexer(filename)
        Lex.RUN( )
        #parser
        C_Parser = Parser(Lex.tokens)
        C_expressions = C_Parser.run()

        #debug mode (shows tokens and parse_result)
        debug_mode = True
        if debug_mode == True:
            print(C_Lexer.tokens)
            print(C_Parser.tokens)
            print(C_expressions)
        return C_expressions

    def RUN(self):
        knownVars = []
        knownFunc = []
        for lineExpr in self.expressions:
            if type(lineExpr) == BinOP:
                print(self.binop(lineExpr, knownFunc, knownVars))
            elif type(lineExpr) == VarAssignNode:
                self.storevar(lineExpr, knownFunc,knownVars)
            elif type(lineExpr) == PrintStatement:
                self.printStat(lineExpr,knownFunc,knownVars)
            elif type(lineExpr) == IfStatement:
                self.ifStat(lineExpr, knownFunc,knownVars)
            elif type(lineExpr) == WhileStatement:
                self.whileStat(lineExpr, knownFunc,knownVars)
            elif type(lineExpr) == FuncStatement:
                self.funcStat(lineExpr, knownFunc)
            elif type(lineExpr) == GetAVStatement:
                self.getAVStat(lineExpr,knownVars)
            elif type(lineExpr) == SetAVStatement:
                self.setAVStat(lineExpr,knownVars)
            elif type(lineExpr) == ReturnStatement:
                print(self.returnStat(lineExpr,knownVars))
            elif type(lineExpr) == RunFuncStatement:
                print(self.runFuncStatement(lineExpr, knownFunc, knownVars))
            elif type(lineExpr) == AppendStatement:
                self.appendStat(lineExpr,knownVars)

"""EXAMPLE OF A GLOBALVAR FORMAT
_Interpreter.globalvars.append([Token(T_IDENTIFIER,"TESTVAR"),Token(T_INT,int(1))])
"""
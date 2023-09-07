from _parser import *

global_variables = []

class Var:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
        self.value, self.type = self.run()

    def run(self):
        curres = None
        if type(self.expression)==BinOP:
            left = self.expression.left
            op = self.expression.op
            right = self.expression.right
            if left.tok.T_TYPE and right.tok.T_TYPE in (T_INT, T_FLOAT):
                if op.T_TYPE == T_PLUS:
                    curres =  left.tok.value + right.tok.value
                elif op.T_TYPE == T_MINUS:
                    curres =  left.tok.value - right.tok.value
                elif op.T_TYPE == T_MUL:
                    curres =  left.tok.value * right.tok.value
                elif op.T_TYPE == T_DIV:
                    curres =  left.tok.value / right.tok.value
            elif left.tok.T_TYPE and right.tok.T_TYPE in (T_STRING):
                if op.T_TYPE == T_PLUS: curres =  left.tok.value + right.tok.value
            if type(curres)==int:
                return curres, T_INT
            elif type(curres)==float:
                return curres, T_FLOAT
            else:
                return curres, T_STRING
        elif type(self.expression)==NumberNode:
            return self.expression.tok.value, self.expression.tok.T_TYPE

class If:
    def __init__(self, condition, expressions, above_vars, _repr):
        self.above_vars = above_vars
        self.condition = condition
        self.expressions = expressions
        self._repr = _repr
        self.current_expr = None
        self.expr_id = -1
        self.advance()
        self.localvariables = self.run()

    def advance(self):
        self.expr_id += 1
        if self.expr_id < len(self.expressions):
            self.current_expr = self.expressions[self.expr_id]

    def cycle_expressions(self):
        localvars = []
        while self.expr_id < len(self.expressions):
            if type(self.current_expr) == VarAssignNode:
                currvar = Var(self.current_expr.var_name, self.current_expr.expr_value)
                localvars.append(currvar)
                self.advance( )
            elif type(self.current_expr) == IfStatement:
                tot_var = localvars
                for lv in self.above_vars:
                    tot_var.append(lv)
                currif = If(self.current_expr.compexpr, self.current_expr.expression, tot_var, True)
                self.advance( )
            else:
                self.advance( )

        return localvars


    def run(self):
        localvars = []
        if type(self.condition)==BinOP:
            if self.condition.op.T_TYPE == T_GRT:
                if self.condition.left.tok.value>self.condition.right.tok.value:
                    localvars = self.cycle_expressions( )
            elif self.condition.op.T_TYPE == T_LST:
                if self.condition.left.tok.value<self.condition.right.tok.value:
                    localvars = self.cycle_expressions()
            elif self.condition.op.T_TYPE == T_GOE:
                if self.condition.left.tok.value>=self.condition.right.tok.value:
                    localvars = self.cycle_expressions( )
            elif self.condition.op.T_TYPE == T_LOE:
                if self.condition.left.tok.value<=self.condition.right.tok.value:
                    localvars = self.cycle_expressions()

        if self._repr:
            print("lV:")
            for lvar in localvars:
                print(f"{lvar.name.value}, {lvar.type}:{lvar.value}")
            print()
        return localvars


class Interpreter:
    def __init__(self, filename):
        self.filename = filename
        self.parse_result = self.initialize()
        self.current_expr = None
        self.expr_id = -1
        self.advance()

    def get_var(self, var, arr_search):
        Found = False
        for Svar in arr_search:
            if Svar.name.value == var.tok.value:
                print(Svar)
                return NumberNode(Token(var.tok.T_TYPE ,Svar.value))
        if Found!=True: print("ERROR: No such variable")
        return

    def advance(self):
        self.expr_id += 1
        if self.expr_id < len(self.parse_result):
            self.current_expr = self.parse_result[self.expr_id]

    def binrescalc(self, left, op, right):
        if op.T_TYPE == T_PLUS:
            curres = left.tok.value + right.tok.value
        elif op.T_TYPE == T_MINUS:
            curres = left.tok.value - right.tok.value
        elif op.T_TYPE == T_MUL:
            curres = left.tok.value * right.tok.value
        elif op.T_TYPE == T_DIV:
            curres = left.tok.value / right.tok.value
        return curres

    def main_bin_op_calc(self, binop):
        left = binop.left
        op = binop.op
        right = binop.right
        if left.tok.T_TYPE in (T_INT, T_FLOAT) and right.tok.T_TYPE in (T_INT, T_FLOAT):
            curres = self.binrescalc(left, op, right)

        elif left.tok.T_TYPE in (T_IDENTIFIER):
            L_V_value = self.get_var(left, global_variables)
            print(L_V_value)
            if right.tok.T_TYPE in (T_IDENTIFIER):
                R_V_value = self.get_var(right, global_variables)
                curres = self.binrescalc(L_V_value, op, R_V_value)
            else:
                curres = self.binrescalc(L_V_value, op, right)

        elif right.tok.T_TYPE in (T_IDENTIFIER):
            R_V_value = self.get_var(right, global_variables)
            if left.tok.T_TYPE in (T_IDENTIFIER):
                L_V_value = self.get_var(left, global_variables)
                curres = self.binrescalc(L_V_value, op, R_V_value)
            else:
                curres = self.binrescalc(left, op, R_V_value)

        elif left.tok.T_TYPE in (T_STRING) and right.tok.T_TYPE in (T_STRING):
            if op.T_TYPE == T_PLUS: curres = left.tok.value + right.tok.value

        elif type(left) == BinOP:
            L_N_value = self.main_bin_op_calc(left)

        return curres

    def run(self):
        curres = None
        while self.expr_id < len(self.parse_result):
            if type(self.current_expr)==BinOP:
                left = self.current_expr.left
                op = self.current_expr.op
                right = self.current_expr.right
                if type(left) == BinOP:
                    L_N_value = self.main_bin_op_calc(left)
                    L_N_Type = type(L_N_value)
                    if L_N_Type==int:
                        L_N_NumNode = NumberNode(Token(T_INT,L_N_value))
                        curres = self.binrescalc(L_N_NumNode,op,right)
                    elif L_N_Type==float:
                        L_N_NumNode = NumberNode(Token(T_FLOAT,L_N_value))
                        curres = self.binrescalc(L_N_NumNode, op, right)
                    elif L_N_Type==str:
                        L_N_NumNode = NumberNode(Token(T_STRING,L_N_value))
                        curres = self.binrescalc(L_N_NumNode, op, right)

                elif left.tok.T_TYPE in (T_INT, T_FLOAT) and right.tok.T_TYPE in (T_INT, T_FLOAT):
                    curres = self.binrescalc(left,op,right)

                elif left.tok.T_TYPE in (T_IDENTIFIER):
                    L_V_value = self.get_var(left, global_variables)
                    print(L_V_value)
                    if right.tok.T_TYPE in (T_IDENTIFIER):
                        R_V_value = self.get_var(right, global_variables)
                        curres = self.binrescalc(L_V_value, op, R_V_value)
                    else:
                        curres = self.binrescalc(L_V_value, op, right)

                elif right.tok.T_TYPE in (T_IDENTIFIER):
                    R_V_value = self.get_var(right, global_variables)
                    if left.tok.T_TYPE in (T_IDENTIFIER):
                        L_V_value = self.get_var(left, global_variables)
                        curres = self.binrescalc(L_V_value, op, R_V_value)
                    else:
                        curres = self.binrescalc(left, op, R_V_value)

                elif left.tok.T_TYPE in (T_STRING) and right.tok.T_TYPE in (T_STRING):
                    if op.T_TYPE == T_PLUS: curres = left.tok.value + right.tok.value




                return curres
            elif type(self.current_expr)==VarAssignNode:
                currvar = Var(self.current_expr.var_name, self.current_expr.expr_value)
                global_variables.append(currvar)
            elif type(self.current_expr)==IfStatement:
                currif = If(self.current_expr.compexpr, self.current_expr.expression,global_variables, True)
            self.advance()

    def initialize(self):
        Loaded_lexer = Lexer( )
        Loaded_lexer.RUN_lexer(self.filename)
        Ltokens = Loaded_lexer.tokens
        Cparser = Parser(Ltokens)
        parser_result = Cparser.run( )
        print(parser_result)
        return parser_result


_Interpreter = Interpreter("test.flux")
print(f"interpreter result: {_Interpreter.run()}\n")
print("global variables:")
for var in global_variables:
    print(f"id: {global_variables.index(var)}, {var.name.value}: {var.value} (type:{var.type})")
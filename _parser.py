import random
from _lexer import *

class NumberNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f"{self.tok}"

class BinOP:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"({self.left},{self.op},{self.right})"

class VarAssignNode:
    def __init__(self, var_name, expr_value):
        self.var_name = var_name
        self.expr_value = expr_value

    def __repr__(self):
        return f"(assign: {self.var_name}, EQUALS, {self.expr_value})"

class IfStatement:
    def __init__(self, compexpr, expression):
        self.compexpr = compexpr
        self.expression = expression

    def __repr__(self):
        return f"(if {self.compexpr}: {self.expression})"

class ElseStatement:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"(else: {self.expression})"

class WhileStatement:
    def __init__(self, compexpr, expression):
        self.compexpr = compexpr
        self.expression = expression

    def __repr__(self):
        return f"(while {self.compexpr}: {self.expression})"

class PrintStatement:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"(print: {self.value})"

class FuncStatement:
    def __init__(self, funcnametok, arguments, expression):
        self.funcnametok = funcnametok
        self.arguments = arguments
        self.expression = expression

    def __repr__(self):
        return f"(func {self.funcnametok}({self.arguments}): {self.expression})"

class RunFuncStatement:
    def __init__(self, funcnametok, arguments):
        self.funcnametok = funcnametok
        self.arguments = arguments

    def __repr__(self):
        return f"(run func: {self.funcnametok}({self.arguments}))"

class GetAVStatement:
    def __init__(self, array, location):
        self.array = array
        self.location = location

    def __repr__(self):
        return f"(getAV: {self.array}[{self.location}])"

class SetAVStatement:
    def __init__(self, array, location, value):
        self.array = array
        self.location = location
        self.value = value
    def __repr__(self):
        return f"(setAV: {self.array}[{self.location}] -> {self.value})"

class ReturnStatement:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"(returnTOK: {self.value})"

class AppendStatement:
    def __init__(self, array, value):
        self.array = array
        self.value = value

    def __repr__(self):
        return f"(append: {self.array} -> {self.value})"

class RandIntStatement:
    def __init__(self, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val

    def __repr__(self):
        return f"(randint: ({self.min_val} - {self.max_val}))"

class RandomStatement:
    def __init__(self):
        self.value = None

    def __repr__(self):
        return f"(random: ({self.value}))"

class RemoveAVStatement:
    def __init__(self, array, location):
        self.array = array
        self.location = location

    def __repr__(self):
        return f"(removeAR: {self.array}[{self.location}])"

class ImportStatement:
    def __init__(self, import_name):
        self.import_name = import_name

    def __repr__(self):
        return f"(import file: {self.import_name})"

class RoundStatement:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"(round value: {self.value})"

class RootStatement:
    def __init__(self, root_exp, root_val):
        self.root_exp = root_exp
        self.root_val = root_val

    def __repr__(self):
        return f"(root: {self.root_val}^1/{self.root_exp})"

class LogStatement:
    def __init__(self, log_base, log_val):
        self.log_base = log_base
        self.log_val = log_val

    def __repr__(self):
        return f"(log: base {self.log_base} of {self.log_val})"

class PowStatement:
    def __init__(self, pow_base, pow_exp):
        self.pow_base = pow_base
        self.pow_exp = pow_exp

    def __repr__(self):
        return f"(power: {self.pow_base}^{self.pow_exp})"

class ToIntStatement:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"(to int value: {self.value})"

class ToFloatStatement:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"(to float value: {self.value})"

class InputStatement:
    def __init__(self, info_value):
        self.info_value = info_value

    def __repr__(self):
        return f"(input_var -> {self.info_value.value})"

class ClassStatement:
    def __init__(self, class_name_token, expression, variables=None, functions=None):
        self.class_name_token = class_name_token
        self.expression = expression
        self.variables = variables
        self.functions = functions

    def __repr__(self):
        return f"(class {self.class_name_token.value}: {self.expression})"

class InstantiateStatement:
    def __init__(self, class_name):
        self.class_name = class_name

    def __repr__(self):
        return f"(Instantiate -> {self.class_name.value})"

class SetCVStatement:
    def __init__(self, class_name, class_value, class_new_value):
        self.class_name = class_name
        self.class_value = class_value
        self.class_new_value = class_new_value

    def __repr__(self):
        return f"(Set class: -> {self.class_name.value}.{self.class_value.value} -> {self.class_new_value.value})"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.currtok = None
        self.tokidx = -1
        self.advance( )
        self.recentlyEndedIf = False

    def advance(self):
        self.tokidx += 1
        if self.tokidx < len(self.tokens):
            self.currtok = self.tokens[self.tokidx]

    def factor(self):
        tok = self.currtok
        try:
            if tok.T_TYPE in (T_INT, T_FLOAT, T_IDENTIFIER, T_STRING, T_ARRAY):
                self.advance( )
                return NumberNode(tok)
        except:
            return NumberNode(tok)

    def term(self):
        left = self.factor( )
        while self.currtok.T_TYPE in (T_MUL, T_DIV):
            op_token = self.currtok
            self.advance( )
            right = self.factor( )
            left = BinOP(left, op_token, right)

        return left

    def leftest_expression_modifier(self, expr, replace_expr):
        def go_left(curr_expr):
            if curr_expr.left != None: return curr_expr.left

        left_depth = 0
        parts = []
        curr_expr = expr
        ending_expr = BinOP(None, None, None)
        while curr_expr.left != None:
            left_depth += 1
            curr_expr = go_left(curr_expr)

        i = 0
        while i < left_depth:
            for n in range(i):
                curr_expr = go_left(expr)
            op = curr_expr.op
            right = curr_expr.right
            if ending_expr.left == None:
                ending_expr = BinOP(replace_expr, op, right)
            else:
                ending_expr = BinOP(ending_expr, op, right)
            i += 1
        if ending_expr.left == None:
            return BinOP(replace_expr, expr.op, expr.right)
        ending_expr = BinOP(ending_expr, expr.op, expr.right)
        return ending_expr

    def expr(self):
        # RUN FUNCTION, RUN CLASS
        if self.currtok.T_TYPE==T_IDENTIFIER:
            if self.tokidx+1<len(self.tokens) and self.tokens[self.tokidx+1].T_TYPE==T_LPAR:
                func_name = self.currtok
                self.advance()
                self.advance()
                arguments = []
                while self.currtok.T_TYPE != T_RPAR:
                    arguments.append(self.expr( ))
                if self.currtok.T_TYPE!=T_RPAR:
                    print("Missing ')' after function call")
                    return Token(T_ERROR)
                self.advance()
                return RunFuncStatement(func_name, arguments)
        # VARIABLE ASSIGNMENT
        if self.currtok.matches(T_KEYWORD, "store"):
            self.advance( )
            if self.currtok.T_TYPE != T_IDENTIFIER:
                print("Expected identifier after store")
                return Token(T_ERROR)
            var_name = self.currtok
            self.advance( )
            if self.currtok.T_TYPE != T_EQUAL:
                print("Expected equals after variable declaration")
                return Token(T_ERROR)
            self.advance( )
            #checks if expr is valid. if not, tryes to complete it with next info
            expr = self.expr( )
            oldexpr = expr
            if type(expr) == GetAVStatement:
                expr = self.expr( )
                if expr != None:
                    expr = self.leftest_expression_modifier(expr, oldexpr)
                else:
                    expr = oldexpr

                while self.currtok.T_TYPE in (T_PLUS, T_MINUS, T_MUL, T_DIV, T_LST, T_GRT, T_LOE, T_GOE, T_EQUAL, T_NOTEQUAL, T_DOLLAR):
                    expr = self.expr( )
            elif self.currtok.T_TYPE in (T_PLUS, T_MINUS, T_MUL, T_DIV, T_LST, T_GRT, T_LOE, T_GOE, T_EQUAL, T_NOTEQUAL, T_DOLLAR):
                expr = self.expr()
                if expr!=None:
                    expr = self.leftest_expression_modifier(expr, oldexpr)
                else:
                    expr = oldexpr
                while self.currtok.T_TYPE in (T_PLUS, T_MINUS, T_MUL, T_DIV, T_LST, T_GRT, T_LOE, T_GOE, T_EQUAL, T_NOTEQUAL, T_DOLLAR):
                    expr = self.expr( )
            self.advance( )
            if self.currtok.T_TYPE == T_NEWLINE or self.currtok.T_TYPE == T_RPAR:
                self.recentlyEndedIf = False
                return VarAssignNode(var_name, expr)
            else:
                print("missing ';'")
                return Token(T_ERROR)
        # IF STATEMENT
        if self.currtok.matches(T_KEYWORD, "if"):
            self.advance( )
            if self.currtok.T_TYPE != T_LPAR:
                print("Required '(' after if statement")
                return Token(T_ERROR)
            self.advance( )
            compare_expression = self.expr( )
            if self.currtok.T_TYPE != T_RPAR:
                print("Required ')' after if statement")
                return Token(T_ERROR)
            self.advance( )
            if self.currtok.T_TYPE != T_LGPAR:
                print("Required '{' at if opening")
                return Token(T_ERROR)
            self.advance( )
            # skip NEWLINE
            if self.currtok.T_TYPE == T_NEWLINE:
                self.advance( )
            expressions = []
            while self.currtok.T_TYPE != T_RGPAR:
                expressions.append(self.expr( ))
                self.advance( )
            self.advance( )
            self.recentlyEndedIf = True
            return IfStatement(compare_expression, expressions)
        # ELSE STATEMENT
        if self.currtok.matches(T_KEYWORD, "else"):
            if self.recentlyEndedIf:
                self.advance( )
                if self.currtok.T_TYPE != T_LGPAR:
                    print("Required '{' after else statement")
                    return Token(T_ERROR)
                self.advance( )
                # skip NEWLINE
                if self.currtok.T_TYPE == T_NEWLINE:
                    self.advance( )
                expressions = []
                while self.currtok.T_TYPE != T_RGPAR:
                    expressions.append(self.expr( ))
                    self.advance( )
                self.advance( )
                self.recentlyEndedIf = False
                return ElseStatement(expressions)
            else:
                print("expected if before else (try to move the else statement closer to the desired if")
                return Token(T_ERROR)
        # WHILE STATEMENT
        if self.currtok.matches(T_KEYWORD, "while"):
            self.advance( )
            if self.currtok.T_TYPE != T_LPAR:
                print("Required '(' after if statement")
                return Token(T_ERROR)
            self.advance( )
            compare_expression = self.expr( )
            if self.currtok.T_TYPE != T_RPAR:
                print("Required ')' after while statement")
                return Token(T_ERROR)
            self.advance( )
            if self.currtok.T_TYPE != T_LGPAR:
                print("Required '{' at if opening")
                return Token(T_ERROR)
            self.advance( )
            # skip NEWLINE
            if self.currtok.T_TYPE == T_NEWLINE:
                self.advance( )
            expressions = []
            while self.currtok.T_TYPE != T_RGPAR:
                expressions.append(self.expr( ))
                self.advance( )
            self.advance( )
            return WhileStatement(compare_expression, expressions)
        # PRINT STATEMENT
        if self.currtok.matches(T_KEYWORD, "print"):
            self.advance( )
            if self.currtok.T_TYPE != T_LPAR:
                print("Required '(' after print statement")
                return Token(T_ERROR)
            self.advance( )
            print_value = self.expr( )
            if self.currtok.T_TYPE != T_RPAR:
                print("Required ')' after print statement")
                return Token(T_ERROR)
            self.advance( )
            return PrintStatement(print_value)
        # getAV STATEMENT
        if self.currtok.matches(T_KEYWORD, "getAV"):
            self.advance( )
            if self.currtok.T_TYPE != T_LPAR:
                print("Required '(' after getAV statement")
                return Token(T_ERROR)
            self.advance( )
            arr_name = self.currtok
            """changed"""
            if arr_name.value == "getAV":
                arr_name = self.expr()
            else:
                self.advance( )
            var_location = self.currtok
            self.advance( )
            if self.currtok.T_TYPE != T_RPAR:
                print("Required ')' after getAV statement")
                return Token(T_ERROR)
            self.advance( )
            return GetAVStatement(arr_name, var_location)
        # SETAV STATEMENT
        if self.currtok.matches(T_KEYWORD, "setAV"):
            self.advance( )
            if self.currtok.T_TYPE != T_LPAR:
                print("Required '(' after setAV statement")
                return Token(T_ERROR)
            self.advance( )
            arr_name = self.currtok
            self.advance( )
            var_location = self.currtok
            self.advance( )
            s_a_value = self.currtok
            self.advance()
            if self.currtok.T_TYPE != T_RPAR:
                print("Required ')' after setAV statement")
                return Token(T_ERROR)
            self.advance( )
            return SetAVStatement(arr_name, var_location, s_a_value)
        # FUNCTION STATEMENT
        if self.currtok.matches(T_KEYWORD, "func"):
            self.advance( )
            if self.currtok.T_TYPE != T_IDENTIFIER:
                print("Required name of function")
                return Token(T_ERROR)
            func_name_token = self.currtok
            self.advance( )
            if self.currtok.T_TYPE != T_LPAR:
                print("Required '(' after function statement")
                return Token(T_ERROR)
            self.advance( )
            arguments = []
            while self.currtok.T_TYPE != T_RPAR:
                arguments.append(self.expr( ))
            self.advance( )
            if self.currtok.T_TYPE != T_LGPAR:
                print("Required '{' at function opening")
                return Token(T_ERROR)
            self.advance( )
            # skip NEWLINE
            if self.currtok.T_TYPE == T_NEWLINE:
                self.advance( )
            expressions = []
            while self.currtok.T_TYPE != T_RGPAR:
                expressions.append(self.expr( ))
                self.advance( )
            self.advance( )
            self.recentlyEndedIf = False

            return FuncStatement(func_name_token, arguments, expressions)
        # RETURN STATEMENT
        if self.currtok.matches(T_KEYWORD, "return"):
            self.advance()
            return_val = self.currtok
            self.advance()
            if self.currtok.matches(T_KEYWORD,";"):
                return ReturnStatement(return_val)
        #APPEND STATEMENT
        if self.currtok.matches(T_KEYWORD, "append"):
            self.advance( )
            if self.currtok.T_TYPE != T_LPAR:
                print("Required '(' after append statement")
                return Token(T_ERROR)
            self.advance( )
            arr_name = self.currtok
            self.advance( )
            s_a_value = self.currtok
            self.advance()
            if self.currtok.T_TYPE != T_RPAR:
                print("Required ')' after setAV statement")
                return Token(T_ERROR)
            self.advance( )
            return AppendStatement(arr_name, s_a_value)
        #RANDOM FLOAT 0-1
        if self.currtok.matches(T_KEYWORD, "random"):
            self.advance( )
            if self.currtok.T_TYPE != T_LPAR:
                print("Required '(' after random statement")
                return Token(T_ERROR)
            self.advance( )
            if self.currtok.T_TYPE != T_RPAR:
                print("Required ')' after getAV statement")
                return Token(T_ERROR)
            self.advance( )
            return RandomStatement()
            """
            tok = Token(T_FLOAT, random.random())
            return NumberNode(tok)
            """
        #RANDOM INT X - Y
        if self.currtok.matches(T_KEYWORD, "randint"):
            self.advance( )
            if self.currtok.T_TYPE != T_LPAR:
                print("Required '(' after random statement")
                return Token(T_ERROR)
            self.advance( )
            min_val = self.currtok
            self.advance( )
            max_val = self.currtok
            self.advance( )
            if self.currtok.T_TYPE != T_RPAR:
                print("Required ')' after setAV statement")
                return Token(T_ERROR)
            self.advance( )
            return RandIntStatement(min_val, max_val)
            """
            tok = Token(T_INT, random.randint(min_val.value, max_val.value))
            return NumberNode(tok)
            """
        # REMOVE STATEMENT
        if self.currtok.matches(T_KEYWORD, "remAV"):
            self.advance( )
            if self.currtok.T_TYPE != T_LPAR:
                print("Required '(' after remAV statement")
                return Token(T_ERROR)
            self.advance( )
            arr_name = self.currtok
            if arr_name.value == "getAV":
                arr_name = self.expr()
            else:
                self.advance( )
            var_location = self.currtok
            self.advance( )
            if self.currtok.T_TYPE != T_RPAR:
                print("Required ')' after remAV statement")
                return Token(T_ERROR)
            self.advance( )
            return RemoveAVStatement(arr_name, var_location)
        # IMPORT STATEMENT
        if self.currtok.matches(T_KEYWORD, "import"):
            self.advance()
            import_name= self.currtok
            self.advance()
            if self.currtok.matches(T_KEYWORD,";"):
                return ImportStatement(import_name)
        # ROUND STATEMENT
        if self.currtok.matches(T_KEYWORD, "round"):
            self.advance( )
            if self.currtok.T_TYPE != T_LPAR:
                print("Required '(' after round statement")
                return Token(T_ERROR)
            self.advance( )
            round_val = self.currtok
            """changed"""
            if round_val.value == "getAV":
                round_val = self.expr()
            else:
                self.advance( )
            if self.currtok.T_TYPE != T_RPAR:
                print("Required ')' after round statement")
                return Token(T_ERROR)
            self.advance( )
            return RoundStatement(round_val)
        # ROOT STATEMENT
        if self.currtok.matches(T_KEYWORD, "Mroot"):
            self.advance( )
            if self.currtok.T_TYPE != T_LPAR:
                print("Required '(' after root statement")
                return Token(T_ERROR)
            self.advance( )
            root_exp = self.currtok
            if root_exp.value == "getAV":
                root_exp = self.expr()
            else:
                self.advance( )
            root_val = self.currtok
            if root_val.value == "getAV":
                root_val = self.expr( )
            else:
                self.advance( )
            if self.currtok.T_TYPE != T_RPAR:
                print("Required ')' after root statement")
                return Token(T_ERROR)
            self.advance( )
            return RootStatement(root_exp, root_val)
        # LOG STATEMENT
        if self.currtok.matches(T_KEYWORD, "Mlog"):
            self.advance( )
            if self.currtok.T_TYPE != T_LPAR:
                print("Required '(' after log statement")
                return Token(T_ERROR)
            self.advance( )
            log_base = self.currtok
            """changed"""
            if log_base.value == "getAV":
                log_base = self.expr( )
            else:
                self.advance( )
            log_val = self.currtok
            if log_val.value == "getAV":
                log_val = self.expr( )
            else:
                self.advance( )
            if self.currtok.T_TYPE != T_RPAR:
                print("Required ')' after log statement")
                return Token(T_ERROR)
            self.advance( )
            return LogStatement(log_base, log_val)
        # POWER STATEMENT
        if self.currtok.matches(T_KEYWORD, "Mpow"):
            self.advance( )
            if self.currtok.T_TYPE != T_LPAR:
                print("Required '(' after pow statement")
                return Token(T_ERROR)
            self.advance( )
            pow_base = self.currtok
            """changed"""
            if pow_base.value == "getAV":
                pow_base = self.expr( )
            else:
                self.advance( )
            pow_exp = self.currtok
            if pow_exp.value == "getAV":
                pow_exp = self.expr( )
            else:
                self.advance( )
            if self.currtok.T_TYPE != T_RPAR:
                print("Required ')' after pow statement")
                return Token(T_ERROR)
            self.advance( )
            return PowStatement(pow_base, pow_exp)
        # TOINT STATEMENT
        if self.currtok.matches(T_KEYWORD, "int"):
            self.advance( )
            if self.currtok.T_TYPE != T_LPAR:
                print("Required '(' after int statement")
                return Token(T_ERROR)
            self.advance( )
            val = self.currtok
            """changed"""
            if val.value == "getAV":
                val = self.expr()
            else:
                self.advance( )
            if self.currtok.T_TYPE != T_RPAR:
                print("Required ')' after int statement")
                return Token(T_ERROR)
            self.advance( )
            return ToIntStatement(val)
        # TOFLOAT STATEMENT
        if self.currtok.matches(T_KEYWORD, "float"):
            self.advance( )
            if self.currtok.T_TYPE != T_LPAR:
                print("Required '(' after float statement")
                return Token(T_ERROR)
            self.advance( )
            val = self.currtok
            """changed"""
            if val.value == "getAV":
                val = self.expr( )
            else:
                self.advance( )
            if self.currtok.T_TYPE != T_RPAR:
                print("Required ')' after int statement")
                return Token(T_ERROR)
            self.advance( )
            return ToFloatStatement(val)
        # INPUT STATEMENT
        if self.currtok.matches(T_KEYWORD, "input"):
            self.advance( )
            if self.currtok.T_TYPE != T_LPAR:
                print("Required '(' after input statement")
                return Token(T_ERROR)
            self.advance( )
            input_info = self.currtok
            """changed"""
            if input_info.value == "getAV":
                input_info = self.expr( )
            else:
                self.advance( )
            if self.currtok.T_TYPE != T_RPAR:
                print("Required ')' after input statement")
                return Token(T_ERROR)
            self.advance( )
            return InputStatement(input_info)
        # CLASS STATEMENT
        if self.currtok.matches(T_KEYWORD, "class"):
            self.advance( )
            if self.currtok.T_TYPE != T_IDENTIFIER:
                print("Required class name")
                return Token(T_ERROR)
            class_name_token = self.currtok
            self.advance( )
            if self.currtok.T_TYPE != T_LGPAR:
                print("Required '{' at function opening")
                return Token(T_ERROR)
            self.advance( )
            # skip NEWLINE
            if self.currtok.T_TYPE == T_NEWLINE:
                self.advance( )
            expressions = []
            while self.currtok.T_TYPE != T_RGPAR:
                expressions.append(self.expr( ))
                self.advance( )
            self.advance( )
            self.recentlyEndedIf = False

            return ClassStatement(class_name_token, expressions)
        #INSTANTIATE STATEMENT
        if self.currtok.matches(T_KEYWORD, "Instantiate"):
            self.advance( )
            if self.currtok.T_TYPE != T_LPAR:
                print("Required '(' after input statement")
                return Token(T_ERROR)
            self.advance( )
            class_name = self.currtok
            """changed"""
            if class_name.value == "getAV":
                class_name = self.expr( )
            else:
                self.advance( )
            if self.currtok.T_TYPE != T_RPAR:
                print("Required ')' after input statement")
                return Token(T_ERROR)
            self.advance( )
            return InstantiateStatement(class_name)
        # INSTANTIATE STATEMENT
        if self.currtok.matches(T_KEYWORD, "setCV"):
            self.advance( )
            if self.currtok.T_TYPE != T_LPAR:
                print("Required '(' after setCV statement")
                return Token(T_ERROR)
            self.advance( )
            class_name = self.currtok
            self.advance( )
            class_value = self.currtok
            self.advance( )
            class_new_value = self.currtok
            if class_new_value.value == "getAV":
                class_new_value = self.expr( )
            else:
                self.advance( )


            if self.currtok.T_TYPE != T_RPAR:
                print("Required ')' after setCV statement")
                return Token(T_ERROR)
            self.advance( )
            return SetCVStatement(class_name, class_value, class_new_value)


        # MATH OPERATIONS
        left = self.term( )
        while self.currtok.T_TYPE in (T_PLUS, T_MINUS, T_MUL, T_DIV, T_LST, T_GRT, T_LOE, T_GOE, T_EQUAL, T_NOTEQUAL, T_DOLLAR):
            op_token = self.currtok
            self.advance( )
            right = None
            if self.currtok.matches(T_KEYWORD, "getAV"):
                right = self.expr( )
            else:
                right = self.term( )
            left = BinOP(left, op_token, right)
        return left

    def run(self):
        res_expr = []
        while self.currtok.T_TYPE != T_EOF:
            res = self.expr( )
            if res != None: res_expr.append(res)
            self.advance( )
        return res_expr
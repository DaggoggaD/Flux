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
        # RUN FUNCTION
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
                """if self.currtok.matches(T_KEYWORD, ";"):
                    
                else:
                    print("Missing ';' after function call")"""
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

                while self.currtok.T_TYPE in (T_PLUS, T_MINUS, T_MUL, T_DIV, T_LST, T_GRT, T_LOE, T_GOE, T_EQUAL, T_NOTEQUAL):
                    expr = self.expr( )
            elif self.currtok.T_TYPE in (T_PLUS, T_MINUS, T_MUL, T_DIV, T_LST, T_GRT, T_LOE, T_GOE, T_EQUAL, T_NOTEQUAL):
                expr = self.expr()
                if expr!=None:
                    expr = self.leftest_expression_modifier(expr, oldexpr)
                else:
                    expr = oldexpr
                while self.currtok.T_TYPE in (T_PLUS, T_MINUS, T_MUL, T_DIV, T_LST, T_GRT, T_LOE, T_GOE, T_EQUAL, T_NOTEQUAL):
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
                print("Required '(' after if statement")
                return Token(T_ERROR)
            self.advance( )
            arguments = []
            while self.currtok.T_TYPE != T_RPAR:
                arguments.append(self.expr( ))
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
            self.recentlyEndedIf = False
            """NEEDS TO COMPLETE ARGUMENTS (, DOESNT WORK"""
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

        # MATH OPERATIONS
        left = self.term( )
        while self.currtok.T_TYPE in (T_PLUS, T_MINUS, T_MUL, T_DIV, T_LST, T_GRT, T_LOE, T_GOE, T_EQUAL, T_NOTEQUAL):
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

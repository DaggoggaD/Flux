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
        return f"(func arguments{self.arguments}: {self.expression})"


class GetAVStatement:
    def __init__(self, array, location):
        self.array = array
        self.location = location

    def __repr__(self):
        return f"(getAV: {self.array}[{self.location}])"


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
            expr = self.expr( )
            oldexpr = expr
            if type(expr) == GetAVStatement:
                expr = self.expr( )
                if expr != None:
                    expr = self.leftest_expression_modifier(expr, oldexpr)
                else:
                    expr = oldexpr

                while self.currtok.T_TYPE in (T_PLUS, T_MINUS, T_LST, T_GRT, T_LOE, T_GOE, T_EQUAL, T_NOTEQUAL):
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
                print("Required ')' after if statement")
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
                print("Required ')' after if statement")
                return Token(T_ERROR)
            self.advance( )
            return GetAVStatement(arr_name, var_location)
        # FUNCTION STATEMENT#
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
        # MATH OPERATIONS
        left = self.term( )
        while self.currtok.T_TYPE in (T_PLUS, T_MINUS, T_LST, T_GRT, T_LOE, T_GOE, T_EQUAL, T_NOTEQUAL):
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

"""
 * @author nhphung
"""
from AST import * 
from Visitor import *
from Utils import Utils
from StaticError import *
from collections import defaultdict
import functools

class MType:
    def __init__(self,partype,rettype):
        self.partype = partype
        self.rettype = rettype

class Symbol:
    def __init__(self,name,mtype,value = None):
        self.name = name
        self.mtype = mtype
        self.value = value

class StaticChecker(BaseVisitor,Utils):

    global_envi = [
    Symbol("getInt",MType([],IntType())),
    Symbol("putInt",MType([IntType()],VoidType())),
    Symbol("putIntLn",MType([IntType()],VoidType())),
    Symbol("getFloat", MType([], FloatType())),
    Symbol("putFloat",MType([FloatType()],VoidType())),
    Symbol("putFloatLn",MType([FloatType()],VoidType())),
    Symbol("putBool",MType([BoolType()],VoidType())),
    Symbol("putBoolLn",MType([BoolType()],VoidType())),
    Symbol("putString",MType([StringType()],VoidType())),
    Symbol("putStringLn",MType([StringType()],VoidType())),
    Symbol("putLn",MType([],VoidType())),
    ]
    
    visited_funcs = []
    validBinOps = defaultdict(dict)

    def __init__(self,ast):
        self.ast = ast
        self.visited_funcs = []
        self.fillBinOpsDict()

    def check(self):
        return self.visit(self.ast,StaticChecker.global_envi)

    # c []
    # c [[funcdecls&vardecls, global env]]
    def visitProgram(self, ast, c):
        program = functools.reduce(lambda x,y: [self.visit(y,x) + x[0]], ast.decl,[list(StaticChecker.global_envi)])
        
        functions = list(filter(lambda x: type(x.mtype) is MType, self.flatten(program)))

        if self.lookup("main", functions, lambda x: x.name) is None: # should it also check for void and params? 
            raise NoEntryPoint
        functions = list(filter(lambda x: x.name != "main", functions))

        for func in self.visited_funcs:
            functions.remove(func)
        functions = list(filter(lambda x: x not in self.global_envi, functions))
        
        if functions != []:
            raise UnreachableFunction(functions[0].name)

        return program

    # c [[funcdecls&vardecls, global env]]
    # no children
    def visitVarDecl(self, ast, c):
        name = ast.variable
        if self.lookup(name, c[0], lambda x: x.name):
            raise Redeclared(Variable(), name)
        return [Symbol(name, ast.varType)]

    # c [[funcdecls&vardecls, global env]]
    # c [[params], [funcname, oldc]]
    def visitFuncDecl(self,ast, c):
        name = ast.name.name
        if self.lookup(name, c[0], lambda x: x.name):
            raise Redeclared(Function(), name)
        
        try:
            c = functools.reduce(lambda x,y: [x[0]+self.visit(y,x),c[0]],ast.param,[[],c[0]])
        except Redeclared as e:
            raise Redeclared(Parameter(), e.n)
        
        paramTypes = list(map(lambda x: x.mtype, c[0]))
        c[1].insert(0,Symbol(name, MType(paramTypes,ast.returnType)))

        self.visit(ast.body, c)
        if not self.isAlwaysReturning(ast.body.member) and type(ast.returnType) is not VoidType:
            raise FunctionNotReturn(name)

        return []
    
    # no special c
    # no children
    def visitId(self,ast,c):
        elem = self.lookup(ast.name, self.flatten(c), lambda x: x.name)
        if elem is not None:
            return elem.mtype.rettype if type(elem.mtype) is MType else elem.mtype
        else:
            raise Undeclared(Identifier(), ast.name)

    # c [[], oldc]
    # body: [[], [vardecls], oldc]
    # else: [[vardecls], oldc]
    def visitBlock(self,ast,c):
        for y in ast.member:
            if isinstance(y,Block):
                self.visit(y, self.flatten([[[]],c]))
            elif isinstance(y, VarDecl):
                c[0] += self.visit(y,c)
            else: 
                self.visit(y,c)
        return []

    # no special c
    # no children that manipulate c
    def visitCallExpr(self, ast, c):
        func = self.lookup(ast.method.name,self.flatten(c),lambda x: x.name)
        if func is None or not type(func.mtype) is MType:
            raise Undeclared(Function(),ast.method.name)

        formalParams = func.mtype.partype

        try:
            givenParams = [self.visit(x,c) for x in ast.param] if ast.param else []
        except TypeMismatchInStatement as e:
            raise TypeMismatchInExpression(e.stmt)

        if len(formalParams) != len(givenParams):
            raise TypeMismatchInStatement(ast)
        else:
            for i, formalParam  in enumerate(formalParams):
                if type(formalParam) != type(givenParams[i]):
                    if type(formalParam) is FloatType and type(givenParams[i]) is IntType:
                        continue
                    elif (type(formalParam) is ArrayPointerType and type(givenParams[i]) is ArrayType and
                        formalParam.eleType == givenParams[i].eleType):
                        continue
                    else: 
                        raise TypeMismatchInExpression(ast)

                elif (type(formalParam) is ArrayPointerType and type(givenParams[i]) is ArrayType and
                    type(self.validBinOps[str(formalParam.eleType)][str(givenParams[i].eleType)]["="]) is type(formalParam)):
                    continue

            if func not in self.visited_funcs:
                self.visited_funcs.append(func) 

            return func.mtype.rettype

    # no special c
    # no children that manipulate c
    def visitUnaryOp(self, ast, c):
        body = self.visit(ast.body, c)
        if ast.op == "!" and type(body) is not BoolType:
            raise TypeMismatchInExpression(ast)
        if ast.op == "-" and type(body) is not IntType and type(body) is not FloatType:
            raise TypeMismatchInExpression(ast)

        return body

    # no special c
    # no children that manipulate c
    def visitBinaryOp(self, ast, c):
        left = self.visit(ast.left, c)
        right = self.visit(ast.right,c)

        if ast.op == "=" and not (isinstance(ast.left, Id) or isinstance(ast.left, ArrayCell)):
            raise NotLeftValue(ast)
        
        try:
            return self.validBinOps[str(left)][str(right)][ast.op]
        except:
            raise TypeMismatchInExpression(ast)

    # no special c
    # c [[], oldc]
    def visitIf(self, ast, c):
     
        expr = self.visit(ast.expr, c)
        if type(expr) is not type(BoolType()):
            raise TypeMismatchInStatement(ast)
        
        self.visit(ast.thenStmt, self.flatten([[[]],c]))
        if ast.elseStmt is not None:
            self.visit(ast.elseStmt, self.flatten([[[]],c]))
        return []

    # no special c
    # c [[], oldc]
    def visitFor(self, ast, c):
        expr1 = self.visit(ast.expr1,c)
        expr2 = self.visit(ast.expr2,c)
        expr3 = self.visit(ast.expr3,c)

        if type(expr1) != type(IntType()) or type(expr2) != type(BoolType()) or type(expr3) != type(IntType()):
            raise TypeMismatchInStatement(ast)
        try:
            self.visit(ast.loop, self.flatten([[[]],c]))
        except BreakNotInLoop:
            pass
        except ContinueNotInLoop:
            pass
        return []

    # no special c
    # c [[], oldc]
    def visitDowhile(self, ast, c):
        expr = self.visit(ast.exp, c)
        if type(expr) is not type(BoolType()):
            raise TypeMismatchInStatement(ast)

        c = self.flatten([[[]],c])
        try:
            for stmt in ast.sl:
                c[0] += self.visit(stmt,c)
        except BreakNotInLoop:
            pass
        except ContinueNotInLoop:
            pass

        return []

    # no children
    def visitBreak(self, ast, c):
        raise BreakNotInLoop

    # no children
    def visitContinue(self, ast, c):
        raise ContinueNotInLoop

    # normal c, but first occurence of func is current scope
    # no children hat manipulate c   
    def visitReturn(self, ast, c):
        retExpr = self.visit(ast.expr, c) if ast.expr is not None else None
        # first occurence of func is closest scope
        retType = next(x.mtype.rettype for x in self.flatten(c) if type(x.mtype) == MType)

        if type(retExpr) == type(retType):
            if type(retExpr) is ArrayType or type(retExpr) is ArrayPointerType:
                if type(retExpr.eleType) is not type(retType.eleType):
                    raise TypeMismatchInStatement(ast)
            else:
                pass
            #return type
        elif retExpr is None and type(retType) is type(VoidType()):
            pass
            #return Void
        elif type(retExpr) is type(IntType()) and type(retType) is type(FloatType()):
            pass
            #return Float
        elif (type(retExpr) is ArrayType and type(retType) is ArrayPointerType and
            type(retExpr.eleType) is type(retType.eleType)):
            pass
            #return ArrayPointerType with type
        else:
            raise TypeMismatchInStatement(ast)

        return []
    
    # no special c
    # no children that manipulate c
    def visitArrayCell(self, ast, c):
        arrname = self.visit(ast.arr,c)
        index = self.visit(ast.idx,c)
        if type(arrname) is not ArrayType or type(index) is not type(IntType()):
            raise TypeMismatchInExpression(ast)
        return arrname.eleType
    
    def visitStringLiteral(self, ast, c):
        return StringType()

    def visitIntLiteral(self, ast, c):
        return IntType()

    def visitFloatLiteral(self, ast, c):
        return FloatType()

    def visitBooleanLiteral(self, ast, c):
        return BoolType()
    
    def visitVoidLiteral(self, ast, c):
        return VoidType()

    def flatten(self, lst):
        return functools.reduce(lambda x,y: x+y if isinstance(y, list) else x + [y], lst, [] )
    
    def isAlwaysReturning(self, list_):
        for elem in list_:
            if type(elem) is Return:
                return True
            elif type(elem) is If:
                if self.isAlwaysReturning(elem.thenStmt.member) and (self.isAlwaysReturning(elem.elseStmt.member) if elem.elseStmt is not None else False):
                    return True
            elif type(elem) is Block:
                if self.isAlwaysReturning(elem.member):
                    return True
            elif type(elem) is For:
                if self.isAlwaysReturning(elem.loop.member): # loop defined as Stmt, assuming: it's always Block
                    return True
            elif type(elem) is Dowhile:
                if self.isAlwaysReturning(elem.sl):
                    return True
        return False

    def fillBinOpsDict(self):
        boolOps = ["==", "!=", "!", "&&", "||"]
        compOps = ["<", ">", "<=", ">="]
        arithOps = ["+", "-", "*", "/"]
        
        self.validBinOps[str(BoolType())][str(BoolType())] = {}
        self.validBinOps[str(IntType())][str(IntType())] = {}
        self.validBinOps[str(IntType())][str(FloatType())] = {}
        self.validBinOps[str(FloatType())][str(IntType())] = {}
        self.validBinOps[str(FloatType())][str(FloatType())] = {}
        self.validBinOps[str(StringType())][str(StringType())] = {}

        for op in boolOps + ["="]:
            self.validBinOps[str(BoolType())][str(BoolType())].update({op: BoolType()})

        self.validBinOps[str(IntType())][str(IntType())].update({"==": BoolType()})
        self.validBinOps[str(IntType())][str(IntType())].update({"!=": BoolType()}) 
        for op in compOps:
            self.validBinOps[str(IntType())][str(IntType())].update({op: BoolType()}) 
            self.validBinOps[str(IntType())][str(FloatType())].update({op: BoolType()}) 
            self.validBinOps[str(FloatType())][str(IntType())].update({op: BoolType()}) 
            self.validBinOps[str(FloatType())][str(FloatType())].update({op: BoolType()}) 
        
        self.validBinOps[str(IntType())][str(IntType())].update({"%": IntType()}) 
        for op in arithOps + ["="]:
            self.validBinOps[str(IntType())][str(IntType())].update({op: IntType()}) 
            self.validBinOps[str(IntType())][str(FloatType())].update({op: FloatType()}) 
            self.validBinOps[str(FloatType())][str(IntType())].update({op: FloatType()}) 
            self.validBinOps[str(FloatType())][str(FloatType())].update({op: FloatType()}) 
        self.validBinOps[str(IntType())][str(FloatType())].pop("=") 
        self.validBinOps[str(StringType())][str(StringType())].update({"=": StringType()})   
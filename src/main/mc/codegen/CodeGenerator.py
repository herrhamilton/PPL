'''
 *   @author Nguyen Hua Phung
 *   @version 1.0
 *   23/10/2015
 *   This file provides a simple version of code generator
 *
'''
from Utils import *
from StaticCheck import *
from StaticError import *
from Emitter import Emitter
from Frame import Frame
from abc import ABC, abstractmethod

class CodeGenerator(Utils):
    def __init__(self):
        self.libName = "io"

    def init(self):
        return [Symbol("getInt", MType(list(), IntType()), CName(self.libName)),
                    Symbol("putInt", MType([IntType()], VoidType()), CName(self.libName)),
                    Symbol("putIntLn", MType([IntType()], VoidType()), CName(self.libName)),
                    Symbol("putFloat", MType([FloatType()], VoidType()), CName(self.libName)),
                    Symbol("putFloatLn", MType([FloatType()], VoidType()), CName(self.libName))
                    ]

    def gen(self, ast, dir_):
        #ast: AST
        #dir_: String

        gl = self.init()
        gc = CodeGenVisitor(ast, gl, dir_)
        gc.visit(ast, None)

class ClassType(Type):
    def __init__(self, cname):
        #cname: String
        self.cname = cname

    def __str__(self):
        return "ClassType"

    def accept(self, v, param):
        return v.visitClassType(self, param)

class SubBody():
    def __init__(self, frame, sym):
        #frame: Frame
        #sym: List[Symbol]

        self.frame = frame
        self.sym = sym

class Access():
    def __init__(self, frame, sym, isLeft, isFirst):
        #frame: Frame
        #sym: List[Symbol]
        #isLeft: Boolean
        #isFirst: Boolean

        self.frame = frame
        self.sym = sym
        self.isLeft = isLeft
        self.isFirst = isFirst

class Val(ABC):
    pass

class Index(Val):
    def __init__(self, value):
        #value: Int

        self.value = value

class CName(Val):
    def __init__(self, value):
        #value: String

        self.value = value

class CodeGenVisitor(BaseVisitor, Utils):
    def __init__(self, astTree, env, dir_):
        #astTree: AST
        #env: List[Symbol]
        #dir_: File

        self.astTree = astTree
        self.env = env
        self.className = "MCClass"
        self.path = dir_
        self.emit = Emitter(self.path + "/" + self.className + ".j")

    def visitProgram(self, ast, c):
        #ast: Program
        #c: Any

        self.emit.printout(self.emit.emitPROLOG(self.className, "java.lang.Object"))
        e = SubBody(None, self.env)
        for x in ast.decl:
            e = self.visit(x, e)
        # generate default constructor
        self.genMETHOD(FuncDecl(Id("<init>"), list(), None, Block(list())), c, Frame("<init>", VoidType))
        self.emit.emitEPILOG()
        return c

    def genMETHOD(self, consdecl, o, frame):
        #consdecl: FuncDecl
        #o: Any
        #frame: Frame

        isInit = consdecl.returnType is None
        isMain = consdecl.name.name == "main" and len(consdecl.param) == 0 and type(consdecl.returnType) is VoidType
        returnType = VoidType() if isInit else consdecl.returnType
        methodName = "<init>" if isInit else consdecl.name.name
        intype = [ArrayPointerType(StringType())] if isMain else list()
        mtype = MType(intype, returnType)

        self.emit.printout(self.emit.emitMETHOD(methodName, mtype, not isInit, frame))

        frame.enterScope(True)

        glenv = o

        # Generate code for parameter declarations
        if isInit:
            self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "this", ClassType(self.className), frame.getStartLabel(), frame.getEndLabel(), frame))
        if isMain:
            self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "args", ArrayPointerType(StringType()), frame.getStartLabel(), frame.getEndLabel(), frame))

        body = consdecl.body
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))

        # Generate code for statements
        if isInit:
            self.emit.printout(self.emit.emitREADVAR("this", ClassType(self.className), 0, frame))
            self.emit.printout(self.emit.emitINVOKESPECIAL(frame))
        list(map(lambda x: self.visit(x, SubBody(frame, glenv)), body.member))

        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        if type(returnType) is VoidType:
            self.emit.printout(self.emit.emitRETURN(VoidType(), frame))
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope();

    def visitFuncDecl(self, ast, o):
        #ast: FuncDecl
        #o: Any

        subctxt = o
        frame = Frame(ast.name, ast.returnType)
        self.genMETHOD(ast, subctxt.sym, frame)
        return SubBody(None, [Symbol(ast.name, MType(list(), ast.returnType), CName(self.className))] + subctxt.sym)

    def visitVarDecl(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        if frame is None: #global
            self.emit.printout(self.emit.emitATTRIBUTE(ast.variable, ast.varType, False, None))
            o.sym.append(Symbol(ast.variable, ast.varType, CName(self.className)))
            return o

        else: #local var
            raise Exception("ÄH HALLOOOOOOOO")
            pass

    def visitCallExpr(self, ast, o):
        #ast: CallExpr
        #o: Any

        ctxt = o
        frame = ctxt.frame
        nenv = ctxt.sym
        sym = self.lookup(ast.method.name, nenv, lambda x: x.name)
        cname = sym.value.value
    
        ctype = sym.mtype

        in_ = ("", list())
        for x in ast.param:
            str1, typ1 = self.visit(x, Access(frame, nenv, False, True))
            in_ = (in_[0] + str1, in_[1].append(typ1))
        self.emit.printout(in_[0])
        self.emit.printout(self.emit.emitINVOKESTATIC(cname + "/" + ast.method.name, ctype, frame))

    def visitDowhile(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        frame.enterLoop()

        self.emit.printout(self.emit.emitLABEL(frame.getContinueLabel(), frame))
        for st in ast.sl:
            self.visit(st, SubBody(frame, ctxt.sym))
        exp, exptyp = self.visit(ast.exp,Access(frame, ctxt.sym, False, False))
        self.emit.printout(self.emit.emitIFTRUE(frame.getContinueLabel(), frame))
        self.emit.printout(self.emit.emitLABEL(frame.getBreakLabel(), frame))

        frame.exitLoop()

    def visitFor(self, ast, o):
    # expr1:Expr
    # expr2:Expr
    # expr3:Expr
    # loop:Stmt
        ctxt = o
        frame = ctxt.frame

        frame.enterLoop()
        exp1, exp1typ = self.visit(ast.expr1,Access(frame, ctxt.sym, False, False))

        self.emit.printout(self.emit.emitLABEL(frame.getContinueLabel(), frame))
        exp2, exp2typ = self.visit(ast.expr2,Access(frame, ctxt.sym, False, False))
        self.emit.printout(self.emit.emitIFFALSE(frame.getBreakLabel(), frame))

        # loop
        self.visit(ast.loop, ctxt) #TODO: ctxt Correct?
        #list(map(lambda x: self.visit(x, SubBody(frame, ctxt.sym)), ast.loop)) # from Jim
        #exp3
        exp3, exp3typ = self.visit(ast.expr3,o)
        

        self.emit.printout(self.emit.emitGOTO(frame.getContinueLabel(),frame))
        self.emit.printout(self.emit.emitLABEL(frame.getBreakLabel(), frame))

        frame.exitLoop()
    # evaluate expr1
    # label1
    # evaluate expr2
    # if false, jump to label 2
    # evaluate loop
    # evaluate expr 3
    # goto label1
    # label 2

    def visitIntLiteral(self, ast, o):
        #ast: IntLiteral
        #o: Any
        
        ctxt = o
        frame = ctxt.frame
        return self.emit.emitPUSHICONST(ast.value, frame), IntType()

    def visitFloatLiteral(self, ast, o):
        #ast: FloatLiteral
        #o: Any
        
        ctxt = o
        frame = ctxt.frame
        return self.emit.emitPUSHFCONST(str(ast.value), frame), FloatType()

    def visitBinaryOp(self, ast, o):
        ctxt = o
        frame = ctxt.frame

        if ast.op == "=":
            return self.visitAssignment(ast, o)
        
        if ast.op in ["+", "-", "*", "/"]:
            operandStr, type_ = self.getOperands(ast.left, ast.right, o)
            if ast.op == "+" or ast.op == "-":
                operandStr += self.emit.emitADDOP(ast.op, type_ ,frame)
            else:
                operandStr += self.emit.emitMULOP(ast.op, type_ ,frame)

            return operandStr, type_
        if ast.op in [">", "<", ">=", "<=", "==", "!="]: 
            #TODO: types
            leftStr, leftType = self.visit(ast.left, Access(frame, o.sym, False, False))
            rightStr, rightType = self.visit(ast.right, Access(frame, o.sym, False, False))

            operandStr = leftStr + rightStr + self.emit.emitREOP(ast.op, leftType, frame)
            self.emit.printout(operandStr)
            return operandStr, BoolType() # TODO: with or without brackets?!

    def visitAssignment(self, ast, o):
        # a = b (index1 = index2)
        # iload_2
        # dup # always leave value on stack after assignment/expression
        # istore_1

        ctxt = o
        frame = ctxt.frame

        #this visit just for type checking
        _, l_ = self.visit(ast.left, Access(frame, o.sym, True, True))

        rightStr, r_ = self.visit(ast.right, Access(frame, o.sym, False, False))
        operandStr = rightStr

        leftType = type(l_)
        rightType = type(r_)

        if leftType is not rightType:
            if leftType is IntType and rightType is FloatType:
                raise Exception("Cannot assign float to int.. But didn't we do that in StaticCheck?!")
            elif leftType is FloatType and rightType is IntType:
                operandStr += self.emit.emitI2F(frame)
            # else:
            #     raise NotImplementedError("Supporting only Int and Float atm") # cannot use this because it breaks genMETHOD. lol.

            # duplicate result of assignment so it stays after storing
            # get store cell
        leftStr, leftType = self.visit(ast.left, Access(frame, o.sym, True, False))
        operandStr += leftStr # TODO: CHECK: deleted "self.emit.emitDUP(frame) + " before leftStr so Code works.. Does it get dup'd elsewhere?

        self.emit.printout(operandStr)
        return operandStr, leftType

    def visitId(self, ast, o):
        frame = o.frame
        symbols = o.sym
        isFirst = o.isFirst
        isLeft = o.isLeft
        id_ = self.lookup(ast.name, symbols, lambda x: x.name)

        if type(id_.value) is CName:
            name = self.className + "/" + id_.name
            if isLeft:
                if isFirst: #just for type checking, NO emit here
                    x = "", id_.mtype
                    return x # find id in symbols
                else:
                    return self.emit.emitPUTSTATIC(name, id_.mtype, frame), id_.mtype # find id, store
            else:
                return self.emit.emitGETSTATIC(name,id_.mtype,frame), id_.mtype #find id in symbols, load index
        else: #local
            raise Exception("Should not enter this yet..")

    def getOperands(self, lOp, rOp, o):
        frame = o.frame

        lStr, l_ = self.visit(lOp, Access(frame, o.sym, False, False))
        rStr, r_ = self.visit(rOp, Access(frame, o.sym, False, False))
        
        lType = type(l_)
        rType = type(r_)

        if lType is rType:
            return lStr + rStr, lType
        elif lType is FloatType and rType is IntType:
            return lStr + rStr + self.emit.emitI2F(frame), FloatType #TODO: delete () again (move to Emitter)
        elif lType is IntType and rType is FloatType:
            return lStr + self.emit.emitI2F(frame) + rStr, FloatType
        else:
            raise Exception("Should never come here")

        
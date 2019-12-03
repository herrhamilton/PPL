from MCParser import MCParser
from MCVisitor import MCVisitor
from AST import *
from functools import reduce

class ASTGeneration(MCVisitor):
    def flatten(self, lst):
        new = reduce(lambda x,y: x+y if isinstance(y, list) else x + [y], lst, [] )
        return new
        
# program: program_parts* EOF;
    def visitProgram(self,ctx:MCParser.ProgramContext):
        return Program(self.flatten([self.visit(x) for x in ctx.program_part()]))
    
# program_part: variable_declaration SEMI | function;
    def visitProgram_part(self, ctx:MCParser.Program_partContext):
        return self.visit(ctx.variable_declaration()) if ctx.SEMI() else self.visit(ctx.function())

# function: (primtype (LSB RSB)? | VOIDTYPE) ID LB param_list? RB block;
    def visitFunction(self, ctx:MCParser.FunctionContext):
        paramList = self.visit(ctx.param_list()) if ctx.param_list() else []
        
        if ctx.VOIDTYPE():
            funcType = VoidType()
        elif ctx.LSB():
            funcType = ArrayPointerType(self.visit(ctx.primtype()))
        else:
            funcType = self.visit(ctx.primtype())
        block = self.visit(ctx.block() if ctx.block() else [])
        return FuncDecl(Id(ctx.ID().getText()), paramList, funcType, block)
            
# param_list: param_decl (COMMA param_decl)*; // foo(int a, float b, boolean c) {...
    def visitParam_list(self, ctx:MCParser.Param_listContext):
        return [self.visit(x) for x in ctx.param_decl()]

# param_decl: primtype ID (LSB RSB)?
    def visitParam_decl(self, ctx:MCParser.Param_declContext):
        if ctx.LSB():
            return VarDecl(ctx.ID().getText(), ArrayPointerType(self.visit(ctx.primtype())))
        else:
            return VarDecl(ctx.ID().getText(), self.visit(ctx.primtype())) 

# if_statement: IF LB exp RB block (ELSE block)?; // dangling-else-problem?
    def visitIf_statement(self, ctx:MCParser.If_statementContext):
        exp = self.visit(ctx.exp())
        if ctx.ELSE():
            _then = self.visit(ctx.block(0))
            _else = self.visit(ctx.block(1))
            return If(exp, _then, _else)
        else:
            _then = self.visit(ctx.block(0)) # TODO: again why index?
            return If(exp, _then, None)

# loop: for_loop | do_while_loop;
    def visitLoop(self, ctx:MCParser.LoopContext):
        return self.visit(ctx.for_loop()) if ctx.for_loop() else self.visit(ctx.do_while_loop())

# for_loop: FOR LB exp SEMI exp SEMI exp RB block;
    def visitFor_loop(self, ctx:MCParser.For_loopContext):
        exp1 = self.visit(ctx.exp(0))
        exp2 = self.visit(ctx.exp(1))
        exp3 = self.visit(ctx.exp(2))
        loop = self.visit(ctx.block())
        return For(exp1, exp2, exp3, loop)

# do_while_loop: DO block WHILE LB exp RB SEMI;
    def visitDo_while_loop(self, ctx:MCParser.Do_while_loopContext):
        return Dowhile(self.visit(ctx.block()).member, self.visit(ctx.exp()))

# block: LP statement* RP;
    def visitBlock(self, ctx:MCParser.BlockContext):
        return Block(self.flatten([self.visit(x) for x in ctx.statement()]))

# statement: (ret_exp | variable_declaration | funcall | exp | BREAK | CONTINUE ) SEMI | if_statement | loop | block;
    def visitStatement(self, ctx:MCParser.StatementContext):
        if ctx.ret_exp():
            return self.visit(ctx.ret_exp())
        elif ctx.variable_declaration():
            return self.visit(ctx.variable_declaration())
        elif ctx.funcall():
            return self.visit(ctx.funcall())
        elif ctx.exp():
            return self.visit(ctx.exp())
        elif ctx.BREAK():
            return Break()
        elif ctx.CONTINUE():
            return Continue()
        elif ctx.if_statement():
            return self.visit(ctx.if_statement())
        elif ctx.loop():
            return self.visit(ctx.loop())
        elif ctx.block():
            return self.visit(ctx.block())
        
# ret_exp: RETURN exp?;
    def visitRet_exp(self, ctx:MCParser.Ret_expContext):
        return Return(self.visit(ctx.exp())) if ctx.exp() else Return(None)

# variable_declaration: primtype var_list;
    def visitVariable_declaration(self, ctx:MCParser.Variable_declarationContext):
        _type = self.visit(ctx.primtype())
        varIds = self.visit(ctx.var_list())
        decls = []
        for x in varIds:
            if not isinstance(x, ArrayType):
                decls += [VarDecl(x, _type)]
            else:
                decls += [VarDecl(x.eleType, ArrayType(x.dimen, _type))]
        return self.flatten(decls)

# var: ID  (LSB INTLIT RSB)?;
    def visitVar(self, ctx:MCParser.VarContext):
        if ctx.INTLIT(): # this hack is so ugly, but no other way to get array dimen
            return ArrayType(ctx.INTLIT(), ctx.ID().getText())
        else:
            return ctx.ID().getText()
# var_list: var (COMMA var_list)?;
    def visitVar_list(self, ctx:MCParser.Var_listContext):    
        if ctx.COMMA():
            return [self.visit(ctx.var())] + self.visit(ctx.var_list())
        else:
            return [self.visit(ctx.var())]

# funcall: ID LB argum_list? RB;
    def visitFuncall(self, ctx:MCParser.FuncallContext):
        return CallExpr(Id(ctx.ID().getText()),self.visit(ctx.argum_list()) if ctx.argum_list() else [])

# argum_list: exp (COMMA exp)*; // foo(a, 3.14, bar());
    def visitArgum_list(self, ctx:MCParser.Argum_listContext):
        return [self.visit(x) for x in ctx.exp()] # if (ctx.COMMA()) else [self.visit(ctx.exp)] is this needed?

# exp: exp1 OP_ASN exp | exp1;
    def visitExp(self, ctx:MCParser.ExpContext):
        if ctx.OP_ASN():
            return BinaryOp(ctx.OP_ASN().getText(), self.visit(ctx.exp1()), self.visit(ctx.exp()))
        else:
            return self.visit(ctx.exp1())

# exp1: exp1 OP_OR exp2 | exp2;
    def visitExp1(self, ctx:MCParser.Exp1Context):
        if ctx.OP_OR():
            return BinaryOp(ctx.OP_OR().getText(), self.visit(ctx.exp1()), self.visit(ctx.exp2()))
        else:
            return self.visit(ctx.exp2())

# exp2: exp2 OP_AND exp3 | exp3;
    def visitExp2(self, ctx:MCParser.Exp2Context):
        if ctx.OP_AND():
            return BinaryOp(ctx.OP_AND().getText(), self.visit(ctx.exp2()), self.visit(ctx.exp3()))
        else:
            return self.visit(ctx.exp3())

# exp3: exp4 (OP_EQ | OP_NEQ) exp4 | exp4;
    def visitExp3(self, ctx:MCParser.Exp3Context):
        if ctx.OP_EQ():
            return BinaryOp(ctx.OP_EQ().getText(), self.visit(ctx.exp4(0)), self.visit(ctx.exp4(1)))
        elif ctx.OP_NEQ():
            return BinaryOp(ctx.OP_NEQ().getText(), self.visit(ctx.exp4(0)), self.visit(ctx.exp4(1)))
        else:
            return self.visit(ctx.exp4(0)) # TODO: find out why you need the index here

# exp4: exp5 (OP_LES |OP_LEQ | OP_GRE | OP_GEQ) exp5 | exp5;
    def visitExp4(self, ctx:MCParser.Exp4Context):
        if ctx.OP_LES():
            return BinaryOp(ctx.OP_LES().getText(), self.visit(ctx.exp5(0)), self.visit(ctx.exp5(1)))
        elif ctx.OP_LEQ():
            return BinaryOp(ctx.OP_LEQ().getText(), self.visit(ctx.exp5(0)), self.visit(ctx.exp5(1)))
        elif ctx.OP_GRE():
            return BinaryOp(ctx.OP_GRE().getText(), self.visit(ctx.exp5(0)), self.visit(ctx.exp5(1)))
        elif ctx.OP_GEQ():
            return BinaryOp(ctx.OP_GEQ().getText(), self.visit(ctx.exp5(0)), self.visit(ctx.exp5(1)))
        else:
            return self.visit(ctx.exp5(0)) # TODO: find out why you need the index here

# exp5: exp5 (OP_ADD | OP_NEG) exp6 | exp6;
    def visitExp5(self, ctx:MCParser.Exp5Context):
        if ctx.OP_ADD():
            return BinaryOp(ctx.OP_ADD().getText(), self.visit(ctx.exp5()), self.visit(ctx.exp6()))
        elif ctx.OP_NEG():
            return BinaryOp(ctx.OP_NEG().getText(), self.visit(ctx.exp5()), self.visit(ctx.exp6()))
        else:
            return self.visit(ctx.exp6())

# exp6: exp6 (OP_DIV | OP_MUL | OP_MOD) exp7 | exp7;
    def visitExp6(self, ctx:MCParser.Exp6Context):
        if ctx.OP_DIV():
            return BinaryOp(ctx.OP_DIV().getText(), self.visit(ctx.exp6()), self.visit(ctx.exp7()))
        elif ctx.OP_MUL():
            return BinaryOp(ctx.OP_MUL().getText(), self.visit(ctx.exp6()), self.visit(ctx.exp7()))
        elif ctx.OP_MOD():
            return BinaryOp(ctx.OP_MOD().getText(), self.visit(ctx.exp6()), self.visit(ctx.exp7()))
        else:
            return self.visit(ctx.exp7())

# exp7: (OP_NEG | OP_NOT) exp8 | exp8;
    def visitExp7(self, ctx:MCParser.Exp7Context):
        if ctx.OP_NEG():
            return UnaryOp(ctx.OP_NEG().getText(), self.visit(ctx.exp8()))
        elif ctx.OP_NOT():
            return UnaryOp(ctx.OP_NOT().getText(), self.visit(ctx.exp8()))
        else:
            return self.visit(ctx.exp8())

# exp8: exp9 LSB RSB | exp9;
    def visitExp8(self, ctx:MCParser.Exp8Context):
        return self.visit(ctx.exp9())

# exp9: operand | subexp;
    def visitExp9(self, ctx:MCParser.Exp9Context):
        return self.visit(ctx.operand()) if ctx.operand() else self.visit(ctx.subexp())

# subexp: LB exp RB;
    def visitSubexp(self, ctx:MCParser.SubexpContext):
        return self.visit(ctx.exp())

# operand: INTLIT | BOOLLIT | FLOATLIT | STRLIT | ID | index_exp | funcall;
    def visitOperand(self, ctx:MCParser.OperandContext):
        if ctx.INTLIT():
            return IntLiteral(ctx.INTLIT())
        elif ctx.BOOLLIT():
            return BooleanLiteral(ctx.BOOLLIT())
        elif ctx.FLOATLIT():
            return FloatLiteral(ctx.FLOATLIT())
        elif ctx.STRLIT():
            return StringLiteral(ctx.STRLIT().getText())
        elif ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.index_exp():
            return self.visit(ctx.index_exp())
        elif ctx.funcall():
            return self.visit(ctx.funcall())

# index_exp: (ID | funcall) LSB exp RSB;
    def visitIndex_exp(self, ctx:MCParser.Index_expContext):
        if ctx.ID():
            return ArrayCell(Id(ctx.ID().getText()), self.visit(ctx.exp()))
        else: 
            return ArrayCell(self.visit(ctx.funcall()), self.visit(ctx.exp()))

# primtype: INTTYPE | FLOATTYPE | BOOLTYPE | STRINGTYPE;
    def visitPrimtype(self, ctx:MCParser.PrimtypeContext):
        if ctx.INTTYPE():
            return IntType()
        elif ctx.FLOATTYPE():
            return FloatType()
        elif ctx.BOOLTYPE():
            return BoolType()
        elif ctx.STRINGTYPE():
            return StringType()

import unittest
from TestUtils import TestCodeGen
from AST import *


class CheckCodeGenSuite(unittest.TestCase):
    # def test_int(self): # TODO: Fix ASTGeneration
    #     """Simple program: int main() {} """
    #     input = """void main() {putInt(100);}"""
    #     expect = "100"
    #     self.assertTrue(TestCodeGen.test(input,expect,500))

    # def test_int_ast(self):
    # 	input = Program([
    # 		FuncDecl(Id("main"),[],VoidType(),Block([
    # 			CallExpr(Id("putInt"),[IntLiteral(5)])]))])
    # 	expect = "5"
    # 	self.assertTrue(TestCodeGen.test(input,expect,501))

    # def test_float_ast(self):
    # 	input = Program([
    # 		FuncDecl(Id("main"),[],VoidType(),Block([
    # 			CallExpr(Id("putFloat"),[FloatLiteral(5.0)])]))])
    # 	expect = "5.0"
    # 	self.assertTrue(TestCodeGen.test(input,expect,502))
    
    # def test_binexp_int_ast(self):
    # 	input = Program([
    # 		FuncDecl(Id("main"),[],VoidType(),Block([
    # 			CallExpr(Id("putInt"),[BinaryOp("+",IntLiteral(2),IntLiteral(1))])]))])
    # 	expect = "3"
    # 	self.assertTrue(TestCodeGen.test(input,expect,503))

    # def test_binexp_mixed1_ast(self):
    # 	input = Program([
    # 		FuncDecl(Id("main"),[],VoidType(),Block([
    # 			CallExpr(Id("putFloat"),[BinaryOp("+",FloatLiteral(2.3),IntLiteral(1))])]))])
    # 	expect = "3.3"
    # 	self.assertTrue(TestCodeGen.test(input,expect,504))

    # def test_binexp_mixed2_ast(self):
    # 	input = Program([
    # 		FuncDecl(Id("main"),[],VoidType(),Block([
    # 			CallExpr(Id("putFloat"),[BinaryOp("+",IntLiteral(2),FloatLiteral(1.5))])]))])
    # 	expect = "3.5"
    # 	self.assertTrue(TestCodeGen.test(input,expect,505))
    
    # def test_binexp_float_ast(self):
    # 	input = Program([
    # 		FuncDecl(Id("main"),[],VoidType(),Block([
    # 			CallExpr(Id("putFloat"),[BinaryOp("+",FloatLiteral(2.2),FloatLiteral(1.2))])]))])
    # 	expect = "3.4"
    # 	self.assertTrue(TestCodeGen.test(input,expect,506))

    # def test_int_vardecl_ast(self):
    # 	input = Program([VarDecl("x", IntType()),
    # 		FuncDecl(Id("main"),[],VoidType(),Block([BinaryOp("=",Id("x"),IntLiteral(1)),
    # 			CallExpr(Id("putInt"),[Id("x")])]))])
    # 	expect = "1"
    # 	self.assertTrue(TestCodeGen.test(input,expect,507))

    # def test_float_vardecl_ast(self):
    #     input = Program([VarDecl("x", FloatType()),
	# 	    		FuncDecl(Id("main"),[],VoidType(),Block([BinaryOp("=",Id("x"),FloatLiteral(1.0)),
    # 			CallExpr(Id("putFloat"),[Id("x")])]))])
    #     expect = "1.0"
    #     self.assertTrue(TestCodeGen.test(input,expect,508))

    # def test_int2float_vardecl_ast(self):
    #     input = Program([VarDecl("x", FloatType()),
    #         FuncDecl(Id("main"),[],VoidType(),Block([BinaryOp("=",Id("x"),IntLiteral(1)),
    #             CallExpr(Id("putFloat"),[Id("x")])]))])
    #     expect = "1.0"
    #     self.assertTrue(TestCodeGen.test(input,expect,509))

    # def test_for_ast(self):
    #     exp1 = BinaryOp("=",Id("i"),IntLiteral(1))
    #     exp2 = BinaryOp("<",Id("i"),IntLiteral(5))
    #     exp3 = BinaryOp("=",Id("i"),BinaryOp("+",Id("i"),IntLiteral(1)))
    #     loop = Block([])
    #     _for = For(exp1, exp2, exp3, loop)

    #     input = Program([VarDecl("i", IntType()),
    # 		FuncDecl(Id("main"),[],VoidType(),Block([_for, CallExpr(Id("putInt"),[Id("i")])]))])
    #     expect = "5"
    #     self.assertTrue(TestCodeGen.test(input, expect, 510))

    # def test_dowhile_ast(self):
    #     exp = BinaryOp("=",Id("i"),BinaryOp("+",Id("i"),IntLiteral(2)))
    #     dowhile = Dowhile([exp], BinaryOp("<",Id("i"),IntLiteral(11)))
    #     input = Program([VarDecl("i", IntType()), FuncDecl(Id("main"),[],VoidType(),
    #         Block([BinaryOp("=",Id("i"),IntLiteral(0)), CallExpr(Id("putInt"),[Id("i")])]))])
    #     expect = "0"
    #     self.assertTrue(TestCodeGen.test(input, expect, 511))

    def test_local_int_vardecl_ast(self):
    	input = Program([FuncDecl(Id("main"),[],VoidType(),Block([
            VarDecl("x", IntType()), BinaryOp("=",Id("x"),IntLiteral(1)), CallExpr(Id("putInt"),[Id("x")])]))])
    	expect = "1"
    	self.assertTrue(TestCodeGen.test(input,expect,512))

    def test_local_float_vardecl_ast(self):
    	input = Program([FuncDecl(Id("main"),[],VoidType(),Block([
            VarDecl("x", FloatType()), BinaryOp("=",Id("x"),FloatLiteral(1.7)), CallExpr(Id("putFloat"),[Id("x")])]))])
    	expect = "1.7"
    	self.assertTrue(TestCodeGen.test(input,expect,513))
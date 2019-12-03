import unittest
from TestUtils import TestChecker
from AST import *

class CheckSuite(unittest.TestCase):

    def test_fitting_retType(self):
        input = """void main(){ return;}"""
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 499))

    def test_fitting_retType2(self):
        input = """
        float foo() { return 3.14;}
        void main(){ foo();}"""
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 493))

    def test_wrong_retType(self):
        input = """float foo() { return 3.14;}
        int bar(){ return 11;}
           void main() { foo();bar();return 2;}
           """
        expect = "Type Mismatch In Statement: Return(IntLiteral(2))"
        self.assertTrue(TestChecker.test(input, expect, 498))   

    def test_fitting_retType_arrays(self):
        input = """int[] foo() {int c[3]; return c; }
        void main() { foo();}
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 497))   

    def test_fitting_retType_arrays2_use_ast(self):
        main = FuncDecl(Id("main"), [], ArrayPointerType(IntType()), Block([Return(CallExpr(Id("foo"), [IntLiteral(2)]))]))
        foo = FuncDecl(Id("foo"), [VarDecl("x", IntType())], ArrayPointerType(IntType()), Block([VarDecl("a", ArrayType(5, IntType())), Return(Id("a"))]))
        input = Program([foo, main])
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 496))   

    def test_wrong_retType_arrays(self):
        input = """
        int[] foo() {float c[3]; return c; }
        void main() { foo();}"""
        expect = "Type Mismatch In Statement: Return(Id(c))"
        self.assertTrue(TestChecker.test(input, expect, 495))   

    def test_wrong_retType_arrays2(self):
        input = """int[] foo() {int c[3]; return c[1]; }
        void main() { foo();}
        """
        expect = "Type Mismatch In Statement: Return(ArrayCell(Id(c),IntLiteral(1)))"
        self.assertTrue(TestChecker.test(input, expect, 494))   

    def test_recursive_function(self):
        input = """ int foo() { return foo();}
        void main() { foo();}
       """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 400))

    def test_undeclared_built_in_func_use_AST(self):
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([CallExpr(Id("getInt"),[])]))])
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 401))

    def test_undeclared_built_in_func_missing_param_use_AST(self):
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([CallExpr(Id("putIntLn"),[])]))])
        expect = "Type Mismatch In Statement: CallExpr(Id(putIntLn),[])"
        self.assertTrue(TestChecker.test(input, expect, 402))

    def test_undeclared_block_in_body_use_AST(self):
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([Block([BinaryOp("=",Id("x"),IntLiteral(1))])]))])
        expect = "Undeclared Identifier: x"
        self.assertTrue(TestChecker.test(input, expect, 403))

    def test_undeclared_body_use_AST(self):
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([BinaryOp("=",Id("x"),IntLiteral(1))]))])
        expect = "Undeclared Identifier: x"
        self.assertTrue(TestChecker.test(input, expect, 404))

    def test_global_vars_use_AST(self):
        input = Program([VarDecl("a",IntType()), VarDecl("b",FloatType()), FuncDecl(Id("main"), [], VoidType(), Block([]))])
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 405))
    
    def test_global_func_use_AST(self):
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([]))])
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 406))

    def test_global_decl_mixed_use_AST(self):        
        input = Program([VarDecl("a",IntType()), FuncDecl(Id("main"), [], VoidType(), Block([])), VarDecl("b",FloatType())])
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 407))

    def test_global_redeclared_var_use_AST(self):
        input = Program([VarDecl("a",IntType()), VarDecl("a",FloatType())])
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input, expect, 408))

    def test_global_redeclared_func_use_AST(self):
        input = Program([FuncDecl(Id("foo"), [], IntType(), Block([Return(IntLiteral(1))])), FuncDecl(Id("foo"), [], IntType(), Block([]))])
        expect = "Redeclared Function: foo" 
        self.assertTrue(TestChecker.test(input, expect, 409))

    def test_global_redeclared_param_use_AST(self):
        input = Program([VarDecl("bar",IntType()), FuncDecl(Id("main"), [VarDecl("bar",IntType())], VoidType(), Block([]))])
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 410))

    def test_global_redeclared_mixed_use_AST(self):
        input = Program([VarDecl("bar",IntType()), FuncDecl(Id("bar"), [], IntType(), Block([Return(IntLiteral(1))])), VarDecl("b",FloatType())])
        expect = "Redeclared Function: bar"
        self.assertTrue(TestChecker.test(input, expect, 411))

    def test_duplicate_param_use_AST(self):
        input = Program([FuncDecl(Id("foo"), [VarDecl("a",IntType()), VarDecl("a",FloatType())], IntType(), Block([]))])
        expect = "Redeclared Parameter: a"
        self.assertTrue(TestChecker.test(input, expect, 412))

    def test_param_and_body_decl_use_AST(self):
        input = Program([FuncDecl(Id("main"), [VarDecl("a",FloatType())], VoidType(), Block([VarDecl("var",IntType())]))])
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 413))

    def test_func_and_param_same_id_use_AST(self):
        input = Program([FuncDecl(Id("main"), [VarDecl("foo",FloatType())], VoidType(), Block([]))])
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 414))

    def test_param_and_body_same_id_use_AST(self):
        input = Program([FuncDecl(Id("foo"), [VarDecl("a",FloatType())], IntType(), Block([VarDecl("a",IntType())]))])
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input, expect, 415))

    def test_global_and_body_same_id_use_AST(self):
        input = Program([VarDecl("a",FloatType()), FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a",IntType())]))])
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 416))

    def test_param_and_block_in_body_same_id_use_AST(self):
        input = Program([FuncDecl(Id("main"), [VarDecl("a",FloatType())], VoidType(), Block([Block([VarDecl("a",IntType())])]))])
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 417))

    def test_global_and_param_same_id_use_AST(self):
        input = Program([VarDecl("a",IntType()), FuncDecl(Id("main"), [VarDecl("a",FloatType())], VoidType(), Block([]))])
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 418))

    def test_body_and_block_same_id_use_AST(self):
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a",IntType()),Block([VarDecl("a",IntType())])]))])
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 419))

    def test_undeclared_function_use_ast(self):
        input = Program([FuncDecl(Id("main"),[],VoidType(),Block([CallExpr(Id("foo"),[])]))])
        expect = "Undeclared Function: foo"
        self.assertTrue(TestChecker.test(input,expect,420))

    def test_undeclared_identifier_use_ast(self):
        input = Program([FuncDecl(Id("main"),[],VoidType(),Block([BinaryOp("=", Id("x"), IntLiteral(1))]))])
        expect = "Undeclared Identifier: x"
        self.assertTrue(TestChecker.test(input,expect,421))

    def test_binary_exp_type_use_ast(self):
        input = Program([FuncDecl(Id("main"),[],VoidType(),Block([VarDecl("x",IntType()),BinaryOp("=", Id("x"), IntLiteral(1))]))])
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,422))

    def test_nested_binary_exp_use_ast(self):
        input = Program([FuncDecl(Id("main"),[],VoidType(),Block([VarDecl("x",IntType()),BinaryOp("=", Id("x"), BinaryOp("+", Id("x"), IntLiteral(1)))]))])
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,423))

    def test_binary_exp_wrong_type_use_ast(self):
        input = Program([FuncDecl(Id("main"),[],VoidType(),Block([VarDecl("x",StringType()),BinaryOp("=", Id("x"), IntLiteral(1))]))])
        expect = "Type Mismatch In Expression: BinaryOp(=,Id(x),IntLiteral(1))"
        self.assertTrue(TestChecker.test(input,expect,424))

    def test_binary_exp_different_but_valid_type_use_ast(self):
        input = Program([FuncDecl(Id("main"),[],VoidType(),Block([VarDecl("x",FloatType()),BinaryOp("=", Id("x"), IntLiteral(1))]))])
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,425))

    def test_nested_binary_exp_wrong_type_use_ast(self):
        input = Program([FuncDecl(Id("main"),[],IntType(),Block([VarDecl("x",IntType()),BinaryOp("=", Id("x"), BinaryOp("+", FloatLiteral(3.2), IntLiteral(5)))]))])
        expect = "Type Mismatch In Expression: BinaryOp(=,Id(x),BinaryOp(+,FloatLiteral(3.2),IntLiteral(5)))"
        self.assertTrue(TestChecker.test(input,expect,426))

    def test_invalid_assign_binary_op_use_ast(self):
        input = Program([FuncDecl(Id("main"),[],IntType(),Block([VarDecl("x",IntType()),BinaryOp("=", IntLiteral(5), Id("x"))]))])
        expect = "Not Left Value: BinaryOp(=,IntLiteral(5),Id(x))"
        self.assertTrue(TestChecker.test(input,expect,427))

    def test_for_loop_use_ast(self):
        exp1 = BinaryOp("=",Id("i"),IntLiteral(1))
        exp2 = BinaryOp("<",Id("i"),IntLiteral(3))
        exp3 = BinaryOp("=",Id("i"),BinaryOp("+",Id("i"),IntLiteral(1)))
        loop = Block([])
        _for = For(exp1, exp2, exp3, loop)
        func = FuncDecl(Id("main"),[VarDecl("i",IntType())], VoidType(), Block([_for]))
        input = Program([func])
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,428))

    def test_for_loop_wrong_type_use_ast(self):
        exp1 = BinaryOp("=",Id("i"),FloatLiteral(1))
        exp2 = BinaryOp("<",Id("i"),IntLiteral(3))
        exp3 = BinaryOp("=",Id("i"),BinaryOp("+",Id("i"),IntLiteral(1)))
        loop = Block([])
        _for = For(exp1, exp2, exp3, loop)
        func = FuncDecl(Id("main"),[VarDecl("i",FloatType())], IntType(), Block([_for]))
        input = Program([func])
        expect = "Type Mismatch In Statement: For(BinaryOp(=,Id(i),FloatLiteral(1));BinaryOp(<,Id(i),IntLiteral(3));BinaryOp(=,Id(i),BinaryOp(+,Id(i),IntLiteral(1)));Block([]))"
        self.assertTrue(TestChecker.test(input,expect,429))

    def test_if_expr_use_ast(self):
        expr = BinaryOp("==",IntLiteral(2),IntLiteral(2))
        if_st = If(expr,Block([]),Block([]))
        input = Program([FuncDecl(Id("main"),[],VoidType(),Block([if_st]))])
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,430))
    
    def test_wrong_if_expr_use_ast(self):
        expr = BinaryOp("+",IntLiteral(2),IntLiteral(2))
        if_st = If(expr,Block([]),Block([]))
        input = Program([FuncDecl(Id("main"),[],IntType(),Block([if_st]))])
        expect = "Type Mismatch In Statement: If(BinaryOp(+,IntLiteral(2),IntLiteral(2)),Block([]),Block([]))"
        self.assertTrue(TestChecker.test(input,expect,431))
        

    def test_dowhile_expr_use_ast(self):
        dowhile = Dowhile([], BooleanLiteral(True))
        input = Program([FuncDecl(Id("main"),[],VoidType(),Block([dowhile]))])
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,432))
    
    def test_wrong_dowhile_expr_use_ast(self):
        expr = BinaryOp("-",IntLiteral(6), IntLiteral(9))
        dowhile = Dowhile([], expr)
        input = Program([FuncDecl(Id("main"),[VarDecl("x",IntType())],IntType(),Block([dowhile]))])
        expect = "Type Mismatch In Statement: Dowhile([],BinaryOp(-,IntLiteral(6),IntLiteral(9)))"
        self.assertTrue(TestChecker.test(input,expect,433))

    def test_undeclared_dowhile_expr_use_ast(self):
        expr = BinaryOp("!=",Id("x"), IntLiteral(9))
        dowhile = Dowhile([], expr)
        input = Program([FuncDecl(Id("main"),[],IntType(),Block([dowhile]))])
        expect = "Undeclared Identifier: x"
        self.assertTrue(TestChecker.test(input,expect,434))
    
    def test_undeclared_dowhile_st_use_ast(self):
        doSt = [BinaryOp("=",Id("x"),BinaryOp("+",Id("x"),IntLiteral(1)))]
        dowhile = Dowhile(doSt, BooleanLiteral(True))
        input = Program([FuncDecl(Id("main"),[],IntType(),Block([dowhile]))])
        expect = "Undeclared Identifier: x"
        self.assertTrue(TestChecker.test(input,expect,435))

    def test_redeclared_dowhile_st_use_ast(self):
        doSt = [VarDecl("a",IntType()), VarDecl("a",IntType())]
        dowhile = Dowhile(doSt, BooleanLiteral(True))
        input = Program([FuncDecl(Id("main"),[],IntType(),Block([dowhile]))])
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,436))

    def test_return(self):
        input = "void main() {return;}"
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,437))

    def test_bool_equal(self):
        input = """void main() {if(true == true) {}}"""
        expect =""
        self.assertTrue(TestChecker.test(input,expect,438))

    def test_float_equal(self):
        input = """void main() {if(3.4 == 3.4) {}}"""
        expect ="Type Mismatch In Expression: BinaryOp(==,FloatLiteral(3.4),FloatLiteral(3.4))"
        self.assertTrue(TestChecker.test(input,expect,439))

    def test_correct_params_funcall1(self):
        input = """int foo(int a, int b) {return 42;}
        void main() {foo(2,5);}"""
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,440))

    def test_correct_params_funcall2(self):
        input = """int foo(int a, string b) {return 42;}
        void main() {foo(2,"hello");}"""
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,441))

    def test_wrong_num_of_params_funcall(self):
        input = """int foo(int a, int b) {return 42;}
        void main() {foo(2);}"""
        expect= "Type Mismatch In Statement: CallExpr(Id(foo),[IntLiteral(2)])"
        self.assertTrue(TestChecker.test(input,expect,442))

    def test_wrong_type_of_param_funcall(self):
        input = """int foo(int a) {return 42;}
        void main() {foo(2.2);}"""
        expect= "Type Mismatch In Expression: CallExpr(Id(foo),[FloatLiteral(2.2)])"
        self.assertTrue(TestChecker.test(input,expect,443))

    def test_okay_type_of_param_funcall(self):
        input = """int foo(float a) {return 42;}
        void main() {foo(2);}"""
        expect= ""
        self.assertTrue(TestChecker.test(input,expect,444))

    def test_okay_type_of_param_funcall_diff_func_type(self):
        input = """float foo(float a) {return 42;}
        void main() {foo(2);}"""
        expect= ""
        self.assertTrue(TestChecker.test(input,expect,445))
    
    def test_correct_type_of_binaryop_arr(self):
        input = """void main() {boolean b[1]; b[0] = true; if(b[0]){}}"""
        expect= ""
        self.assertTrue(TestChecker.test(input,expect,446))

    def test_assignment_arr_cell(self):
        input = """void main() {float f[2]; f[0] = 3.7; f[1] = 5;}"""
        expect= ""
        self.assertTrue(TestChecker.test(input,expect,447))

    def test_wrong_assignment_arr_cell(self):
        input = """void main() {float f[2]; f[0] = 3.7; f[1] = "what";}"""
        expect= "Type Mismatch In Expression: BinaryOp(=,ArrayCell(Id(f),IntLiteral(1)),StringLiteral(what))"
        self.assertTrue(TestChecker.test(input,expect,448))

    def test_break_in_loop(self):
        input = """void main() {
            int i;
            for(i=0; i<4; i=i+1) 
            {
                break;
            }
            }"""
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,449))
    
    def test_break_not_in_loop(self):
        input = """void main() {
            break;
            }"""
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,450))

    def test_continue_in_loop(self):
        input = """void main() {
            int i;
            for(i=0; i<4; i=i+1) 
            {
                continue;
            }
            }"""
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,451))
    
    def test_continue_not_in_loop(self):
        input = """void main() {
            continue;
            }"""
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,452))

    def test_type_mismatch_in_if(self):
        input="""void main() {if(4){}}"""
        expect="Type Mismatch In Statement: If(IntLiteral(4),Block([]))"
        self.assertTrue(TestChecker.test(input,expect,453))

    def test_diff_numofparam_stmt(self):
        """More complex program"""
        input = """void main () {
            putIntLn();
        }"""
        expect = "Type Mismatch In Statement: CallExpr(Id(putIntLn),[])"
        self.assertTrue(TestChecker.test(input,expect,454))
    
    def test_diff_numofparam_expr(self):
        """More complex program"""
        input = """void main () {
            putIntLn(getInt(4));
        }"""
        expect = "Type Mismatch In Expression: CallExpr(Id(getInt),[IntLiteral(4)])"
        self.assertTrue(TestChecker.test(input,expect,455))

    def test_diff_numofparam_expr_use_ast(self):
        """More complex program"""
        input = Program([
                FuncDecl(Id("main"),[],IntType(),Block([
                    CallExpr(Id("putIntLn"),[
                        CallExpr(Id("getInt"),[IntLiteral(4)])
                        ])]))])
        expect = "Type Mismatch In Expression: CallExpr(Id(getInt),[IntLiteral(4)])"
        self.assertTrue(TestChecker.test(input,expect,456))

    def test_diff_numofparam_stmt_use_ast(self):
        """More complex program"""
        input = Program([
                FuncDecl(Id("main"),[],IntType(),Block([
                    CallExpr(Id("putIntLn"),[])]))])
        expect = "Type Mismatch In Statement: CallExpr(Id(putIntLn),[])"
        self.assertTrue(TestChecker.test(input,expect,457))
    
    def test_unary_op(self):
        input ="""void main(){int i = -5;}"""
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,460))
    
    def test_unary_op2(self):
        input ="""void main(){float a = -43.1;}"""
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,457))

    def test_unary_op3(self):
        input ="""void main(){int i = 1;}"""
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,461))

    def test_unary_op4(self):
        input ="""void main(){string a = -"hehe";}"""
        expect = "Type Mismatch In Expression: UnaryOp(-,StringLiteral(hehe))"
        self.assertTrue(TestChecker.test(input,expect,462))

    def test_unary_op5(self):
        input ="""void main(){int f = !5;}"""
        expect = "Type Mismatch In Expression: UnaryOp(!,IntLiteral(5))"
        self.assertTrue(TestChecker.test(input,expect,463))

    def test_unary_op6(self):
        input ="""void main(){if(!(-5*3 == 45)){}{}}"""
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,464))

    def test_unreachable_func(self):
        input = """int foo(){return 2;};void main(){}"""
        expect= "Unreachable Function: foo"
        self.assertTrue(TestChecker.test(input, expect, 465))

    def test_unreachable_func2(self):
        input = """int foo(){return 2;} float bar(){return 4.3;} void main(){foo();} """
        expect= "Unreachable Function: bar"
        self.assertTrue(TestChecker.test(input, expect, 466))

    def test_no_entry(self):
        input = """int foo(){return 2;}"""
        expect= "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 467))

    def test_if_all_ret_paths(self):
        input = """int foo() {if(true){return 2;} else {return 4;}}
        void main() {foo();}"""
        expect= ""
        self.assertTrue(TestChecker.test(input, expect, 467))

    def test_if_missing_ret_path(self):
        input = """int foo() {if(true){return 2;} else {}}
        void main() {foo();}"""
        expect= "Function foo Not Return "
        self.assertTrue(TestChecker.test(input, expect, 468))

    def test_func_ret_path(self):
        input = """int foo() {return 1;}
        void main() {foo();}"""
        expect= ""
        self.assertTrue(TestChecker.test(input, expect, 469))

    def test_func_missing_ret_path(self):
        input = """int foo() {}
        void main() {foo();}"""
        expect= "Function foo Not Return "
        self.assertTrue(TestChecker.test(input, expect, 470))

    def test_if_mising_ret_but_later(self):
        input = """int foo() {if(true){return 2;} else {} return 1;}
        void main() {foo();}"""
        expect= ""
        self.assertTrue(TestChecker.test(input, expect, 471))

    def test_ret_path_block(self):
        input = """int foo() {{return 3;}}
        void main() {foo();}"""
        expect= ""
        self.assertTrue(TestChecker.test(input, expect, 472))

    def test_ret_path_for(self):
        input = """int foo() {int i;for(i=1;i<4;i=i+1){return 4;} return 4;)}
        void main() {foo();}"""
        expect= ""
        self.assertTrue(TestChecker.test(input, expect, 473))

    def test_ret_path_after_for(self):
        input = """int foo() {int i;for(i=1;i<4;i=i+1){} return 3;}
        void main() {foo();}"""
        expect= ""
        self.assertTrue(TestChecker.test(input, expect, 474))
   
    def test_ret_path_dowhile(self):
        input = """int foo() {int i;do{return 2;}while(true);}
        void main() {foo();}"""
        expect= ""
        self.assertTrue(TestChecker.test(input, expect, 475))

    def test_ret_path_after_dowhile(self):
        input = """int foo() {int i;do{return 1;}while(true); return 7;}
        void main() {foo();}"""
        expect= ""
        self.assertTrue(TestChecker.test(input, expect, 476))

    def test_missing_ret_path_for(self):
        input = """int foo() {int i;for(i=1;i<4;i=i+1){}}
        void main() {foo();}"""
        expect= "Function foo Not Return "
        self.assertTrue(TestChecker.test(input, expect, 477))
       
    def test_missing_ret_path_but_void(self):
        input = """void main() {}"""
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 478))

    def test_missing_ret_path_big(self):
        input="""int foo() {
            if(true)
            {return 1;} 
            do{
                if(false) {}
                else {return 1;}
            }while(true);
            {{int i; for(i=1;i<5;i=i+1){}}}
        }
        void main() {foo();}"""
        expect = "Function foo Not Return "
        self.assertTrue(TestChecker.test(input, expect, 479))


    def test_valid_ret_path_big(self):
        input="""int foo() {
            if(true)
            { 
            do{
                if(false) {return 0;}
                else {return 1;}
            }while(true);
            {{int i; for(i=1;i<5;i=i+1){return 5;}}}
            }
            else {return 12;}
        }
        void main() {foo();}"""
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 480))

    def test_another_valid_ret_path_big(self):
        input="""int foo() {
            if(true)
            { 
            do{
                if(false) {}
                else {}
            } while(true);
            {{int i; for(i=1;i<5;i=i+1){}}}
            }
            else {}
            return 42;
        }
        void main() {foo();}"""
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 481))

    def test_undeclared_built_in_func(self):
        input = """void main() {getInt();}"""
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 493))

    def test_undeclared_built_in_func_missing_param(self):
        input = """void main() {putIntLn();}"""
        expect = "Type Mismatch In Statement: CallExpr(Id(putIntLn),[])"
        self.assertTrue(TestChecker.test(input, expect, 482))

    def test_undeclared_block_in_body(self):
        input = """void main() {{x=1;}}"""
        expect = "Undeclared Identifier: x"
        self.assertTrue(TestChecker.test(input, expect, 483))

    def test_undeclared_body(self):
        input = """void main() {x=1;}"""
        expect = "Undeclared Identifier: x"
        self.assertTrue(TestChecker.test(input, expect, 484))

    def test_global_vars(self):
        input = """int a; float x; void main() {x=1;}"""
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 485))
    
    def test_global_func(self):
        input = """void main() {}"""
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 486))

    def test_global_decl_mixed(self):        
        input = """int a; void main() {float b;}"""
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 487))

    def test_global_redeclared_var(self):
        input = """int a; float a;"""
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input, expect, 488))

    def test_global_redeclared_func(self):
        input = """int foo() {return 1;} float foo(){return 1.2;}"""
        expect = "Redeclared Function: foo" 
        self.assertTrue(TestChecker.test(input, expect, 489))

    def test_global_redeclared_param(self):
        input = """int bar; void main() {int bar;}"""
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 490))

    def test_global_redeclared_mixed(self):
        input = """int bar; void bar() {}"""
        expect = "Redeclared Function: bar"
        self.assertTrue(TestChecker.test(input, expect, 491))

    def test_duplicate_param(self):
        input = """int foo(int a, float a) {return a;} void main() {foo();}"""
        expect = "Redeclared Parameter: a"
        self.assertTrue(TestChecker.test(input, expect, 492))
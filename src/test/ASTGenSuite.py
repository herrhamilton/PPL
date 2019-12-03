import unittest
from TestUtils import TestAST
from AST import *

class ASTGenSuite(unittest.TestCase):

    def test_random_comment(self):
        input = """int vietnam() {
            do{ enjoyDay/*HI I AM A COMMENT HEHEHEH
            */();} while(carrot[7011997] == asleep());
        }"""
        operation = BinaryOp("==", ArrayCell(Id("carrot"), IntLiteral(7011997)), CallExpr(Id("asleep"), []))
        body = Block([Dowhile([CallExpr(Id("enjoyDay"), [])], operation)])
        func = FuncDecl(Id("vietnam"), [], IntType(), body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,3332)) # TODO: Add comments?

    def test_simple_program(self):
        """Simple program: int main() {} """
        input = """int main() {}"""
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,300))

    def test_more_complex_program(self):
        """More complex program"""
        input = """int main () {
            putIntLn(4);
        }"""
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([CallExpr(Id("putIntLn"),[IntLiteral(4)])]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,301))
    
    def test_call_without_parameter(self):
        """Without parameter"""
        input = """int main () {
            getIntLn();
        }"""
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([CallExpr(Id("getIntLn"),[])]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,302))
   
    def test_arrpointer_func(self):
        """func with arr pointer types"""
        input = """float[] func(int a[], boolean b) {}"""
        params = [VarDecl("a", ArrayPointerType(IntType())), VarDecl("b", BoolType())]
        fun = FuncDecl(Id("func"), params, ArrayPointerType(FloatType()), Block([]))
        expect = str(Program([fun]))
        self.assertTrue(TestAST.checkASTGen(input, expect,303))
    
    def test_params(self):
        """With parameter"""
        input = """int main (float foo) {}"""
        expect = str(Program([FuncDecl(Id("main"),[ VarDecl("foo", FloatType())], IntType(), Block([]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect, 304))

    def test_var_decl(self):
        """global variable declaration"""
        input = """int a, b[5];
        float x;"""
        expect = str(Program([VarDecl("a",IntType()),VarDecl("b", ArrayType(5, IntType())),VarDecl("x",FloatType())]))

        self.assertTrue(TestAST.checkASTGen(input, expect, 305))

    def test_if(self):
        input = """int main() {
            if(true) { 
                putIntLn(4); 
            }
        }"""
        _if = If(BooleanLiteral("true"),Block([CallExpr(Id("putIntLn"), [IntLiteral(4)])]))
        func = FuncDecl(Id("main"),[], IntType(), Block([_if]))
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,306))

    def test_for_loop(self):
        input = """int main() {
            for(i=1; i<3; i=i+1) {
                putIntLn(4);
            }
        }"""

        exp1 = BinaryOp("=",Id("i"),IntLiteral(1))
        exp2 = BinaryOp("<",Id("i"),IntLiteral(3))
        exp3 = BinaryOp("=",Id("i"),BinaryOp("+",Id("i"),IntLiteral(1)))
        loop = Block([CallExpr(Id("putIntLn"),[IntLiteral(4)])])
        _for = For(exp1, exp2, exp3, loop)
        func = FuncDecl(Id("main"),[], IntType(), Block([_for]))
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,307))

    def test_do_while_loop(self):
        input = """int main() {
            int x;
            x=1;
            do {
                x = x+1;
            } while(x!=9);
        }"""
        st1 = VarDecl("x", IntType())
        st2 = BinaryOp("=",Id("x"),IntLiteral(1))
        doSt = BinaryOp("=",Id("x"),BinaryOp("+",Id("x"),IntLiteral(1)))
        expr = BinaryOp("!=",Id("x"), IntLiteral(9))
        dowhile = Dowhile([doSt], expr)
        func = FuncDecl(Id("main"),[], IntType(), Block([st1, st2,dowhile]))
        expect = str(Program([func]))
        
        self.assertTrue(TestAST.checkASTGen(input,expect,308))

    def test_local_var(self):
        input = """
        boolean myFunc() {
            int i;
            i=3;
        }"""
        st1 = VarDecl("i", IntType())
        st2 = BinaryOp("=",Id("i"),IntLiteral(3))
        func = FuncDecl(Id("myFunc"),[], BoolType(), Block([st1, st2]))
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,309))

    def test_more_func(self):
        input = """
        int main() {
            int i;
            i=3;
        }
        void foo() {}"""
        st1 = VarDecl("i", IntType())
        st2 = BinaryOp("=",Id("i"),IntLiteral(3))
        func1 = FuncDecl(Id("main"),[], IntType(), Block([st1, st2]))
        func2 = FuncDecl(Id("foo"),[], VoidType(), Block([]))

        expect = str(Program([func1, func2]))
        self.assertTrue(TestAST.checkASTGen(input,expect,310))

    def test_more_ifs(self):
        input = """
        int main() {
            if(x==5) {
                printLn("LEL");
                if(y < 42) {
                    i = 1;
                }
            }
            else { foo();
            }
        }"""
        
        outerElse = Block([CallExpr(Id("foo"), [])])
        innerIf = If(BinaryOp("<", Id("y"), IntLiteral(42)), Block([BinaryOp("=", Id("i"), IntLiteral(1))]))
        outerIf = If(BinaryOp("==", Id("x"), IntLiteral(5)),Block([CallExpr(Id("printLn"), [StringLiteral("LEL")]), innerIf]), outerElse)
        func = FuncDecl(Id("main"),[], IntType(), Block([outerIf]))
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,312))

    def test_empty_file(self):
        input = ""
        expect = str(Program([]))
        self.assertTrue(TestAST.checkASTGen(input,expect,313))

    def test_only_var_dec(self):
        input = "int xy;"
        expect = str(Program([VarDecl("xy", IntType())]))
        self.assertTrue(TestAST.checkASTGen(input,expect,314))

    def test_return_statement(self):
        input = """float circumfence(float radius, boolean metric) {
            return x;
        }"""
        body = [Return(Id("x"))]
        params = [VarDecl("radius", FloatType()), VarDecl("metric", BoolType())]
        expect = str(Program([FuncDecl(Id("circumfence"), params, FloatType(), Block(body))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,315))

    def test_nested_statement(self):
        input = """int rand() {
            return foo()+b;
        }"""
        retSt = Return(BinaryOp("+", CallExpr(Id("foo"),[]), Id("b")))
        func = FuncDecl(Id("rand"), [], IntType(), Block([retSt]))
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,316)) 

    def test_var_with_arr_size(self):
        input = """int rand() {
            string a[2];
        }"""
        body = Block([VarDecl("a", ArrayType(2,StringType()))])
        func = FuncDecl(Id("rand"), [], IntType(),body)
        expect = str(Program([func]))

        self.assertTrue(TestAST.checkASTGen(input,expect,317))

    def test_var_list(self):
        input = """int rand() {
            string a[2], b, TragedyOfDarthPlagueisTheWise;
        }"""
        body = Block([VarDecl("a", ArrayType(2,StringType())), VarDecl("b", StringType()), VarDecl("TragedyOfDarthPlagueisTheWise", StringType())])
        func = FuncDecl(Id("rand"), [], IntType(),body)
        expect = str(Program([func]))

        self.assertTrue(TestAST.checkASTGen(input,expect,318))

    def test_funccall_separator(self):
        input = """int cheesy() {
            edamer(4, 5);
        }"""
        body = Block([CallExpr(Id("edamer"), [IntLiteral(4), IntLiteral(5)])])
        func = FuncDecl(Id("cheesy"), [], IntType(),body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,319))

    def test_exp3(self):
        input = """int cheesy() {
            x = (a*5)/(4-(88.7%3));
        }"""
        inner = BinaryOp("%", FloatLiteral(88.7), IntLiteral(3))
        right = BinaryOp("-", IntLiteral(4), inner)
        left = BinaryOp("*", Id("a"), IntLiteral(5))
        body = Block([BinaryOp("=", Id("x"), BinaryOp("/", left, right))])
        func = FuncDecl(Id("cheesy"), [], IntType(),body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,320))

    def test_exp4(self):
        input = """void cheesy(boolean bee) {
            a = a || b;
        }"""
        body = Block([BinaryOp("=", Id("a"), BinaryOp("||", Id("a"), Id("b")))])
        func = FuncDecl(Id("cheesy"), [VarDecl("bee", BoolType())], VoidType(),body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,321))

    def test_exp5(self):
        input = """int cheesy() {
            if(false) { pilot = 4%3;}
        }"""
        body = Block([If(BooleanLiteral("false"), Block([BinaryOp("=", Id("pilot"), BinaryOp("%", IntLiteral(4), IntLiteral(3)))]))])
        func = FuncDecl(Id("cheesy"), [], IntType(),body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,322))

    def test_exp7(self):
        input = """int cheesy() {
            a = foo (bar(42)  / t);
        }"""
        body = Block([BinaryOp("=", Id("a"), CallExpr(Id("foo"), [BinaryOp("/", CallExpr(Id("bar"), [IntLiteral(42)]),Id("t") )]))])
        func = FuncDecl(Id("cheesy"), [], IntType(),body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,323))

    def test_exp8(self):
        input = """int cheesy() {
            do { loopForeverLol();} while(1.2 != 5); 
        }"""
        exp = BinaryOp("!=", FloatLiteral(1.2), IntLiteral(5))
        stList = [CallExpr(Id("loopForeverLol"), [])]
        do = Dowhile(stList, exp)
        body = Block([do])
        func = FuncDecl(Id("cheesy"), [], IntType(),body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,324))

    def test_exp_index(self):
        input = """int cheesy() {
            music = nice[stuff()];
        }"""
        body = Block([BinaryOp("=", Id("music"), ArrayCell(Id("nice"),CallExpr(Id("stuff"), [])))])
        func = FuncDecl(Id("cheesy"), [], IntType(),body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,325))

    def test_nested_exp(self):
        input = """int vietnam() {
            do{ enjoyDay();} while(carrot[7011997] == asleep());
        }"""

        operation = BinaryOp("==", ArrayCell(Id("carrot"), IntLiteral(7011997)), CallExpr(Id("asleep"), []))
        body = Block([Dowhile([CallExpr(Id("enjoyDay"), [])], operation)])
        func = FuncDecl(Id("vietnam"), [], IntType(), body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,326))


    def test_pizza(self):
        input = """int cheesy() {
            do{ keepProgramming(a+b, xy, faster());} while(pizza != delivered);
        }"""
        param3 = CallExpr(Id("faster"), [])
        param2 = Id("xy")
        param1 = BinaryOp("+", Id("a"), Id("b"))
        body = Block([Dowhile([CallExpr(Id("keepProgramming"), [param1, param2, param3])], BinaryOp("!=", Id("pizza"), Id("delivered")))])
        func = FuncDecl(Id("cheesy"), [], IntType(), body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,327))

    def test_arg_with_index(self):
        input = """int cheesy() {
            cheesy(what[2]);
        }"""
        body = Block([CallExpr(Id("cheesy"), [ArrayCell(Id("what"), IntLiteral(2))])])
        expect = str(Program([FuncDecl(Id("cheesy"), [], IntType(), body)]))
        self.assertTrue(TestAST.checkASTGen(input,expect,328))

    def test_ret_without_exp(self):
        input = """int cheesy() {
            return;
        }"""
        body = Block([Return()])
        expect = str(Program([FuncDecl(Id("cheesy"), [], IntType(), body)]))
        self.assertTrue(TestAST.checkASTGen(input,expect,329))

    def test_ISTHISTHEREALLIFE(self):
        input = """int reallife() {
            if(this == reallife) {
                return 0;
            } else {
                return fantasy();
            }
        }"""
        elsee = Block([Return(CallExpr(Id("fantasy"), []))])
        thenn = Block([Return(IntLiteral(0))])
        if_st = If(BinaryOp("==", Id("this"), Id("reallife")), thenn, elsee)
        body = Block([if_st])
        func = FuncDecl(Id("reallife"), [], IntType(), body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,330))

    def test_asdf(self):
        input = """int cheesy() {
            string str;
            str = "ASDF";
        }"""
        body = Block([VarDecl("str", StringType()), BinaryOp("=", Id("str"), StringLiteral("ASDF"))])
        func = FuncDecl(Id("cheesy"), [], IntType(), body)
        expect = str(Program([func]))

        self.assertTrue(TestAST.checkASTGen(input,expect,331))

    def test_bmi(self):
        input = """float bmi(float thicc, float smol) {
            return thicc / (smol*smol);
        }"""
        body = Block([Return(BinaryOp("/", Id("thicc"), BinaryOp("*", Id("smol"), Id("smol"))))])
        func = FuncDecl(Id("bmi"), [VarDecl("thicc", FloatType()), VarDecl("smol", FloatType())], FloatType(), body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,333))

    def test_nested_if(self):
        input = """int cheesy() {
            do{
                if(i<25){
                    nothing();
                } else {
                    if(i<30) {
                        aLittle(bit());
                    } else {
                        everything(a[123]);
                    }
                }
                i = i+1;
            } while (i < 100);
        }"""
        asst = BinaryOp("=", Id("i"), BinaryOp("+", Id("i"), IntLiteral(1)))
        els = Block([CallExpr(Id("everything"), [ArrayCell(Id("a"), IntLiteral(123))])])        
        the = Block([CallExpr(Id("aLittle"), [CallExpr(Id("bit"), [])])])
        scndif= If(BinaryOp("<", Id("i"), IntLiteral(30)), the, els)
        elsee = Block([scndif])
        thenn = Block([CallExpr(Id("nothing"), [])])
        ifst = If(BinaryOp("<", Id("i"), IntLiteral(25)),thenn, elsee)
        dow = Dowhile([ifst, asst], BinaryOp("<", Id("i"), IntLiteral(100)))
        body = Block([dow])
        func = FuncDecl(Id("cheesy"), [], IntType(), body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,334))

    def test_nested_loops(self):
        input = """int cheesy() {
            for(i=1; i<5;i=i+1) {
                do{allthatcoolstuff();} while(i<3);
            }
        }"""
        dol = Dowhile([CallExpr(Id("allthatcoolstuff"), [])], BinaryOp("<", Id("i"), IntLiteral(3)))
        forl = For(BinaryOp("=", Id("i"), IntLiteral(1)), BinaryOp("<", Id("i"), IntLiteral(5)), BinaryOp("=", Id("i"), BinaryOp("+",Id("i"), IntLiteral(1))),Block([dol]))
        func = FuncDecl(Id("cheesy"), [], IntType(), Block([forl]))
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,335))
      
    def test_program(self):
        input = """float x; int main(){} int snd(){} boolean b;"""  
        expect = str(Program([VarDecl("x", FloatType()), FuncDecl(Id("main"), [], IntType(), Block([])),FuncDecl(Id("snd"), [], IntType(), Block([])),VarDecl("b", BoolType())]))
        
        self.assertTrue(TestAST.checkASTGen(input, expect, 336))

    def test_func_param(self):
        input = """float x; int main(string x){} int snd(){} boolean b;"""  
        expect = str(Program([VarDecl("x", FloatType()), FuncDecl(Id("main"), [VarDecl("x", StringType())], IntType(), Block([])),FuncDecl(Id("snd"), [], IntType(), Block([])),VarDecl("b", BoolType())]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 337))

    def test_break_continue(self):
        input = """int vietnam() {
            do{ if(i<25){break;} enjoyDay();} while(carrot[7011997] == asleep());
        }"""

        operation = BinaryOp("==", ArrayCell(Id("carrot"), IntLiteral(7011997)), CallExpr(Id("asleep"), []))
        body = Block([Dowhile([If(BinaryOp("<", Id("i"), IntLiteral(25)),Block([Break()])), CallExpr(Id("enjoyDay"), [])], operation)])
        func = FuncDecl(Id("vietnam"), [], IntType(), body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,338))

    def test_bmi(self):
        input = """float bmi(float thicc, float smol) {
            bmi(75.0, 150.0);
        }"""
        body = Block([CallExpr(Id("bmi"), [FloatLiteral(75.0), FloatLiteral(150.0)])])
        func = FuncDecl(Id("bmi"), [VarDecl("thicc", FloatType()), VarDecl("smol", FloatType())], FloatType(), body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,339))

    def test_eval_order1(self):
        input = "int main() {a = 5 + 30.5 / 20}"
        block = BinaryOp("=", Id("a"), BinaryOp("+", IntLiteral(5), BinaryOp("/", FloatLiteral(30.5), IntLiteral(20))))
        fun = FuncDecl(Id("main"), [], IntType(), Block([block]))
        expect = str(Program([fun]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 340))

    def test_eval_order2(self):
        input = "int main() {a = 30.5 / 20 + 5}"
        body = Block([BinaryOp("=", Id("a"), BinaryOp("+", BinaryOp("/", FloatLiteral(30.5), IntLiteral(20)), IntLiteral(5)))])
        fun = FuncDecl(Id("main"), [], IntType(), body)
        expect = str(Program([fun]))

        self.assertTrue(TestAST.checkASTGen(input, expect, 332))

    def test_example_code_MC(self):
        input = """int i ;
        int f ( ) {
            return 200;
        }
        void main ( ) {
            int main ;
            main = f ( ) ;
            putIntLn ( main ) ;
            {
                int i ;
                int main ;
                int f ;
                main = f = i = 100;
                putIntLn ( i ) ;
                putIntLn ( main ) ;
                putIntLn ( f ) ;
            }
            putIntLn ( main ) ;
        }"""
        outerDecls = [VarDecl("main", IntType()), BinaryOp("=", Id("main"), CallExpr(Id("f"), [])), CallExpr(Id("putIntLn"), [Id("main")])]
        calls = [CallExpr(Id("putIntLn"), [Id("i")]),CallExpr(Id("putIntLn"), [Id("main")]),CallExpr(Id("putIntLn"), [Id("f")])]
        mdecl = BinaryOp("=", Id("main"), BinaryOp("=", Id("f"), BinaryOp("=", Id("i"), IntLiteral(100))))
        decls = [VarDecl("i", IntType()), VarDecl("main", IntType()), VarDecl("f", IntType())]
        body = Block(outerDecls +  [Block(decls + [mdecl] + calls)] + [CallExpr(Id("putIntLn"), [Id("main")])])
        f2 = FuncDecl(Id("main"), [], VoidType(), body)
        f1 = FuncDecl(Id("f"), [], IntType(), Block([Return(IntLiteral(200))]))
        dec = VarDecl("i", IntType())
        expect = str(Program([dec, f1, f2]))
        self.assertTrue(TestAST.checkASTGen(input,expect,399))

    def test_random_commenta(self):
        input = """int vietnam() {
            do{ enjoyDay/*HI I AM A COMMENT HEHEHEH
            */();} while(carrot[7011997] == asleep());
        }"""
        operation = BinaryOp("==", ArrayCell(Id("carrot"), IntLiteral(7011997)), CallExpr(Id("asleep"), []))
        body = Block([Dowhile([CallExpr(Id("enjoyDay"), [])], operation)])
        func = FuncDecl(Id("vietnam"), [], IntType(), body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,4332)) # TODO: Add comments?

    def test_simple_programa(self):
        """Simple program: int main() {} """
        input = """int main() {}"""
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,400))

    def test_more_complex_programa(self):
        """More complex program"""
        input = """int main () {
            putIntLn(4);
        }"""
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([CallExpr(Id("putIntLn"),[IntLiteral(4)])]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,401))
    
    def test_call_without_parametera(self):
        """Without parameter"""
        input = """int main () {
            getIntLn();
        }"""
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([CallExpr(Id("getIntLn"),[])]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,402))
   
    def test_arrpointer_funca(self):
        """func with arr pointer types"""
        input = """float[] func(int a[], boolean b) {}"""
        params = [VarDecl("a", ArrayPointerType(IntType())), VarDecl("b", BoolType())]
        fun = FuncDecl(Id("func"), params, ArrayPointerType(FloatType()), Block([]))
        expect = str(Program([fun]))
        self.assertTrue(TestAST.checkASTGen(input, expect,403))
    
    def test_paramsa(self):
        """With parameter"""
        input = """int main (float foo) {}"""
        expect = str(Program([FuncDecl(Id("main"),[ VarDecl("foo", FloatType())], IntType(), Block([]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect, 304))

    def test_var_decla(self):
        """global variable declaration"""
        input = """int a, b[5];
        float x;"""
        expect = str(Program([VarDecl("a",IntType()),VarDecl("b", ArrayType(5, IntType())),VarDecl("x",FloatType())]))

        self.assertTrue(TestAST.checkASTGen(input, expect, 305))

    def test_ifa(self):
        input = """int main() {
            if(true) { 
                putIntLn(4); 
            }
        }"""
        _if = If(BooleanLiteral("true"),Block([CallExpr(Id("putIntLn"), [IntLiteral(4)])]))
        func = FuncDecl(Id("main"),[], IntType(), Block([_if]))
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,406))

    def test_for_loopa(self):
        input = """int main() {
            for(i=1; i<3; i=i+1) {
                putIntLn(4);
            }
        }"""

        exp1 = BinaryOp("=",Id("i"),IntLiteral(1))
        exp2 = BinaryOp("<",Id("i"),IntLiteral(3))
        exp3 = BinaryOp("=",Id("i"),BinaryOp("+",Id("i"),IntLiteral(1)))
        loop = Block([CallExpr(Id("putIntLn"),[IntLiteral(4)])])
        _for = For(exp1, exp2, exp3, loop)
        func = FuncDecl(Id("main"),[], IntType(), Block([_for]))
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,407))

    def test_do_while_loopa(self):
        input = """int main() {
            int x;
            x=1;
            do {
                x = x+1;
            } while(x!=9);
        }"""
        st1 = VarDecl("x", IntType())
        st2 = BinaryOp("=",Id("x"),IntLiteral(1))
        doSt = BinaryOp("=",Id("x"),BinaryOp("+",Id("x"),IntLiteral(1)))
        expr = BinaryOp("!=",Id("x"), IntLiteral(9))
        dowhile = Dowhile([doSt], expr)
        func = FuncDecl(Id("main"),[], IntType(), Block([st1, st2,dowhile]))
        expect = str(Program([func]))
        
        self.assertTrue(TestAST.checkASTGen(input,expect,408))

    def test_local_vara(self):
        input = """
        boolean myFunc() {
            int i;
            i=3;
        }"""
        st1 = VarDecl("i", IntType())
        st2 = BinaryOp("=",Id("i"),IntLiteral(3))
        func = FuncDecl(Id("myFunc"),[], BoolType(), Block([st1, st2]))
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,409))

    def test_more_funca(self):
        input = """
        int main() {
            int i;
            i=3;
        }
        void foo() {}"""
        st1 = VarDecl("i", IntType())
        st2 = BinaryOp("=",Id("i"),IntLiteral(3))
        func1 = FuncDecl(Id("main"),[], IntType(), Block([st1, st2]))
        func2 = FuncDecl(Id("foo"),[], VoidType(), Block([]))

        expect = str(Program([func1, func2]))
        self.assertTrue(TestAST.checkASTGen(input,expect,410))

    def test_more_ifsa(self):
        input = """
        int main() {
            if(x==5) {
                printLn("LEL");
                if(y < 42) {
                    i = 1;
                }
            }
            else { foo();
            }
        }"""
        
        outerElse = Block([CallExpr(Id("foo"), [])])
        innerIf = If(BinaryOp("<", Id("y"), IntLiteral(42)), Block([BinaryOp("=", Id("i"), IntLiteral(1))]))
        outerIf = If(BinaryOp("==", Id("x"), IntLiteral(5)),Block([CallExpr(Id("printLn"), [StringLiteral("LEL")]), innerIf]), outerElse)
        func = FuncDecl(Id("main"),[], IntType(), Block([outerIf]))
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,412))

    def test_empty_filea(self):
        input = ""
        expect = str(Program([]))
        self.assertTrue(TestAST.checkASTGen(input,expect,413))

    def test_only_var_deca(self):
        input = "int xy;"
        expect = str(Program([VarDecl("xy", IntType())]))
        self.assertTrue(TestAST.checkASTGen(input,expect,414))

    def test_return_statementa(self):
        input = """float circumfence(float radius, boolean metric) {
            return x;
        }"""
        body = [Return(Id("x"))]
        params = [VarDecl("radius", FloatType()), VarDecl("metric", BoolType())]
        expect = str(Program([FuncDecl(Id("circumfence"), params, FloatType(), Block(body))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,415))

    def test_nested_statementa(self):
        input = """int rand() {
            return foo()+b;
        }"""
        retSt = Return(BinaryOp("+", CallExpr(Id("foo"),[]), Id("b")))
        func = FuncDecl(Id("rand"), [], IntType(), Block([retSt]))
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,416)) 

    def test_var_with_arr_sizea(self):
        input = """int rand() {
            string a[2];
        }"""
        body = Block([VarDecl("a", ArrayType(2,StringType()))])
        func = FuncDecl(Id("rand"), [], IntType(),body)
        expect = str(Program([func]))

        self.assertTrue(TestAST.checkASTGen(input,expect,417))

    def test_var_lista(self):
        input = """int rand() {
            string a[2], b, TragedyOfDarthPlagueisTheWise;
        }"""
        body = Block([VarDecl("a", ArrayType(2,StringType())), VarDecl("b", StringType()), VarDecl("TragedyOfDarthPlagueisTheWise", StringType())])
        func = FuncDecl(Id("rand"), [], IntType(),body)
        expect = str(Program([func]))

        self.assertTrue(TestAST.checkASTGen(input,expect,418))

    def test_funccall_separatora(self):
        input = """int cheesy() {
            edamer(4, 5);
        }"""
        body = Block([CallExpr(Id("edamer"), [IntLiteral(4), IntLiteral(5)])])
        func = FuncDecl(Id("cheesy"), [], IntType(),body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,419))

    def test_exp3a(self):
        input = """int cheesy() {
            x = (a*5)/(4-(88.7%3));
        }"""
        inner = BinaryOp("%", FloatLiteral(88.7), IntLiteral(3))
        right = BinaryOp("-", IntLiteral(4), inner)
        left = BinaryOp("*", Id("a"), IntLiteral(5))
        body = Block([BinaryOp("=", Id("x"), BinaryOp("/", left, right))])
        func = FuncDecl(Id("cheesy"), [], IntType(),body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,420))

    def test_exp4a(self):
        input = """void cheesy(boolean bee) {
            a = a || b;
        }"""
        body = Block([BinaryOp("=", Id("a"), BinaryOp("||", Id("a"), Id("b")))])
        func = FuncDecl(Id("cheesy"), [VarDecl("bee", BoolType())], VoidType(),body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,421))

    def test_exp5a(self):
        input = """int cheesy() {
            if(false) { pilot = 4%3;}
        }"""
        body = Block([If(BooleanLiteral("false"), Block([BinaryOp("=", Id("pilot"), BinaryOp("%", IntLiteral(4), IntLiteral(3)))]))])
        func = FuncDecl(Id("cheesy"), [], IntType(),body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,422))

    def test_exp7a(self):
        input = """int cheesy() {
            a = foo (bar(42)  / t);
        }"""
        body = Block([BinaryOp("=", Id("a"), CallExpr(Id("foo"), [BinaryOp("/", CallExpr(Id("bar"), [IntLiteral(42)]),Id("t") )]))])
        func = FuncDecl(Id("cheesy"), [], IntType(),body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,423))

    def test_exp8a(self):
        input = """int cheesy() {
            do { loopForeverLol();} while(1.2 != 5); 
        }"""
        exp = BinaryOp("!=", FloatLiteral(1.2), IntLiteral(5))
        stList = [CallExpr(Id("loopForeverLol"), [])]
        do = Dowhile(stList, exp)
        body = Block([do])
        func = FuncDecl(Id("cheesy"), [], IntType(),body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,424))

    def test_exp_indexa(self):
        input = """int cheesy() {
            music = nice[stuff()];
        }"""
        body = Block([BinaryOp("=", Id("music"), ArrayCell(Id("nice"),CallExpr(Id("stuff"), [])))])
        func = FuncDecl(Id("cheesy"), [], IntType(),body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,425))

    def test_nested_expa(self):
        input = """int vietnam() {
            do{ enjoyDay();} while(carrot[7011997] == asleep());
        }"""

        operation = BinaryOp("==", ArrayCell(Id("carrot"), IntLiteral(7011997)), CallExpr(Id("asleep"), []))
        body = Block([Dowhile([CallExpr(Id("enjoyDay"), [])], operation)])
        func = FuncDecl(Id("vietnam"), [], IntType(), body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,426))


    def test_pizzaa(self):
        input = """int cheesy() {
            do{ keepProgramming(a+b, xy, faster());} while(pizza != delivered);
        }"""
        param3 = CallExpr(Id("faster"), [])
        param2 = Id("xy")
        param1 = BinaryOp("+", Id("a"), Id("b"))
        body = Block([Dowhile([CallExpr(Id("keepProgramming"), [param1, param2, param3])], BinaryOp("!=", Id("pizza"), Id("delivered")))])
        func = FuncDecl(Id("cheesy"), [], IntType(), body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,427))

    def test_arg_with_indexa(self):
        input = """int cheesy() {
            cheesy(what[2]);
        }"""
        body = Block([CallExpr(Id("cheesy"), [ArrayCell(Id("what"), IntLiteral(2))])])
        expect = str(Program([FuncDecl(Id("cheesy"), [], IntType(), body)]))
        self.assertTrue(TestAST.checkASTGen(input,expect,428))

    def test_ret_without_expa(self):
        input = """int cheesy() {
            return;
        }"""
        body = Block([Return()])
        expect = str(Program([FuncDecl(Id("cheesy"), [], IntType(), body)]))
        self.assertTrue(TestAST.checkASTGen(input,expect,429))

    def test_ISTHISTHEREALLIFEa(self):
        input = """int reallife() {
            if(this == reallife) {
                return 0;
            } else {
                return fantasy();
            }
        }"""
        elsee = Block([Return(CallExpr(Id("fantasy"), []))])
        thenn = Block([Return(IntLiteral(0))])
        if_st = If(BinaryOp("==", Id("this"), Id("reallife")), thenn, elsee)
        body = Block([if_st])
        func = FuncDecl(Id("reallife"), [], IntType(), body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,430))

    def test_asdfa(self):
        input = """int cheesy() {
            string str;
            str = "ASDF";
        }"""
        body = Block([VarDecl("str", StringType()), BinaryOp("=", Id("str"), StringLiteral("ASDF"))])
        func = FuncDecl(Id("cheesy"), [], IntType(), body)
        expect = str(Program([func]))

        self.assertTrue(TestAST.checkASTGen(input,expect,431))

    def test_bmia(self):
        input = """float bmi(float thicc, float smol) {
            return thicc / (smol*smol);
        }"""
        body = Block([Return(BinaryOp("/", Id("thicc"), BinaryOp("*", Id("smol"), Id("smol"))))])
        func = FuncDecl(Id("bmi"), [VarDecl("thicc", FloatType()), VarDecl("smol", FloatType())], FloatType(), body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,433))

    def test_nested_ifa(self):
        input = """int cheesy() {
            do{
                if(i<25){
                    nothing();
                } else {
                    if(i<30) {
                        aLittle(bit());
                    } else {
                        everything(a[123]);
                    }
                }
                i = i+1;
            } while (i < 100);
        }"""
        asst = BinaryOp("=", Id("i"), BinaryOp("+", Id("i"), IntLiteral(1)))
        els = Block([CallExpr(Id("everything"), [ArrayCell(Id("a"), IntLiteral(123))])])        
        the = Block([CallExpr(Id("aLittle"), [CallExpr(Id("bit"), [])])])
        scndif= If(BinaryOp("<", Id("i"), IntLiteral(30)), the, els)
        elsee = Block([scndif])
        thenn = Block([CallExpr(Id("nothing"), [])])
        ifst = If(BinaryOp("<", Id("i"), IntLiteral(25)),thenn, elsee)
        dow = Dowhile([ifst, asst], BinaryOp("<", Id("i"), IntLiteral(100)))
        body = Block([dow])
        func = FuncDecl(Id("cheesy"), [], IntType(), body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,434))

    def test_nested_loopsa(self):
        input = """int cheesy() {
            for(i=1; i<5;i=i+1) {
                do{allthatcoolstuff();} while(i<3);
            }
        }"""
        dol = Dowhile([CallExpr(Id("allthatcoolstuff"), [])], BinaryOp("<", Id("i"), IntLiteral(3)))
        forl = For(BinaryOp("=", Id("i"), IntLiteral(1)), BinaryOp("<", Id("i"), IntLiteral(5)), BinaryOp("=", Id("i"), BinaryOp("+",Id("i"), IntLiteral(1))),Block([dol]))
        func = FuncDecl(Id("cheesy"), [], IntType(), Block([forl]))
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,435))
      
    def test_programa(self):
        input = """float x; int main(){} int snd(){} boolean b;"""  
        expect = str(Program([VarDecl("x", FloatType()), FuncDecl(Id("main"), [], IntType(), Block([])),FuncDecl(Id("snd"), [], IntType(), Block([])),VarDecl("b", BoolType())]))
        
        self.assertTrue(TestAST.checkASTGen(input, expect, 336))

    def test_func_parama(self):
        input = """float x; int main(string x){} int snd(){} boolean b;"""  
        expect = str(Program([VarDecl("x", FloatType()), FuncDecl(Id("main"), [VarDecl("x", StringType())], IntType(), Block([])),FuncDecl(Id("snd"), [], IntType(), Block([])),VarDecl("b", BoolType())]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 337))

    def test_break_continuea(self):
        input = """int vietnam() {
            do{ if(i<25){break;} enjoyDay();} while(carrot[7011997] == asleep());
        }"""

        operation = BinaryOp("==", ArrayCell(Id("carrot"), IntLiteral(7011997)), CallExpr(Id("asleep"), []))
        body = Block([Dowhile([If(BinaryOp("<", Id("i"), IntLiteral(25)),Block([Break()])), CallExpr(Id("enjoyDay"), [])], operation)])
        func = FuncDecl(Id("vietnam"), [], IntType(), body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,438))

    def test_bmia(self):
        input = """float bmi(float thicc, float smol) {
            bmi(75.0, 150.0);
        }"""
        body = Block([CallExpr(Id("bmi"), [FloatLiteral(75.0), FloatLiteral(150.0)])])
        func = FuncDecl(Id("bmi"), [VarDecl("thicc", FloatType()), VarDecl("smol", FloatType())], FloatType(), body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,439))

    def test_eval_order1a(self):
        input = "int main() {a = 5 + 30.5 / 20}"
        block = BinaryOp("=", Id("a"), BinaryOp("+", IntLiteral(5), BinaryOp("/", FloatLiteral(30.5), IntLiteral(20))))
        fun = FuncDecl(Id("main"), [], IntType(), Block([block]))
        expect = str(Program([fun]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 340))

    def test_eval_order2a(self):
        input = "int main() {a = 30.5 / 20 + 5}"
        body = Block([BinaryOp("=", Id("a"), BinaryOp("+", BinaryOp("/", FloatLiteral(30.5), IntLiteral(20)), IntLiteral(5)))])
        fun = FuncDecl(Id("main"), [], IntType(), body)
        expect = str(Program([fun]))

        self.assertTrue(TestAST.checkASTGen(input, expect, 332))

    def test_example_code_MCa(self):
        input = """int i ;
        int f ( ) {
            return 200;
        }
        void main ( ) {
            int main ;
            main = f ( ) ;
            putIntLn ( main ) ;
            {
                int i ;
                int main ;
                int f ;
                main = f = i = 100;
                putIntLn ( i ) ;
                putIntLn ( main ) ;
                putIntLn ( f ) ;
            }
            putIntLn ( main ) ;
        }"""
        outerDecls = [VarDecl("main", IntType()), BinaryOp("=", Id("main"), CallExpr(Id("f"), [])), CallExpr(Id("putIntLn"), [Id("main")])]
        calls = [CallExpr(Id("putIntLn"), [Id("i")]),CallExpr(Id("putIntLn"), [Id("main")]),CallExpr(Id("putIntLn"), [Id("f")])]
        mdecl = BinaryOp("=", Id("main"), BinaryOp("=", Id("f"), BinaryOp("=", Id("i"), IntLiteral(100))))
        decls = [VarDecl("i", IntType()), VarDecl("main", IntType()), VarDecl("f", IntType())]
        body = Block(outerDecls +  [Block(decls + [mdecl] + calls)] + [CallExpr(Id("putIntLn"), [Id("main")])])
        f2 = FuncDecl(Id("main"), [], VoidType(), body)
        f1 = FuncDecl(Id("f"), [], IntType(), Block([Return(IntLiteral(200))]))
        dec = VarDecl("i", IntType())
        expect = str(Program([dec, f1, f2]))
        self.assertTrue(TestAST.checkASTGen(input,expect,499))

        
    def test_random_commentb(self):
        input = """int vietnam() {
            do{ enjoyDay/*HI I AM A COMMENT HEHEHEH
            */();} while(carrot[7011997] == asleep());
        }"""
        operation = BinaryOp("==", ArrayCell(Id("carrot"), IntLiteral(7011997)), CallExpr(Id("asleep"), []))
        body = Block([Dowhile([CallExpr(Id("enjoyDay"), [])], operation)])
        func = FuncDecl(Id("vietnam"), [], IntType(), body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,5332)) # TODO: Add comments?

    def test_simple_programb(self):
        """Simple program: int main() {} """
        input = """int main() {}"""
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,500))

    def test_more_complex_programb(self):
        """More complex program"""
        input = """int main () {
            putIntLn(4);
        }"""
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([CallExpr(Id("putIntLn"),[IntLiteral(4)])]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,501))
    
    def test_call_without_parameterb(self):
        """Without parameter"""
        input = """int main () {
            getIntLn();
        }"""
        expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([CallExpr(Id("getIntLn"),[])]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,502))
   
    def test_arrpointer_funcb(self):
        """func with arr pointer types"""
        input = """float[] func(int a[], boolean b) {}"""
        params = [VarDecl("a", ArrayPointerType(IntType())), VarDecl("b", BoolType())]
        fun = FuncDecl(Id("func"), params, ArrayPointerType(FloatType()), Block([]))
        expect = str(Program([fun]))
        self.assertTrue(TestAST.checkASTGen(input, expect,503))
    
    def test_paramsb(self):
        """With parameter"""
        input = """int main (float foo) {}"""
        expect = str(Program([FuncDecl(Id("main"),[ VarDecl("foo", FloatType())], IntType(), Block([]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect, 304))

    def test_var_declb(self):
        """global variable declaration"""
        input = """int a, b[5];
        float x;"""
        expect = str(Program([VarDecl("a",IntType()),VarDecl("b", ArrayType(5, IntType())),VarDecl("x",FloatType())]))

        self.assertTrue(TestAST.checkASTGen(input, expect, 305))

    def test_ifb(self):
        input = """int main() {
            if(true) { 
                putIntLn(4); 
            }
        }"""
        _if = If(BooleanLiteral("true"),Block([CallExpr(Id("putIntLn"), [IntLiteral(4)])]))
        func = FuncDecl(Id("main"),[], IntType(), Block([_if]))
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,506))

    def test_for_loopb(self):
        input = """int main() {
            for(i=1; i<3; i=i+1) {
                putIntLn(4);
            }
        }"""

        exp1 = BinaryOp("=",Id("i"),IntLiteral(1))
        exp2 = BinaryOp("<",Id("i"),IntLiteral(3))
        exp3 = BinaryOp("=",Id("i"),BinaryOp("+",Id("i"),IntLiteral(1)))
        loop = Block([CallExpr(Id("putIntLn"),[IntLiteral(4)])])
        _for = For(exp1, exp2, exp3, loop)
        func = FuncDecl(Id("main"),[], IntType(), Block([_for]))
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,507))

    def test_do_while_loopb(self):
        input = """int main() {
            int x;
            x=1;
            do {
                x = x+1;
            } while(x!=9);
        }"""
        st1 = VarDecl("x", IntType())
        st2 = BinaryOp("=",Id("x"),IntLiteral(1))
        doSt = BinaryOp("=",Id("x"),BinaryOp("+",Id("x"),IntLiteral(1)))
        expr = BinaryOp("!=",Id("x"), IntLiteral(9))
        dowhile = Dowhile([doSt], expr)
        func = FuncDecl(Id("main"),[], IntType(), Block([st1, st2,dowhile]))
        expect = str(Program([func]))
        
        self.assertTrue(TestAST.checkASTGen(input,expect,508))

    def test_local_varb(self):
        input = """
        boolean myFunc() {
            int i;
            i=3;
        }"""
        st1 = VarDecl("i", IntType())
        st2 = BinaryOp("=",Id("i"),IntLiteral(3))
        func = FuncDecl(Id("myFunc"),[], BoolType(), Block([st1, st2]))
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,509))

    def test_more_funcb(self):
        input = """
        int main() {
            int i;
            i=3;
        }
        void foo() {}"""
        st1 = VarDecl("i", IntType())
        st2 = BinaryOp("=",Id("i"),IntLiteral(3))
        func1 = FuncDecl(Id("main"),[], IntType(), Block([st1, st2]))
        func2 = FuncDecl(Id("foo"),[], VoidType(), Block([]))

        expect = str(Program([func1, func2]))
        self.assertTrue(TestAST.checkASTGen(input,expect,510))

    def test_more_ifsb(self):
        input = """
        int main() {
            if(x==5) {
                printLn("LEL");
                if(y < 42) {
                    i = 1;
                }
            }
            else { foo();
            }
        }"""
        
        outerElse = Block([CallExpr(Id("foo"), [])])
        innerIf = If(BinaryOp("<", Id("y"), IntLiteral(42)), Block([BinaryOp("=", Id("i"), IntLiteral(1))]))
        outerIf = If(BinaryOp("==", Id("x"), IntLiteral(5)),Block([CallExpr(Id("printLn"), [StringLiteral("LEL")]), innerIf]), outerElse)
        func = FuncDecl(Id("main"),[], IntType(), Block([outerIf]))
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,512))

    def test_empty_fileb(self):
        input = ""
        expect = str(Program([]))
        self.assertTrue(TestAST.checkASTGen(input,expect,513))

    def test_only_var_decb(self):
        input = "int xy;"
        expect = str(Program([VarDecl("xy", IntType())]))
        self.assertTrue(TestAST.checkASTGen(input,expect,514))

    def test_return_statementb(self):
        input = """float circumfence(float radius, boolean metric) {
            return x;
        }"""
        body = [Return(Id("x"))]
        params = [VarDecl("radius", FloatType()), VarDecl("metric", BoolType())]
        expect = str(Program([FuncDecl(Id("circumfence"), params, FloatType(), Block(body))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,515))

    def test_nested_statementb(self):
        input = """int rand() {
            return foo()+b;
        }"""
        retSt = Return(BinaryOp("+", CallExpr(Id("foo"),[]), Id("b")))
        func = FuncDecl(Id("rand"), [], IntType(), Block([retSt]))
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,516)) 

    def test_var_with_arr_sizeb(self):
        input = """int rand() {
            string a[2];
        }"""
        body = Block([VarDecl("a", ArrayType(2,StringType()))])
        func = FuncDecl(Id("rand"), [], IntType(),body)
        expect = str(Program([func]))

        self.assertTrue(TestAST.checkASTGen(input,expect,517))

    def test_var_listb(self):
        input = """int rand() {
            string a[2], b, TragedyOfDarthPlagueisTheWise;
        }"""
        body = Block([VarDecl("a", ArrayType(2,StringType())), VarDecl("b", StringType()), VarDecl("TragedyOfDarthPlagueisTheWise", StringType())])
        func = FuncDecl(Id("rand"), [], IntType(),body)
        expect = str(Program([func]))

        self.assertTrue(TestAST.checkASTGen(input,expect,518))

    def test_funccall_separatorb(self):
        input = """int cheesy() {
            edamer(4, 5);
        }"""
        body = Block([CallExpr(Id("edamer"), [IntLiteral(4), IntLiteral(5)])])
        func = FuncDecl(Id("cheesy"), [], IntType(),body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,519))

    def test_exp3b(self):
        input = """int cheesy() {
            x = (a*5)/(4-(88.7%3));
        }"""
        inner = BinaryOp("%", FloatLiteral(88.7), IntLiteral(3))
        right = BinaryOp("-", IntLiteral(4), inner)
        left = BinaryOp("*", Id("a"), IntLiteral(5))
        body = Block([BinaryOp("=", Id("x"), BinaryOp("/", left, right))])
        func = FuncDecl(Id("cheesy"), [], IntType(),body)
        expect = str(Program([func]))
        self.assertTrue(TestAST.checkASTGen(input,expect,520))


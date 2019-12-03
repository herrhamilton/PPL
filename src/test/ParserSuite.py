import unittest
from TestUtils import TestParser

class ParserSuite(unittest.TestCase):
    def test_simple_program(self):
        """Simple program: int main() {} """
        input = """int main() {}"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,200))

    def test_more_complex_program(self):
        """More complex program"""
        input = """int main () {
            putIntLn(4);
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,201))
    
    def test_wrong_miss_close(self):
        """Miss ) int main( {}"""
        input = """int main( {}"""
        expect = "Error on line 1 col 10: {"
        self.assertTrue(TestParser.checkParser(input,expect,202))

    def test_if(self):
        input = """int main() {
            if(true) { 
                putIntLn(4); 
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 203))

    def test_comment(self):
        input = """int main() { // this is an ignored comment
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 204))
    def test_block_comment(self):
        input = """int main() {
            /* 
            ** Random invald \nStuff in a block comment 
               ' &3 1.e- 
            */
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 205))
    def test_for_loop(self):
        input = """int main() {
            for(i=1; i<3; i=i+1) {
                putIntLn(4);
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 206))
    def test_do_while_loop(self):
        input = """int main() {
            int x;
            x=1;
            do {
                x = x+1;
            } while(x!=9);
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 207))
    def test_global_var(self):
        input = """int i;
        int main() {
            
            i=3;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 208))
    def test_local_var(self):
        input = """
        int main() {
            int i;
            i=3;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 209))
    def test_more_func(self):
        input = """
        int main() {
            int i;
            i=3;
        }
        void foo() {}"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 210))
    def test_more_func_with_global_var(self):
        input = """
        int main() {
            int i;
            i=3;
        }
        boolean b;
        void foo() {}"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 211))
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
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 212))

    def test_func_with_param(self):
        input = """int foo(int _id, boolean hasBread) {
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 213))
    def test_func_without_param(self):
        input = """int foo() {
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 214))

    def test_empty_file(self):
        input = ""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 215))

    def test_only_var_dec(self):
        input = "int xy;"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 216))

    def test_wrong_param_separator(self):
        input = """float circumfence(float radius; boolean metric) {}"""
        expect = "Error on line 1 col 30: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 217))

    def test_missing_param_Ids(self):
        input = """float circumfence(float, boolean) {}"""
        expect = "Error on line 1 col 23: ,"
        self.assertTrue(TestParser.checkParser(input, expect, 218))
    
    def test_param_arrays(self):
        input = """float circumfence(float radius[], boolean metric) {}"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 219))

    def test_missing_parenthesis_in_block(self):
        input = """float circumfence(float radius[], boolean metric) {
            int i;
            {
                i = 5;
        }"""
        expect = "Error on line 5 col 9: <EOF>"
        self.assertTrue(TestParser.checkParser(input, expect, 220))

    def test_return_statement(self):
        input = """float circumfence(float radius, boolean metric) {
            return x;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 221))

    def test_missing_statement_in_if(self):
        input = """int rand() {
            if() { doSth();}
        }"""
        expect = "Error on line 2 col 15: )"
        self.assertTrue(TestParser.checkParser(input, expect, 222))  

    def test_empty_brackets_in_loop(self):
        input = """int rand() {
            for(){}
        }"""
        expect = "Error on line 2 col 16: )"
        self.assertTrue(TestParser.checkParser(input, expect, 223))

    def test_invalid_brackets_in_loop(self):
        input = """int rand() {
            for(i=4;i<10;){}
        }"""
        expect = "Error on line 2 col 25: )"
        self.assertTrue(TestParser.checkParser(input, expect, 224))

    def test_invalid_brackets_in_loop2(self):
        input = """int rand() {
            for(i=4,i<10,i=i+1){}
        }"""
        expect = "Error on line 2 col 19: ,"
        self.assertTrue(TestParser.checkParser(input, expect, 225))   

    def test_nested_statement(self):
        input = """int rand() {
            return foo()+b;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 226)) 

    def test_void_var_decl(self):
        input = """int rand() {
            void a;
        }"""
        expect = "Error on line 2 col 12: void"
        self.assertTrue(TestParser.checkParser(input, expect, 227))

    def test_var_without_arr_size(self):
        input = """int rand() {
            string a[];
        }"""
        expect = "Error on line 2 col 21: ]"
        self.assertTrue(TestParser.checkParser(input, expect, 228))

    def test_var_with_arr_size(self):
        input = """int rand() {
            string a[2];
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 229))                  

    def test_var_list(self):
        input = """int rand() {
            string a[2], b, TragedyOfDarthPlagueisTheWise;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 230))

    def test_wrong_funccall_brackets(self):
        input = """int cheesy() {
            edamer{};
        }"""
        expect = "Error on line 2 col 18: {"
        self.assertTrue(TestParser.checkParser(input, expect, 231))

    def test_wrong_funccall_param_naming(self):
        input = """int cheesy() {
            edamer(int, float);
        }"""
        expect = "Error on line 2 col 19: int"
        self.assertTrue(TestParser.checkParser(input, expect, 232))

    def test_wrong_funccall_separator(self):
        input = """int cheesy() {
            edamer(4, 5);
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 233))

    def test_missing_funccall_bracket(self):
        input = """int cheesy() {
            edamer(4, 5;
        }"""
        expect = "Error on line 2 col 23: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 234))                          

    def test_funcall_random_whitespace(self):
        input = """int cheesy() {
            eda mer(4, 5);
        }"""
        expect = "Error on line 2 col 16: mer"
        self.assertTrue(TestParser.checkParser(input, expect, 235))

    def test_exp(self):
        input = """int cheesy() {
            a = a+b;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 236))

    def test_exp2(self):
        input = """int cheesy() {
            if(a==5){}
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 237))

    def test_exp3(self):
        input = """int cheesy() {
            x = (a*5)/(4-(88%3));
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 238))

    def test_exp4(self):
        input = """int cheesy() {
            a = a || b;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 239))

    def test_exp5(self):
        input = """int cheesy() {
            if(false) { pilot = 4%3;}
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 240))

    def test_exp6(self):
        input = """int cheesy() {
            if(false) { pilot = 4 3;}
        }"""
        expect = "Error on line 2 col 34: 3"
        self.assertTrue(TestParser.checkParser(input, expect, 241))

    def test_exp7(self):
        input = """int cheesy() {
            a = foo (bar(42 ) \t);
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 242))

    def test_exp8(self):
        input = """int cheesy() {
            do { loopForeverLol();} while(1.2 != 5); 
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 243))

    def test_exp_index(self):
        input = """int cheesy() {
            music = nice[stuff()];
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 244))

    def test_nested_exp(self):
        input = """int vietnam() {
            do{ enjoyDay();} while(carrot[07011997] == asleep());
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 245))

    def test_random_comment(self):
        input = """int vietnam() {
            do{ enjoyDay/*HI I AM A COMMENT HEHEHEH
            */();} while(carrot[07011997] == asleep());
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 246))

    def test_random_comment2(self):
        input = """int vietnam() { // COMMENT THIS
            do{ enjoyDay();} while(carrot[07011997] == asleep());
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 247))

    def test_pizza(self):
        input = """int cheesy() {
            do{ keepProgramming(a+b, xy, faster());} while(pizza != delivered);
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 248))

    def test_block(self):
        input = """int cheesy() {
            int a, b, c;
            a = 3;
            b = 2;
            c = a+b;
            {
                a = 5;
                printLn(a+c);
            }
                printLn(a+c);
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 249))

    def test_whitespaces(self):
        input = """int cheesy() {
            int\n  a \t , \r b;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 250))

    def test_random_exp(self): #parsed correctly, but syntax invalid
        input = """int cheesy() {
            a !=b;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 251))

    def test_newline_maniac(self):
        input = """int sos() {
            if\n\n\n\n\n\n(\n\n\na\n\n\n!=\n\n\n2)\n\n\n\n\n\n{sendHelp(\n\n\n);\n\n\n\n\n\n}
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 252))

    def test_missing_semi_glob_var(self):
        input = """boolean boooo
        int cheesy() {
        }"""
        expect = "Error on line 2 col 8: int"
        self.assertTrue(TestParser.checkParser(input, expect, 253))

    def test_no_func_block(self):
        input = """int cheesy() """
        expect = "Error on line 1 col 13: <EOF>"
        self.assertTrue(TestParser.checkParser(input, expect, 254))

    def test_too_many_brackets(self):
        input = """int cheesy()) {
            
        }"""
        expect = "Error on line 1 col 12: )"
        self.assertTrue(TestParser.checkParser(input, expect, 255))

    def test_param_with_index(self):
        input = """int cheesy(float what[2]) {
        }"""
        expect = "Error on line 1 col 22: 2"
        self.assertTrue(TestParser.checkParser(input, expect, 256))

    def test_arg_with_index(self):
        input = """int cheesy() {
            cheesy(what[2]);
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 257))

    def test_arg_with_type(self):
        input = """int cheesy() {
            cheesy(float what[2]);
        }"""
        expect = "Error on line 2 col 19: float"
        self.assertTrue(TestParser.checkParser(input, expect, 258))

    def test_lonely_else(self):
        input = """int cheesy() {
            else { whatHappened();}
        }"""
        expect = "Error on line 2 col 12: else"
        self.assertTrue(TestParser.checkParser(input, expect, 259))

    def test_else_first(self):
        input = """int cheesy() {
            else{}
            if(a!=b) {}
        }"""
        expect = "Error on line 2 col 12: else"
        self.assertTrue(TestParser.checkParser(input, expect, 260))

    def test_keyword_as_function(self):
        input = """int continue() {}"""
        expect = "Error on line 1 col 4: continue"
        self.assertTrue(TestParser.checkParser(input, expect, 261))

    def test_long_var_dec(self):
        input = """int cheesy() {
            int a,b,c,d,e,f,g,h[8],i,e1,_41,E24cfg,aAaaAA;
            float f[52],g[55],h[128347];
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 262))

    def test_ret_without_exp(self):
        input = """int cheesy() {
            return;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 263))

    def test_wrong_var_list_separator(self):
        input = """int cheesy() {
            int a;b;c;;
        }"""
        expect = "Error on line 2 col 22: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 264))

    def test_multiple_operators(self):
        input = """int cheesy() {
            i = a +% 5;
        }"""
        expect = "Error on line 2 col 19: %"
        self.assertTrue(TestParser.checkParser(input, expect, 265))

    def test_func_in_func(self):
        input = """int cheesy() {
            float main() {}
        }"""
        expect = "Error on line 2 col 22: ("
        self.assertTrue(TestParser.checkParser(input, expect, 266))

    def test_func_in_param(self):
        input = """int cheesy(foo()) {
            
        }"""
        expect = "Error on line 1 col 11: foo"
        self.assertTrue(TestParser.checkParser(input, expect, 267))

    def test_var_dec_in_param(self):
        input = """int cheesy(int i;) {
            
        }"""
        expect = "Error on line 1 col 16: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 268))

    def test_func_dec_in_param(self):
        input = """int cheesy(void main() {return 42;}) {
            
        }"""
        expect = "Error on line 1 col 11: void"
        self.assertTrue(TestParser.checkParser(input, expect, 269))

    def test_param_list_in_var_dec(self):
        input = """int cheesy() {
            int a, foo(), 42;
        }"""
        expect = "Error on line 2 col 22: ("
        self.assertTrue(TestParser.checkParser(input, expect, 270))

    def test_missing_bracket_in_exp(self):
        input = """int cheesy() {
            a = (4*12) + ((3-b)));
        }"""
        expect = "Error on line 2 col 32: )"
        self.assertTrue(TestParser.checkParser(input, expect, 271))

    def test_missing_bracket_in_exp2(self):
        input = """int cheesy() {
            a = (4*12) + ((3-b);
        }"""
        expect = "Error on line 2 col 31: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 272))

    def test_exp_wrong_operand(self):
        input = """int cheesy() {
            invalid = a * if;
        }"""
        expect = "Error on line 2 col 26: if"
        self.assertTrue(TestParser.checkParser(input, expect, 273))

    def test_wtfiswrongwiththisif(self):
        input = """int cheesy() {
            if(if(if(a!=b) { lel();})whut();) { lol();}
        }"""
        expect = "Error on line 2 col 15: if"
        self.assertTrue(TestParser.checkParser(input, expect, 274))

    def test_comments_again(self):
        input = """int cheesy() {
            do/*DOWHAT*/ { 
                something(); //wow you are so creative.
                // NOT
                }
            while (/*yes?*/ a != b) /*...*/ ; 
            // at least you remembered the semicolon
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 275))

    def test_ISTHISTHEREALLIFE(self):
        input = """int reallife() {
            if(this == reallife) {
                return 0;
            } else {
                return fantasy();
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 276))

    def test_intvoid(self):
        input = """int cheesy() {
            int void;
        }"""
        expect = "Error on line 2 col 16: void"
        self.assertTrue(TestParser.checkParser(input, expect, 277))

    def test_asdf(self):
        input = """int cheesy() {
            string str;
            str = "ASDF";
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 278))

    def test_what(self):
        input = """int cheesy() {
            "WHAT DID YOU SAY?"
        }"""
        expect = "Error on line 3 col 8: }"
        self.assertTrue(TestParser.checkParser(input, expect, 279))

    def test_pi(self):
        input = """float pi;
        float volumeCircle(float radius) {
            pi = 3.141592653589793238;
            return 4/3 * pi * r*r*r;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 280))

    def test_bmi(self):
        input = """float bmi(float thicc, float smol) {
            return thicc / (smol*smol);
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 281))

    def test_stuff(self):
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
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 282))

    def test_keyword(self):
        input = """int cheesy() {
            int true;
        }"""
        expect = "Error on line 2 col 16: true"
        self.assertTrue(TestParser.checkParser(input, expect, 283))

    def test_keyword2(self):
        input = """int cheesy() {
            false = 42;
            // works because parser is stupid
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 284))

    def test_lonely_ret(self):
        input = """return everything;"""
        expect = "Error on line 1 col 0: return"
        self.assertTrue(TestParser.checkParser(input, expect, 285))

    def test_else_without_block(self):
        input = """int cheesy() {
            if(a!=b) {
                start();
            } else
        }"""
        expect = "Error on line 5 col 8: }"
        self.assertTrue(TestParser.checkParser(input, expect, 286))

    def test_else_with_exp(self):
        input = """int cheesy() {
            if(a!=b) {
                start();
            } else (a != c) { what();}
        }"""
        expect = "Error on line 4 col 19: ("
        self.assertTrue(TestParser.checkParser(input, expect, 287))

    def test_nofunc(self):
        input = """void notAFunc;"""
        expect = "Error on line 1 col 13: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 288))

    def test_nested_loops(self):
        input = """int cheesy() {
            for(i=1; i<5;i=i+1) {
                do{allthatcoolstuff();} while(i<3);
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 289))

    def test_randStuff(self):
        input = """int cheesy() {
            int a;
            int b;
            int c;
            b = randInt();
            c = 5;
            a = c;
            if(a == b) {
                return c;
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 290))

    def test_void_return(self):
        input = """void cheesy() {
            return void;
        }"""
        expect = "Error on line 2 col 19: void"
        self.assertTrue(TestParser.checkParser(input, expect, 291))

    def test_block_around_program(self):
        input = """{int cheesy() {
            
        } }"""
        expect = "Error on line 1 col 0: {"
        self.assertTrue(TestParser.checkParser(input, expect, 292))

    def test_arr_fail(self):
        input = """int cheesy() {
            int i{3};
        }"""
        expect = "Error on line 2 col 17: {"
        self.assertTrue(TestParser.checkParser(input, expect, 293))

    def test_if_with_semi(self):
        input = """int cheesy() {
            if(u!=m) { return 1;};
        }"""
        expect = "Error on line 2 col 33: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 294))

    def test_while_without_do(self):
        input = """int cheesy() {
            while(2!=4);
        }"""
        expect = "Error on line 2 col 12: while"
        self.assertTrue(TestParser.checkParser(input, expect, 295))

    def test_(self):
        input = """int cheesy() {
            do {
                printf("Continue? [Y]es  [N]o", name);
                } while(i==42);
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 296))

    def test_broken_while(self):
        input = """int cheesy() {
            do{} wh ile(a);
        }"""
        expect = "Error on line 2 col 17: wh"
        self.assertTrue(TestParser.checkParser(input, expect, 297))
    def test_broken_while2(self):
        input = """int cheesy() {
            d/*comment!*/o{} while(a);
        }"""
        expect = "Error on line 2 col 25: o"
        self.assertTrue(TestParser.checkParser(input, expect, 298))
    def test_op(self):
        input = """int a() {
            a = 3+2;
        }"""
        expect = "successful";
        self.assertTrue(TestParser.checkParser(input, expect, 300))

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
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 299))
import unittest
from TestUtils import TestLexer

class LexerSuite(unittest.TestCase):

    """test whitespaces"""
    def test_whitespaces(self):
        self.assertTrue(TestLexer.checkLexeme("\t","<EOF>",100))
    def test_whitespaces1(self):
        self.assertTrue(TestLexer.checkLexeme("\r","<EOF>",101))
    def test_whitespaces2(self):
        self.assertTrue(TestLexer.checkLexeme("\n","<EOF>",102))
    def test_whitespaces3(self):
        self.assertTrue(TestLexer.checkLexeme("Hello\tWorld","Hello,World,<EOF>",103))

    """test comments"""
    def test_comments(self):        
        self.assertTrue(TestLexer.checkLexeme("//","<EOF>",104))
    def test_comments1(self):        
        self.assertTrue(TestLexer.checkLexeme("//abc123","<EOF>",105))
    def test_comments2(self):        
        self.assertTrue(TestLexer.checkLexeme("//abc/*123","<EOF>",106))
    def test_comments3(self):        
        self.assertTrue(TestLexer.checkLexeme("//abc\n123","123,<EOF>",107))
    def test_comments4(self):        
        self.assertTrue(TestLexer.checkLexeme("int i;// this is i","int,i,;,<EOF>",108))
    def test_comments5(self):        
        self.assertTrue(TestLexer.checkLexeme("int i;/* this is i*/","int,i,;,<EOF>",109))
    def test_comments6(self):        
        self.assertTrue(TestLexer.checkLexeme("/*hello!\nNewline?*/","<EOF>",110))
    def test_comments7(self):        
        self.assertTrue(TestLexer.checkLexeme("void _a;/*$$\n?*/string str;","void,_a,;,string,str,;,<EOF>",111))
    def test_comments8(self):        
        self.assertTrue(TestLexer.checkLexeme("/ /","/,/,<EOF>",112))

    """test identifiers"""
    def test_identifiers(self):
        self.assertTrue(TestLexer.checkLexeme("abc","abc,<EOF>",113))
    def test_identifiers1(self):
        self.assertTrue(TestLexer.checkLexeme("aCBbdc","aCBbdc,<EOF>",114))
    def test_identifiers2(self):
        self.assertTrue(TestLexer.checkLexeme("a321E","a321E,<EOF>",115))
    def test_identifiers3(self):
        self.assertTrue(TestLexer.checkLexeme("_ab","_ab,<EOF>",116))
    def test_identifiers4(self):
        self.assertTrue(TestLexer.checkLexeme("_1","_1,<EOF>",117))
    def test_identifiers5(self):
        self.assertTrue(TestLexer.checkLexeme("_","_,<EOF>",118))
    def test_identifiers6(self):
        self.assertTrue(TestLexer.checkLexeme("i","i,<EOF>",119))
    def test_identifiers7(self):
        self.assertTrue(TestLexer.checkLexeme("A","A,<EOF>",120))
    def test_identifiers8(self):
        self.assertTrue(TestLexer.checkLexeme("_break_","_break_,<EOF>",121))
    def test_identifiers9(self):
        self.assertTrue(TestLexer.checkLexeme("if1","if1,<EOF>",122))

    """test invalid identifiers"""
    def test_invalid_id(self):
        self.assertTrue(TestLexer.checkLexeme("aA?sVN","aA,Error Token ?",123))
    def test_invalid_id1(self):
        self.assertTrue(TestLexer.checkLexeme("3_ab","3,_ab,<EOF>",124))
    def test_invalid_id2(self):
        self.assertTrue(TestLexer.checkLexeme("ab cd","ab,cd,<EOF>",125))
    def test_invalid_id3(self):
        self.assertTrue(TestLexer.checkLexeme("3while","3,while,<EOF>",126))

    """test integers"""
    def test_integer(self):
        self.assertTrue(TestLexer.checkLexeme("5","5,<EOF>",127))
    def test_integer1(self):
        self.assertTrue(TestLexer.checkLexeme("123a123","123,a123,<EOF>",128))
    def test_integer2(self):
        self.assertTrue(TestLexer.checkLexeme("12 3", "12,3,<EOF>", 129))
    def test_integer3(self):
        self.assertTrue(TestLexer.checkLexeme("12&3", "12,Error Token &", 130))

    """test floats"""
    def test_floats(self):
        self.assertTrue(TestLexer.checkLexeme("1.3","1.3,<EOF>", 131))
    def test_floats1(self):
        self.assertTrue(TestLexer.checkLexeme("1.","1.,<EOF>", 132))
    def test_floats2(self):
        self.assertTrue(TestLexer.checkLexeme(".3",".3,<EOF>", 133))
    def test_floats3(self):
        self.assertTrue(TestLexer.checkLexeme("1e2", "1e2,<EOF>", 134))
    def test_floats4(self):
        self.assertTrue(TestLexer.checkLexeme("1E2", "1E2,<EOF>", 135))
    def test_floats5(self):
        self.assertTrue(TestLexer.checkLexeme("1.3e2","1.3e2,<EOF>", 136))
    def test_floats6(self):
        self.assertTrue(TestLexer.checkLexeme("1.3e-2","1.3e-2,<EOF>", 137))
    def test_floats7(self):
        self.assertTrue(TestLexer.checkLexeme("1.3E-2","1.3E-2,<EOF>", 138))
    def test_floats8(self):
        self.assertTrue(TestLexer.checkLexeme("1 .3e-2","1,.3e-2,<EOF>", 139))
    def test_floats9(self):
        self.assertTrue(TestLexer.checkLexeme("1.3e+2","1.3,e,+,2,<EOF>", 140))
    def test_floats10(self):
        self.assertTrue(TestLexer.checkLexeme("1.3e-?2","1.3,e,-,Error Token ?", 141))
    def test_floats11(self):
        self.assertTrue(TestLexer.checkLexeme(".3e2",".3e2,<EOF>", 141))
    def test_floats12(self):
        self.assertTrue(TestLexer.checkLexeme("1.e2","1.e2,<EOF>", 142)) # TODO valid??

    """test invalid floats"""
    def test_invalid_floats(self):
        self.assertTrue(TestLexer.checkLexeme("e12","e12,<EOF>", 143)) # will be accepted as ID
    def test_invalid_floats1(self):
        self.assertTrue(TestLexer.checkLexeme("1.3e","1.3,e,<EOF>", 144))
    def test_invalid_floats2(self):
        self.assertTrue(TestLexer.checkLexeme("1E+1","1,E,+,1,<EOF>", 145))
    def test_invalid_floats3(self):
        self.assertTrue(TestLexer.checkLexeme("1e","1,e,<EOF>", 146))
    def test_invalid_floats4(self):
        self.assertTrue(TestLexer.checkLexeme("1.3e-","1.3,e,-,<EOF>", 147))
    def test_invalid_floats5(self):
        self.assertTrue(TestLexer.checkLexeme("1. 3e2","1.,3e2,<EOF>", 148))

    """test strings"""
    def test_strings(self):
        self.assertTrue(TestLexer.checkLexeme("\"hello world\"","hello world,<EOF>",149))
    def test_strings1(self):
        self.assertTrue(TestLexer.checkLexeme("\"Nice t0 meet you! :)\"","Nice t0 meet you! :),<EOF>",150))
    def test_strings2(self):
        self.assertTrue(TestLexer.checkLexeme("\"\"",",<EOF>",151))
    def test_strings3(self):
        self.assertTrue(TestLexer.checkLexeme("\"@ % & ! $\"","@ % & ! $,<EOF>",152))
    def test_strings4(self):
        self.assertTrue(TestLexer.checkLexeme("\"}>(==%)\"", "}>(==%),<EOF>", 153))
    def test_strings5(self):
        self.assertTrue(TestLexer.checkLexeme("\"\\b \\n \\f \\r \\t \"","\\b \\n \\f \\r \\t ,<EOF>",154))

    """test invalid strings"""
    def test_invalid_strings(self):
        self.assertTrue(TestLexer.checkLexeme("\"","Error Token \"",155))
    def test_invalid_strings1(self):
        self.assertTrue(TestLexer.checkLexeme("\"hello world","Unclosed String: hello world",156))
    def test_invalid_strings2(self):
        self.assertTrue(TestLexer.checkLexeme("\"hello\nworld\"","Unclosed String: hello",157))
    def test_invalid_strings3(self):
        self.assertTrue(TestLexer.checkLexeme("\"hello\$world\"","Illegal Escape In String: hello\$",158))

    """test keywords"""
    def test_keywords(self):
        self.assertTrue(TestLexer.checkLexeme("int","int,<EOF>",159))
    def test_keywords1(self):
        self.assertTrue(TestLexer.checkLexeme("void","void,<EOF>",160))
    def test_keywords2(self):
        self.assertTrue(TestLexer.checkLexeme("float","float,<EOF>",161))
    def test_keywords3(self):
        self.assertTrue(TestLexer.checkLexeme("boolean","boolean,<EOF>",162))
    def test_keywords4(self):
        self.assertTrue(TestLexer.checkLexeme("boo lean","boo,lean,<EOF>",163))
    def test_keywords5(self):
        self.assertTrue(TestLexer.checkLexeme("string","string,<EOF>",164))
    def test_keywords6(self):
        self.assertTrue(TestLexer.checkLexeme("for","for,<EOF>",165))
    def test_keywords7(self):
        self.assertTrue(TestLexer.checkLexeme("do","do,<EOF>",166))
    def test_keywords8(self):
        self.assertTrue(TestLexer.checkLexeme("while","while,<EOF>",167))
    def test_keywords9(self):
        self.assertTrue(TestLexer.checkLexeme("break","break,<EOF>",168))
    def test_keywords10(self):
        self.assertTrue(TestLexer.checkLexeme("br\neak","br,eak,<EOF>",169))
    def test_keywords11(self):
        self.assertTrue(TestLexer.checkLexeme("continue","continue,<EOF>",170))
    def test_keywords12(self):
        self.assertTrue(TestLexer.checkLexeme("if","if,<EOF>",171))
    def test_keywords13(self):
        self.assertTrue(TestLexer.checkLexeme("else","else,<EOF>",172))
    def test_keywords14(self):
        self.assertTrue(TestLexer.checkLexeme("return","return,<EOF>",173))

    """test operators"""
    def test_operators(self):
        self.assertTrue(TestLexer.checkLexeme("a + 3", "a,+,3,<EOF>",174))
    def test_operators1(self):
        self.assertTrue(TestLexer.checkLexeme("a / 3", "a,/,3,<EOF>",175))
    def test_operators2(self):
        self.assertTrue(TestLexer.checkLexeme("a - 3", "a,-,3,<EOF>",176))
    def test_operators3(self):
        self.assertTrue(TestLexer.checkLexeme("9 % 3", "9,%,3,<EOF>",177))
    def test_operators4(self):
        self.assertTrue(TestLexer.checkLexeme("_123xyz $ 3", "_123xyz,Error Token $",178))
    def test_operators5(self):
        self.assertTrue(TestLexer.checkLexeme("a * 3", "a,*,3,<EOF>",179))
    def test_operators6(self):
        self.assertTrue(TestLexer.checkLexeme("x==4", "x,==,4,<EOF>",180))
    def test_operators7(self):
        self.assertTrue(TestLexer.checkLexeme("5!=7", "5,!=,7,<EOF>",181))
    def test_operators8(self):
        self.assertTrue(TestLexer.checkLexeme("i=9;", "i,=,9,;,<EOF>",182))
    def test_operators9(self):
        self.assertTrue(TestLexer.checkLexeme("if(a && b)", "if,(,a,&&,b,),<EOF>",183))
    def test_operators10(self):
        self.assertTrue(TestLexer.checkLexeme("& &", "Error Token &",184))
    def test_operators11(self):
        self.assertTrue(TestLexer.checkLexeme("x <\n=7", "x,<,=,7,<EOF>",185))
    def test_operators12(self):
        self.assertTrue(TestLexer.checkLexeme("}>(==%)", "},>,(,==,%,),<EOF>",186))

    """ test others"""
    def test_others(self):
        self.assertTrue(TestLexer.checkLexeme("(", "(,<EOF>",187))
    def test_others1(self):
        self.assertTrue(TestLexer.checkLexeme(")", "),<EOF>",188))
    def test_others2(self):
        self.assertTrue(TestLexer.checkLexeme("{", "{,<EOF>",189))
    def test_others3(self):
        self.assertTrue(TestLexer.checkLexeme("}", "},<EOF>",190))
    def test_others4(self):
        self.assertTrue(TestLexer.checkLexeme("[", "[,<EOF>",191))
    def test_others5(self):
        self.assertTrue(TestLexer.checkLexeme("]", "],<EOF>",192))
    def test_others6(self):
        self.assertTrue(TestLexer.checkLexeme(";", ";,<EOF>",193))
    def test_others7(self):
        self.assertTrue(TestLexer.checkLexeme(",", ",,<EOF>",194))
    def test_others8(self):
        self.assertTrue(TestLexer.checkLexeme("", "<EOF>",195))
    def test_others9(self):
        self.assertTrue(TestLexer.checkLexeme(".", "Error Token .",196))
    def test_others10(self):
        self.assertTrue(TestLexer.checkLexeme("a 45 8.4e9 ~", "a,45,8.4e9,Error Token ~",197))
    def test_others11(self):
        self.assertTrue(TestLexer.checkLexeme("   a\t= /*\n*/  2  ", "a,=,2,<EOF>",198))
    def test_others12(self):
        self.assertTrue(TestLexer.checkLexeme("FINALLY", "FINALLY,<EOF>",199))
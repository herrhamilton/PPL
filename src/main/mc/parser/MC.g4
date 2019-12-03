grammar MC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

// PARSER

program: (program_part)* EOF;
program_part: variable_declaration SEMI | function;
function: (primtype (LSB RSB)? | VOIDTYPE) ID LB param_list? RB block;
param_list: param_decl (COMMA param_decl)*; // foo(int a, float b, boolean c) {...
param_decl: primtype ID (LSB RSB)?; 

if_statement: IF LB exp RB block (ELSE block)?; // dangling-else-problem?
loop: for_loop | do_while_loop;
for_loop: FOR LB exp SEMI exp SEMI exp RB block;
do_while_loop: DO block WHILE LB exp RB SEMI;

block: LP statement* RP;
statement: (ret_exp | variable_declaration | funcall | exp | BREAK | CONTINUE ) SEMI | if_statement | loop | block;

ret_exp: RETURN exp?;
variable_declaration: primtype var_list;
var: ID  (LSB INTLIT RSB)?;
var_list: var (COMMA var_list)?;

funcall: ID LB argum_list? RB;
argum_list: exp (COMMA exp)*; // foo(a, 3.14, bar());

exp: exp1 OP_ASN exp | exp1;
exp1: exp1 OP_OR exp2 | exp2;
exp2: exp2 OP_AND exp3 | exp3;
exp3: exp4 (OP_EQ | OP_NEQ) exp4 | exp4;
exp4: exp5 (OP_LES |OP_LEQ | OP_GRE | OP_GEQ) exp5 | exp5;
exp5: exp5 (OP_ADD | OP_NEG) exp6 | exp6;
exp6: exp6 (OP_DIV | OP_MUL | OP_MOD) exp7 | exp7;
exp7: (OP_NEG | OP_NOT) exp8 | exp8;
exp8: exp9 LSB RSB | exp9;
exp9: operand | subexp;

subexp: LB exp RB;
operand: INTLIT | BOOLLIT | FLOATLIT | STRLIT | ID | index_exp | funcall;
index_exp: (ID | funcall) LSB exp RSB;
primtype: INTTYPE | FLOATTYPE | BOOLTYPE | STRINGTYPE;


// LEXER

WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines
NEWLINE: '\n';

LINE_COMMENT: '//' ~('\r' | '\n')* -> skip; //channel(HIDDEN);
BLOCK_COMMENT: BLOCK_COMM_START .*? BLOCK_COMM_END -> skip; //channel(HIDDEN);

BLOCK_COMM_START: '/*';
BLOCK_COMM_END: '*/';

INTTYPE: 'int';
VOIDTYPE: 'void';
FLOATTYPE: 'float';
BOOLTYPE: 'boolean';
STRINGTYPE: 'string';

FOR: 'for';
DO: 'do';
WHILE: 'while';
BREAK: 'break';
CONTINUE: 'continue';

IF: 'if';
ELSE: 'else';
RETURN: 'return';

INTLIT: NUMBER+;
BOOLLIT: TRUE | FALSE;
FLOATLIT: (INTLIT? '.' INTLIT EXPO?) | INTLIT EXPO | INTLIT '.' EXPO?;
fragment EXPO: [eE] OP_NEG? INTLIT; 
STRLIT: '"' ( ~('\b' | '\n' | '\f' | '\r' | '\t' | '\\' | '"' ) | '\\'[bnfrt"\\] )* '"' {self.text = self.text[1:-1]};
TRUE: 'true';
FALSE: 'false';
ID: LETTER (LETTER | NUMBER)*;
fragment LETTER: [a-zA-Z_];
fragment NUMBER: [0-9];

OP_ADD: '+';
OP_NEG: '-';
OP_MUL: '*';
OP_DIV: '/';
OP_MOD: '%';

OP_NOT: '!';
OP_AND: '&&';
OP_OR: '||';

OP_EQ: '==';
OP_NEQ: '!=';
OP_LES: '<';
OP_GRE: '>';
OP_LEQ: '<=';
OP_GEQ: '>=';

OP_ASN: '=';

LB: '(';
RB: ')';
LP: '{';
RP: '}';
LSB: '[';
RSB: ']';
SEMI: ';';
COMMA: ',';

ERROR_CHAR: .;
ILLEGAL_ESCAPE: '"' ( ~('\b' | '\n' | '\f' | '\r' | '\t' | '\\' | '"' ) | '\\'[bnfrt"\\] )* '\\'~[bnfrt"\\] {raise IllegalEscape(self.text[1:])};
UNCLOSE_STRING: '"' ( ~('\b' | '\n' | '\f' | '\r' | '\t' | '\\' | '"' ) | '\\'[bnfrt"\\] )* {raise UncloseString(self.text[1:])};
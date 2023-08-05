#  Copyright (c) 1999 John Aycock
#  Copyright (c) 2000-2002 by hartmut Goebel <h.goebel@crazy-compilers.com>
#  Copyright (c) 2005 by Dan Pascu <dan@windowmaker.org>
#  Copyright (c) 2015 Rocky Bernstein
#
#  See LICENSE for license
"""
A spark grammar for Python 2.x.

However instead of terminal symbols being the usual ASCII text,
e.g. 5, myvariable, "for", etc.  they are CPython Bytecode tokens,
e.g. "LOAD_CONST 5", "STORE NAME myvariable", "SETUP_LOOP", etc.

If we succeed in creating a parse tree, then we have a Python program
that a later phase can tern into a sequence of ASCII text.
"""

from __future__ import print_function

from uncompyle6.parser import PythonParser, PythonParserSingle, nop_func
from uncompyle6.parsers.astnode import AST
from spark_parser import DEFAULT_DEBUG as PARSER_DEFAULT_DEBUG
from uncompyle6 import PYTHON3

class Python2Parser(PythonParser):

    def __init__(self, debug_parser=PARSER_DEFAULT_DEBUG):
        if PYTHON3:
            super().__init__(AST, 'stmts', debug=debug_parser)
        else:
            super(Python2Parser, self).__init__(AST, 'stmts', debug=debug_parser)
        self.customized = {}

    def p_list_comprehension2(self, args):
        """
        list_for ::= expr _for designator list_iter JUMP_BACK
        """

    def p_setcomp2(self, args):
        '''
        # This is different in python3 - should it be?
        comp_for ::= expr _for designator comp_iter JUMP_BACK
        '''

    def p_print(self, args):
        '''
        stmt ::= print_items_stmt
        stmt ::= print_nl
        stmt ::= print_items_nl_stmt

        print_items_stmt ::= expr PRINT_ITEM print_items_opt
        print_items_nl_stmt ::= expr PRINT_ITEM print_items_opt PRINT_NEWLINE_CONT
        print_items_opt ::= print_items
        print_items_opt ::=
        print_items ::= print_items print_item
        print_items ::= print_item
        print_item ::= expr PRINT_ITEM_CONT
        print_nl ::= PRINT_NEWLINE
        '''

    def p_print_to(self, args):
        '''
        stmt ::= print_to
        stmt ::= print_to_nl
        stmt ::= print_nl_to
        print_to ::= expr print_to_items POP_TOP
        print_to_nl ::= expr print_to_items PRINT_NEWLINE_TO
        print_nl_to ::= expr PRINT_NEWLINE_TO
        print_to_items ::= print_to_items print_to_item
        print_to_items ::= print_to_item
        print_to_item ::= DUP_TOP expr ROT_TWO PRINT_ITEM_TO
        '''

    def p_grammar(self, args):
        '''
        sstmt ::= stmt
        sstmt ::= ifelsestmtr
        sstmt ::= return_stmt RETURN_LAST

        stmts_opt ::= stmts
        stmts_opt ::= passstmt
        passstmt ::=

        _stmts ::= _stmts stmt
        _stmts ::= stmt

        c_stmts ::= _stmts
        c_stmts ::= _stmts lastc_stmt
        c_stmts ::= lastc_stmt
        c_stmts ::= continue_stmts

        lastc_stmt ::= iflaststmt
        lastc_stmt ::= whileelselaststmt
        lastc_stmt ::= forelselaststmt
        lastc_stmt ::= ifelsestmtr
        lastc_stmt ::= ifelsestmtc
        lastc_stmt ::= tryelsestmtc

        c_stmts_opt ::= c_stmts
        c_stmts_opt ::= passstmt

        l_stmts ::= _stmts
        l_stmts ::= return_stmts
        l_stmts ::= continue_stmts
        l_stmts ::= _stmts lastl_stmt
        l_stmts ::= lastl_stmt

        lastl_stmt ::= iflaststmtl
        lastl_stmt ::= ifelsestmtl
        lastl_stmt ::= forelselaststmtl
        lastl_stmt ::= tryelsestmtl

        l_stmts_opt ::= l_stmts
        l_stmts_opt ::= passstmt

        suite_stmts ::= _stmts
        suite_stmts ::= return_stmts
        suite_stmts ::= continue_stmts

        suite_stmts_opt ::= suite_stmts
        suite_stmts_opt ::= passstmt

        else_suite ::= suite_stmts
        else_suitel ::= l_stmts
        else_suitec ::= c_stmts
        else_suitec ::= return_stmts

        designList ::= designator designator
        designList ::= designator DUP_TOP designList

        designator ::= STORE_FAST
        designator ::= STORE_NAME
        designator ::= STORE_GLOBAL
        designator ::= STORE_DEREF
        designator ::= expr STORE_ATTR
        designator ::= expr STORE_SLICE+0
        designator ::= expr expr STORE_SLICE+1
        designator ::= expr expr STORE_SLICE+2
        designator ::= expr expr expr STORE_SLICE+3
        designator ::= store_subscr
        store_subscr ::= expr expr STORE_SUBSCR
        designator ::= unpack
        designator ::= unpack_list

        stmt ::= classdef
        stmt ::= call_stmt
        call_stmt ::= expr POP_TOP

        stmt ::= return_stmt
        return_stmt ::= ret_expr RETURN_VALUE
        return_stmts ::= return_stmt
        return_stmts ::= _stmts return_stmt

        return_if_stmts ::= return_if_stmt
        return_if_stmts ::= _stmts return_if_stmt
        return_if_stmt ::= ret_expr RETURN_END_IF

        stmt ::= break_stmt
        break_stmt ::= BREAK_LOOP

        stmt ::= continue_stmt
        continue_stmt ::= CONTINUE
        continue_stmt ::= CONTINUE_LOOP
        continue_stmts ::= _stmts lastl_stmt continue_stmt
        continue_stmts ::= lastl_stmt continue_stmt
        continue_stmts ::= continue_stmt

        stmt ::= raise_stmt0
        stmt ::= raise_stmt1
        stmt ::= raise_stmt2
        stmt ::= raise_stmt3

        raise_stmt0 ::= RAISE_VARARGS_0
        raise_stmt1 ::= expr RAISE_VARARGS_1
        raise_stmt2 ::= expr expr RAISE_VARARGS_2
        raise_stmt3 ::= expr expr expr RAISE_VARARGS_3

        stmt ::= exec_stmt
        exec_stmt ::= expr exprlist DUP_TOP EXEC_STMT
        exec_stmt ::= expr exprlist EXEC_STMT

        stmt ::= assert
        stmt ::= assert2
        stmt ::= ifstmt
        stmt ::= ifelsestmt

        stmt ::= whilestmt
        stmt ::= whilenotstmt
        stmt ::= while1stmt
        stmt ::= whileelsestmt
        stmt ::= while1elsestmt
        stmt ::= forstmt
        stmt ::= forelsestmt
        stmt ::= trystmt
        stmt ::= tryelsestmt
        stmt ::= tryfinallystmt
        stmt ::= withstmt
        stmt ::= withasstmt

        stmt ::= del_stmt
        del_stmt ::= DELETE_FAST
        del_stmt ::= DELETE_NAME
        del_stmt ::= DELETE_GLOBAL
        del_stmt ::= expr DELETE_SLICE+0
        del_stmt ::= expr expr DELETE_SLICE+1
        del_stmt ::= expr expr DELETE_SLICE+2
        del_stmt ::= expr expr expr DELETE_SLICE+3
        del_stmt ::= delete_subscr
        delete_subscr ::= expr expr DELETE_SUBSCR
        del_stmt ::= expr DELETE_ATTR

        kwarg   ::= LOAD_CONST expr

        classdef ::= buildclass designator

        buildclass ::= LOAD_CONST expr mkfunc
                     CALL_FUNCTION_0 BUILD_CLASS

        stmt ::= classdefdeco
        classdefdeco ::= classdefdeco1 designator
        classdefdeco1 ::= expr classdefdeco1 CALL_FUNCTION_1
        classdefdeco1 ::= expr classdefdeco2 CALL_FUNCTION_1
        classdefdeco2 ::= LOAD_CONST expr mkfunc CALL_FUNCTION_0 BUILD_CLASS

        _jump ::= JUMP_ABSOLUTE
        _jump ::= JUMP_FORWARD
        _jump ::= JUMP_BACK

        jmp_false   ::= POP_JUMP_IF_FALSE
        jmp_false   ::= JUMP_IF_FALSE
        jmp_true    ::= POP_JUMP_IF_TRUE
        jmp_true    ::= JUMP_IF_TRUE

        assert ::= assert_expr jmp_true LOAD_ASSERT RAISE_VARARGS_1
        assert2 ::= assert_expr jmp_true LOAD_ASSERT expr CALL_FUNCTION_1 RAISE_VARARGS_1
        assert2 ::= assert_expr jmp_true LOAD_ASSERT expr RAISE_VARARGS_2

        assert_expr ::= expr
        assert_expr ::= assert_expr_or
        assert_expr ::= assert_expr_and
        assert_expr_or ::= assert_expr jmp_true expr
        assert_expr_and ::= assert_expr jmp_false expr

        ifstmt ::= testexpr _ifstmts_jump

        testexpr ::= testfalse
        testexpr ::= testtrue
        testfalse ::= expr jmp_false
        testtrue ::= expr jmp_true

        _ifstmts_jump ::= return_if_stmts
        _ifstmts_jump ::= c_stmts_opt JUMP_FORWARD COME_FROM

        iflaststmt ::= testexpr c_stmts_opt JUMP_ABSOLUTE

        iflaststmtl ::= testexpr c_stmts_opt JUMP_BACK

        ifelsestmt ::= testexpr c_stmts_opt JUMP_FORWARD else_suite COME_FROM

        ifelsestmtc ::= testexpr c_stmts_opt JUMP_ABSOLUTE else_suitec

        ifelsestmtr ::= testexpr return_if_stmts return_stmts

        ifelsestmtl ::= testexpr c_stmts_opt JUMP_BACK else_suitel


        trystmt ::= SETUP_EXCEPT suite_stmts_opt POP_BLOCK
                    try_middle COME_FROM

        # this is nested inside a trystmt
        tryfinallystmt ::= SETUP_FINALLY suite_stmts
                           POP_BLOCK LOAD_CONST
                           COME_FROM suite_stmts_opt END_FINALLY

        tryelsestmt    ::= SETUP_EXCEPT suite_stmts_opt POP_BLOCK
                           try_middle else_suite COME_FROM

        tryelsestmtc ::= SETUP_EXCEPT suite_stmts_opt POP_BLOCK
                         try_middle else_suitec COME_FROM

        tryelsestmtl ::= SETUP_EXCEPT suite_stmts_opt POP_BLOCK
                         try_middle else_suitel COME_FROM

        try_middle ::= jmp_abs COME_FROM except_stmts
                       END_FINALLY
        try_middle ::= JUMP_FORWARD COME_FROM except_stmts
                       END_FINALLY COME_FROM

        except_stmts ::= except_stmts except_stmt
        except_stmts ::= except_stmt

        except_stmt ::= except_cond1 except_suite
        except_stmt ::= except_cond2 except_suite
        except_stmt ::= except

        except_suite ::= c_stmts_opt JUMP_FORWARD
        except_suite ::= c_stmts_opt jmp_abs
        except_suite ::= return_stmts

        except_cond1 ::= DUP_TOP expr COMPARE_OP
                jmp_false POP_TOP POP_TOP POP_TOP

        except_cond2 ::= DUP_TOP expr COMPARE_OP
                jmp_false POP_TOP designator POP_TOP

        except  ::=  POP_TOP POP_TOP POP_TOP c_stmts_opt JUMP_FORWARD
        except  ::=  POP_TOP POP_TOP POP_TOP c_stmts_opt jmp_abs
        except  ::=  POP_TOP POP_TOP POP_TOP return_stmts

        jmp_abs ::= JUMP_ABSOLUTE
        jmp_abs ::= JUMP_BACK

        withstmt ::= expr SETUP_WITH POP_TOP suite_stmts_opt
                POP_BLOCK LOAD_CONST COME_FROM
                WITH_CLEANUP END_FINALLY

        withasstmt ::= expr SETUP_WITH designator suite_stmts_opt
                POP_BLOCK LOAD_CONST COME_FROM
                WITH_CLEANUP END_FINALLY

        whilestmt ::= SETUP_LOOP
                testexpr
                l_stmts_opt JUMP_BACK
                POP_BLOCK COME_FROM

        whilestmt ::= SETUP_LOOP
                testexpr
                return_stmts
                POP_BLOCK COME_FROM

        while1stmt ::= SETUP_LOOP l_stmts JUMP_BACK COME_FROM
        while1stmt ::= SETUP_LOOP return_stmts COME_FROM
        while1elsestmt ::= SETUP_LOOP l_stmts JUMP_BACK else_suite COME_FROM

        whileelsestmt ::= SETUP_LOOP testexpr
                l_stmts_opt JUMP_BACK
                POP_BLOCK
                else_suite COME_FROM

        whileelselaststmt ::= SETUP_LOOP testexpr
                l_stmts_opt JUMP_BACK
                POP_BLOCK
                else_suitec COME_FROM

        _for ::= GET_ITER FOR_ITER
        _for ::= LOAD_CONST FOR_LOOP

        for_block ::= l_stmts_opt JUMP_BACK
        for_block ::= return_stmts _come_from

        forstmt ::= SETUP_LOOP expr _for designator
                for_block POP_BLOCK COME_FROM

        forelsestmt ::= SETUP_LOOP expr _for designator
                for_block POP_BLOCK else_suite COME_FROM

        forelselaststmt ::= SETUP_LOOP expr _for designator
                for_block POP_BLOCK else_suitec COME_FROM

        forelselaststmtl ::= SETUP_LOOP expr _for designator
                for_block POP_BLOCK else_suitel COME_FROM

        '''

    def p_expr(self, args):
        '''
        expr ::= _mklambda
        expr ::= SET_LINENO
        expr ::= LOAD_FAST
        expr ::= LOAD_NAME
        expr ::= LOAD_CONST
        expr ::= LOAD_GLOBAL
        expr ::= LOAD_DEREF
        expr ::= LOAD_LOCALS
        expr ::= load_attr
        expr ::= binary_expr
        expr ::= binary_expr_na
        expr ::= build_list
        expr ::= cmp
        expr ::= mapexpr
        expr ::= and
        expr ::= and2
        expr ::= or
        expr ::= unary_expr
        expr ::= call_function
        expr ::= unary_not
        expr ::= unary_convert
        expr ::= binary_subscr
        expr ::= binary_subscr2
        expr ::= load_attr
        expr ::= get_iter
        expr ::= slice0
        expr ::= slice1
        expr ::= slice2
        expr ::= slice3
        expr ::= buildslice2
        expr ::= buildslice3
        expr ::= yield

        binary_expr ::= expr expr binary_op
        binary_op ::= BINARY_ADD
        binary_op ::= BINARY_MULTIPLY
        binary_op ::= BINARY_AND
        binary_op ::= BINARY_OR
        binary_op ::= BINARY_XOR
        binary_op ::= BINARY_SUBTRACT
        binary_op ::= BINARY_DIVIDE
        binary_op ::= BINARY_TRUE_DIVIDE
        binary_op ::= BINARY_FLOOR_DIVIDE
        binary_op ::= BINARY_MODULO
        binary_op ::= BINARY_LSHIFT
        binary_op ::= BINARY_RSHIFT
        binary_op ::= BINARY_POWER

        unary_expr ::= expr unary_op
        unary_op ::= UNARY_POSITIVE
        unary_op ::= UNARY_NEGATIVE
        unary_op ::= UNARY_INVERT

        unary_not ::= expr UNARY_NOT
        unary_convert ::= expr UNARY_CONVERT

        binary_subscr ::= expr expr BINARY_SUBSCR
        binary_subscr2 ::= expr expr DUP_TOPX_2 BINARY_SUBSCR

        load_attr ::= expr LOAD_ATTR
        get_iter ::= expr GET_ITER
        slice0 ::= expr SLICE+0
        slice0 ::= expr DUP_TOP SLICE+0
        slice1 ::= expr expr SLICE+1
        slice1 ::= expr expr DUP_TOPX_2 SLICE+1
        slice2 ::= expr expr SLICE+2
        slice2 ::= expr expr DUP_TOPX_2 SLICE+2
        slice3 ::= expr expr expr SLICE+3
        slice3 ::= expr expr expr DUP_TOPX_3 SLICE+3
        buildslice3 ::= expr expr expr BUILD_SLICE_3
        buildslice2 ::= expr expr BUILD_SLICE_2

        yield ::= expr YIELD_VALUE

        _mklambda ::= load_closure mklambda
        _mklambda ::= mklambda

        or   ::= expr JUMP_IF_TRUE_OR_POP expr COME_FROM
        or   ::= expr jmp_true expr _come_from
        and  ::= expr jmp_false expr _come_from
        and  ::= expr JUMP_IF_FALSE_OR_POP expr COME_FROM
        and2 ::= _jump jmp_false COME_FROM expr COME_FROM

        expr ::= conditional
        conditional ::= expr jmp_false expr JUMP_FORWARD expr COME_FROM
        conditional ::= expr jmp_false expr JUMP_ABSOLUTE expr
        expr ::= conditionalnot
        conditionalnot ::= expr jmp_true expr _jump expr COME_FROM

        ret_expr ::= expr
        ret_expr ::= ret_and
        ret_expr ::= ret_or

        ret_expr_or_cond ::= ret_expr
        ret_expr_or_cond ::= ret_cond
        ret_expr_or_cond ::= ret_cond_not

        ret_and  ::= expr JUMP_IF_FALSE_OR_POP ret_expr_or_cond COME_FROM
        ret_or   ::= expr JUMP_IF_TRUE_OR_POP ret_expr_or_cond COME_FROM
        ret_cond ::= expr POP_JUMP_IF_FALSE expr RETURN_END_IF ret_expr_or_cond
        ret_cond_not ::= expr POP_JUMP_IF_TRUE expr RETURN_END_IF ret_expr_or_cond

        stmt ::= return_lambda
        stmt ::= conditional_lambda

        return_lambda ::= ret_expr RETURN_VALUE LAMBDA_MARKER
        conditional_lambda ::= expr jmp_false return_if_stmt return_stmt LAMBDA_MARKER

        cmp ::= cmp_list
        cmp ::= compare
        compare ::= expr expr COMPARE_OP
        cmp_list ::= expr cmp_list1 ROT_TWO POP_TOP
                _come_from
        cmp_list1 ::= expr DUP_TOP ROT_THREE
                COMPARE_OP JUMP_IF_FALSE_OR_POP
                cmp_list1 COME_FROM
        cmp_list1 ::= expr DUP_TOP ROT_THREE
                COMPARE_OP jmp_false
                cmp_list1 _come_from
        cmp_list1 ::= expr DUP_TOP ROT_THREE
                COMPARE_OP JUMP_IF_FALSE_OR_POP
                cmp_list2 COME_FROM
        cmp_list1 ::= expr DUP_TOP ROT_THREE
                COMPARE_OP jmp_false
                cmp_list2 _come_from
        cmp_list2 ::= expr COMPARE_OP JUMP_FORWARD
        cmp_list2 ::= expr COMPARE_OP RETURN_VALUE
        mapexpr ::= BUILD_MAP kvlist

        kvlist ::= kvlist kv
        kvlist ::= kvlist kv2
        kvlist ::= kvlist kv3
        kvlist ::=

        kv ::= DUP_TOP expr ROT_TWO expr STORE_SUBSCR
        kv2 ::= DUP_TOP expr expr ROT_THREE STORE_SUBSCR
        kv3 ::= expr expr STORE_MAP

        exprlist ::= exprlist expr
        exprlist ::= expr

        nullexprlist ::=
        '''

    def add_custom_rules(self, tokens, customize):
        """
        Special handling for opcodes that take a variable number
        of arguments -- we add a new rule for each:

            build_list  ::= {expr}^n BUILD_LIST_n
            build_list  ::= {expr}^n BUILD_TUPLE_n
            unpack_list ::= UNPACK_LIST {expr}^n
            unpack      ::= UNPACK_TUPLE {expr}^n
            unpack      ::= UNPACK_SEQEUENCE {expr}^n

            mkfunc      ::= {expr}^n LOAD_CONST MAKE_FUNCTION_n
            mklambda    ::= {expr}^n LOAD_LAMBDA MAKE_FUNCTION_n
            mkfunc      ::= {expr}^n load_closure LOAD_CONST MAKE_FUNCTION_n
            expr ::= expr {expr}^n CALL_FUNCTION_n
            expr ::= expr {expr}^n CALL_FUNCTION_VAR_n POP_TOP
            expr ::= expr {expr}^n CALL_FUNCTION_VAR_KW_n POP_TOP
            expr ::= expr {expr}^n CALL_FUNCTION_KW_n POP_TOP
        """
        for k, v in list(customize.items()):
            # avoid adding the same rule twice to this parser
            if k in self.customized:
                continue
            self.customized[k] = None

            op = k[:k.rfind('_')]
            if op in ('BUILD_LIST', 'BUILD_TUPLE', 'BUILD_SET'):
                rule = 'build_list ::= ' + 'expr '*v + k
            elif op in ('UNPACK_TUPLE', 'UNPACK_SEQUENCE'):
                rule = 'unpack ::= ' + k + ' designator'*v
            elif op == 'UNPACK_LIST':
                rule = 'unpack_list ::= ' + k + ' designator'*v
            elif op in ('DUP_TOPX', 'RAISE_VARARGS'):
                # no need to add a rule
                continue
                # rule = 'dup_topx ::= ' + 'expr '*v + k
            elif op == 'MAKE_FUNCTION':
                self.addRule('mklambda ::= %s LOAD_LAMBDA %s' %
                      ('expr '*v, k), nop_func)
                rule = 'mkfunc ::= %s LOAD_CONST %s' % ('expr '*v, k)
            elif op == 'MAKE_CLOSURE':
                self.addRule('mklambda ::= %s load_closure LOAD_LAMBDA %s' %
                      ('expr '*v, k), nop_func)
                self.addRule('genexpr ::= %s load_closure LOAD_GENEXPR %s expr GET_ITER CALL_FUNCTION_1' %
                      ('expr '*v, k), nop_func)
                self.addRule('setcomp ::= %s load_closure LOAD_SETCOMP %s expr GET_ITER CALL_FUNCTION_1' %
                      ('expr '*v, k), nop_func)
                self.addRule('dictcomp ::= %s load_closure LOAD_DICTCOMP %s expr GET_ITER CALL_FUNCTION_1' %
                      ('expr '*v, k), nop_func)
                rule = 'mkfunc ::= %s load_closure LOAD_CONST %s' % ('expr '*v, k)
                # rule = 'mkfunc ::= %s closure_list LOAD_CONST %s' % ('expr '*v, k)
            elif op in ('CALL_FUNCTION', 'CALL_FUNCTION_VAR',
                    'CALL_FUNCTION_VAR_KW', 'CALL_FUNCTION_KW'):
                na = (v & 0xff)           # positional parameters
                nk = (v >> 8) & 0xff      # keyword parameters
                # number of apply equiv arguments:
                nak = ( len(op)-len('CALL_FUNCTION') ) // 3
                rule = 'call_function ::= expr ' + 'expr '*na + 'kwarg '*nk \
                       + 'expr ' * nak + k
            else:
                raise Exception('unknown customize token %s' % k)
            self.addRule(rule, nop_func)

class Python2ParserSingle(Python2Parser, PythonParserSingle):
    pass

# -*- coding: utf-8 -*-
# A secured Python sandbox for tempson
# Author: Jason
import re, ast, copy
import RestrictedPython
from .error import *

class vm (object):

    def _evalExp(self, exp, context):
        # protect context
        # _context = copy.deepcopy(context)
        _context = context
        # compile expressions
        try:
            code = RestrictedPython.compile_restricted(exp, '<string>', 'eval')
        except:
            raise RuntimeError('ERROR import expression')
        return eval(code, _context)

    """
    Execute a expression and return result

    Args:
        [exp]       :str  the expression you want to execute
        [context]   :dict the context when executing the expression
        [xssProtect]:bool whether to filter xss attacks, default is True

    Returns:
        All of the expression execution results are converted to !!!string!!! returns

    Raises:
        nameError: name 'xxx' is not defined

    """
    def evalExpToStr (self, exp, context, xssProtect = True):
        # evaluate expression
        rawValue = str(self._evalExp(exp, context))
        
        # whether xss attacks protect
        return self.xssFilter(rawValue) if xssProtect else rawValue

    def evalExpToBool (self, exp, context):
        # evaluate expression
        rawValue = str(self._evalExp(exp, context))

        if rawValue is 'False':
            return False
        elif rawValue is 'True':
            return True
        else:
            bool(rawValue)

    """
    Filter import expression

    Args:
        [code]:str  the code you want to filter

    Returns:
        The filtered code

    """
    def xssFilter (self, raw):
        import cgi
        return cgi.escape(raw)

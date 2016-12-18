# -*- coding: utf-8 -*-
# A secured Python sandbox for tempson
# Author: Jason
import re, ast, copy
import RestrictedPython
from .error import *

class vm (object):

    """
    Execute a expression and return result

    Args:
        [exp]       :str  the expression you want to execute
        [context]   :dict the context when executing the expression
        [xssProtect]:bool whether to filter xss attacks, default is True

    Returns:
        All of the expression execution results are converted to !!!string!!! returns

    Raises:
        VmNameError: variable is not defined

    """
    def evalExpToStr (self, exp, context, xssProtect = True):
        # protect context
        _context = copy.deepcopy(context)

        # compile expressions
        try:
            code = RestrictedPython.compile_restricted(exp, '<string>', 'eval')
        except:
            raise RuntimeError('ERROR import expression')

        rawValue = str(eval(code, _context))
        
        # whether xss attacks protect
        return self.xssFilter(rawValue) if xssProtect else rawValue

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

# -*- coding: utf-8 -*-
import re
from .vm import *
v = vm()

class renderer(object):

    def renderVariable(self, ast, scope):
        try:
            if ast['type'] == 'VAREXP':
                expressionMatch = re.match(r'\{\{\s*(.+)\s*\}\}', ast['value'])
                if expressionMatch.group(1):
                    return v.evalExpToStr(expressionMatch.group(1), scope, True)
                else:
                    raise RuntimeError('Error expression template.')
            else:
                raise RuntimeError('Error in dispatching ast tree.')
        except BaseException as e:
            raise RuntimeError(e)
    
    """
    Render ast for for-expression to html

    Args:
        [ast]  :dict  ast tree
        [scope]:dict  the variable scope

    Returns:
        HTML string

    Raises:
        nameError: name 'xxx' is not defined
    """
    def renderForExpression(self, ast, scope):
        pass
    
    """
    Render ast for if-expression to html

    Args:
        [ast]  :dict  ast tree
        [scope]:dict  the variable scope

    Returns:
        HTML string

    Raises:
        nameError: name 'xxx' is not defined
    """
    def renderIfExpression(self, ast, scope):
        pass
        

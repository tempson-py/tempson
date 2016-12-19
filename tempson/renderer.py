# -*- coding: utf-8 -*-
from .vm import *

class renderer(object):

    def renderVariable(self, ast, scope):
        pass
    
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
        

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
        try:
            template = ''
            _context = scope
            items = ast['body']
            for i in _context[ast['squence']]:
                _context[ast['iteratingVar']] = i

                for item in items:

                    curHTML = ''
                    valType = item['type'].upper()
                    if (valType == 'HTML'):
                        curHTML = item['value']
                    elif (valType == 'FOREXP'):
                        curHTML =  self.renderForExpression(item, _context)
                    elif (valType == 'IFEXP'):
                        curHTML = self.renderIfExpression(item, _context)
                    elif (valType == 'VAREXP'):
                        curHTML = self.renderVariable(item, _context)
                    else:
                        curHTML = item['value']
                    template += curHTML
            return template
        except BaseException as e:
            raise RuntimeError(e)
    
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
        try:
            template = ''
            items = ast['body']
            _context = scope
            condition = v.evalExpToStr(ast['expression'], _context, True)
            if condition:
                print condition
                for item in items:
                    temp = ''
                    valType = item['type'].upper()
                    if valType == 'HTML':
                        temp = item['value']
                    elif valType == 'FOREXP':
                        temp = self.renderForExpression(item, _context)
                    elif valType == 'IFEXP':
                        temp = self.renderIfExpression(item, _context)
                    elif valType == 'VAREXP':
                        temp = self.renderVariable(item, _context)
                        # print temp
                    else:
                        temp = item['value']
                    template += temp
            else:
                template = ''
            return template
        except BaseException as e:
            raise RuntimeError(e)

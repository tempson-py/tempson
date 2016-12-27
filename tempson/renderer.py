# -*- coding: utf-8 -*-
import re
import copy
from .vm import *
v = vm()

class renderer(object):

    def renderVariable(self, ast, scope, raw = False):
        try:
            if ast['type'] == 'VAREXP':
                expressionMatch = re.match(r'\{\{\s*(.+)\s*\}\}', ast['value'])
                if expressionMatch.group(1):
                    return v.evalExpToStr(expressionMatch.group(1), scope, not raw)
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
            _context = copy.deepcopy(scope)
            items = ast['body']
            squence = _context[ast['squence']]
            if squence:
                for i in squence:
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
            else:
                raise RuntimeError('Undefined variable for expression sequence.')
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
    def renderIfExpression(self, item, scope):
        html = ''
        condition = item['expression']
        judge = v.evalExpToBool(condition, scope)
        if judge:
            for ast in item['body']:
                valType = ast['type'].upper()
                renderResult = ''
                if valType == 'HTML':
                    renderResult = ast['value']
                elif valType == 'VAREXP':
                    renderResult = self.renderVariable(ast, scope)
                elif valType == 'IFEXP':
                    renderResult = self.renderIfExpression(ast, scope)
                elif valType == 'FOREXP':
                    renderResult = self.renderForExpression(ast, scope)
                
                if isinstance(renderResult, str):
                    html += renderResult
                else:
                    raise RuntimeError('Unknown renderer error in render variable-expression')
        return html
# -*- coding: utf-8 -*-
import re, copy

class compiler(object):

    def __init__(self, template):
        self._template = template

    def tokenize (self):
        # template string
        t = self._template

        # throw a error when template is not a string
        if not isinstance(t, str):
            raise RuntimeError('Error template type: ' + str(type(t)))

        # template length
        t_length = len(t)
        # current offset
        cur = 0
        # token list
        tokens = []
        # init token
        token = {
            'type': None,
            'value': ''
        }
        # string template
        isString = False

        while cur < t_length:
            # switch string flag if test string symbol: '/"
            if t[cur] == '\'' or t[cur] == '\"':
                isString = not isString

            # jump every symbol if string flag is True
            if isString:
                token['value'] += t[cur]
                cur += 1
                continue

            # delimiter end
            if t[cur] == '}':
                if t[cur + 1] == '}':
                    if t[cur + 2] == '}':
                        token['value'] += '}}}'
                        cur += 3
                        tokens.append(token)
                        token = {
                            'type': None,
                            'value': ''
                        }
                    else:
                        token['value'] += '}}'
                        cur += 2
                        tokens.append(token)
                        token = {
                            'type': None,
                            'value': ''
                        }

            if t[cur] == '%':
                if t[cur + 1] == '}':
                    token['value'] += '%}'
                    cur += 2
                    tokens.append(token)
                    token = {
                        'type': None,
                        'value': ''
                    }

            if t[cur] == '*':
                if t[cur + 1] == '}':
                    token['value'] += '*}'
                    cur += 2
                    tokens.append(token)
                    token = {
                        'type': None,
                        'value': ''
                    }

            # delimiter start
            if t[cur] == '{':

                # varible expression
                if t[cur + 1] == '{':
                    # save last token
                    if token['type'] == 'HTML':
                        tokens.append(token)

                    if t[cur + 2] == '{':
                        # define a new token
                        token = {
                            'type': 'RAWEXP',
                            'value': '{{{'
                        }

                        # next char
                        cur += 3
                    else:
                        # define a new token
                        token = {
                            'type': 'VAREXP',
                            'value': '{{'
                        }
                        
                        # next char
                        cur += 2

            if t[cur] == '{':

                # varible expression
                if t[cur + 1] == '%':
                    # save last token
                    if token['type'] == 'HTML':
                        tokens.append(token)

                    # define a new token
                    token = {
                        'type': 'BLKEXP',
                        'value': '{%'
                    }

                    # next char
                    cur += 2

            if t[cur] == '{':

                # varible expression
                if t[cur + 1] == '*':
                    # save last token
                    if token['type'] == 'HTML':
                        tokens.append(token)

                    # define a new token
                    token = {
                        'type': 'COMEXP',
                        'value': '{*'
                    }

                    # next char
                    cur += 2

            # default is HTML
            if token['type'] == None:
                token = {
                    'type': 'HTML',
                    'value': ''
                }

            token['value'] += t[cur]

            cur += 1

            if cur == t_length:
                tokens.append(token)

        self.tokens = tokens
        return tokens

    """
    [{'type': 'HTML', 'value': '<div>\n            '},
    {'type': 'BLKEXP', 'value': '{% for item in list %}'},
    {'type': 'HTML', 'value': '\n                '},
    {'type': 'VAREXP', 'value': '{{ item }}'},
    {'type': 'HTML', 'value': '\n            '},
    {'type': 'BLKEXP', 'value': '{% endfor %}'},
    {'type': 'HTML', 'value': '\n        </div>'}]
    """
    def _ast(self, tokens):
        # ast fragments
        fragment = []
        # offset
        o = 0
        # ast branch
        ast = {
            'type': None,
            'body': []
        }

        while o < len(tokens):
            t = tokens[o]

            if t['type'] == 'BLKEXP':
                # end of block expression
                blockEndFlag = re.findall(r'end(for|if)', t['value'].lower())
                if blockEndFlag and blockEndFlag[0].upper() + 'EXP' == ast['type']:
                    # print ast
                    # recursion parse body
                    ast['body'] = self._ast(copy.deepcopy(ast['body']))
                    # save to fragment
                    fragment.append(ast)
                    ast = {
                        'type': None,
                        'body': []
                    }
                    o += 1
                    continue

                # find for expression
                elif re.findall(r'for\s+(\w+)\s+in\s+(\w+)\s*:?', t['value']) and ast['type'] == None:
                    matchObject = re.findall(r'\s*for\s+(\w+)\s+in\s+(\w+)\s*:?', t['value'])
                    ast['type'] = 'FOREXP'
                    ast['squence'] = matchObject[0][1]
                    ast['iteratingVar'] = matchObject[0][0]
                    # next token
                    o += 1
                    continue

                # find if expression
                elif re.findall(r'if\s+(.+):', t['value']) and ast['type'] == None:
                    matchObject = re.findall(r'if\s+(.+):', t['value'])
                    ast['type'] = 'IFEXP'
                    ast['expression'] = matchObject[0]
                    # next token
                    o += 1
                    continue

            if ast['type'] in ('FOREXP', 'IFEXP'):
                ast['body'].append(t)
                # next token
                o += 1
                continue

            if t['type'] in ('HTML', 'VAREXP', 'RAWEXP'):
                fragment.append(t)

            o += 1

        return fragment

    def astParser(self, tokens):
        return self._ast(tokens)
